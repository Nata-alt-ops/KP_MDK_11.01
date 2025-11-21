import hashlib
from tkinter import *
from tkinter import messagebox
import pyodbc

# Подключение к базе данных
def connect_db():
    try:
        conn = pyodbc.connect(
            "DRIVER={SQL Server};"
            "SERVER=408-05\\SQLEXPRESS;"
            "DATABASE=Hotel;"
            "Trusted_Connection=yes;"
        )
        return conn
    except Exception as e:
        print(f"Ошибка подключения: {e}")
        return None

# Хэширование пароля
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Авторизация
def authenticate_user():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        label_status.config(text="Введите логин и пароль")
        return
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            hashed_password = hash_password(password)
            
            cursor.execute("SELECT user_id, user_type FROM Users WHERE username=? AND password=?", (username, hashed_password))
            result = cursor.fetchone()

            if result:
                user_id, user_type = result
                open_main_window(username, user_id, user_type)
            else:
                label_status.config(text="Неверный логин или пароль")
        except Exception as e:
            label_status.config(text=f"Ошибка: {e}")
        finally:
            conn.close()
    else:
        label_status.config(text="Нет подключения к БД")

# Регистрация
def register_user():
    def submit_registration():
        new_username = entry_new_username.get().strip()
        new_password = entry_new_password.get()
        new_first_name = entry_new_firstname.get().strip()
        new_last_name = entry_new_lastname.get().strip()
        new_phone = entry_new_phone.get().strip()
        new_email = entry_new_email.get().strip()
        
        if not new_username or not new_password:
            label_register_status.config(text="Заполните логин и пароль")
            return
            
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT user_id FROM Users WHERE username=?", (new_username,))
                if cursor.fetchone():
                    label_register_status.config(text="Пользователь уже существует")
                    return

                hashed_password = hash_password(new_password)

                cursor.execute(
                    "INSERT INTO Users (username, FirstName, LastName, password, Phone, Email, user_type) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (new_username, new_first_name, new_last_name, hashed_password, new_phone, new_email, 'user')
                )

                conn.commit()
                label_register_status.config(text="Регистрация успешна!", fg="green")
                entry_username.delete(0, END)
                entry_username.insert(0, new_username)
                registration.after(1500, registration.destroy)
                    
            except Exception as e:
                label_register_status.config(text=f"Ошибка: {e}")
            finally:
                conn.close()
        else:
            label_register_status.config(text="Нет подключения к БД")

    registration = Toplevel(root)
    registration.title("Регистрация")
    registration.configure(bg='lightblue')
    registration.geometry('400x400')  

    Label(registration, text="Регистрация", font=('Arial', 16), bg='lightblue').pack(pady=10)

    frame = Frame(registration, bg='lightblue')
    frame.pack(pady=10)

    Label(frame, text="Логин:*", bg='lightblue').grid(row=0, column=0, sticky=W, pady=5)
    entry_new_username = Entry(frame, width=20)
    entry_new_username.grid(row=0, column=1, pady=5, padx=5)

    Label(frame, text="Пароль:*", bg='lightblue').grid(row=1, column=0, sticky=W, pady=5)
    entry_new_password = Entry(frame, show='*', width=20)
    entry_new_password.grid(row=1, column=1, pady=5, padx=5)

    Label(frame, text="Имя:", bg='lightblue').grid(row=2, column=0, sticky=W, pady=5)
    entry_new_firstname = Entry(frame, width=20)
    entry_new_firstname.grid(row=2, column=1, pady=5, padx=5)

    Label(frame, text="Фамилия:", bg='lightblue').grid(row=3, column=0, sticky=W, pady=5)
    entry_new_lastname = Entry(frame, width=20)
    entry_new_lastname.grid(row=3, column=1, pady=5, padx=5)

    Label(frame, text="Телефон:", bg='lightblue').grid(row=4, column=0, sticky=W, pady=5)
    entry_new_phone = Entry(frame, width=20)
    entry_new_phone.grid(row=4, column=1, pady=5, padx=5)

    Label(frame, text="Email:", bg='lightblue').grid(row=5, column=0, sticky=W, pady=5)
    entry_new_email = Entry(frame, width=20)
    entry_new_email.grid(row=5, column=1, pady=5, padx=5)

    Button(frame, text="Зарегистрироваться", command=submit_registration, bg='lightgreen').grid(row=6, column=1, pady=10)
    Button(frame, text="Назад", command=registration.destroy, bg='lightcoral').grid(row=7, column=1, pady=5)

    label_register_status = Label(registration, text="", bg='lightblue')
    label_register_status.pack()

