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
        self.title("Quản Lý Hóa Đơn Nhập")
        self.geometry("1100x650")
        self.configure(bg="#fce4ec")

        # ===== Biến =====
        self.vars_ct = {
            "VatLieu": tk.StringVar(),
            "SoLuong": tk.StringVar(),
            "DonVi": tk.StringVar(),
            "DonGia": tk.StringVar(),
            "ThanhTien": tk.StringVar()
        }

        # ===== Tiêu đề =====
        lbl_title = tk.Label(self, text="CHI TIẾT HÓA ĐƠN NHẬP", 
                             font=("Times New Roman",20,"bold"),
                             bg="#fce4ec", fg="#ad1457")
        lbl_title.pack(pady=10)

        # ===== Khung chi tiết HĐ =====
        frame_ct = tk.LabelFrame(self, text="Chi tiết Hóa Đơn", font=("Times New Roman",12,"bold"),
                                 fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=8)
        frame_ct.pack(padx=15, pady=5, fill="x")
        
        tk.Label(frame_ct,text="Hóa đơn nhập:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct,textvariable=self.vars_ct["VatLieu"], width=20,font=("Times New Roman",11,"bold"),bg="#f8bbd0").grid(row=0,column=1,padx=5,pady=5)
        
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

        columns = ("Hóa đơn nhập","Vật liệu","Số lượng","Đơn vị","Đơn giá","Thành tiền")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Times New Roman",11,"bold"))
        style.configure("Treeview", rowheight=25)
        style.map("Treeview", background=[('selected', '#f48fb1')])

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.tag_configure('oddrow', background="#fce4ec")
        self.tree.tag_configure('evenrow', background="#ffffff")

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
        tk.Button(frame_btn,text="Lưu", bg="#81c784", command=self.luu, **btn_style).grid(row=0,column=4,padx=5)
        tk.Button(frame_btn,text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0,column=5,padx=5)

        self.selected_id = None
        self.load_data()

    # ===== Load dữ liệu từ MySQL =====
    def load_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaHDN, MaVL, SoLuong, DonVi, DonGia, ThanhTien FROM chitiethoadonnhap")
            rows = cursor.fetchall()
            self.tree.delete(*self.tree.get_children())
            for idx, row in enumerate(rows):
                tag = 'evenrow' if idx%2==0 else 'oddrow'
                self.tree.insert("", "end", values=row, tags=(tag,))
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

    # ===== CRUD =====
    def on_select(self,event):
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected,"values")
        self.vars_ct["VatLieu"].set(vals[1])
        self.vars_ct["SoLuong"].set(vals[2])
        self.vars_ct["DonVi"].set(vals[3])
        self.vars_ct["DonGia"].set(vals[4])
        self.selected_id = vals[0]

    def them(self):
        self.save_to_tree()

    def xoa(self):
        if not self.selected_id:
            messagebox.showwarning("Chú ý", "Chọn một dòng để xóa!")
            return
        for item in self.tree.get_children():
            if self.tree.item(item,"values")[0] == self.selected_id:
                self.tree.delete(item)
                break
        self.boqua()

    def sua(self):
        if not self.selected_id:
            messagebox.showwarning("Chú ý", "Chọn một dòng để sửa!")
            return
        for item in self.tree.get_children():
            if self.tree.item(item,"values")[0] == self.selected_id:
                self.tree.item(item, values=(self.selected_id,
                                             self.vars_ct["VatLieu"].get(),
                                             self.vars_ct["SoLuong"].get(),
                                             self.vars_ct["DonVi"].get(),
                                             self.vars_ct["DonGia"].get(),
                                             self.vars_ct["ThanhTien"].get()))
                break
        self.boqua()

    def boqua(self):
        for v in self.vars_ct.values():
            v.set("")
        self.selected_id = None

    def save_to_tree(self):
        # Tạo MaHDN tự động
        mahd = f"HD{len(self.tree.get_children())+1:03d}"
        self.tree.insert("", "end", values=(mahd,
                                            self.vars_ct["VatLieu"].get(),
                                            self.vars_ct["SoLuong"].get(),
                                            self.vars_ct["DonVi"].get(),
                                            self.vars_ct["DonGia"].get(),
                                            self.vars_ct["ThanhTien"].get()))
        self.boqua()

    # ===== Lưu tất cả Treeview vào MySQL =====
    def luu(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            for item in self.tree.get_children():
                vals = self.tree.item(item,"values")
                cursor.execute(
                    "INSERT INTO chitiethoadonnhap (MaHDN, MaVL, SoLuong, DonVi, DonGia, ThanhTien) VALUES (%s,%s,%s,%s,%s,%s)",
                    vals
                )
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Thành công","Đã lưu dữ liệu vào MySQL!")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

if __name__=="__main__":
    app = HoaDonNhapFull()
    app.mainloop()
