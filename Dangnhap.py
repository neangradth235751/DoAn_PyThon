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
            root.destroy()  # mở giao diện chính sau này
        else:
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu!")

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối MySQL:\n{err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


# ==== CỬA SỔ CHÍNH ==== #
root = tk.Tk()
root.title("Đăng nhập - Quản Lí Cửa Hàng VLXD")
root.geometry("520x360")
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
    text="ĐĂNG NHẬP",
    font=("Segoe UI Semibold", 28, "bold"),
    fg="#ad1457",
    bg="#fce4ec"
)
lbl_title.pack(pady=20)

# ==== KHUNG ==== #
frame = tk.Frame(root, bg="#ffffff", bd=0, relief="ridge")
frame.pack(pady=10, padx=30, fill="x")

# ==== ẢNH ==== #
try:
    img = Image.open("lock.png")
    img = img.resize((100, 100))
    photo = ImageTk.PhotoImage(img)
    lbl_img = tk.Label(frame, image=photo, bg="#ffffff")
    lbl_img.grid(row=0, column=0, rowspan=2, padx=20, pady=10)
except:
    pass

# ==== NHÃN VÀ ENTRY ==== #
tk.Label(frame, text="Tên đăng nhập:", font=("Arial", 12), bg="#ffffff").grid(row=0, column=1, sticky="w", pady=10, padx=5)
entry_user = tk.Entry(frame, font=("Arial", 12), width=25, bg="#f8bbd0")
entry_user.grid(row=0, column=2, padx=10)

tk.Label(frame, text="Mật khẩu:", font=("Arial", 12), bg="#ffffff").grid(row=1, column=1, sticky="w", pady=10, padx=5)
entry_pass = tk.Entry(frame, font=("Arial", 12), width=25, show="*", bg="#f8bbd0")
entry_pass.grid(row=1, column=2, padx=10)

# ==== NÚT ĐĂNG NHẬP ==== #
btn_login = tk.Button(
    root,
    text="Đăng nhập",
    font=("Segoe UI Semibold", 14),
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
btn_login.pack(pady=25)

# ==== NÚT THOÁT ==== #
btn_exit = tk.Button(frame, text="Thoát", font=("Arial", 12, "bold"),
                     bg="#f8bbd0", fg="#ad1457", activebackground="#f06292",
                     width=15, command=thoat)
btn_exit.grid(row=3, column=1, columnspan=2, pady=5)

# ==== PHÍM ENTER ==== #
root.bind('<Return>', lambda event: dang_nhap())

root.mainloop()
