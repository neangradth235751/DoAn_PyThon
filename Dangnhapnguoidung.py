import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class NhanVien(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản Lý Nhân Viên")
        self.geometry("1350x620")
        self.configure(bg="#fce4ec")  # pastel hồng đồng bộ đăng nhập

        # === Kết nối MySQL ===
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="123456789",  # đổi nếu cần
                database="quanly_cuahangvatlieuxaydung"
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Không thể kết nối MySQL:\n{err}")
            self.destroy()
            return

        # === TIÊU ĐỀ ===
        lbl_title = tk.Label(self, text="QUẢN LÝ NHÂN VIÊN",
                             font=("Helvetica", 22, "bold"),
                             fg="#ad1457", bg="#fce4ec")
        lbl_title.pack(pady=15)

        # === KHUNG NHẬP LIỆU ===
        frame_input = tk.LabelFrame(self, text="Thông tin nhân viên",
                                    font=("Arial", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff",
                                    bd=3, relief="ridge", padx=15, pady=10)
        frame_input.pack(padx=30, pady=10, fill="x")

        self.vars = {
            "MaNV": tk.StringVar(),
            "TenNV": tk.StringVar(),
            "GioiTinh": tk.StringVar(value="Nam"),
            "DiaChi": tk.StringVar(),
            "DienThoai": tk.StringVar(),
            "NgaySinh": tk.StringVar(),
            "ChucVu": tk.StringVar(),
            "Luong": tk.StringVar()
        }

        labels = [
            ("Mã nhân viên:", "MaNV"),
            ("Tên nhân viên:", "TenNV"),
            ("Giới tính:", "GioiTinh"),
            ("Địa chỉ:", "DiaChi"),
            ("Điện thoại:", "DienThoai"),
            ("Ngày sinh:", "NgaySinh"),
            ("Chức vụ:", "ChucVu"),
            ("Lương:", "Luong")
        ]

        for i, (label, key) in enumerate(labels):
            tk.Label(frame_input, text=label, bg="#ffffff",
                     font=("Arial", 11)).grid(row=i//4, column=(i%4)*2,
                                              sticky="w", padx=10, pady=5)
            if key == "GioiTinh":
                cb = ttk.Combobox(frame_input, textvariable=self.vars[key],
                                  values=["Nam", "Nữ"], width=22, state="readonly")
                cb.grid(row=i//4, column=(i%4)*2 + 1, padx=10, pady=5)
            else:
                tk.Entry(frame_input, textvariable=self.vars[key],
                         width=25, font=("Arial", 11), bg="#f8bbd0").grid(
                    row=i//4, column=(i%4)*2 + 1, padx=10, pady=5
                )

        # === BẢNG DỮ LIỆU ===
        frame_table = tk.LabelFrame(self, text="Danh sách nhân viên",
                                    font=("Arial", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff",
                                    bd=3, relief="ridge", padx=10, pady=10)
        frame_table.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("MaNV", "TenNV", "GioiTinh", "DiaChi", "DienThoai",
                   "NgaySinh", "ChucVu", "Luong")
        col_texts = ["Mã NV", "Tên NV", "Giới tính", "Địa chỉ", "Điện thoại",
                     "Ngày sinh", "Chức vụ", "Lương"]

        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        for i, col in enumerate(columns):
            self.tree.heading(col, text=col_texts[i])
            self.tree.column(col, width=140, anchor="center")

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")
        self.tree.pack(padx=5, pady=5, fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # === NÚT CHỨC NĂNG ===
        frame_btn = tk.LabelFrame(self, text="Chức năng",
                                  font=("Arial", 12, "bold"),
                                  fg="#ad1457", bg="#fce4ec",
                                  bd=3, relief="ridge", padx=10, pady=10)
        frame_btn.pack(pady=10)

        btn_style = {
            "font": ("Arial", 11, "bold"),
            "fg": "white",
            "width": 12,
            "relief": "flat"
        }

        tk.Button(frame_btn, text="Thêm", bg="#f48fb1",
                  command=self.them_nv, **btn_style).grid(row=0, column=0, padx=5)
        tk.Button(frame_btn, text="Xóa", bg="#e57373",
                  command=self.xoa_nv, **btn_style).grid(row=0, column=1, padx=5)
        tk.Button(frame_btn, text="Sửa", bg="#ffb74d",
                  command=self.sua_nv, **btn_style).grid(row=0, column=2, padx=5)
        tk.Button(frame_btn, text="Lưu", bg="#81c784",
                  command=self.luu_nv, **btn_style).grid(row=0, column=3, padx=5)
        tk.Button(frame_btn, text="Bỏ qua", bg="#90a4ae",
                  command=self.boqua_nv, **btn_style).grid(row=0, column=4, padx=5)
        tk.Button(frame_btn, text="Đóng", bg="#ce93d8",
                  command=self.destroy, **btn_style).grid(row=0, column=5, padx=5)

        self.sua_mode = False
        self.selected_ma = None
        self.load_data()

    # === HÀM ===
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cursor.execute("SELECT * FROM nhanvien")
        for r in self.cursor.fetchall():
            self.tree.insert("", "end", values=r)

    def them_nv(self):
        try:
            sql = "INSERT INTO nhanvien VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            data = tuple(v.get() for v in self.vars.values())
            self.cursor.execute(sql, data)
            self.conn.commit()
            self.load_data()
            messagebox.showinfo("Thành công", "Đã thêm nhân viên mới!")
            self.boqua_nv()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi", f"Lỗi thêm dữ liệu:\n{err}")

    def xoa_nv(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên để xóa!")
            return
        ma = self.tree.item(selected, "values")[0]
        self.cursor.execute("DELETE FROM nhanvien WHERE MaNV=%s", (ma,))
        self.conn.commit()
        self.load_data()
        messagebox.showinfo("Xóa", "Đã xóa nhân viên!")

    def sua_nv(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn nhân viên để sửa!")
            return
        self.sua_mode = True
        vals = self.tree.item(selected, "values")
        for i, key in enumerate(self.vars.keys()):
            self.vars[key].set(vals[i])
        self.selected_ma = vals[0]

    def luu_nv(self):
        if not self.sua_mode or not self.selected_ma:
            return
        sql = """UPDATE nhanvien SET TenNV=%s, GioiTinh=%s, DiaChi=%s,
                 DienThoai=%s, NgaySinh=%s, ChucVu=%s, Luong=%s WHERE MaNV=%s"""
        data = (
            self.vars["TenNV"].get(),
            self.vars["GioiTinh"].get(),
            self.vars["DiaChi"].get(),
            self.vars["DienThoai"].get(),
            self.vars["NgaySinh"].get(),
            self.vars["ChucVu"].get(),
            self.vars["Luong"].get(),
            self.selected_ma
        )
        self.cursor.execute(sql, data)
        self.conn.commit()
        self.load_data()
        messagebox.showinfo("Lưu", "Đã cập nhật thông tin nhân viên!")
        self.boqua_nv()
        self.sua_mode = False

    def boqua_nv(self):
        for v in self.vars.values():
            v.set("")
        self.vars["GioiTinh"].set("Nam")

    def on_select(self, event):
        pass


if __name__ == "__main__":
    app = NhanVien()
    app.mainloop()