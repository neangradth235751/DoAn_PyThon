import tkinter as tk
from tkinter import messagebox, Toplevel
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
            messagebox.showinfo("Thành công", f"Đăng nhập thành công!")
            root.destroy()  # sau này có thể mở giao diện chính
        else:
            messagebox.showerror("Thất bại", "Sai tên đăng nhập hoặc mật khẩu!")

    except mysql.connector.Error as err:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối MySQL:\n{err}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()


def thoat():
    root.destroy()


# ==== HÀM ĐĂNG KÝ ==== #
def mo_dang_ky():
    def dang_ky():
        new_user = entry_new_user.get()
        new_pass = entry_new_pass.get()
        confirm_pass = entry_confirm_pass.get()

        if not new_user or not new_pass:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập đầy đủ thông tin!")
            return
        if new_pass != confirm_pass:
            messagebox.showwarning("Mật khẩu", "Mật khẩu nhập lại không khớp!")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456789",
                database="quanly_cuahangvatlieuxaydung"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM nguoidung WHERE tennguoidung=%s", (new_user,))
            if cursor.fetchone():
                messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại!")
                return

            cursor.execute("INSERT INTO nguoidung (tennguoidung, matkhau) VALUES (%s, %s)", (new_user, new_pass))
            conn.commit()
            messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
            win_dk.destroy()

        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối MySQL:\n{err}")

        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()

    win_dk = Toplevel(root)
    win_dk.title("Đăng ký tài khoản")
    win_dk.geometry("450x350")
    win_dk.configure(bg="#fce4ec")
    win_dk.resizable(False, False)

    tk.Label(win_dk, text="TẠO TÀI KHOẢN MỚI", font=("Helvetica", 18, "bold"),
             bg="#fce4ec", fg="#ad1457").pack(pady=15)

    frame_dk = tk.Frame(win_dk, bg="white", bd=0, relief="ridge")
    frame_dk.pack(padx=20, pady=10, fill="x")

    tk.Label(frame_dk, text="Tên đăng nhập:", font=("Arial", 12), bg="white").grid(row=0, column=0, pady=10, padx=10, sticky="w")
    entry_new_user = tk.Entry(frame_dk, font=("Arial", 12), width=25, bg="#f8bbd0")
    entry_new_user.grid(row=0, column=1)

    tk.Label(frame_dk, text="Mật khẩu:", font=("Arial", 12), bg="white").grid(row=1, column=0, pady=10, padx=10, sticky="w")
    entry_new_pass = tk.Entry(frame_dk, font=("Arial", 12), width=25, bg="#f8bbd0", show="*")
    entry_new_pass.grid(row=1, column=1)

    tk.Label(frame_dk, text="Nhập lại mật khẩu:", font=("Arial", 12), bg="white").grid(row=2, column=0, pady=10, padx=10, sticky="w")
    entry_confirm_pass = tk.Entry(frame_dk, font=("Arial", 12), width=25, bg="#f8bbd0", show="*")
    entry_confirm_pass.grid(row=2, column=1)

    tk.Button(frame_dk, text="Đăng ký", font=("Arial", 12, "bold"), bg="#f48fb1", fg="white",
              activebackground="#f06292", width=15, command=dang_ky).grid(row=3, column=0, columnspan=2, pady=20)


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
lbl_title = tk.Label(root, text="ĐĂNG NHẬP", font=("Helvetica", 26, "bold"),
                     fg="#ad1457", bg="#fce4ec")
lbl_title.pack(pady=15)

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

# ==== NÚT NGANG ==== #
btn_frame = tk.Frame(frame, bg="white")
btn_frame.grid(row=2, column=1, columnspan=2, pady=20)

btn_login = tk.Button(btn_frame, text="Đăng nhập", font=("Arial", 12, "bold"),
                      bg="#f48fb1", fg="white", activebackground="#f06292",
                      width=12, command=dang_nhap)
btn_login.grid(row=0, column=0, padx=10)

btn_signup = tk.Button(btn_frame, text="Đăng ký", font=("Arial", 12, "bold"),
                       bg="#ce93d8", fg="white", activebackground="#ba68c8",
                       width=12, command=mo_dang_ky)
btn_signup.grid(row=0, column=1, padx=10)

# ==== NÚT THOÁT ==== #
btn_exit = tk.Button(frame, text="Thoát", font=("Arial", 12, "bold"),
                     bg="#f8bbd0", fg="#ad1457", activebackground="#f06292",
                     width=15, command=thoat)
btn_exit.grid(row=3, column=1, columnspan=2, pady=5)

# ==== PHÍM ENTER ==== #
root.bind('<Return>', lambda event: dang_nhap())

root.mainloop()
