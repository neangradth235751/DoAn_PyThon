import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import mysql.connector

class NhanVien(tk.Toplevel):   # Tạo cửa sổ con
    def __init__(self, parent):
        super().__init__(parent)  # parent là root Tk
        self.title("Thông tin nhân Viên")
        self.geometry("1050x630")
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
        tk.Label(self, text="THÔNG TIN NHÂN VIÊN", font=("Times New Roman", 22, "bold"),
                 fg="#ad1457", bg="#fce4ec").pack(pady=10)

        # === Khung nhập liệu ===
        frame_input = tk.LabelFrame(self, text="Thông tin nhân viên", font=("Times New Roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=8)
        frame_input.pack(padx=15, pady=5, fill="x")

        # Variables
        self.vars = {
            "MaNV": tk.StringVar(),
            "TenNV": tk.StringVar(),
            "GioiTinh": tk.StringVar(),
            "DiaChi": tk.StringVar(),
            "DienThoai": tk.StringVar(),
            "NgaySinh": tk.StringVar(),
            "ChucVu": tk.StringVar(),
            "Luong": tk.StringVar()
        }

        # ComboBox lists
        list_diachi = ["Hà Nội","Đà Nẵng","Hồ Chí Minh","Cần Thơ","Hải Phòng","Huế",
                       "Bình Dương","Quảng Ninh","Nam Định","Nha Trang"]
        list_chucvu = ["Quản lý","Thu ngân","Bán hàng","Kế toán","Kho hàng","Nhân sự"]

        # Labels & keys
        labels = [
            ("Mã NV:", "MaNV"),
            ("Tên NV:", "TenNV"),
            ("Giới tính:", "GioiTinh"),
            ("Địa chỉ:", "DiaChi"),
            ("Điện thoại:", "DienThoai"),
            ("Ngày sinh:", "NgaySinh"),
            ("Chức vụ:", "ChucVu"),
            ("Lương:", "Luong")
        ]

        for i, (label, key) in enumerate(labels):
            tk.Label(frame_input, text=label, bg="#ffffff", font=("Times New Roman", 11, "bold")).grid(
                row=i//4, column=(i%4)*2, sticky="w", padx=8, pady=4
            )

            if key == "GioiTinh":
                # RadioButton cho Giới tính
                frame_radio = tk.Frame(frame_input, bg="#ffffff")
                frame_radio.grid(row=i//4, column=(i%4)*2+1, padx=8, pady=4, sticky="w")
                tk.Radiobutton(frame_radio, text="Nam", variable=self.vars[key], value="Nam", bg="#ffffff",
                               font=("Times New Roman",11)).pack(side="left", padx=5)
                tk.Radiobutton(frame_radio, text="Nữ", variable=self.vars[key], value="Nữ", bg="#ffffff",
                               font=("Times New Roman",11)).pack(side="left", padx=5)
                self.vars[key].set("")  # mặc định chưa chọn

            elif key == "DiaChi":
                cb = ttk.Combobox(frame_input, textvariable=self.vars[key],
                                  values=list_diachi, width=18, state="readonly",
                                  font=("Times New Roman", 11))
                cb.grid(row=i//4, column=(i%4)*2+1, padx=8, pady=4)
                self.vars[key].set("")

            elif key == "ChucVu":
                cb = ttk.Combobox(frame_input, textvariable=self.vars[key],
                                  values=list_chucvu, width=18, state="readonly",
                                  font=("Times New Roman", 11))
                cb.grid(row=i//4, column=(i%4)*2+1, padx=8, pady=4)
                self.vars[key].set("")

            elif key == "NgaySinh":
                de = DateEntry(frame_input, textvariable=self.vars[key],
                               date_pattern='dd/mm/yyyy', width=18,
                               background="#f48fb1", foreground="white",
                               borderwidth=2, font=("Times New Roman", 11))
                de.grid(row=i//4, column=(i%4)*2+1, padx=5, pady=5)
                self.vars[key].set("")

            else:
                tk.Entry(frame_input, textvariable=self.vars[key],
                         width=22, font=("Times New Roman", 11), bg="#f8bbd0").grid(
                    row=i//4, column=(i%4)*2+1, padx=5, pady=5)

        # === Treeview ===
        columns = ("MaNV", "TenNV", "GioiTinh", "DiaChi", "DienThoai", "NgaySinh", "ChucVu", "Luong")
        col_texts = ["Mã NV","Tên NV","Giới tính","Địa chỉ","Điện thoại","Ngày sinh","Chức vụ","Lương"]

        frame_table = tk.LabelFrame(self, text="Danh sách nhân viên", font=("Times New Roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=8, pady=8)
        frame_table.pack(padx=15, pady=5, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=25, font=("Times New Roman", 11))
        style.configure("Treeview.Heading", font=("Times New Roman", 12, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col_texts[i])
            self.tree.column(col, width=120, anchor="center", stretch=False)

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
        btn_style = {"font":("Times New Roman",11,"bold"),"fg":"white","width":11,"relief":"flat"}

        tk.Button(frame_btn, text="Thêm", bg="#f48fb1", command=self.them_nv, **btn_style).grid(row=0,column=0,padx=3)
        tk.Button(frame_btn, text="Xóa", bg="#e57373", command=self.xoa_nv, **btn_style).grid(row=0,column=1,padx=3)
        tk.Button(frame_btn, text="Sửa", bg="#ffb74d", command=self.sua_nv, **btn_style).grid(row=0,column=2,padx=3)
        tk.Button(frame_btn, text="Lưu", bg="#81c784", command=self.luu_nv, **btn_style).grid(row=0,column=3,padx=3)
        tk.Button(frame_btn, text="Bỏ qua", bg="#90a4ae", command=self.boqua_nv, **btn_style).grid(row=0,column=4,padx=3)
        tk.Button(frame_btn, text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0,column=5,padx=3)

        self.sua_mode = False
        self.selected_ma = None
        self.load_data()

    # === CRUD ===
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM nhanvien")
        rows = self.cursor.fetchall()
        for index, r in enumerate(rows):
            tag = 'evenrow' if index % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=r, tags=(tag,))

    def on_select(self,event):
        selected = self.tree.selection()
        if selected:
            vals = self.tree.item(selected, "values")
            for i,key in enumerate(self.vars.keys()):
                self.vars[key].set(vals[i])
            self.selected_ma = vals[0]

    def them_nv(self):
        try:
            sql = "INSERT INTO nhanvien VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            data = tuple(v.get() for v in self.vars.values())
            self.cursor.execute(sql, data)
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Thành công","Đã thêm nhân viên mới!")
            self.boqua_nv()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi",f"Lỗi thêm dữ liệu:\n{err}")

    def xoa_nv(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Chọn nhân viên cần xóa!")
            return
        ma = self.tree.item(selected,"values")[0]
        self.cursor.execute("DELETE FROM nhanvien WHERE MaNV=%s",(ma,))
        self.conn.commit()
        self.load_data()
        messagebox.showinfo("Xóa","Đã xóa nhân viên!")

    def sua_nv(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn","Chọn nhân viên cần sửa!")
            return
        self.sua_mode=True
        vals = self.tree.item(selected,"values")
        for i,key in enumerate(self.vars.keys()):
            self.vars[key].set(vals[i])
        self.selected_ma = vals[0]

    def luu_nv(self):
        if not self.sua_mode or not self.selected_ma:
            return
        sql="""UPDATE nhanvien SET TenNV=%s, GioiTinh=%s, DiaChi=%s,
               DienThoai=%s, NgaySinh=%s, ChucVu=%s, Luong=%s WHERE MaNV=%s"""
        data=(self.vars["TenNV"].get(),self.vars["GioiTinh"].get(),self.vars["DiaChi"].get(),
              self.vars["DienThoai"].get(),self.vars["NgaySinh"].get(),self.vars["ChucVu"].get(),
              self.vars["Luong"].get(),self.selected_ma)
        self.cursor.execute(sql,data)
        self.conn.commit()
        self.load_data()
        messagebox.showinfo("Lưu","Đã cập nhật thông tin nhân viên!")
        self.boqua_nv()
        self.sua_mode=False

    def boqua_nv(self):
        for v in self.vars.values():
            v.set("")
        self.sua_mode=False
        self.selected_ma=None

if __name__=="__main__":
    root = tk.Tk()
    app = NhanVien(root)
    root.mainloop()