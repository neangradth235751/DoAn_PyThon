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

# ======== CLASS QUẢN LÝ VẬT LIỆU ========
class VatLieu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý vật liệu")
        self.geometry("950x550")
        self.configure(bg="#fce4ec")

        # --- Tiêu đề ---
        tk.Label(self, text="THÔNG TIN VẬT LIỆU", font=("times new roman", 20, "bold"),
                 fg="#ad1457", bg="#fce4ec").pack(pady=10)

        # --- Khung nhập liệu ---
        frame_input = tk.LabelFrame(self, text="Thông tin vật liệu", font=("times new roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=10, pady=10)
        frame_input.pack(padx=15, pady=5, fill="x")

        self.vars = {
            "MaVL": tk.StringVar(),
            "TenVL": tk.StringVar(),
            "DonVi": tk.StringVar(),
            "Gia": tk.StringVar(),
            "SoLuong": tk.StringVar()
            
        }

        labels = ["Mã VL:", "Tên VL:", "Đơn vị:", "Giá:", "Số lượng:"]
        keys = ["MaVL", "TenVL", "DonVi", "Gia", "SoLuong"]
        list_donvi = ["Kg", "Bao", "Viên", "m3", "Lít", "Cây", "Tấm"]

        # Lấy danh sách nhà cung cấp từ MySQL
        self.ncc_dict = self.get_ncc_dict()
        list_ncc = list(self.ncc_dict.keys())

        for i, (label, key) in enumerate(zip(labels, keys)):
            tk.Label(frame_input, text=label, bg="#ffffff", font=("times new roman", 10, "bold")).grid(
                row=i // 2, column=(i % 2) * 2, sticky="w", padx=8, pady=5
            )
            if key == "DonVi":
                cb = ttk.Combobox(frame_input, textvariable=self.vars[key], values=list_donvi,
                                  width=22, state="readonly", font=("times new roman", 11))
                cb.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=8, pady=5)
                cb.current(0)
            elif key == "TenNCC":
                cbncc = ttk.Combobox(frame_input, textvariable=self.vars[key], values=list_ncc,
                                     width=22, state="readonly", font=("times new roman", 11))
                cbncc.grid(row=i // 2, column=(i % 2) * 2 + 1, padx=8, pady=5)
                if list_ncc:
                    cbncc.current(0)
            else:
                tk.Entry(frame_input, textvariable=self.vars[key], width=25,
                         font=("times new roman", 11), bg="#f8bbd0").grid(
                    row=i // 2, column=(i % 2) * 2 + 1, padx=8, pady=5
                )

        # --- Treeview ---
        columns = ("Mã VL", "Tên VL", "Đơn vị", "Giá", "Số lượng", "Nhà cung cấp")
        frame_table = tk.LabelFrame(self, text="Danh sách vật liệu", font=("times new roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff", bd=2, relief="ridge", padx=8, pady=8)
        frame_table.pack(padx=15, pady=10, fill="both", expand=True)

        style = ttk.Style()
        style.configure("Treeview", rowheight=22, font=("times new roman", 10))
        style.configure("Treeview.Heading", font=("Times New Roman", 11, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])

        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130, anchor="center")
        self.tree.pack(side="left", fill="both", expand=True)

        # màu xen kẽ
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
        btn_style = {"font": ("times new roman", 10, "bold"), "fg": "white", "width": 12, "relief": "flat"}

        tk.Button(frame_btn, text="Thêm", bg="#f48fb1", command=self.them, **btn_style).grid(row=0, column=0, padx=3)
        tk.Button(frame_btn, text="Xóa", bg="#e57373", command=self.xoa, **btn_style).grid(row=0, column=1, padx=3)
        tk.Button(frame_btn, text="Sửa", bg="#ffb74d", command=self.sua, **btn_style).grid(row=0, column=2, padx=3)
        tk.Button(frame_btn, text="Lưu", bg="#81c784", command=self.luu, **btn_style).grid(row=0, column=3, padx=3)
        tk.Button(frame_btn, text="Bỏ qua", bg="#90a4ae", command=self.bo_qua, **btn_style).grid(row=0, column=4, padx=3)
        tk.Button(frame_btn, text="Đóng", bg="#ce93d8", command=self.destroy, **btn_style).grid(row=0, column=5, padx=3)

        # --- Tải dữ liệu ---
        self.load_data()

    # ======== HÀM LẤY DANH SÁCH NHÀ CUNG CẤP ========
    def get_ncc_dict(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT TenNCC, MaNCC FROM nhacungcap ORDER BY TenNCC")
            data = cursor.fetchall()
            conn.close()
            return {ten: ma for ten, ma in data}
        except mysql.connector.Error:
            return {}

    # ======== CRUD ========
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            query = """
                SELECT vl.MaVL, vl.TenVL, vl.DonVi, vl.Gia, vl.SoLuong, ncc.TenNCC
                FROM vatlieu vl
                LEFT JOIN nhacungcap ncc ON vl.MaNCC = ncc.MaNCC
                ORDER BY vl.MaVL
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", f"Lỗi kết nối: {err}")
            rows = []

        for i, r in enumerate(rows):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=r, tags=(tag,))
        self.data = rows

    def them(self):
        ma, ten, donvi, gia, sl, tenncc = [v.get().strip() for v in self.vars.values()]
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên vật liệu!")
            return
        try:
            mancc = self.ncc_dict.get(tenncc, None)
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO vatlieu(MaVL, TenVL, DonVi, Gia, SoLuong, MaNCC) VALUES(%s,%s,%s,%s,%s,%s)",
                (ma, ten, donvi, gia, sl, mancc)
            )
            conn.commit()
            conn.close()
            self.load_data()
            self.bo_qua()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", f"Lỗi thêm: {err}")

    def xoa(self):
        if self.selected_index is None:
            messagebox.showinfo("Chọn dòng", "Vui lòng chọn vật liệu cần xóa!")
            return
        ma = self.data[self.selected_index][0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vatlieu WHERE MaVL=%s", (ma,))
            conn.commit()
            conn.close()
            self.load_data()
            self.bo_qua()
        except mysql.connector.Error as err:
            messagebox.showerror("Lỗi MySQL", f"Lỗi xóa: {err}")

    def sua(self):
        if self.selected_index is None:
            messagebox.showinfo("Chọn dòng", "Vui lòng chọn vật liệu cần sửa!")
            return
        ma, ten, donvi, gia, sl, tenncc = [v.get().strip() for v in self.vars.values()]
        mancc = self.ncc_dict.get(tenncc, None)
        old_ma = self.data[self.selected_index][0]
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vatlieu 
                SET MaVL=%s, TenVL=%s, DonVi=%s, Gia=%s, SoLuong=%s, MaNCC=%s
                WHERE MaVL=%s
            """, (ma, ten, donvi, gia, sl, mancc, old_ma))
            conn.commit()
            conn.close()
            self.load_data()
            self.bo_qua()
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
    app = VatLieu()
    app.mainloop()
