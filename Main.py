import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk

# ======== HÀM MỞ FORM MẪU ========
def open_form(title):
    form = Toplevel()
    form.title(title)
    form.geometry("700x400")
    form.configure(bg="#fce4ec")
    tk.Label(form, text=title, font=("Helvetica", 16, "bold"), fg="#ad1457", bg="#fce4ec").pack(pady=20)
    tk.Label(form, text="[Nội dung quản lý sẽ được thêm ở đây]", bg="#fce4ec", fg="#555", font=("Arial", 12)).pack(pady=10)

# ======== HÀM CHÍNH MAIN MENU ========
def open_main_menu():
    root = tk.Tk()
    root.title("QUẢN LÝ CỬA HÀNG VLXD")
    root.geometry("1050x650")
    root.resizable(False, False)

    # ==== ẢNH NỀN ====
    try:
        bg_image = Image.open("construction_materials.jpg")
        bg_image = bg_image.resize((1000, 600))
        bg_photo = ImageTk.PhotoImage(bg_image)
        lbl_bg = tk.Label(root, image=bg_photo)
        lbl_bg.image = bg_photo
        lbl_bg.place(x=0, y=0, relwidth=1, relheight=1)
    except:
        root.configure(bg="#fce4ec")

    # ==== THANH MENU NGANG ====
    toolbar = tk.Frame(root, bg="#ffffff", height=80)
    toolbar.pack(fill="x", pady=(10, 0))

    buttons = [
        ("👨‍💼 Nhân viên", "Quản lý nhân viên"),
        ("🧾 Hóa đơn", "Danh sách hóa đơn"),
        ("🧱 Vật liệu", "Danh mục vật liệu"),
        ("👥 Khách hàng", "Danh sách khách hàng"),
        ("📦 Hàng hóa", "Quản lý hàng hóa"),
        ("🚚 Nhà cung cấp", "Danh sách nhà cung cấp"),
        (" ❌Thoát", None)
    ]

    def on_enter(e):
        e.widget['bg'] = "#f8bbd0"

    def on_leave(e):
        e.widget['bg'] = "#ffffff"

    for i, (text, title) in enumerate(buttons):
        def cmd(t=title):
            if t: open_form(t)
            else: root.destroy()
        btn = tk.Button(toolbar, text=text, font=("Arial", 10, "bold"),
                        bg="#ffffff", fg="#4a148c", activebackground="#f8bbd0",
                        relief="flat", cursor="hand2", width=16, command=cmd)
        btn.grid(row=0, column=i, padx=5, pady=10)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    # ==== TIÊU ĐỀ ====
    lbl_title = tk.Label(root, text="CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG VẬT LIỆU XÂY DỰNG",
                         bg="#ffffff", fg="#4a148c", font=("Helvetica", 20, "bold"))
    lbl_title.pack(pady=(20, 10))

    # ==== ẢNH TRUNG TÂM ====
    try:
        img_main = Image.open("backgroup.jpg")
        img_main = img_main.resize((700, 350))
        photo_main = ImageTk.PhotoImage(img_main)
        lbl_img = tk.Label(root, image=photo_main, bg="#ffffff")
        lbl_img.image = photo_main
        lbl_img.pack(pady=10)
    except:
        lbl_noimg = tk.Label(root, text="♻️",
                             bg="#ffffff", fg="#555", font=("Arial", 14))
        lbl_noimg.pack(pady=20)

    root.mainloop()

# ======== CHẠY CHƯƠNG TRÌNH ========
if __name__ == "__main__":
    open_main_menu()
