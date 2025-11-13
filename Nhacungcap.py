import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

# ======== KẾT NỐI MYSQL ========
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="quanly_cuahangvatlieuxaydung"
    )

# ======== CLASS QUẢN LÝ NHÀ CUNG CẤP ========
class NhaCungCap(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Thông tin nhà cung cấp")
        self.geometry("800x600")
        self.configure(bg="#fce4ec")

        # --- Tiêu đề ---
        tk.Label(self, text="THÔNG TIN NHÀ CUNG CẤP",
                 font=("Times New Roman", 20, "bold"), fg="#ad1457", bg="#fce4ec").pack(pady=10)

        # --- Khung nhập liệu ---
        frame_input = tk.LabelFrame(self, text="Thông tin nhà cung cấp",
                                    font=("Times New Roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=10)
        frame_input.pack(padx=15, pady=5, fill="x")

        # ======== Biến ========
        self.vars = {
            "MaNCC": tk.StringVar(),
            "TenNCC": tk.StringVar(),
            "DiaChi": tk.StringVar(),
            "SDT": tk.StringVar()
        }

        labels = ["Mã NCC:", "Tên NCC:", "Địa chỉ:", "Số điện thoại:"]
        keys = ["MaNCC", "TenNCC", "DiaChi", "SDT"]

        # Lấy danh sách địa chỉ có sẵn từ database
        self.list_diachi = self.get_distinct("DiaChi")

        # ======== Tạo ô nhập liệu / Combobox ========
        for i, (label, key) in enumerate(zip(labels, keys)):
            tk.Label(frame_input, text=label, bg="#ffffff", font=("Times New Roman", 11, "bold")).grid(
                row=i//2, column=(i%2)*2, sticky="w", padx=8, pady=5
            )
            if key == "DiaChi":  # Combobox cho địa chỉ
                cb = ttk.Combobox(frame_input, textvariable=self.vars[key], values=self.list_diachi,
                                  width=25, state="readonly", font=("Times New Roman", 11))
                cb.grid(row=i//2, column=(i%2)*2 + 1, padx=8, pady=5)
                self.vars[key].set("")
            else:  # MaNCC, TenNCC, SDT nhập tự do
                tk.Entry(frame_input, textvariable=self.vars[key], width=25,
                         font=("Times New Roman", 11), bg="#f8bbd0").grid(
                    row=i//2, column=(i%2)*2 + 1, padx=8, pady=5
                )

        # --- Treeview ---
        columns = ("Mã NCC", "Tên NCC", "Địa chỉ", "Số điện thoại")
        frame_table = tk.LabelFrame(self, text="Danh sách nhà cung cấp",
                                    font=("Times New Roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=8, pady=8)
        frame_table.pack(padx=15, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=22, font=("Times New Roman", 10))
        style.configure("Treeview.Heading", font=("Times New Roman", 11, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        self.tree.tag_configure('evenrow', background='#f9f9f9')
        self.tree.tag_configure('oddrow', background='#ffffff')

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.selected_index = None

        # --- Nút chức năng ---
        frame_btn = tk.Frame(self, bg="#fce4ec")
        frame_btn.pack(pady=5)
        btn_style = {"font": ("Times New Roman", 10, "bold"), "fg": "white", "width": 12, "relief": "flat"}

        tk.Button(frame_btn, text="Thêm", bg="#f48fb1", command=self.them, **btn_style).grid(row=0, column=0, padx=3)
        tk.Button(frame_btn, text="Xóa", bg="#e57373", command=self.xoa, **btn_style).grid(row=0, column=1, padx=3)
        tk.Button(frame_btn, text="Sửa", bg="#ffb74d", command=self.sua, **btn_style).grid(row=0, column=2, padx=3)
        tk.Button(frame_btn, text="Lưu", bg="#81c784", command=self.luu, **btn_style).grid(row=0, column=3, padx=3)
        tk.Button(frame_btn, text="Bỏ qua", bg="#90a4ae", command=self.bo_qua, **btn_style).grid(row=0, column=4, padx=3)
        tk.Button(frame_btn, text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0, column=5, padx=3)

        # --- Tải dữ liệu ---
        self.load_data()

    # ======== Lấy danh sách distinct cho Combobox ========
    def get_distinct(self, column):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"SELECT DISTINCT {column} FROM nhacungcap ORDER BY {column}")
            rows = [r[0] for r in cursor.fetchall() if r[0]]  # bỏ giá trị None
            conn.close()
            return rows
        except mysql.connector.Error:
            return []

    # ======== CRUD ========
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT MaNCC, TenNCC, DiaChi, SDT FROM nhacungcap ORDER BY MaNCC")
            rows = cursor.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", f"Lỗi kết nối: {err}")
            rows = []

        for i, r in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=r, tags=(tag,))
        self.data = rows
        # Cập nhật lại danh sách địa chỉ cho Combobox
        self.list_diachi = self.get_distinct("DiaChi")

    def them(self):
        ma = self.vars["MaNCC"].get().strip()
        ten, diachi, sdt = self.vars["TenNCC"].get().strip(), self.vars["DiaChi"].get().strip(), self.vars["SDT"].get().strip()
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên nhà cung cấp!")
            return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO nhacungcap(MaNCC, TenNCC, DiaChi, SDT) VALUES(%s,%s,%s,%s)",
                           (ma, ten, diachi, sdt))
            conn.commit()
            conn.close()
            self.load_data()
            self.bo_qua()
            messagebox.showinfo("Thành công", "Đã thêm nhà cung cấp mới!")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", f"Lỗi thêm: {err}")

    def xoa(self):
        if self.selected_index is None:
            messagebox.showinfo("Chọn dòng", "Vui lòng chọn nhà cung cấp cần xóa!")
            return
        ma = self.data[self.selected_index][0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM nhacungcap WHERE MaNCC=%s", (ma,))
            conn.commit()
            conn.close()
            self.load_data()
            self.bo_qua()
            messagebox.showinfo("Đã xóa", "Đã xóa nhà cung cấp thành công!")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", f"Lỗi xóa: {err}")

    def sua(self):
        if self.selected_index is None:
            messagebox.showinfo("Chọn dòng", "Vui lòng chọn nhà cung cấp cần sửa!")
            return
        ma = self.vars["MaNCC"].get().strip()
        ten, diachi, sdt = self.vars["TenNCC"].get().strip(), self.vars["DiaChi"].get().strip(), self.vars["SDT"].get().strip()
        old_ma = self.data[self.selected_index][0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE nhacungcap SET MaNCC=%s, TenNCC=%s, DiaChi=%s, SDT=%s WHERE MaNCC=%s",
                           (ma, ten, diachi, sdt, old_ma))
            conn.commit()
            conn.close()
            self.load_data()
            self.bo_qua()
            messagebox.showinfo("Cập nhật", "Đã sửa thông tin nhà cung cấp!")
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", f"Lỗi sửa: {err}")

    def luu(self):
        messagebox.showinfo("Lưu", "Dữ liệu đã được lưu vào MySQL!")

    def bo_qua(self):
        for v in self.vars.values():
            v.set("")
        self.selected_index = None
        self.tree.selection_remove(self.tree.selection())

    def on_select(self, event):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            self.selected_index = idx
            for i, key in enumerate(self.vars.keys()):
                self.vars[key].set(self.data[idx][i])

# ======== CHẠY CHƯƠNG TRÌNH ========
if __name__ == "__main__":
    app = NhaCungCap()
    app.mainloop()
