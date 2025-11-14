import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

# ===== KẾT NỐI MYSQL =====
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="quanly_cuahangvatlieuxaydung"
    )

class HoaDonXuatFull(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hóa Đơn Xuất")
        self.geometry("1200x650")
        self.configure(bg="#fce4ec")

        # ===== Biến =====
        self.vars_ct = {
            "MaVL": tk.StringVar(),
            "SoLuong": tk.StringVar(),
            "SoLuongKho": tk.StringVar(),
            "DonVi": tk.StringVar(),
            "DonGia": tk.StringVar(),
            "ThanhTien": tk.StringVar()
        }

        # ===== Tiêu đề =====
        tk.Label(self, text="DANH MỤC HÓA ĐƠN XUẤT", font=("Times New Roman",20,"bold"),
                 bg="#fce4ec", fg="#ad1457").pack(pady=10)

        # ===== Khung chi tiết HĐ =====
        frame_ct = tk.LabelFrame(self, text="Chi tiết Hóa Đơn Xuất", font=("Times New Roman",12,"bold"),
                                 fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=8)
        frame_ct.pack(padx=15, pady=5, fill="x")

        tk.Label(frame_ct, text="Mã Vật liệu:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct, textvariable=self.vars_ct["MaVL"], width=20, font=("Times New Roman",11,"bold"), bg="#f8bbd0").grid(row=0,column=1,padx=5,pady=5)

        tk.Label(frame_ct, text="Số lượng tồn kho:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=0,column=2,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct, textvariable=self.vars_ct["SoLuongKho"], width=20, font=("Times New Roman",11,"bold"), state="readonly", bg="#e0e0e0").grid(row=0,column=3,padx=5,pady=5)

        tk.Label(frame_ct, text="Số lượng xuất:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=1,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct, textvariable=self.vars_ct["SoLuong"], width=20, font=("Times New Roman",11,"bold"), bg="#f8bbd0").grid(row=1,column=1,padx=5,pady=5)

        tk.Label(frame_ct, text="Đơn vị:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=1,column=2,padx=5,pady=5,sticky="w")
        ttk.Combobox(frame_ct, textvariable=self.vars_ct["DonVi"], values=["Kg","Cái","Mét","Chiếc","Bao","Viên","m3","Lít","Cây","Tấm"], state="readonly", width=18, font=("Times New Roman",11,"bold")).grid(row=1,column=3,padx=5,pady=5)

        tk.Label(frame_ct, text="Đơn giá:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=2,column=0,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct, textvariable=self.vars_ct["DonGia"], width=20, font=("Times New Roman",11,"bold"), bg="#f8bbd0").grid(row=2,column=1,padx=5,pady=5)

        tk.Label(frame_ct, text="Thành tiền:", bg="#ffffff", font=("Times New Roman",11,"bold")).grid(row=2,column=2,padx=5,pady=5,sticky="w")
        tk.Entry(frame_ct, textvariable=self.vars_ct["ThanhTien"], width=20, font=("Times New Roman",11,"bold"), bg="#f8bbd0", state="readonly").grid(row=2,column=3,padx=5,pady=5)

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
        frame_table = tk.LabelFrame(self, text="Danh sách chi tiết xuất", font=("Times New Roman",12,"bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge")
        frame_table.pack(padx=15,pady=5, fill="both", expand=True)

        columns = ("MaHDX","MaVL","SoLuongKho","SoLuong","DonVi","DonGia","ThanhTien")
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

    # ===== CRUD & các hàm =====
    def on_select(self,event):
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected,"values")
        self.vars_ct["MaVL"].set(vals[1])
        self.vars_ct["SoLuongKho"].set(vals[2])
        self.vars_ct["SoLuong"].set(vals[3])
        self.vars_ct["DonVi"].set(vals[4])
        self.vars_ct["DonGia"].set(vals[5])
        self.selected_id = vals[0]

    def them(self):
        mahdx = f"HDX{len(self.tree.get_children())+1:03d}"
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT SoLuong, DonVi, Gia FROM vatlieu WHERE MaVL=%s", (self.vars_ct["MaVL"].get(),))
            result = cursor.fetchone()
            if not result:
                messagebox.showwarning("Lỗi","Vật liệu không tồn tại!")
                return
            so_luong_kho, donvi, dongia = result
            self.vars_ct["SoLuongKho"].set(so_luong_kho)
            self.vars_ct["DonVi"].set(donvi)
            self.vars_ct["DonGia"].set(dongia)
            sl_xuat = int(self.vars_ct["SoLuong"].get())
            if sl_xuat > so_luong_kho:
                messagebox.showwarning("Lỗi","Số lượng xuất vượt quá kho!")
                return
            tag = 'evenrow' if len(self.tree.get_children()) % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(mahdx,
                                                self.vars_ct["MaVL"].get(),
                                                so_luong_kho,
                                                sl_xuat,
                                                donvi,
                                                dongia,
                                                round(sl_xuat*dongia,2)),
                             tags=(tag,))
            cursor.close()
            conn.close()
            self.boqua()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

    def xoa(self):
        if not self.selected_id:
            messagebox.showwarning("Chú ý","Chọn một dòng để xóa!")
            return
        for item in self.tree.get_children():
            if self.tree.item(item,"values")[0] == self.selected_id:
                self.tree.delete(item)
                break
        self.boqua()

    def sua(self):
        if not self.selected_id:
            messagebox.showwarning("Chú ý","Chọn một dòng để sửa!")
            return
        for item in self.tree.get_children():
            if self.tree.item(item,"values")[0] == self.selected_id:
                sl_xuat = int(self.vars_ct["SoLuong"].get())
                sl_kho = int(self.vars_ct["SoLuongKho"].get())
                if sl_xuat > sl_kho:
                    messagebox.showwarning("Lỗi","Số lượng xuất vượt kho!")
                    return
                self.tree.item(item, values=(self.selected_id,
                                             self.vars_ct["MaVL"].get(),
                                             sl_kho,
                                             sl_xuat,
                                             self.vars_ct["DonVi"].get(),
                                             self.vars_ct["DonGia"].get(),
                                             round(sl_xuat*float(self.vars_ct["DonGia"].get()),2)))
                break
        self.boqua()

    def boqua(self):
        for v in self.vars_ct.values():
            v.set("")
        self.selected_id = None

    def luu(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            for item in self.tree.get_children():
                vals = self.tree.item(item,"values")
                # Lưu vào chitiethoadonxuat
                cursor.execute(
                    "INSERT INTO chitiethoadonxuat (MaHDX, MaVL, SoLuong, SoLuongKho, DonVi, DonGia, ThanhTien) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                    vals
                )
                # Cập nhật tồn kho
                cursor.execute("UPDATE vatlieu SET SoLuong = SoLuong - %s WHERE MaVL=%s", (vals[3], vals[1]))
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Thành công","Đã lưu hóa đơn xuất và cập nhật kho!")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", str(err))

if __name__=="__main__":
    app = HoaDonXuatFull()
    app.mainloop()