# Основное окно
def open_main_window(username, user_id, user_type):
    main_window = Toplevel(root)
    main_window.configure(bg='lightblue')
    main_window.geometry('800x600') 
    main_window.title(f"Добро пожаловать, {username}")

    root.withdraw()
    
    def logout():
        main_window.destroy()
        root.deiconify()  
        entry_password.delete(0, END)  
        label_status.config(text="Вы вышли из системы")

    main_frame = Frame(main_window, bg='lightblue')
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

    left_frame = Frame(main_frame, bg='lightblue')
    left_frame.pack(side=LEFT, fill=BOTH, expand=True)
    
    try:
        photo = PhotoImage(file="user.png")
        image_label = Label(left_frame, image=photo, bg='lightblue')
        image_label.pack(expand=True)
        main_window.photo = photo 
    except Exception as e:
        print(f"Ошибка загрузки изображения: {e}")

  
    right_frame = Frame(main_frame, bg='lightblue')
    right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

  
    Label(right_frame, text="Меню", font=('Arial', 18, 'bold'), 
          bg='lightblue', fg='darkblue').pack(pady=20)

   
    Button(right_frame, text="🏨 Комнаты", width=25, height=2,
           command=lambda: view_all_rooms(user_type), font=('Arial', 12), 
           bg='#87CEEB', fg='black').pack(pady=10)
    
    Button(right_frame, text="🎯 Услуги отеля", width=25, height=2,
           command=view_services, font=('Arial', 12), 
           bg='#98FB98', fg='black').pack(pady=10)

    if user_type == 'user':
        Button(right_frame, text="📅 Мои бронирования", width=25, height=2,
               command=lambda: view_my_bookings(user_id), font=('Arial', 12), 
               bg='#FFD700', fg='black').pack(pady=10)
    
        Button(right_frame, text="👤 Редактировать профиль", width=25, height=2,
               command=lambda: edit_profile(user_id), font=('Arial', 12), 
               bg='#FFB6C1', fg='black').pack(pady=10)
        
        Button(right_frame, text="🗑️ Удалить учетную запись", width=25, height=2,
               command=lambda: delete_user_account(user_id, username), 
               font=('Arial', 12), bg='#FF6347', fg='white').pack(pady=10)

    if user_type == 'admin':

        Button(right_frame, text="📋 Управление бронированиями", width=25, height=2,
               command=manage_bookings, font=('Arial', 12), 
               bg='#DA70D6', fg='black').pack(pady=10)

    Button(right_frame, text="🚪 Выйти", command=logout, 
           width=20, height=2, font=('Arial', 12), 
           bg='#DC143C', fg='white').pack(pady=30)


def delete_user_account(user_id, username):
    if not messagebox.askyesno("Подтверждение удаления", 
                              f"Вы уверены, что хотите удалить свою учетную запись '{username}'?\n\n"
                              "Это действие невозможно отменить!"):
        return
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT BookingID FROM Bookings WHERE UserID = ?", (user_id,))
            bookings = cursor.fetchall()
            for booking in bookings:
                booking_id = booking[0]

                cursor.execute("DELETE FROM BookingServices WHERE BookingID = ?", (booking_id,))
                cursor.execute("DELETE FROM Payments WHERE BookingID = ?", (booking_id,))
            cursor.execute("""
                UPDATE Rooms 
                SET RoomStatus = 'Свободна' 
                WHERE RoomID IN (SELECT RoomID FROM Bookings WHERE UserID = ?)
            """, (user_id,))
            cursor.execute("DELETE FROM Bookings WHERE UserID = ?", (user_id,))
            cursor.execute("DELETE FROM Users WHERE user_id = ?", (user_id,))
            
            conn.commit()
            
            messagebox.showinfo("Успех", "Ваша учетная запись была успешно удалена.")
            
            for window in root.winfo_children():
                if isinstance(window, Toplevel):
                    window.destroy()
            
            root.deiconify()
            entry_username.delete(0, END)
            entry_password.delete(0, END)
            label_status.config(text="Учетная запись удалена")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось удалить учетную запись: {e}")
        finally:
            conn.close()

