import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from Main import MenuChinh  # import menu chính

# ======= KẾT NỐI MYSQL =======
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="quanly_cuahangvatlieuxaydung"
    )

# ======= XỬ LÝ LOGIN =======
def dang_nhap():
    user = entry_user.get().strip()
    pw = entry_pass.get().strip()
    if not user or not pw:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu!")
        return
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM nguoidung WHERE tennguoidung=%s AND matkhau=%s", (user, pw))
        result = cursor.fetchone()
        if result:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            root.withdraw()  # ẩn login
            MenuChinh(root)  # mở menu chính
        else:
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu!")
    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối MySQL:\n{err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def thoat():
    if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát không?"):
        root.destroy()

# ======= GIAO DIỆN LOGIN =======
root = tk.Tk()
root.title("Đăng nhập - Quản Lý Cửa Hàng VLXD")
root.geometry("600x350")
root.resizable(False, False)
root.configure(bg="#fce4ec")

# ==== ICON WINDOW ====
try:
    root.iconbitmap("icon.ico")
except:
    pass

# ==== TIÊU ĐỀ ====
lbl_title = tk.Label(root, text="ĐĂNG NHẬP HỆ THỐNG",
                     font=("Times New Roman", 22, "bold"), fg="#ad1457", bg="#fce4ec")
lbl_title.pack(pady=15)

# ==== FRAME CHỨA FORM ====
frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
frame.pack(padx=30, pady=10, fill="x")

# ==== ẢNH Ổ KHÓA ====
try:
    img_lock = Image.open("lock.png")
    img_lock = img_lock.resize((100, 100))
    photo_lock = ImageTk.PhotoImage(img_lock)
    lbl_img = tk.Label(frame, image=photo_lock, bg="#ffffff")
    lbl_img.grid(row=0, column=0, rowspan=2, padx=20, pady=10)
except:
    lbl_img = tk.Label(frame, text="🔒", font=("Arial", 50), bg="#ffffff")
    lbl_img.grid(row=0, column=0, rowspan=2, padx=20, pady=10)

# ==== TÊN ĐĂNG NHẬP ====
lbl_user = tk.Label(frame, text="Tên đăng nhập:", font=("Times New Roman", 13, "bold"), bg="#ffffff")
lbl_user.grid(row=0, column=1, sticky="w", pady=10, padx=5)
entry_user = tk.Entry(frame, font=("Times New Roman", 13), width=25, bg="#f8bbd0")
entry_user.grid(row=0, column=2, padx=10, pady=5)

# ==== MẬT KHẨU ====
lbl_pass = tk.Label(frame, text="Mật khẩu:", font=("Times New Roman", 13, "bold"), bg="#ffffff")
lbl_pass.grid(row=1, column=1, sticky="w", pady=10, padx=5)
entry_pass = tk.Entry(frame, font=("Times New Roman", 13), width=25, show="*", bg="#f8bbd0")
entry_pass.grid(row=1, column=2, padx=10, pady=5)

# ==== NÚT ĐĂNG NHẬP & THOÁT ====
btn_login = tk.Button(root, text="Đăng nhập", font=("Times New Roman", 14, "bold"),
                      bg="#f48fb1", fg="white", activebackground="#f06292",
                      width=15, height=1, relief="flat", cursor="hand2", command=dang_nhap)
btn_login.pack(pady=15)

btn_exit = tk.Button(root, text="Thoát", font=("Times New Roman", 12, "bold"),
                     bg="#f8bbd0", fg="#ad1457", width=12, command=thoat)
btn_exit.pack()

# ==== PHÍM ENTER ====
root.bind('<Return>', lambda event: dang_nhap())

root.mainloop()
