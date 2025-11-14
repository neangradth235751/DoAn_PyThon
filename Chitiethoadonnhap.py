import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ======== KẾT NỐI MYSQL ========
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",  # đổi theo mật khẩu MySQL của bạn
        database="quanly_cuahangvatlieuxaydung"
    )

# ======== CLASS CHI TIẾT HÓA ĐƠN NHẬP ========
class ChiTietHoaDonNhap(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chi Tiết Hóa Đơn Nhập")
        self.geometry("1100x650")
        self.configure(bg="#dfeaf5")

        # ========== HEADER ==========
        tk.Label(
            self, text="CHI TIẾT HÓA ĐƠN NHẬP",
            font=("Times New Roman", 26, "bold"),
            bg="#1565c0", fg="white", pady=10
        ).pack(fill="x")

        # ========== KHUNG CHÍNH ==========
        frame_main = tk.Frame(self, bg="#dfeaf5")
        frame_main.pack(fill="both", expand=True, padx=10, pady=10)

        # ========== KHUNG TRÁI ==========
        frame_left = tk.LabelFrame(
            frame_main, text="Cập nhật Chi tiết Hóa Đơn Nhập",
            font=("Times New Roman", 12, "bold"),
            bg="#dfeaf5", padx=20, pady=10
        )
        frame_left.place(x=10, y=10, width=760, height=330)

        # Biến dùng chung
        self.vars = {
            "MaHDN": tk.StringVar(value="HDN001"),
            "NgayLap": tk.StringVar(value="2025-11-01"),
            "NCC": tk.StringVar(value="Công ty Thép ABC"),
            "NhanVien": tk.StringVar(value="Nguyễn Văn A"),

            "VatLieu": tk.StringVar(),
            "SoLuong": tk.StringVar(),
            "DonGia": tk.StringVar(),
            "DonVi": tk.StringVar(),
            "ThanhTien": tk.StringVar()
        }

        # ========== THÔNG TIN HÓA ĐƠN ==========
        tk.Label(frame_left, text="Số hóa đơn:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=3)
        tk.Entry(frame_left, textvariable=self.vars["MaHDN"], width=20, font=("Times New Roman", 12)).grid(row=0, column=1, pady=3)

        tk.Label(frame_left, text="Ngày lập HĐ:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=0, column=2, sticky="w", pady=3)
        tk.Entry(frame_left, textvariable=self.vars["NgayLap"], width=20, font=("Times New Roman", 12)).grid(row=0, column=3, pady=3)

        tk.Label(frame_left, text="Nhà cung cấp:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=3)
        tk.Entry(frame_left, textvariable=self.vars["NCC"], width=20, font=("Times New Roman", 12)).grid(row=1, column=1, pady=3)

        tk.Label(frame_left, text="Nhân viên:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=1, column=2, sticky="w", pady=3)
        tk.Entry(frame_left, textvariable=self.vars["NhanVien"], width=20, font=("Times New Roman", 12)).grid(row=1, column=3, pady=3)

        # ========== THÔNG TIN CHI TIẾT ==========
        tk.Label(frame_left, text="Vật liệu:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=3)
        ttk.Combobox(frame_left, textvariable=self.vars["VatLieu"],
                     values=self.load_vatlieu(), width=18).grid(row=2, column=1)

        tk.Label(frame_left, text="Số lượng:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=2, column=2, sticky="w")
        tk.Entry(frame_left, textvariable=self.vars["SoLuong"], width=20, font=("Times New Roman", 12)).grid(row=2, column=3)

        tk.Label(frame_left, text="Đơn vị:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=3, column=0, sticky="w", pady=3)
        tk.Entry(frame_left, textvariable=self.vars["DonVi"], width=20, font=("Times New Roman", 12)).grid(row=3, column=1)

        tk.Label(frame_left, text="Đơn giá:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=3, column=2, sticky="w")
        tk.Entry(frame_left, textvariable=self.vars["DonGia"], width=20, font=("Times New Roman", 12)).grid(row=3, column=3)

        tk.Label(frame_left, text="Thành tiền:", bg="#dfeaf5", font=("Times New Roman", 12)).grid(row=4, column=2, sticky="w", pady=3)
        tk.Entry(frame_left, textvariable=self.vars["ThanhTien"], width=20, font=("Times New Roman", 12)).grid(row=4, column=3)

        # ========== KHUNG CHỨC NĂNG ==========
        frame_btn = tk.LabelFrame(
            frame_main, text="Chức năng",
            font=("Times New Roman", 12, "bold"),
            bg="#dfeaf5", padx=10, pady=10
        )
        frame_btn.place(x=800, y=10, width=280, height=330)

        for text in ["Thêm", "Sửa", "Xóa", "Lưu", "Hủy", "In"]:
            tk.Button(frame_btn, text=text, width=14, height=1,
                      font=("Times New Roman", 12, "bold"),
                      bg="#c5e1a5").pack(pady=7)

        # ========== TABLE ==========
        frame_table = tk.Frame(frame_main, bg="white")
        frame_table.place(x=10, y=350, width=1070, height=270)

        columns = ("VatLieu", "SoLuong", "DonVi", "DonGia", "ThanhTien")
        self.table = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)

        self.table.heading("VatLieu", text="Vật liệu")
        self.table.heading("SoLuong", text="Số lượng")
        self.table.heading("DonVi", text="Đơn vị")
        self.table.heading("DonGia", text="Đơn giá")
        self.table.heading("ThanhTien", text="Thành tiền")

        for col in columns:
            self.table.column(col, width=200)

        self.table.pack(fill="both", expand=True)

        # Load dữ liệu từ database
        self.load_table_data()

    # ======== LOAD VẬT LIỆU CHO COMBOBOX ==========
    def load_vatlieu(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT TenVL FROM vatlieu")
            vatlieu = [row[0] for row in cursor.fetchall()]
            conn.close()
            return vatlieu
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi kết nối", str(err))
            return []

    # ======== LOAD DỮ LIỆU CHO BẢNG ==========
    def load_table_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT v.TenVL, c.SoLuong, c.DonVi, c.DonGia, c.ThanhTien
                FROM chitiethoadonnhap c
                JOIN vatlieu v ON c.MaVL = v.MaVL
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                self.table.insert("", "end", values=row)
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi truy vấn", str(err))


# ========== CHẠY ==========
if __name__ == "__main__":
    app = ChiTietHoaDonNhap()
    app.mainloop()
