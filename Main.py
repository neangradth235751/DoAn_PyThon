import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Import các cửa sổ quản lý
from Nhanvien import NhanVien
from Nhacungcap import NhaCungCap
from Vatlieu import VatLieu
from Khachhang import KhachHang
from Hoadonxuat import HoaDonXuat
from Hoadonnhap import HoaDonNhap

class MenuChinh(tk.Toplevel):
    def __init__(self, parent_root):
        super().__init__()
        self.parent_root = parent_root
        self.title("QUẢN LÝ CỬA HÀNG VẬT LIỆU XÂY DỰNG")
        self.geometry("1000x600")
        self.configure(bg="#fce4ec")  # màu nền pastel hồng
        
        # ==== ẢNH NỀN ====
        try:
            bg_image = Image.open("construction_materials.jpg")  # ảnh nền
            bg_image = bg_image.resize((1000, 600))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            bg_label = tk.Label(self, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            pass
        
        # ===== KHUNG MENU DỌC =====
        menu_frame = tk.Frame(self, bg="#f8bbd0", width=250, height=600)  # pastel hồng đậm hơn
        menu_frame.place(x=0, y=0)
        
        title = tk.Label(menu_frame, text="CHỨC NĂNG",
                         fg="white", bg="#f48fb1", font=("Times New Roman", 16, "bold"))
        title.pack(pady=20)
        
        # Style cho các nút
        btn_bg = "#f48fb7"   # pastel hồng
        btn_hover = "#f06292"  # hover đậm hơn
        style = {"font": ("Times New Roman", 13, "bold"), 
                 "fg": "white", "bg": btn_bg, "activebackground": btn_hover,
                 "width": 22, "height": 2, "bd": 0, "relief": "flat"}
        
        # ===== CÁC NÚT CHỨC NĂNG =====
        tk.Button(menu_frame, text="👨‍💼  Nhân viên", command=lambda: NhanVien(self), **style).pack(pady=5)
        tk.Button(menu_frame, text="🏢  Nhà cung cấp", command=lambda: NhaCungCap(self), **style).pack(pady=5)
        tk.Button(menu_frame, text="🧑‍🤝‍🧑  Khách hàng", command=lambda: KhachHang(self), **style).pack(pady=5)
        tk.Button(menu_frame, text="🧱  Vật liệu", command=lambda: VatLieu(self), **style).pack(pady=5)
        tk.Button(menu_frame, text="📦  Hóa đơn nhập", command=lambda: HoaDonNhap(self), **style).pack(pady=5)
        tk.Button(menu_frame, text="🛒  Hóa đơn xuất", command=lambda: HoaDonXuat(self), **style).pack(pady=5)
        
        # Giới thiệu & thoát
        tk.Button(menu_frame, text="❓  Giới thiệu", 
                  bg=btn_bg, fg="white", font=("Times New Roman", 13, "bold"),
                  width=22, height=2, command=self.gioithieu).pack(pady=10)
        tk.Button(menu_frame, text="❌  Thoát", 
                  bg="#e57373", fg="white", font=("Times New Roman", 13, "bold"),
                  width=22, height=2, command=self.thoat_chuongtrinh).pack(pady=10)
        
        # ===== TIÊU ĐỀ CHÍNH =====
        tk.Label(self, text="CHƯƠNG TRÌNH QUẢN LÝ CỬA HÀNG VẬT LIỆU",
                 font=("Times New Roman", 20, "bold"), fg="#ad1457", bg="#fce4ec").place(x=300, y=50)
    
    def gioithieu(self):
        messagebox.showinfo ("Giới thiệu", "Chương trình quản lý cửa hàng vật liệu xây dựng.\nPhiên bản 1.0")
    
    def thoat_chuongtrinh(self):
        if messagebox.askyesno("Thoát", "Bạn có chắc muốn thoát chương trình?"):
            self.destroy()
            self.parent_root.destroy()  # đóng luôn login

# ===== TEST =====
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # ẩn root
    app = MenuChinh(root)
    app.mainloop()
