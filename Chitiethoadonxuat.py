import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import mysql.connector

# =========================
# KẾT NỐI MYSQL
# =========================
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="quanly_cuahangvatlieuxaydung"
    )

# =========================
# ĐỊNH DẠNG SỐ THÀNH VNĐ
# =========================
def format_vnd(n):
    return f"{n:,.0f} VNĐ".replace(",", ".")

# =========================
# APP TKINTER
# =========================
class HoaDonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("HÓA ĐƠN XUẤT VẬT LIỆU")
        self.geometry("1200x650")
        self.configure(bg="#ffe6f2")

        # Title
        tk.Label(self, text="CHI TIẾT HÓA ĐƠN XUẤT",
                 font=("Arial", 24, "bold"), bg="#ffe6f2",
                 fg="#cc0066").pack(pady=10)

        # THÔNG TIN HÓA ĐƠN
        frame_info = tk.LabelFrame(self, text="Thông tin hóa đơn", 
                                   bg="#ffe6f2", font=("Arial", 11, "bold"))
        frame_info.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_info, text="Mã HD:", bg="#ffe6f2").grid(row=0, column=0, pady=5)
        self.txt_ma = tk.Entry(frame_info, width=20)
        self.txt_ma.grid(row=0, column=1, padx=5)
        self.txt_ma.insert(0, "HD001")

        tk.Label(frame_info, text="Tên NV:", bg="#ffe6f2").grid(row=0, column=2)
        self.txt_nv = tk.Entry(frame_info, width=25)
        self.txt_nv.grid(row=0, column=3, padx=5)

        tk.Label(frame_info, text="Tên KH:", bg="#ffe6f2").grid(row=1, column=0)
        self.txt_kh = tk.Entry(frame_info, width=25)
        self.txt_kh.grid(row=1, column=1, padx=5)

        tk.Label(frame_info, text="SĐT:", bg="#ffe6f2").grid(row=1, column=2)
        self.txt_sdt = tk.Entry(frame_info, width=20)
        self.txt_sdt.grid(row=1, column=3, padx=5)

        tk.Label(frame_info, text="Ngày lập:", bg="#ffe6f2").grid(row=2, column=0)
        self.txt_date = tk.Entry(frame_info, width=30)
        self.txt_date.grid(row=2, column=1, padx=5)
        self.txt_date.insert(0, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

        # CHỌN VẬT LIỆU
        frame_select = tk.LabelFrame(self, text="Chọn vật liệu", 
                                     bg="#ffe6f2", font=("Arial", 11, "bold"))
        frame_select.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_select, text="Tên VL:", bg="#ffe6f2").grid(row=0, column=0, pady=5)
        self.cbo_vl = ttk.Combobox(frame_select, width=30)
        self.cbo_vl.grid(row=0, column=1, padx=5)
        self.cbo_vl.bind("<<ComboboxSelected>>", self.load_info)

        tk.Label(frame_select, text="Đơn vị tính:", bg="#ffe6f2").grid(row=0, column=2)
        self.txt_dvt = tk.Entry(frame_select, width=20)
        self.txt_dvt.grid(row=0, column=3)

        tk.Label(frame_select, text="SL tồn kho:", bg="#ffe6f2").grid(row=1, column=0)
        self.txt_ton = tk.Entry(frame_select, width=20)
        self.txt_ton.grid(row=1, column=1)

        tk.Label(frame_select, text="SL xuất:", bg="#ffe6f2").grid(row=1, column=2)
        self.txt_sl = tk.Entry(frame_select, width=20)
        self.txt_sl.grid(row=1, column=3)

        # LIST VIEW
        frame_list = tk.LabelFrame(self, text="Danh sách xuất hàng", 
                                   bg="#ffe6f2", font=("Arial", 11, "bold"))
        frame_list.pack(fill="both", expand=True, padx=15, pady=5)

        self.tree = ttk.Treeview(frame_list, columns=("ten","dvt","sl","dg","tt"), show="headings", height=10)
        self.tree.heading("ten", text="Tên VL")
        self.tree.heading("dvt", text="Đơn vị tính")
        self.tree.heading("sl", text="SL xuất")
        self.tree.heading("dg", text="Đơn giá")
        self.tree.heading("tt", text="Thành tiền")

        self.tree.column("ten", width=250, anchor="center")
        self.tree.column("dvt", width=150, anchor="center")
        self.tree.column("sl", width=100, anchor="center")
        self.tree.column("dg", width=120, anchor="center")
        self.tree.column("tt", width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # BUTTON ZONE
        frame_btn = tk.Frame(self, bg="#ffe6f2")
        frame_btn.pack(pady=10)

        ttk.Button(frame_btn, text="Thêm", command=self.them).grid(row=0, column=0, padx=5)
        ttk.Button(frame_btn, text="Xóa", command=self.xoa).grid(row=0, column=1, padx=5)
        ttk.Button(frame_btn, text="Sửa", command=self.sua).grid(row=0, column=2, padx=5)
        ttk.Button(frame_btn, text="Lưu", command=self.luu).grid(row=0, column=3, padx=5)
        ttk.Button(frame_btn, text="Hủy", command=self.huy).grid(row=0, column=4, padx=5)
        ttk.Button(frame_btn, text="In hóa đơn", command=self.inbill).grid(row=0, column=5, padx=5)

        # Load dữ liệu vật liệu từ MySQL
        self.load_vatlieu()

    # =========================
    # LOAD VẬT LIỆU TỪ MYSQL
    # =========================
    def load_vatlieu(self):
        self.vat_lieu = {}
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaVL, TenVL, DonVi, SoLuong, DonGia FROM vatlieu")
            rows = cursor.fetchall()
            for r in rows:
                self.vat_lieu[r[1]] = {"MaVL": r[0], "dvt": r[2], "ton": r[3], "gia": float(r[4])}
            self.cbo_vl['values'] = list(self.vat_lieu.keys())
            cursor.close()
            conn.close()
        except mysql.connector.Error as e:
            messagebox.showerror("MySQL Error", str(e))

    # =========================
    # LOAD THÔNG TIN KHO CHO VL CHỌN
    # =========================
    def load_info(self, event):
        ten = self.cbo_vl.get()
        if ten in self.vat_lieu:
            self.txt_dvt.delete(0, tk.END)
            self.txt_dvt.insert(0, self.vat_lieu[ten]["dvt"])
            self.txt_ton.delete(0, tk.END)
            self.txt_ton.insert(0, self.vat_lieu[ten]["ton"])

    # =========================
    # THÊM
    # =========================
    def them(self):
        ten = self.cbo_vl.get()
        if ten not in self.vat_lieu:
            messagebox.showerror("Lỗi", "Vui lòng chọn vật liệu hợp lệ!")
            return
        if not self.txt_sl.get().isdigit():
            messagebox.showerror("Lỗi", "Số lượng xuất phải là số nguyên")
            return

        sl = int(self.txt_sl.get())
        if sl > self.vat_lieu[ten]["ton"]:
            messagebox.showerror("Lỗi", f"Số lượng tồn chỉ còn: {self.vat_lieu[ten]['ton']}")
            return

        dg = self.vat_lieu[ten]["gia"]
        tt = sl * dg
        self.tree.insert("", tk.END, values=(ten, self.vat_lieu[ten]["dvt"], sl, format_vnd(dg), format_vnd(tt)))

        self.vat_lieu[ten]["ton"] -= sl
        self.txt_ton.delete(0, tk.END)
        self.txt_ton.insert(0, self.vat_lieu[ten]["ton"])

    # =========================
    # XÓA
    # =========================
    def xoa(self):
        item = self.tree.focus()
        if item:
            v = self.tree.item(item, "values")
            ten = v[0]
            sl = int(v[2])
            self.vat_lieu[ten]["ton"] += sl
            self.tree.delete(item)

    # =========================
    # SỬA
    # =========================
    def sua(self):
        item = self.tree.focus()
        if not item:
            return
        ten = self.cbo_vl.get()
        if ten not in self.vat_lieu:
            messagebox.showerror("Lỗi", "Vui lòng chọn vật liệu hợp lệ!")
            return
        if not self.txt_sl.get().isdigit():
            messagebox.showerror("Lỗi", "Số lượng xuất phải là số nguyên")
            return

        sl_new = int(self.txt_sl.get())
        v_old = self.tree.item(item, "values")
        sl_old = int(v_old[2])

        self.vat_lieu[ten]["ton"] += sl_old
        if sl_new > self.vat_lieu[ten]["ton"]:
            messagebox.showerror("Lỗi", f"Số lượng tồn chỉ còn: {self.vat_lieu[ten]['ton']}")
            self.vat_lieu[ten]["ton"] -= sl_old
            return

        dg = self.vat_lieu[ten]["gia"]
        tt = sl_new * dg
        self.tree.item(item, values=(ten, self.vat_lieu[ten]["dvt"], sl_new, format_vnd(dg), format_vnd(tt)))

        self.vat_lieu[ten]["ton"] -= sl_new
        self.txt_ton.delete(0, tk.END)
        self.txt_ton.insert(0, self.vat_lieu[ten]["ton"])

    # =========================
    # LƯU HÓA ĐƠN VÀ CHI TIẾT VÀO MYSQL
    # =========================
    def luu(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            mahd = self.txt_ma.get()
            tennv = self.txt_nv.get()
            tenkh = self.txt_kh.get()
            sdt = self.txt_sdt.get()
            ngay = datetime.now()

            cursor.execute(
                "INSERT INTO hoadonxuat (MaHD, TenNV, TenKH, SDT, NgayLap) VALUES (%s, %s, %s, %s, %s)",
                (mahd, tennv, tenkh, sdt, ngay)
            )

            for item in self.tree.get_children():
                v = self.tree.item(item, "values")
                mavl = self.vat_lieu[v[0]]["MaVL"]
                cursor.execute(
                    "INSERT INTO chitiethoadonxuat (MaHD, MaVL, SoLuong, DonGia) VALUES (%s, %s, %s, %s)",
                    (mahd, mavl, int(v[2]), float(self.vat_lieu[v[0]]["gia"]))
                )

            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Lưu", "Đã lưu hóa đơn vào MySQL!")
        except mysql.connector.Error as e:
            messagebox.showerror("MySQL Error", str(e))

    # =========================
    # HỦY
    # =========================
    def huy(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    # =========================
    # IN HÓA ĐƠN
    # =========================
    def inbill(self):
        bill = f"""
====== HÓA ĐƠN XUẤT VẬT LIỆU ======
Mã HD: {self.txt_ma.get()}
Tên NV: {self.txt_nv.get()}
Tên KH: {self.txt_kh.get()}
SĐT: {self.txt_sdt.get()}
Ngày lập: {self.txt_date.get()}
-----------------------------------
Tên VL - SL - Đơn giá - Thành tiền
"""
        tong = 0
        for item in self.tree.get_children():
            v = self.tree.item(item, "values")
            bill += f"{v[0]} - {v[2]} - {v[3]} - {v[4]}\n"
            tong += int(v[2]) * self.vat_lieu[v[0]]["gia"]

        bill += f"\nTỔNG CỘNG: {format_vnd(tong)}\n"
        bill += "\nCẢM ƠN QUÝ KHÁCH!"
        messagebox.showinfo("HÓA ĐƠN", bill)

# =========================
# RUN APP
# =========================
if __name__ == "__main__":
    app = HoaDonApp()
    app.mainloop()
