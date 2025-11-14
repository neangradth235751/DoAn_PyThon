import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

class HoaDonXuat(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thông tin Hóa Đơn Xuất")
        self.geometry("850x600")
        self.configure(bg="#fce4ec")

        # === Kết nối MySQL ===
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456789",
                database="quanly_cuahangvatlieuxaydung"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể kết nối MySQL:\n{err}")
            self.destroy()
            return

        # === Tiêu đề ===
        tk.Label(self, text="THÔNG TIN HÓA ĐƠN XUẤT", font=("Times New Roman", 20, "bold"),
                 fg="#ad1457", bg="#fce4ec").pack(pady=10)

        # === Khung nhập liệu ===
        frame_input = tk.LabelFrame(self, text="Thông tin hóa đơn xuất", font=("Times New Roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=8)
        frame_input.pack(padx=15, pady=5, fill="x")

        # Variables
        self.vars = {
            "MaHDX": tk.StringVar(),
            "MaKH": tk.StringVar(),
            "NgayLap": tk.StringVar(),
            "MaNV": tk.StringVar()
        }

        # Load dữ liệu khách hàng và nhân viên
        self.kh_dict = self.load_khachhang()  # {MaKH: TenKH}
        self.nv_dict = self.load_nv()         # {MaNV: TenNV}

        # ComboBox values
        self.cmb_kh_values = list(self.kh_dict.keys())
        self.cmb_nv_values = list(self.nv_dict.keys())

        # Labels & entries
        tk.Label(frame_input, text="Mã hóa đơn xuất:", bg="#ffffff", font=("Times New Roman", 11, "bold")).grid(row=0,column=0,padx=5,pady=5, sticky="w")
        tk.Entry(frame_input, textvariable=self.vars["MaHDX"], width=20, font=("Times New Roman",11), bg="#f8bbd0").grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame_input, text="Khách hàng:", bg="#ffffff", font=("Times New Roman", 11, "bold")).grid(row=0,column=2,padx=5,pady=5, sticky="w")
        tk.Entry(frame_input, textvariable=self.vars["MaKH"], width=20, font=("Times New Roman",11), bg="#f8bbd0").grid(row=0,column=3,padx=5,pady=5)

        tk.Label(frame_input, text="Ngày lập:", bg="#ffffff", font=("Times New Roman", 11, "bold")).grid(row=1,column=0,padx=5,pady=5, sticky="w")
        self.deNgayLap = DateEntry(frame_input, textvariable=self.vars["NgayLap"], date_pattern='yyyy-mm-dd',
                                   width=20, background="#f48fb1", foreground="white", borderwidth=2, font=("Times New Roman",11))
        self.deNgayLap.grid(row=1,column=1,padx=5,pady=5)

        tk.Label(frame_input, text="Nhân viên:", bg="#ffffff", font=("Times New Roman", 11, "bold")).grid(row=1,column=2,padx=5,pady=5, sticky="w")
        tk.Entry(frame_input, textvariable=self.vars["MaNV"], width=20, font=("Times New Roman",11), bg="#f8bbd0").grid(row=1,column=3,padx=5,pady=5)

        # === Treeview hiển thị dữ liệu ===
        columns = ("MaHDX","TenKH","NgayLap","TenNV")
        col_texts = ["Mã hóa đơn xuất","Khách hàng","Ngày lập","Nhân viên"]

        frame_table = tk.LabelFrame(self, text="Danh sách hóa đơn xuất", font=("Times New Roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=8, pady=8)
        frame_table.pack(padx=15,pady=5, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Times New Roman",11))
        style.configure("Treeview.Heading", font=("Times New Roman",12,"bold"))

        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        for i,col in enumerate(columns):
            self.tree.heading(col, text=col_texts[i])
            self.tree.column(col, width=180, anchor="center", stretch=False)

        # Màu xen kẽ
        self.tree.tag_configure('evenrow', background='#f9f9f9')
        self.tree.tag_configure('oddrow', background='#ffffff')

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(padx=3, pady=3, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # === Nút chức năng ===
        frame_btn = tk.Frame(self, bg="#fce4ec")
        frame_btn.pack(pady=5)
        btn_style = {"font":("Times New Roman",11,"bold"),"fg":"white","width":10,"relief":"flat"}

        tk.Button(frame_btn,text="Thêm", bg="#f48fb1", command=self.them_hdx, **btn_style).grid(row=0,column=0,padx=3)
        tk.Button(frame_btn,text="Xóa", bg="#e57373", command=self.xoa_hdx, **btn_style).grid(row=0,column=1,padx=3)
        tk.Button(frame_btn,text="Sửa", bg="#ffb74d", command=self.sua_hdx, **btn_style).grid(row=0,column=2,padx=3)
        tk.Button(frame_btn,text="Lưu", bg="#81c784", command=self.luu_hdx, **btn_style).grid(row=0,column=3,padx=3)
        tk.Button(frame_btn,text="Bỏ qua", bg="#90a4ae", command=self.boqua_hdx, **btn_style).grid(row=0,column=4,padx=3)
        tk.Button(frame_btn,text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0,column=5,padx=3)

        self.sua_mode=False
        self.selected_ma=None
        self.load_data()

    # ==================== Load comboBox với dict ====================
    def load_khachhang(self):
        self.cursor.execute("SELECT MaKH, TenKH FROM khachhang")
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    def load_nv(self):
        self.cursor.execute("SELECT MaNV, TenNV FROM nhanvien")
        return {row[0]: row[1] for row in self.cursor.fetchall()}

    # ==================== CRUD ====================
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT MaHDX, MaKH, NgayLap, MaNV FROM hoadonxuat")
        rows = self.cursor.fetchall()
        for idx,r in enumerate(rows):
            tag='evenrow' if idx%2==0 else 'oddrow'
            ma_kh, ma_nv = r[1], r[3]
            ten_kh = self.kh_dict.get(ma_kh, ma_kh)
            ten_nv = self.nv_dict.get(ma_nv, ma_nv)
            self.tree.insert("", "end", values=(r[0], ten_kh, r[2], ten_nv), tags=(tag,))
        self.boqua_hdx()

    def on_select(self,event):
        selected = self.tree.selection()
        if selected:
            vals = self.tree.item(selected,"values")
            ma_kh = next((k for k,v in self.kh_dict.items() if v==vals[1]), vals[1])
            ma_nv = next((k for k,v in self.nv_dict.items() if v==vals[3]), vals[3])
            self.vars["MaHDX"].set(vals[0])
            self.vars["MaKH"].set(ma_kh)
            self.vars["NgayLap"].set(vals[2])
            self.vars["MaNV"].set(ma_nv)
            self.selected_ma = vals[0]

    def them_hdx(self):
        try:
            sql="INSERT INTO hoadonxuat (MaHDX, MaKH, NgayLap, MaNV) VALUES (%s,%s,%s,%s)"
            data=tuple(v.get() for v in self.vars.values())
            self.cursor.execute(sql,data)
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Thành công","Đã thêm hóa đơn xuất!")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi",f"Lỗi thêm dữ liệu:\n{err}")

    def xoa_hdx(self):
        selected=self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Chọn hóa đơn cần xóa!")
            return
        ma=self.vars["MaHDX"].get()
        self.cursor.execute("DELETE FROM hoadonxuat WHERE MaHDX=%s",(ma,))
        self.conn.commit()
        self.load_data()
        messagebox.showinfo("Xóa","Đã xóa hóa đơn xuất!")

    def sua_hdx(self):
        selected=self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Chọn hóa đơn cần sửa!")
            return
        self.sua_mode=True

    def luu_hdx(self):
        if not self.sua_mode or not self.selected_ma:
            return
        sql="UPDATE hoadonxuat SET MaKH=%s, NgayLap=%s, MaNV=%s WHERE MaHDX=%s"
        data=(self.vars["MaKH"].get(), self.vars["NgayLap"].get(), self.vars["MaNV"].get(), self.selected_ma)
        self.cursor.execute(sql,data)
        self.conn.commit()
        self.load_data()
        messagebox.showinfo("Lưu","Đã cập nhật hóa đơn xuất!")
        self.sua_mode=False

    def boqua_hdx(self):
        for v in self.vars.values():
            v.set("")
        self.sua_mode=False
        self.selected_ma=None

if __name__=="__main__":
    app=HoaDonXuat()
    app.mainloop()
