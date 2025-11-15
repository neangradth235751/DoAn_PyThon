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

# ===== HÓA ĐƠN XUẤT =====
class HoaDonXuat(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Thông tin Hóa Đơn Xuất")
        self.geometry("900x600")
        self.configure(bg="#fce4ec")

        # Biến
        self.vars = {
            "MaHDX": tk.StringVar(),
            "MaKH": tk.StringVar(),
            "NgayLap": tk.StringVar(),
            "MaNV": tk.StringVar()
        }

        # Load dữ liệu khách hàng & nhân viên
        self.kh_dict = self.load_khachhang()
        self.nv_dict = self.load_nv()

        # ===== Tiêu đề =====
        tk.Label(self, text="THÔNG TIN HÓA ĐƠN XUẤT",
                 font=("Times New Roman",20,"bold"),
                 fg="#ad1457", bg="#fce4ec").pack(pady=10)

        # ===== Khung nhập liệu =====
        frame_input = tk.LabelFrame(self, text="Thông tin hóa đơn xuất",
                                    font=("Times New Roman",12,"bold"),
                                    fg="#ad1457", bg="#ffffff",
                                    padx=10, pady=8)
        frame_input.pack(padx=15,pady=5, fill="x")

        tk.Label(frame_input, text="Mã hóa đơn xuất:", bg="#ffffff",
                 font=("Times New Roman",11,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_input, textvariable=self.vars["MaHDX"], bg="#f8bbd0", width=25).grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame_input, text="Khách hàng:", bg="#ffffff",
                 font=("Times New Roman",11,"bold")).grid(row=0,column=2,padx=5,pady=5,sticky="w")
        tk.Entry(frame_input, textvariable=self.vars["MaKH"], bg="#f8bbd0", width=25).grid(row=0,column=3,padx=5,pady=5)

        tk.Label(frame_input, text="Ngày lập:", bg="#ffffff",
                 font=("Times New Roman",11,"bold")).grid(row=1,column=0,padx=5,pady=5,sticky="w")
        DateEntry(frame_input, textvariable=self.vars["NgayLap"], date_pattern="yyyy-mm-dd",
                  width=23, background="#f48fb1", foreground="white").grid(row=1,column=1,padx=5,pady=5)

        tk.Label(frame_input, text="Nhân viên:", bg="#ffffff",
                 font=("Times New Roman",11,"bold")).grid(row=1,column=2,padx=5,pady=5,sticky="w")
        tk.Entry(frame_input, textvariable=self.vars["MaNV"], bg="#f8bbd0", width=25).grid(row=1,column=3,padx=5,pady=5)

        # ===== TREEVIEW =====
        frame_table = tk.LabelFrame(self, text="Danh sách hóa đơn xuất",
                                    font=("Times New Roman",12,"bold"),
                                    fg="#ad1457", bg="#ffffff")
        frame_table.pack(padx=15, pady=5, fill="both", expand=True)

        columns = ("Mã Hóa Đơn Xuất","Khách Hàng","Ngày Lập","Nhân Viên")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Times New Roman",11))
        style.configure("Treeview.Heading", font=("Times New Roman",12,"bold"))

        self.tree.tag_configure("evenrow", background="#f9f9f9")
        self.tree.tag_configure("oddrow", background="#ffffff")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180, anchor="center", stretch=False)

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ===== NÚT =====
        frame_btn = tk.Frame(self, bg="#fce4ec")
        frame_btn.pack(pady=5)
        btn_style = {"font":("Times New Roman",11,"bold"),"fg":"white","width":12,"relief":"flat"}

        tk.Button(frame_btn,text="Thêm", bg="#f48fb1", command=self.them, **btn_style).grid(row=0,column=0,padx=3)
        tk.Button(frame_btn,text="Xóa", bg="#e57373", command=self.xoa, **btn_style).grid(row=0,column=1,padx=3)
        tk.Button(frame_btn,text="Sửa", bg="#ffb74d", command=self.sua, **btn_style).grid(row=0,column=2,padx=3)
        tk.Button(frame_btn,text="Lưu", bg="#81c784", command=self.luu, **btn_style).grid(row=0,column=3,padx=3)
        tk.Button(frame_btn,text="Bỏ qua", bg="#90a4ae", command=self.boqua, **btn_style).grid(row=0,column=4,padx=3)
        tk.Button(frame_btn,text="Chi tiết", bg="#4fc3f7", command=self.mo_chitiet, **btn_style).grid(row=0,column=5,padx=3)
        tk.Button(frame_btn,text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0,column=6,padx=3)

        self.selected_ma=None
        self.load_data()

    # ===== LOAD KH & NV =====
    def load_khachhang(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaKH, TenKH FROM khachhang")
            data = {row[0]: row[1] for row in cursor.fetchall()}
            conn.close()
            return data
        except:
            return {}

    def load_nv(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaNV, TenNV FROM nhanvien")
            data = {row[0]: row[1] for row in cursor.fetchall()}
            conn.close()
            return data
        except:
            return {}

    # ===== LOAD DATA =====
    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MaHDX, MaKH, NgayLap, MaNV FROM hoadonxuat")
        rows = cursor.fetchall()
        for i,r in enumerate(rows):
            tag = "evenrow" if i%2==0 else "oddrow"
            ten_kh = self.kh_dict.get(r[1], r[1])
            ten_nv = self.nv_dict.get(r[3], r[3])
            self.tree.insert("", "end", values=(r[0], ten_kh, r[2], ten_nv), tags=(tag,))
        conn.close()
        self.boqua()

    # ===== SELECTION =====
    def on_select(self,event):
        sel = self.tree.selection()
        if not sel: return
        vals = self.tree.item(sel,"values")
        ma_kh = next((k for k,v in self.kh_dict.items() if v==vals[1]), vals[1])
        ma_nv = next((k for k,v in self.nv_dict.items() if v==vals[3]), vals[3])
        self.vars["MaHDX"].set(vals[0])
        self.vars["MaKH"].set(ma_kh)
        self.vars["NgayLap"].set(vals[2])
        self.vars["MaNV"].set(ma_nv)
        self.selected_ma = vals[0]

    # ===== CRUD =====
    def them(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO hoadonxuat(MaHDX,MaKH,NgayLap,MaNV) VALUES(%s,%s,%s,%s)",
                           (self.vars["MaHDX"].get(),
                            self.vars["MaKH"].get(),
                            self.vars["NgayLap"].get(),
                            self.vars["MaNV"].get()))
            conn.commit()
            messagebox.showinfo("Thành công","Đã thêm hóa đơn!")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", str(err))
        finally:
            conn.close()
        self.load_data()

    def xoa(self):
        if not self.selected_ma:
            messagebox.showwarning("Chưa chọn","Chọn hóa đơn để xóa!")
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM hoadonxuat WHERE MaHDX=%s",(self.selected_ma,))
        conn.commit()
        conn.close()
        self.load_data()
        messagebox.showinfo("Xóa","Đã xóa hóa đơn!")

    def sua(self):
        if not self.selected_ma:
            messagebox.showwarning("Chưa chọn","Chọn hóa đơn để sửa!")
            return

    def luu(self):
        if not self.selected_ma:
            return
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE hoadonxuat SET MaKH=%s, NgayLap=%s, MaNV=%s WHERE MaHDX=%s",
                       (self.vars["MaKH"].get(), self.vars["NgayLap"].get(), self.vars["MaNV"].get(), self.selected_ma))
        conn.commit()
        conn.close()
        self.load_data()
        messagebox.showinfo("Lưu","Đã cập nhật hóa đơn xuất!")

    def boqua(self):
        for v in self.vars.values():
            v.set("")
        self.selected_ma=None

    # ===== CHI TIẾT =====
    def mo_chitiet(self):
        if not self.selected_ma:
            messagebox.showwarning("Chưa chọn","Chọn hóa đơn để xem chi tiết!")
            return
        ChiTietHDX(self, self.selected_ma)

# ===== CHI TIẾT HÓA ĐƠN XUẤT =====
class ChiTietHDX(tk.Toplevel):
    def __init__(self,parent, mahdx):
        super().__init__(parent)
        self.title(f"Chi tiết Hóa đơn {mahdx}")
        self.geometry("900x500")
        self.configure(bg="#fce4ec")
        self.mahdx = mahdx

        tk.Label(self, text=f"CHI TIẾT HÓA ĐƠN XUẤT {mahdx}",
                 font=("Times New Roman",16,"bold"),
                 fg="#ad1457", bg="#fce4ec").pack(pady=10)

        columns = ("STT","Vật liệu","SL","Đơn vị","Đơn giá","Thành tiền")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=12)
        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Times New Roman",11))
        style.configure("Treeview.Heading", font=("Times New Roman",12,"bold"))
        self.tree.tag_configure("evenrow", background="#f9f9f9")
        self.tree.tag_configure("oddrow", background="#ffffff")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        # Nút
        frame_btn = tk.Frame(self, bg="#fce4ec")
        frame_btn.pack(pady=5)

        btn_style = {"font":("Times New Roman",11,"bold"), "fg":"white", "width":12, "relief":"flat"}

        tk.Button(frame_btn, text="Xem hóa đơn", bg="#4fc3f7", command=self.xem_hoa_don, **btn_style).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0, column=1, padx=5)

        self.load_data()

    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.TenVL, c.SoLuong, c.DonVi, c.DonGia, c.ThanhTien
            FROM chitiethoadonxuat c
            JOIN vatlieu v ON c.MaVL=v.MaVL
            WHERE c.MaHDX=%s
        """,(self.mahdx,))
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for i,row in enumerate(rows,1):
            tag="evenrow" if i%2==0 else "oddrow"
            self.tree.insert("", "end", values=(i,row[0],row[1],row[2],row[3],row[4]), tags=(tag,))
        conn.close()

    def xem_hoa_don(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.TenVL, c.SoLuong, c.DonVi, c.DonGia, c.ThanhTien
            FROM chitiethoadonxuat c
            JOIN vatlieu v ON c.MaVL=v.MaVL
            WHERE c.MaHDX=%s
        """,(self.mahdx,))
        rows = cursor.fetchall()
        conn.close()

        popup = tk.Toplevel(self)
        popup.title(f"Hóa đơn {self.mahdx}")
        popup.geometry("600x400")
        text = tk.Text(popup, font=("Times New Roman",12))
        text.pack(fill="both", expand=True)
        text.insert("end", f"HÓA ĐƠN XUẤT {self.mahdx}\n")
        text.insert("end", "-"*70 + "\n")
        text.insert("end", f"{'STT':<5}{'Vật liệu':<20}{'SL':<10}{'Đơn vị':<10}{'Đơn giá':<10}{'Thành tiền':<10}\n")
        text.insert("end", "-"*70 + "\n")
        total = 0
        for i,row in enumerate(rows,1):
            text.insert("end", f"{i:<5}{row[0]:<20}{row[1]:<10}{row[2]:<10}{row[3]:<10}{row[4]:<10}\n")
            total += float(row[4])
        text.insert("end", "-"*70 + "\n")
        text.insert("end", f"{'Tổng tiền:':<55}{total:<10}\n")
        text.configure(state="disabled")

if __name__=="__main__":
    root = tk.Tk()
    root.withdraw() 
    app = HoaDonXuat(root)
    app.mainloop()
