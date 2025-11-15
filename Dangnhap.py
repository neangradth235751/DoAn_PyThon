import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector

# ==== HÀM XỬ LÝ ==== #
def dang_nhap():
    user = entry_user.get()
    pw = entry_pass.get()

    if not user or not pw:
        messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên đăng nhập và mật khẩu!")
        return

    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="123456789",
            database="quanly_cuahangvatlieuxaydung"
        )
        cursor = conn.cursor()
        query = "SELECT * FROM nguoidung WHERE tennguoidung=%s AND matkhau=%s"
        cursor.execute(query, (user, pw))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Thành công", "Đăng nhập thành công!")
            root.destroy()  # sau này mở menu chính
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


# ==== CỬA SỔ CHÍNH ==== #
root = tk.Tk()
root.title("Đăng nhập - Quản Lý Cửa Hàng VLXD")
root.geometry("550x330")
root.resizable(False, False)
root.configure(bg="#fce4ec")

# ==== ICON WINDOW ==== #
try:
    root.iconbitmap("icon.ico")
except:
    pass

# ==== TIÊU ĐỀ ==== #
lbl_title = tk.Label(
    root,
    text="ĐĂNG NHẬP HỆ THỐNG",
    font=("Times New Roman", 22, "bold"),
    fg="#ad1457",
    bg="#fce4ec"
)
lbl_title.pack(pady=15)

# ==== KHUNG TRẮNG ==== #
frame = tk.Frame(root, bg="#ffffff", bd=2, relief="ridge")
frame.pack(pady=10, padx=30, fill="x")

# ==== ẢNH Ổ KHÓA ==== #
try:
    img_lock = Image.open("lock.png")
    img_lock = img_lock.resize((100, 100))
    photo_lock = ImageTk.PhotoImage(img_lock)
    lbl_img = tk.Label(frame, image=photo_lock, bg="#ffffff")
    lbl_img.grid(row=0, column=0, rowspan=2, padx=20, pady=10)
except:
    lbl_img = tk.Label(frame, text="🔒", font=("Arial", 50), bg="#ffffff")
    lbl_img.grid(row=0, column=0, rowspan=2, padx=20, pady=10)

# ==== ICON NGƯỜI ==== #
try:
    img_user = Image.open("user.png")
    img_user = img_user.resize((22, 22))
    photo_user = ImageTk.PhotoImage(img_user)
except:
    photo_user = None

# ==== TÊN ĐĂNG NHẬP ==== #
lbl_user = tk.Label(frame, text="Tên đăng nhập:", font=("Times New Roman", 13, "bold"), bg="#ffffff")
lbl_user.grid(row=0, column=1, sticky="w", pady=10, padx=5)

entry_user_frame = tk.Frame(frame, bg="#f8bbd0", bd=0)
entry_user_frame.grid(row=0, column=2, padx=10)
if photo_user:
    tk.Label(entry_user_frame, image=photo_user, bg="#f8bbd0").pack(side="left", padx=5)
entry_user = tk.Entry(entry_user_frame, font=("Times New Roman", 13), width=20, bd=0, bg="#f8bbd0")
entry_user.pack(side="left", padx=2, pady=3)

# ==== MẬT KHẨU ==== #
lbl_pass = tk.Label(frame, text="Mật khẩu:", font=("Times New Roman", 13, "bold"), bg="#ffffff")
lbl_pass.grid(row=1, column=1, sticky="w", pady=10, padx=5)

entry_pass = tk.Entry(frame, font=("Times New Roman", 13), width=25, show="*", bg="#f8bbd0", bd=0)
entry_pass.grid(row=1, column=2, padx=10)

# ==== NÚT ==== #
btn_login = tk.Button(
    root,
    text="Đăng nhập",
    font=("Times New Roman", 14, "bold"),
    bg="#f48fb1",
    fg="white",
    activebackground="#f06292",
    activeforeground="white",
    width=15,
    height=1,
    command=dang_nhap,
    relief="flat",
    cursor="hand2"
)
btn_login.pack(pady=20)

btn_exit = tk.Button(
    root,
    text="Thoát",
    font=("Times New Roman", 12, "bold"),
    bg="#f8bbd0",
    fg="#ad1457",
    activebackground="#f06292",
    width=12,
    command=thoat
)
btn_exit.pack()

# ==== PHÍM ENTER ==== #
root.bind('<Return>', lambda event: dang_nhap())

root.mainloop()