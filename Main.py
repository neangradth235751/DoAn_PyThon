import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# ======== HÀM CHÍNH ========
def open_main_menu():
    root = tk.Tk()
    root.title("CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG VẬT LIỆU XÂY DỰNG")
    root.geometry("1000x600")
    root.resizable(False, False)

    # ==== ẢNH NỀN ====
    try:
        bg_image = Image.open("steel_background.jpg")  # ảnh nền (thép)
        bg_image = bg_image.resize((1000, 600))
        bg_photo = ImageTk.PhotoImage(bg_image)
        lbl_bg = tk.Label(root, image=bg_photo)
        lbl_bg.image = bg_photo
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        root.configure(bg="#fce4ec")  # fallback màu pastel hồng

    # ==== THANH THANH CÔNG CỤ NGANG ====
    toolbar = tk.Frame(root, bg="#f8bbd0", height=90)
    toolbar.pack(fill="x")

    # Danh sách các nút menu (icon_path, text, command)
    buttons = [
        ("icon_login.png", "Đăng nhập", lambda: messagebox.showinfo("Đăng nhập", "Mở form đăng nhập")),
        ("icon_staff.png", "Nhân viên", lambda: messagebox.showinfo("Nhân viên", "Mở danh sách nhân viên")),
        ("icon_invoice.png", "Hóa đơn", lambda: messagebox.showinfo("Hóa đơn", "Mở hóa đơn bán hàng")),
        ("icon_material.png", "Vật liệu", lambda: messagebox.showinfo("Vật liệu", "Mở danh mục vật liệu")),
        ("icon_customer.png", "Khách hàng", lambda: messagebox.showinfo("Khách hàng", "Mở danh sách khách hàng")),
        ("icon_goods.png", "Hàng hóa", lambda: messagebox.showinfo("Hàng hóa", "Mở quản lý hàng hóa")),
        ("icon_supplier.png", "Nhà cung cấp", lambda: messagebox.showinfo("Nhà cung cấp", "Mở danh sách NCC")),
        ("icon_exit.png", "Thoát", root.destroy)
    ]

    # ==== TẠO NÚT CÔNG CỤ ====
    icons = []
    for i, (icon_path, text, cmd) in enumerate(buttons):
        try:
            img = Image.open(icon_path)
            img = img.resize((48, 48))
            photo = ImageTk.PhotoImage(img)
            icons.append(photo)
            btn = tk.Button(
                toolbar,
                image=photo,
                text=text,
                compound="top",
                font=("Arial", 10, "bold"),
                bg="#f8bbd0",
                fg="#4a148c",
                activebackground="#f48fb1",
                relief="flat",
                cursor="hand2",
                width=100,
                command=cmd
            )
        except:
            btn = tk.Button(
                toolbar,
                text=text,
                font=("Arial", 10, "bold"),
                bg="#f8bbd0",
                fg="#4a148c",
                activebackground="#f48fb1",
                relief="flat",
                cursor="hand2",
                width=100,
                command=cmd
            )
        btn.grid(row=0, column=i, padx=5, pady=10)

    # ==== TIÊU ĐỀ LỚN ====
    lbl_title = tk.Label(
        root,
        text="CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG VẬT LIỆU XÂY DỰNG",
        bg="#ffffffcc",
        fg="#4a148c",
        font=("Helvetica", 18, "bold"),
        pady=10
    )
    lbl_title.pack(fill="x", pady=(10, 0))

    # ==== ẢNH TRUNG TÂM ====
    try:
        img_main = Image.open("steel_pipes.jpg")  # ảnh ống thép
        img_main = img_main.resize((800, 400))
        photo_main = ImageTk.PhotoImage(img_main)
        lbl_img = tk.Label(root, image=photo_main, bg="#ffffffcc")
        lbl_img.image = photo_main
        lbl_img.pack(pady=20)
    except:
        lbl_noimg = tk.Label(root, text="[Không tìm thấy ảnh nền thép]",
                             bg="#ffffffcc", fg="#555", font=("Arial", 14))
        lbl_noimg.pack(pady=20)

    root.mainloop()


# ======== CHẠY ========
if __name__ == "__main__":
    open_main_menu()
