import tkinter as tk
from tkinter import messagebox

# Import class NhanVien đã sửa kế thừa Toplevel
from Nhanvien import NhanVien
from Nhacungcap import NhaCungCap


class MenuChinh(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("QUẢN LÝ CỬA HÀNG VẬT LIỆU XÂY DỰNG")
        self.geometry("800x500")
        self.configure(bg="#fce4ec")

        # ===== Tạo menu =====
        menubar = tk.Menu(self)

        # Quản lý
        ql_menu = tk.Menu(menubar, tearoff=0)
        ql_menu.add_command(label="Nhân viên", command=lambda: NhanVien(self))
        ql_menu.add_command(label="Nhà cung cấp", command=lambda: NhaCungCap(self))

        # Nếu muốn, các menu khác có thể thêm sau:
        # ql_menu.add_command(label="Vật liệu", command=lambda: VatLieu(self))
        # ql_menu.add_command(label="Hóa đơn nhập", command=lambda: HoaDonNhap(self))
        # ql_menu.add_command(label="Hóa đơn xuất", command=lambda: HoaDonXuat(self))
        menubar.add_cascade(label="Quản lý", menu=ql_menu)

        # Hệ thống
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="Thoát", command=self.destroy)
        menubar.add_cascade(label="Hệ thống", menu=help_menu)

        self.config(menu=menubar)

        # Tiêu đề
        tk.Label(self, text="CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG VẬT LIỆU",
                 font=("Times New Roman",20,"bold"), fg="#ad1457", bg="#fce4ec").pack(pady=50)

if __name__ == "__main__":
    app = MenuChinh()
    app.mainloop()