def view_all_rooms(user_type='user'):
    rooms_window = Toplevel()
    rooms_window.title("Доступные комнаты")
    rooms_window.configure(bg='lightblue')
    rooms_window.geometry('600x400')
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT RoomID, Room_number, RoomType, Price, RoomStatus FROM Rooms")
            rooms = cursor.fetchall()
         
            main_frame = Frame(rooms_window, bg='white')
            main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            canvas = Canvas(main_frame, bg='lightblue', highlightthickness=0)
            scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg='lightblue')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            try:
                room_photo = PhotoImage(file="rooms.png")
            except:
                room_photo = None
                print("Не удалось загрузить картинку комнаты")
            
            for room in rooms:
                room_id, room_number, room_type, price, status = room
                
                room_frame = Frame(scrollable_frame, relief=GROOVE, borderwidth=1, bg='white')
                room_frame.pack(fill=X, pady=5, padx=10)
                
                if room_photo:
                    image_label = Label(room_frame, image=room_photo, bg='white')
                    image_label.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky='nw')
                else:
                    Label(room_frame, text="🏨", font=('Times New Roman', 24), bg='#e6f2ff', 
                          fg='#0066cc', width=4, height=3).grid(row=0, column=0, rowspan=2, 
                                                              padx=10, pady=10, sticky='nw')
                
                info_text = f"Комната №{room_number}\nТип: {room_type}\nЦена: {price} руб./ночь\nСтатус: {status}"
                info_label = Label(room_frame, text=info_text, font=('Times New Roman', 10, 'bold'), 
                                 bg='white', justify=LEFT, anchor='w')
                info_label.grid(row=0, column=1, padx=10, pady=10, sticky='w')
                
                if status == 'Свободна' and user_type != 'admin':
                    btn = Button(room_frame, text="Забронировать", bg='lightgreen', font=('Arial', 9),
                                command=lambda rid=room_id, rnum=room_number: book_room(rid, rnum))
                    btn.grid(row=1, column=1, padx=10, pady=5, sticky='e')
                else:
                    status_label = Label(room_frame, text="Занята", fg='red', 
                                       font=('Arial', 9, 'bold'), bg='white')
                    status_label.grid(row=1, column=1, padx=10, pady=5, sticky='e')
                
                room_frame.columnconfigure(1, weight=1)

            if room_photo:
                scrollable_frame.room_photo = room_photo

            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")

            Button(rooms_window, text="Назад", command=rooms_window.destroy, 
                   bg='lightcoral', width=15).pack(pady=10)
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить комнаты: {e}")
        finally:
            conn.close()

