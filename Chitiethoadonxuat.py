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

class ChiTietHoaDonXuatFull(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chi Tiết Hóa Đơn Xuất")
        self.geometry("1200x670")
        self.configure(bg="#fce4ec")

        # ===== Biến =====
        self.vars_ct = {
            "MaHDX": tk.StringVar(),
            "MaVL": tk.StringVar(),
            "TenVL": tk.StringVar(),
            "SoLuong": tk.StringVar(),
            "SoLuongTonKho": tk.StringVar(),
            "DonVi": tk.StringVar(),
            "DonGia": tk.StringVar(),
            "ThanhTien": tk.StringVar()
        }

        self.selected_id = None

        # ===== LOAD DANH SÁCH VẬT LIỆU =====
        self.ds_vatlieu = self.load_vatlieu()

        # ===== Tiêu đề =====
        tk.Label(self, text="CHI TIẾT HÓA ĐƠN XUẤT", 
                 font=("Times New Roman", 22, "bold"),
                 bg="#fce4ec", fg="#ad1457").pack(pady=10)

        # ===== Khung nhập liệu =====
        frame_ct = tk.LabelFrame(self, text="Thông tin chi tiết hóa đơn xuất", 
                                 font=("Times New Roman", 12, "bold"),
                                 fg="#ad1457", bg="#ffffff",
                                 padx=10, pady=8)
        frame_ct.pack(padx=15, pady=5, fill="x")

        # --- Hóa đơn ---
        tk.Label(frame_ct, text="Hóa đơn xuất:", bg="#ffffff",
                 font=("Times New Roman", 11, "bold")).grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(frame_ct, textvariable=self.vars_ct["MaHDX"],
                 bg="#f8bbd0", width=25,
                 font=("Times New Roman", 11, "bold")).grid(row=0, column=1, padx=5, pady=5)

        # --- Vật liệu ---
        tk.Label(frame_ct, text="Vật liệu:", bg="#ffffff",
                 font=("Times New Roman", 11, "bold")).grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.cb_vl = ttk.Combobox(frame_ct, textvariable=self.vars_ct["TenVL"],
                                  values=[vl[1] for vl in self.ds_vatlieu],
                                  state="readonly", width=25, font=("Times New Roman", 11))
        self.cb_vl.grid(row=0, column=3, padx=5, pady=5)
        # Khi chọn tên vật liệu → tự tìm MaVL và tồn kho
        def select_ma_vl(event):
            ten = self.vars_ct["TenVL"].get()
            for row in self.ds_vatlieu:
                if row[1] == ten:
                    self.vars_ct["MaVL"].set(row[0])
                    self.vars_ct["DonVi"].set(row[2])
                    self.vars_ct["SoLuongTonKho"].set(row[5])
                    self.vars_ct["DonGia"].set(row[3])
                    break
        self.cb_vl.bind("<<ComboboxSelected>>", select_ma_vl)

        # --- Số lượng ---
        tk.Label(frame_ct, text="Số lượng xuất:", bg="#ffffff",
                 font=("Times New Roman", 11, "bold")).grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(frame_ct, textvariable=self.vars_ct["SoLuong"],
                 bg="#f8bbd0", width=25,
                 font=("Times New Roman", 11, "bold")).grid(row=1, column=1, padx=5, pady=5)

        # --- Số lượng tồn kho ---
        tk.Label(frame_ct, text="Số lượng tồn kho:", bg="#ffffff",
                 font=("Times New Roman", 11, "bold")).grid(row=1, column=2, padx=5, pady=5)
        tk.Entry(frame_ct, textvariable=self.vars_ct["SoLuongTonKho"],
                 bg="#f8bbd0", width=25,
                 font=("Times New Roman", 11, "bold"), state="readonly").grid(row=1, column=3, padx=5, pady=5)

        # --- Đơn vị ---
        tk.Label(frame_ct, text="Đơn vị:", bg="#ffffff",
                 font=("Times New Roman", 11, "bold")).grid(row=2, column=0, padx=5, pady=5)
        tk.Label(frame_ct, text="Đơn vị:", bg="#ffffff",
         font=("Times New Roman", 11, "bold")).grid(row=2, column=0, padx=5, pady=5)

        self.cb_donvi = ttk.Combobox(frame_ct, textvariable=self.vars_ct["DonVi"],
                             values=["Kg", "Cái", "Mét", "Bao", "Viên", "Cây", "Tấm"],
                             state="readonly", width=25, font=("Times New Roman", 11))
        self.cb_donvi.grid(row=2, column=1, padx=5, pady=5)
        # --- Đơn giá ---
        tk.Label(frame_ct, text="Đơn giá:", bg="#ffffff",
                 font=("Times New Roman", 11, "bold")).grid(row=2, column=2, padx=5, pady=5)
        tk.Entry(frame_ct, textvariable=self.vars_ct["DonGia"],
                 bg="#f8bbd0", width=25,
                 font=("Times New Roman", 11, "bold")).grid(row=2, column=3, padx=5, pady=5)

        # --- Thành tiền ---
        tk.Label(frame_ct, text="Thành tiền:", bg="#ffffff",
                 font=("Times New Roman", 11, "bold")).grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(frame_ct, textvariable=self.vars_ct["ThanhTien"],
                 bg="#f8bbd0", width=25,
                 font=("Times New Roman", 11, "bold"), state="readonly").grid(row=3, column=1, padx=5, pady=5)

        # Tự tính thành tiền
        def update_tt(*args):
            try:
                sl = float(self.vars_ct["SoLuong"].get())
                dg = float(self.vars_ct["DonGia"].get())
                self.vars_ct["ThanhTien"].set(f"{sl * dg:.2f}")
            except:
                self.vars_ct["ThanhTien"].set("")
        self.vars_ct["SoLuong"].trace("w", update_tt)
        self.vars_ct["DonGia"].trace("w", update_tt)

        # ===== TREEVIEW =====
        frame_table = tk.LabelFrame(self, text="Danh sách chi tiết hóa đơn xuất", 
                                    font=("Times New Roman", 12, "bold"),
                                    fg="#ad1457", bg="#ffffff")
        frame_table.pack(padx=5, pady=5, fill="both", expand=True)

        columns = ("Hóa Đơn Xuất","Vật liệu","Số Lượng","Số Lượng Tồn Kho","Đơn Vị","Đơn Giá","Thành Tiền")
        self.tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=10)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Times New Roman", 12, "bold"), background="#ffd1dc")
        style.configure("Treeview", rowheight=27, font=("Times New Roman", 11))

        self.tree.tag_configure("evenrow", background="#ffffff")
        self.tree.tag_configure("oddrow", background="#f9f9f9")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        self.tree.pack(fill="both", expand=True)

        vsb = ttk.Scrollbar(frame_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # ===== NÚT =====
        frame_btn = tk.Frame(self, bg="#fce4ec")
        frame_btn.pack(pady=5)

        def pastel_btn(text, color, cmd, col):
            tk.Button(frame_btn, text=text, command=cmd,
                      bg=color, fg="white",
                      font=("Times New Roman", 11, "bold"),
                      width=12, relief="flat").grid(row=0, column=col, padx=6)

        pastel_btn("Thêm", "#f48fb1", self.them, 0)
        pastel_btn("Xóa", "#e57373", self.xoa, 1)
        pastel_btn("Sửa", "#ffb74d", self.sua, 2)
        pastel_btn("Bỏ qua", "#90a4ae", self.boqua, 3)
        pastel_btn("Lưu", "#81c784", self.luu, 4)
        pastel_btn("Đóng", "#ce93d8", self.destroy, 5)

        self.load_data()

    # ================== LOAD VẬT LIỆU ==================
    def load_vatlieu(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT MaVL, TenVL, DonVi, Gia, MaNCC, SoLuong FROM vatlieu")
        rows = cursor.fetchall()
        conn.close()
        return rows

    # ================== LOAD DATA ==================
    def load_data(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.MaHDX, v.TenVL, c.SoLuong, c.DonVi, c.DonGia, c.ThanhTien
            FROM chitiethoadonxuat c
            JOIN vatlieu v ON c.MaVL = v.MaVL
        """)
        rows = cursor.fetchall()
        self.tree.delete(*self.tree.get_children())
        for i, row in enumerate(rows):
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            # Lấy tồn kho từ vatlieu
            cursor.execute("SELECT SoLuong FROM vatlieu WHERE TenVL=%s", (row[1],))
            soluongton = cursor.fetchone()[0]
            self.tree.insert("", "end", values=(row[0], row[1], row[2], soluongton, row[3], row[4], row[5]), tags=(tag,))
        conn.close()

    # ================== HANDLE SELECT ==================
    def on_select(self, event):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel)["values"]

        self.selected_id = vals[0]

        self.vars_ct["MaHDX"].set(vals[0])
        self.vars_ct["TenVL"].set(vals[1])
        self.vars_ct["SoLuong"].set(vals[2])
        self.vars_ct["SoLuongTonKho"].set(vals[3])
        self.vars_ct["DonVi"].set(vals[4])
        self.vars_ct["DonGia"].set(vals[5])
        self.vars_ct["ThanhTien"].set(vals[6])

    # ================== CRUD ==================
    def them(self):
        # Kiểm tra tồn kho
        sl = float(self.vars_ct["SoLuong"].get())
        slton = float(self.vars_ct["SoLuongTonKho"].get())
        if sl > slton:
            messagebox.showwarning("Cảnh báo", "Số lượng xuất vượt tồn kho!")
            return

        mahd = f"HDX{len(self.tree.get_children())+1:03d}"
        self.tree.insert("", "end",
                         values=(mahd,
                                 self.vars_ct["TenVL"].get(),
                                 self.vars_ct["SoLuong"].get(),
                                 slton-sl,
                                 self.vars_ct["DonVi"].get(),
                                 self.vars_ct["DonGia"].get(),
                                 self.vars_ct["ThanhTien"].get()))
        self.boqua()

    def xoa(self):
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn dòng để xóa!")
            return
        for item in self.tree.get_children():
            if self.tree.item(item)["values"][0] == self.selected_id:
                self.tree.delete(item)
                break
        self.boqua()

    def sua(self):
        if not self.selected_id:
            messagebox.showwarning("Cảnh báo", "Bạn chưa chọn dòng để sửa!")
            return
        for item in self.tree.get_children():
            if self.tree.item(item)["values"][0] == self.selected_id:
                sl = float(self.vars_ct["SoLuong"].get())
                slton = float(self.vars_ct["SoLuongTonKho"].get())
                if sl > slton + sl:
                    messagebox.showwarning("Cảnh báo", "Số lượng xuất vượt tồn kho!")
                    return
                self.tree.item(item, values=(self.selected_id,
                                             self.vars_ct["TenVL"].get(),
                                             sl,
                                             slton,
                                             self.vars_ct["DonVi"].get(),
                                             self.vars_ct["DonGia"].get(),
                                             self.vars_ct["ThanhTien"].get()))
                break
        self.boqua()

    def boqua(self):
        for v in self.vars_ct.values():
            v.set("")
        self.selected_id = None

    # ================== SAVE TO MYSQL ==================
    def luu(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chitiethoadonxuat")  # Ghi lại toàn bộ
        for row in self.tree.get_children():
            vals = self.tree.item(row)["values"]

            tenvl = vals[1]
            mavl = None
            for x in self.ds_vatlieu:
                if x[1] == tenvl:
                    mavl = x[0]
                    break

            # Cập nhật tồn kho trong vatlieu
            cursor.execute("UPDATE vatlieu SET SoLuong = %s WHERE MaVL = %s", (vals[3], mavl))

            cursor.execute("""
                INSERT INTO chitiethoadonxuat(MaHDX, MaVL, SoLuong, DonVi, DonGia, ThanhTien)
                VALUES (%s,%s,%s,%s,%s,%s)
            """, (vals[0], mavl, vals[2], vals[4], vals[5], vals[6]))
        conn.commit()
        conn.close()
        messagebox.showinfo("Thành công", "Đã lưu dữ liệu và cập nhật tồn kho vào MySQL!")

if __name__=="__main__":
    app = ChiTietHoaDonXuatFull()
    app.mainloop()
