import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ======== KẾT NỐI MYSQL ========
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="quanly_cuahangvatlieuxaydung"
    )

class HoaDonNhapFull(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hóa Đơn Nhập")
        self.geometry("1100x600")
        self.configure(bg="#fce4ec")

        # ===== Biến =====
        self.vars_hd = {
            "MaHDN": tk.StringVar(),
            "NgayLap": tk.StringVar(),
            "NhanVien": tk.StringVar()
        }
        self.vars_ct = {
            "VatLieu": tk.StringVar(),
            "SoLuong": tk.StringVar(),
            "DonVi": tk.StringVar(),
            "DonGia": tk.StringVar(),
            "ThanhTien": tk.StringVar()
        }

        # ===== Khung Hóa đơn =====
        frame_hd = tk.LabelFrame(self, text="Thông tin Hóa Đơn", font=("Times New Roman",12,"bold"),
                                 fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=8)
        frame_hd.pack(padx=15, pady=5, fill="x")

        tk.Label(frame_hd,text="Hóa đơn:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_hd,textvariable=self.vars_hd["MaHDN"], width=20,font=("Times New Roman",11,"bold"),bg="#f8bbd0").grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame_hd,text="Ngày lập:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=2,padx=5,pady=5,sticky="w")
        DateEntry(frame_hd,textvariable=self.vars_hd["NgayLap"],date_pattern='yyyy-mm-dd',width=20).grid(row=0,column=3,padx=5,pady=5)

        tk.Label(frame_hd,text="Nhân viên:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=4,padx=5,pady=5,sticky="w")
        tk.Entry(frame_hd,textvariable=self.vars_hd["NhanVien"], width=20,font=("Times New Roman",11,"bold"),bg="#f8bbd0").grid(row=0,column=5,padx=5,pady=5)

        # ===== Khung chi tiết HĐ =====
        frame_ct = tk.LabelFrame(self, text="Chi tiết Hóa Đơn", font=("Times New Roman",12,"bold"),
                                 fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=8)
        frame_ct.pack(padx=15, pady=5, fill="x")

        tk.Label(frame_ct,text="Vật liệu:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct,textvariable=self.vars_ct["VatLieu"], width=20,font=("Times New Roman",11,"bold"),bg="#f8bbd0").grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame_ct,text="Số lượng:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=2,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct,textvariable=self.vars_ct["SoLuong"], width=20,font=("Times New Roman",11,"bold"),bg="#f8bbd0").grid(row=0,column=3,padx=5,pady=5)

        tk.Label(frame_ct,text="Đơn vị:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=1,column=0,padx=5,pady=5,sticky="w")
        ttk.Combobox(frame_ct,textvariable=self.vars_ct["DonVi"], values=["Kg","Cái","Mét","Chiếc","Bao","Viên","m3","Lít","Cây","Tấm"],
                     state="readonly", width=18, font=("Times New Roman",11,"bold")).grid(row=1,column=1,padx=5,pady=5)

        tk.Label(frame_ct,text="Đơn giá:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=1,column=2,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct,textvariable=self.vars_ct["DonGia"], width=20,font=("Times New Roman",11,"bold"),bg="#f8bbd0").grid(row=1,column=3,padx=5,pady=5)

        tk.Label(frame_ct,text="Thành tiền:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=2,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct,textvariable=self.vars_ct["ThanhTien"], width=20,font=("Times New Roman",11,"bold"),bg="#f8bbd0",state="readonly").grid(row=2,column=1,padx=5,pady=5)

        # ===== Tự tính Thành tiền =====
        def update_tt(*args):
            try:
                sl = float(self.vars_ct["SoLuong"].get())
                dg = float(self.vars_ct["DonGia"].get())
                self.vars_ct["ThanhTien"].set(round(sl*dg,2))
            except:
                self.vars_ct["ThanhTien"].set("")
        self.vars_ct["SoLuong"].trace("w", update_tt)
        self.vars_ct["DonGia"].trace("w", update_tt)

        # ===== Treeview =====
        frame_table = tk.LabelFrame(self, text="Danh sách chi tiết HĐ", font=("Times New Roman",12,"bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge")
        frame_table.pack(padx=15,pady=5, fill="both", expand=True)

        columns = ("MaHDN","MaVL","SoLuong","DonVi","DonGia","ThanhTien")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ===== Nút chức năng =====
        frame_btn = tk.Frame(self, bg="#fce4ec")
        frame_btn.pack(pady=5)
        btn_style = {"font":("Times New Roman",11,"bold"),"fg":"white","width":10,"relief":"flat"}
        tk.Button(frame_btn,text="Thêm", bg="#f48fb1", command=self.them, **btn_style).grid(row=0,column=0,padx=5)
        tk.Button(frame_btn,text="Xóa", bg="#e57373", command=self.xoa, **btn_style).grid(row=0,column=1,padx=5)
        tk.Button(frame_btn,text="Sửa", bg="#ffb74d", command=self.sua, **btn_style).grid(row=0,column=2,padx=5)
        tk.Button(frame_btn,text="Bỏ qua", bg="#90a4ae", command=self.boqua, **btn_style).grid(row=0,column=3,padx=5)
        tk.Button(frame_btn,text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0,column=4,padx=5)

        self.selected_id = None

        # ===== Load dữ liệu từ MySQL =====
        self.load_data()

    # ===== Load dữ liệu từ MySQL =====
    def load_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaHDN, MaVL, SoLuong, DonVi, DonGia, ThanhTien FROM chitiethoadonnhap")
            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for row in rows:
                self.tree.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

    # ===== CRUD =====
    def on_select(self,event):
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected,"values")
        self.vars_hd["MaHDN"].set(vals[0])
        self.vars_ct["VatLieu"].set(vals[1])
        self.vars_ct["SoLuong"].set(vals[2])
        self.vars_ct["DonVi"].set(vals[3])
        self.vars_ct["DonGia"].set(vals[4])
        self.selected_id = vals[0]

    def them(self):
        mahd = self.vars_hd["MaHDN"].get()
        mavl = self.vars_ct["VatLieu"].get()
        sl = self.vars_ct["SoLuong"].get()
        dv = self.vars_ct["DonVi"].get()
        dg = self.vars_ct["DonGia"].get()
        tt = self.vars_ct["ThanhTien"].get()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO chitiethoadonnhap (MaHDN, MaVL, SoLuong, DonVi, DonGia, ThanhTien) VALUES (%s,%s,%s,%s,%s,%s)",
                (mahd, mavl, sl, dv, dg, tt)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.load_data()
            self.boqua()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

    def xoa(self):
        if not self.selected_id:
            messagebox.showwarning("Chú ý", "Chọn một dòng để xóa!")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM chitiethoadonnhap WHERE MaHDN=%s", (self.selected_id,))
            conn.commit()
            cursor.close()
            conn.close()
            self.load_data()
            self.boqua()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

    def sua(self):
        if not self.selected_id:
            messagebox.showwarning("Chú ý", "Chọn một dòng để sửa!")
            return
        mahd = self.vars_hd["MaHDN"].get()
        mavl = self.vars_ct["VatLieu"].get()
        sl = self.vars_ct["SoLuong"].get()
        dv = self.vars_ct["DonVi"].get()
        dg = self.vars_ct["DonGia"].get()
        tt = self.vars_ct["ThanhTien"].get()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE chitiethoadonnhap SET MaVL=%s, SoLuong=%s, DonVi=%s, DonGia=%s, ThanhTien=%s WHERE MaHDN=%s",
                (mavl, sl, dv, dg, tt, self.selected_id)
            )
            conn.commit()
            cursor.close()
            conn.close()
            self.load_data()
            self.boqua()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

    def boqua(self):
        for v in self.vars_hd.values():
            v.set("")
        for v in self.vars_ct.values():
            v.set("")
        self.selected_id = None

if __name__=="__main__":
    app = HoaDonNhapFull()
    app.mainloop()