# Бронирование комнаты
def book_room(room_id, room_number):
    booking_window = Toplevel()
    booking_window.title(f"Бронирование комнаты №{room_number}")
    booking_window.geometry('350x250')  
    booking_window.configure(bg='lightblue')
    
    Label(booking_window, text=f"Комната №{room_number}", font=('Arial', 14), bg='lightblue').pack(pady=10)
    
    frame = Frame(booking_window, bg='lightblue')
    frame.pack(pady=10)
    
    Label(frame, text="Дата заезда (ГГГГ-ММ-ДД):", bg='lightblue').grid(row=0, column=0, sticky=W, pady=5)
    entry_checkin = Entry(frame, width=15)
    entry_checkin.insert(0, "2024-01-15")
    entry_checkin.grid(row=0, column=1, pady=5, padx=5)
    
    Label(frame, text="Дата выезда (ГГГГ-ММ-ДД):", bg='lightblue').grid(row=1, column=0, sticky=W, pady=5)
    entry_checkout = Entry(frame, width=15)
    entry_checkout.insert(0, "2024-01-20")
    entry_checkout.grid(row=1, column=1, pady=5, padx=5)
    
    def confirm_booking():
        checkin = entry_checkin.get()
        checkout = entry_checkout.get()
        
        if not checkin or not checkout:
            messagebox.showerror("Ошибка", "Заполните даты")
            return
        
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                
                cursor.execute("SELECT user_id FROM Users WHERE username = ?", (entry_username.get(),))
                user_result = cursor.fetchone()
                
                if user_result:
                    user_id = user_result[0]
                    
                    cursor.execute("SELECT RoomStatus FROM Rooms WHERE RoomID = ?", (room_id,))
                    room_status = cursor.fetchone()[0]
                    
                    if room_status != 'Свободна':
                        messagebox.showerror("Ошибка", "Комната уже занята")
                        return
                    
                    cursor.execute("""
                        INSERT INTO Bookings (UserID, RoomID, CheckInDate, CheckOutDate)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, room_id, checkin, checkout))
                    
                    cursor.execute("UPDATE Rooms SET RoomStatus = 'Занята' WHERE RoomID = ?", (room_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Успех", f"Комната №{room_number} забронирована!")
                    booking_window.destroy()
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка бронирования: {e}")
            finally:
                conn.close()
    
    Button(booking_window, text="Подтвердить", command=confirm_booking, 
           bg='lightgreen', width=15).pack(pady=5)
    Button(booking_window, text="Назад", command=booking_window.destroy, 
           bg='lightcoral', width=15).pack(pady=5)

# Просмотр услуг отеля 
def view_services():
    services_window = Toplevel()
    services_window.title("Услуги отеля")
    services_window.configure(bg='lightblue')
    services_window.geometry('600x600')
    
    Label(services_window, text="Услуги отеля", font=('Arial', 12, 'bold'), 
          bg='lightblue', fg='darkblue').pack(pady=20)
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT ServiceName, Price FROM Service")
            services = cursor.fetchall()
            
            main_frame = Frame(services_window, bg='lightblue')
            main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
            
            canvas = Canvas(main_frame, bg='lightblue', highlightthickness=0)
            scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = Frame(canvas, bg='lightblue')
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            grid_frame = Frame(scrollable_frame, bg='lightblue')
            grid_frame.pack(padx=10, pady=10, fill=BOTH, expand=True)
            
            for i, service in enumerate(services):
                service_name, price = service
                
                row = i // 2  
                col = i % 2   
                
                service_frame = Frame(grid_frame, relief=RAISED, borderwidth=1, 
                                    bg='white', padx=10, pady=10)
                service_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                
                Label(service_frame, text=service_name, font=('Arial', 11, 'bold'), 
                      bg='white', fg='#333333').pack(anchor='w')
                
                Label(service_frame, text=f"{price} руб.", font=('Arial', 10), 
                      bg='white', fg='#006600').pack(anchor='w')
                
                grid_frame.columnconfigure(col, weight=1)
                grid_frame.rowconfigure(row, weight=1)
            
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            Button(services_window, text="Назад", command=services_window.destroy, 
                   bg='lightcoral', width=15, font=('Arial', 10)).pack(pady=20)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки услуг: {e}")
        finally:
            conn.close()

# Просмотр бронирований пользователя 
def view_my_bookings(user_id):
    bookings_window = Toplevel()
    bookings_window.title("Мои бронирования")
    bookings_window.configure(bg='lightblue')  
    bookings_window.geometry('500x500')
    
   
    header_frame = Frame(bookings_window, bg='lightblue')
    header_frame.pack(fill=X, padx=20, pady=15)
    
    Label(header_frame, text="Мои бронирования", font=('Arial', 18, 'bold'), 
          bg='lightblue', fg='#000000').pack(side=LEFT, padx=10)
    
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.BookingID, r.Room_number, r.RoomType, r.Price, 
                       b.CheckInDate, b.CheckOutDate
                FROM Bookings b 
                JOIN Rooms r ON b.RoomID = r.RoomID 
                WHERE b.UserID = ?
            """, (user_id,))
            
            bookings = cursor.fetchall()
            
            if bookings:
               
                main_frame = Frame(bookings_window, bg="#ffffff")
                main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
                
                for booking in bookings:
                    booking_id, room_number, room_type, price, checkin, checkout = booking
                    
                    
                    card_frame = Frame(main_frame, bg='white', relief=RAISED, 
                                     borderwidth=2, highlightbackground='#bdc3c7')
                    card_frame.pack(fill=X, pady=8, padx=5)
                    
                    
                    top_frame = Frame(card_frame, bg='#ffffff')
                    top_frame.pack(fill=X)
                    
                    Label(top_frame, text=f"Комната №{room_number}", 
                          font=('Arial', 14, 'bold'), bg="#ffffff", fg='#000000',
                          padx=15, pady=8).pack(anchor='w')
                    
                
                    info_frame = Frame(card_frame, bg='white')
                    info_frame.pack(fill=X, padx=15, pady=12)
                    
                    
                    Label(info_frame, text="Тип:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=0, column=0, sticky='w')
                    Label(info_frame, text=room_type, font=('Arial', 10), 
                          bg='white', fg='#2c3e50').grid(row=0, column=1, sticky='w', padx=(5, 20))
                    
                  
                    Label(info_frame, text="Цена:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=0, column=2, sticky='w')
                    Label(info_frame, text=f"{price} руб.", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#27ae60').grid(row=0, column=3, sticky='w', padx=5)
                    
                   
                    Label(info_frame, text="Заезд:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=1, column=0, sticky='w', pady=(8, 0))
                    Label(info_frame, text=checkin, font=('Arial', 10), 
                          bg='white', fg='#2c3e50').grid(row=1, column=1, sticky='w', padx=5, pady=(8, 0))
                    
                    Label(info_frame, text="Выезд:", font=('Arial', 10, 'bold'), 
                          bg='white', fg='#7f8c8d').grid(row=1, column=2, sticky='w', pady=(8, 0))
                    Label(info_frame, text=checkout, font=('Arial', 10), 
                          bg='white', fg='#2c3e50').grid(row=1, column=3, sticky='w', padx=5, pady=(8, 0))
                    
                  
                    btn_frame = Frame(card_frame, bg='white')
                    btn_frame.pack(fill=X, padx=15, pady=(5, 12))
                    
                    Button(btn_frame, text="Отменить", 
                           command=lambda bid=booking_id, rnum=room_number: cancel_booking(bid, rnum),
                           bg="#ff270f", fg='white', font=('Arial', 9, 'bold'),
                           relief=RAISED, bd=2, padx=10, pady=4).pack(side=RIGHT)
                    
            else:
               
                empty_frame = Frame(bookings_window, bg='#f0f8ff')
                empty_frame.pack(expand=True)
                
                Label(empty_frame, text="", font=('Arial', 48), 
                      bg='#f0f8ff', fg="#000000").pack(pady=10)
                Label(empty_frame, text="Нет активных бронирований", 
                      font=('Arial', 14), bg='#f0f8ff', fg='#7f8c8d').pack()
                Label(empty_frame, text="Забронируйте комнату в разделе 'Комнаты'", 
                      font=('Arial', 10), bg='#f0f8ff', fg='#95a5a6').pack()
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки бронирований: {e}")
        finally:
            conn.close()
    
   
    Button(bookings_window, text="Назад", command=bookings_window.destroy, 
           bg="#f8233f", fg='white', width=15, font=('Arial', 10),
           relief=RAISED, bd=2).pack(pady=15)

def cancel_booking(booking_id, room_number):
    if messagebox.askyesno("Подтверждение", f"Отменить бронирование комнаты №{room_number}?"):
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM BookingServices WHERE BookingID = ?", (booking_id,))
                cursor.execute("DELETE FROM Payments WHERE BookingID = ?", (booking_id,))
                cursor.execute("SELECT RoomID FROM Bookings WHERE BookingID = ?", (booking_id,))
                room_result = cursor.fetchone()
                
                if room_result:
                    room_id = room_result[0]
                    
                    cursor.execute("DELETE FROM Bookings WHERE BookingID = ?", (booking_id,))
                    
                    cursor.execute("UPDATE Rooms SET RoomStatus = 'Свободна' WHERE RoomID = ?", (room_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Успех", f"Бронирование отменено!")
                    
                    for window in root.winfo_children():
                        if isinstance(window, Toplevel) and "Мои бронирования" in window.title():
                            window.destroy()
                            view_my_bookings(get_current_user_id())
                            break
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка отмены бронирования: {e}")
            finally:
                conn.close()

# поиск пользователя по ID (нужно для отмены бронирования)
def get_current_user_id():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id FROM Users WHERE username = ?", (entry_username.get(),))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Ошибка получения ID пользователя: {e}")
            return None
        finally:
            conn.close()

# Редактирование профиля
def edit_profile(user_id):
    profile_window = Toplevel()
    profile_window.title("Редактирование профиля")
    profile_window.configure(bg='lightblue')
    profile_window.geometry('400x350')

    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username, FirstName, LastName, Phone, Email FROM Users WHERE user_id=?", (user_id,))
            user_data = cursor.fetchone()
            
            if user_data:
                username, first_name, last_name, phone, email = user_data
                
                Label(profile_window, text="Редактирование профиля", font=('Arial', 16), bg='lightblue').pack(pady=10)
                
                frame = Frame(profile_window, bg='lightblue')
                frame.pack(pady=10)
                
                entries = {}
                fields = [
                    ("Логин:", "username", username),
                    ("Имя:", "firstname", first_name),
                    ("Фамилия:", "lastname", last_name),
                    ("Телефон:", "phone", phone),
                    ("Email:", "email", email)
                ]
                
                for i, (label, field, value) in enumerate(fields):
                    Label(frame, text=label, bg='lightblue').grid(row=i, column=0, sticky=W, pady=5)
                    entry = Entry(frame, width=20)
                    entry.insert(0, value)
                    entry.grid(row=i, column=1, pady=5, padx=5)
                    entries[field] = entry
                
                def save_profile():
                    save_conn = connect_db()
                    if save_conn:
                        try:
                            save_cursor = save_conn.cursor()
                            
                            new_username = entries['username'].get()
                            new_firstname = entries['firstname'].get()
                            new_lastname = entries['lastname'].get()
                            new_phone = entries['phone'].get()
                            new_email = entries['email'].get()
                            
                            if not new_username:
                                messagebox.showerror("Ошибка", "Заполните логин")
                                return
                            
                            save_cursor.execute("""
                                UPDATE Users 
                                SET username=?, FirstName=?, LastName=?, Phone=?, Email=?
                                WHERE user_id=?
                            """, (new_username, new_firstname, new_lastname, new_phone, new_email, user_id))
                            save_conn.commit()
                            messagebox.showinfo("Успех", "Профиль обновлен!")
                            profile_window.destroy()
                        except Exception as e:
                            messagebox.showerror("Ошибка", f"Ошибка обновления: {e}")
                        finally:
                            save_conn.close()
                
                Button(frame, text="Сохранить", command=save_profile, 
                       bg='lightgreen', width=10).grid(row=5, column=1, pady=10, sticky=E)
                Button(frame, text="Отмена", command=profile_window.destroy, 
                       bg='lightcoral', width=10).grid(row=5, column=0, pady=10, sticky=W)
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки профиля: {e}")
        finally:
            conn.close()



# Управление бронированиями 
def manage_bookings():
    bookings_window = Toplevel()
    bookings_window.title("Управление бронированиями")
    bookings_window.configure(bg='lightblue')
    bookings_window.geometry('900x600')
    
    Label(bookings_window, text="Управление бронирований", font=('Arial', 16), bg='lightblue').pack(pady=10)
    
    def refresh_bookings():
        main_frame = Frame(bookings_window, bg='lightblue')
        main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        canvas = Canvas(main_frame, bg='lightblue')
        scrollbar = Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas, bg='lightblue')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT b.BookingID, u.username, r.Room_number, r.RoomType,
                           b.CheckInDate, b.CheckOutDate
                    FROM Bookings b
                    JOIN Users u ON b.UserID = u.user_id
                    JOIN Rooms r ON b.RoomID = r.RoomID
                """)
                bookings = cursor.fetchall()
                
               
                headers = ["ID", "Пользователь", "Комната", "Тип", "Заезд", "Выезд", "Действия"]
                for i, header in enumerate(headers):
                    Label(scrollable_frame, text=header, font=('Arial', 10, 'bold'), 
                          bg='lightgray', width=12).grid(row=0, column=i, padx=2, pady=5, sticky=W+E)
                
                for row_idx, booking in enumerate(bookings, 1):
                    booking_id, username, room_number, room_type, checkin, checkout = booking
                    
                    Label(scrollable_frame, text=booking_id, bg='white', width=12).grid(row=row_idx, column=0, padx=2, pady=2, sticky=W+E)
                    Label(scrollable_frame, text=username, bg='white', width=12).grid(row=row_idx, column=1, padx=2, pady=2, sticky=W+E)
                    Label(scrollable_frame, text=room_number, bg='white', width=12).grid(row=row_idx, column=2, padx=2, pady=2, sticky=W+E)
                    Label(scrollable_frame, text=room_type, bg='white', width=12).grid(row=row_idx, column=3, padx=2, pady=2, sticky=W+E)
                    Label(scrollable_frame, text=str(checkin), bg='white', width=12).grid(row=row_idx, column=4, padx=2, pady=2, sticky=W+E)
                    Label(scrollable_frame, text=str(checkout), bg='white', width=12).grid(row=row_idx, column=5, padx=2, pady=2, sticky=W+E)
                    
                    Button(scrollable_frame, text="Удалить", bg='lightcoral', font=('Arial', 8), width=10,
                          command=lambda bid=booking_id: delete_booking(bid)).grid(row=row_idx, column=6, padx=2, pady=2)
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки бронирований: {e}")
            finally:
                conn.close()
        
       
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def delete_booking(booking_id):
        if messagebox.askyesno("Подтверждение", "Удалить бронирование?"):
            conn = connect_db()
            if conn:
                try:
                    cursor = conn.cursor()
                        
                    cursor.execute("DELETE FROM BookingServices WHERE BookingID = ?", (booking_id,))
                    
                 
                    cursor.execute("DELETE FROM Payments WHERE BookingID = ?", (booking_id,))
                    
                  
                    cursor.execute("SELECT RoomID FROM Bookings WHERE BookingID = ?", (booking_id,))
                    room_result = cursor.fetchone()
                    
                    if room_result:
                        room_id = room_result[0]
                        
                       
                        cursor.execute("DELETE FROM Bookings WHERE BookingID = ?", (booking_id,))
                        
                    
                        cursor.execute("UPDATE Rooms SET RoomStatus = 'Свободна' WHERE RoomID = ?", (room_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Успех", "Бронирование удалено")
                    
                    
                    for widget in bookings_window.winfo_children():
                        widget.destroy()
                    refresh_bookings()
                
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка удаления: {e}")
                finally:
                    conn.close()
    
    refresh_bookings()
    
    Button(bookings_window, text="Назад", command=bookings_window.destroy, bg='lightcoral').pack(pady=5)

# Основное окно авторизации
root = Tk()
root.title("Авторизация")
root.configure(bg='lightblue')
root.geometry('350x300')

Label(root, text="Вход в аккаунт", font=('Arial', 16), bg='lightblue').pack(pady=10)

frame = Frame(root, bg='lightblue')
frame.pack(pady=10)

Label(frame, text="Логин:", bg='lightblue').grid(row=0, column=0, sticky=W, pady=5)
entry_username = Entry(frame, width=20)
entry_username.grid(row=0, column=1, pady=5, padx=5)

Label(frame, text="Пароль:", bg='lightblue').grid(row=1, column=0, sticky=W, pady=5)
entry_password = Entry(frame, show='*', width=20)
entry_password.grid(row=1, column=1, pady=5, padx=5)

Button(root, text="Войти", command=authenticate_user, bg='lightgrey', width=10).pack(pady=5)
Button(root, text="Регистрация", command=register_user, bg='lightgreen', width=10).pack(pady=5)

label_status = Label(root, text="Введите данные для входа", fg='black', bg='lightblue')
label_status.pack(pady=10)


root.mainloop()
