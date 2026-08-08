
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime


# ============================================================
# DATABASE
# ============================================================

DB_NAME = "hospital.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Users
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'Admin'
        )
    """)

    # Patients
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            address TEXT,
            blood_group TEXT,
            disease TEXT,
            created_at TEXT
        )
    """)

    # Doctors
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            specialization TEXT,
            phone TEXT,
            room TEXT,
            availability TEXT
        )
    """)

    # Appointments
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            doctor_id INTEGER,
            date TEXT,
            time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Scheduled',
            FOREIGN KEY(patient_id) REFERENCES patients(id),
            FOREIGN KEY(doctor_id) REFERENCES doctors(id)
        )
    """)

    # Bills
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            consultation REAL DEFAULT 0,
            medicine REAL DEFAULT 0,
            room REAL DEFAULT 0,
            tests REAL DEFAULT 0,
            total REAL DEFAULT 0,
            date TEXT,
            status TEXT DEFAULT 'Unpaid',
            FOREIGN KEY(patient_id) REFERENCES patients(id)
        )
    """)

    # Medicines
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            quantity INTEGER DEFAULT 0,
            price REAL DEFAULT 0,
            expiry TEXT
        )
    """)

    # Default admin
    cursor.execute(
        "SELECT * FROM users WHERE username=?",
        ("admin",)
    )

    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users(username, password, role)
            VALUES (?, ?, ?)
        """, ("admin", "admin123", "Admin"))

    conn.commit()
    conn.close()


# ============================================================
# MAIN APPLICATION
# ============================================================

class HospitalApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management & Appointment System")
        self.root.geometry("1200x700")
        self.root.minsize(1000, 600)

        self.current_user = None

        self.setup_style()
        self.login_screen()

    # ========================================================
    # STYLE
    # ========================================================

    def setup_style(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Heading.TLabel",
            font=("Arial", 16, "bold")
        )

        style.configure(
            "TButton",
            font=("Arial", 10),
            padding=6
        )

        style.configure(
            "Treeview",
            rowheight=28,
            font=("Arial", 10)
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

    # ========================================================
    # CLEAR SCREEN
    # ========================================================

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ========================================================
    # LOGIN
    # ========================================================

    def login_screen(self):

        self.clear_screen()

        main = tk.Frame(self.root, bg="#eaf4f4")
        main.pack(fill="both", expand=True)

        card = tk.Frame(
            main,
            bg="white",
            bd=2,
            relief="ridge"
        )

        card.place(
            relx=0.5,
            rely=0.5,
            anchor="center",
            width=420,
            height=430
        )

        tk.Label(
            card,
            text="🏥",
            font=("Arial", 50),
            bg="white"
        ).pack(pady=(25, 0))

        tk.Label(
            card,
            text="Hospital Management System",
            font=("Arial", 18, "bold"),
            bg="white"
        ).pack(pady=10)

        tk.Label(
            card,
            text="Admin Login",
            font=("Arial", 13),
            bg="white"
        ).pack(pady=5)

        tk.Label(
            card,
            text="Username",
            bg="white",
            font=("Arial", 11)
        ).pack(anchor="w", padx=55, pady=(15, 3))

        self.username_entry = tk.Entry(
            card,
            font=("Arial", 12),
            width=30
        )
        self.username_entry.pack()

        tk.Label(
            card,
            text="Password",
            bg="white",
            font=("Arial", 11)
        ).pack(anchor="w", padx=55, pady=(15, 3))

        self.password_entry = tk.Entry(
            card,
            font=("Arial", 12),
            width=30,
            show="*"
        )
        self.password_entry.pack()

        tk.Button(
            card,
            text="LOGIN",
            font=("Arial", 12, "bold"),
            bg="#2196f3",
            fg="white",
            width=25,
            command=self.login
        ).pack(pady=25)

        tk.Label(
            card,
            text="Default: admin / admin123",
            fg="gray",
            bg="white"
        ).pack()

        self.username_entry.focus()

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT username, role
            FROM users
            WHERE username=? AND password=?
        """, (username, password))

        user = cursor.fetchone()

        conn.close()

        if user:
            self.current_user = user
            self.dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )

    # ========================================================
    # DASHBOARD
    # ========================================================

    def dashboard(self):

        self.clear_screen()

        # Header
        header = tk.Frame(
            self.root,
            bg="#1565c0",
            height=70
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="🏥 HOSPITAL MANAGEMENT SYSTEM",
            bg="#1565c0",
            fg="white",
            font=("Arial", 20, "bold")
        ).pack(side="left", padx=25, pady=18)

        tk.Button(
            header,
            text="Logout",
            command=self.login_screen,
            bg="#d32f2f",
            fg="white",
            font=("Arial", 10, "bold")
        ).pack(side="right", padx=20)

        # Sidebar
        sidebar = tk.Frame(
            self.root,
            bg="#263238",
            width=220
        )
        sidebar.pack(side="left", fill="y")

        buttons = [
            ("🏠 Dashboard", self.dashboard),
            ("👤 Patients", self.patient_page),
            ("👨‍⚕ Doctors", self.doctor_page),
            ("📅 Appointments", self.appointment_page),
            ("💰 Billing", self.billing_page),
            ("💊 Medicines", self.medicine_page),
            ("🔎 Patient Search", self.search_page),
        ]

        for text, command in buttons:

            tk.Button(
                sidebar,
                text=text,
                command=command,
                bg="#263238",
                fg="white",
                activebackground="#455a64",
                activeforeground="white",
                bd=0,
                anchor="w",
                font=("Arial", 11),
                padx=20,
                pady=13
            ).pack(fill="x")

        # Main
        self.main_frame = tk.Frame(
            self.root,
            bg="#f5f7fa"
        )
        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.dashboard_content()

    # ========================================================
    # DASHBOARD CONTENT
    # ========================================================

    def dashboard_content(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Dashboard",
            font=("Arial", 24, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=30, pady=25)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM patients")
        patients = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM doctors")
        doctors = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM appointments")
        appointments = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM bills")
        bills = cursor.fetchone()[0]

        conn.close()

        cards = tk.Frame(
            self.main_frame,
            bg="#f5f7fa"
        )
        cards.pack(fill="x", padx=30)

        self.create_card(
            cards,
            "👤 Patients",
            patients,
            "#2196f3"
        )

        self.create_card(
            cards,
            "👨‍⚕ Doctors",
            doctors,
            "#4caf50"
        )

        self.create_card(
            cards,
            "📅 Appointments",
            appointments,
            "#ff9800"
        )

        self.create_card(
            cards,
            "💰 Bills",
            bills,
            "#9c27b0"
        )

        # Recent appointments
        tk.Label(
            self.main_frame,
            text="Recent Appointments",
            font=("Arial", 16, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=30, pady=(35, 10))

        tree_frame = tk.Frame(self.main_frame)
        tree_frame.pack(fill="both", expand=True, padx=30)

        columns = (
            "ID",
            "Patient",
            "Doctor",
            "Date",
            "Time",
            "Status"
        )

        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)

        tree.pack(fill="both", expand=True)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.id,
                p.name,
                d.name,
                a.date,
                a.time,
                a.status
            FROM appointments a
            LEFT JOIN patients p
                ON a.patient_id = p.id
            LEFT JOIN doctors d
                ON a.doctor_id = d.id
            ORDER BY a.id DESC
            LIMIT 10
        """)

        rows = cursor.fetchall()
        conn.close()

        for row in rows:
            tree.insert("", "end", values=row)

    def create_card(self, parent, title, value, color):

        card = tk.Frame(
            parent,
            bg=color,
            width=200,
            height=120
        )

        card.pack(
            side="left",
            padx=10,
            fill="x",
            expand=True
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title,
            bg=color,
            fg="white",
            font=("Arial", 13, "bold")
        ).pack(pady=(20, 5))

        tk.Label(
            card,
            text=str(value),
            bg=color,
            fg="white",
            font=("Arial", 26, "bold")
        ).pack()

    # ========================================================
    # PATIENT PAGE
    # ========================================================

    def patient_page(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Patient Management",
            font=("Arial", 22, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=25, pady=15)

        form = tk.LabelFrame(
            self.main_frame,
            text="Register Patient",
            font=("Arial", 12, "bold"),
            bg="#f5f7fa"
        )

        form.pack(fill="x", padx=25)

        labels = [
            "Name",
            "Age",
            "Gender",
            "Phone",
            "Address",
            "Blood Group",
            "Disease"
        ]

        self.patient_entries = {}

        for i, label in enumerate(labels):

            row = i // 2
            col = (i % 2) * 2

            tk.Label(
                form,
                text=label,
                bg="#f5f7fa"
            ).grid(
                row=row,
                column=col,
                padx=10,
                pady=8,
                sticky="w"
            )

            entry = tk.Entry(
                form,
                width=28
            )

            entry.grid(
                row=row,
                column=col + 1,
                padx=10,
                pady=8
            )

            self.patient_entries[label] = entry

        tk.Button(
            form,
            text="Register Patient",
            bg="#2196f3",
            fg="white",
            command=self.add_patient
        ).grid(
            row=4,
            column=0,
            columnspan=4,
            pady=12
        )

        # Table
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        columns = (
            "ID",
            "Name",
            "Age",
            "Gender",
            "Phone",
            "Blood",
            "Disease"
        )

        self.patient_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.patient_tree.heading(col, text=col)
            self.patient_tree.column(col, width=110)

        self.patient_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.patient_tree.yview
        )

        scrollbar.pack(side="right", fill="y")

        self.patient_tree.configure(
            yscrollcommand=scrollbar.set
        )

        tk.Button(
            self.main_frame,
            text="Delete Selected Patient",
            bg="#d32f2f",
            fg="white",
            command=self.delete_patient
        ).pack(pady=(0, 15))

        self.load_patients()

    def add_patient(self):

        data = {
            key: entry.get().strip()
            for key, entry in self.patient_entries.items()
        }

        if not data["Name"]:
            messagebox.showwarning(
                "Missing",
                "Patient name is required."
            )
            return

        try:
            age = int(data["Age"]) if data["Age"] else None
        except ValueError:
            messagebox.showerror(
                "Invalid",
                "Age must be a number."
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO patients
            (name, age, gender, phone, address,
             blood_group, disease, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["Name"],
            age,
            data["Gender"],
            data["Phone"],
            data["Address"],
            data["Blood Group"],
            data["Disease"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Patient registered successfully."
        )

        self.patient_page()

    def load_patients(self):

        for item in self.patient_tree.get_children():
            self.patient_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                age,
                gender,
                phone,
                blood_group,
                disease
            FROM patients
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:
            self.patient_tree.insert(
                "",
                "end",
                values=row
            )

    def delete_patient(self):

        selected = self.patient_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select",
                "Select a patient first."
            )
            return

        values = self.patient_tree.item(
            selected[0]
        )["values"]

        patient_id = values[0]

        if not messagebox.askyesno(
            "Confirm",
            "Delete this patient?"
        ):
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM patients WHERE id=?",
            (patient_id,)
        )

        conn.commit()
        conn.close()

        self.load_patients()

    # ========================================================
    # DOCTOR PAGE
    # ========================================================

    def doctor_page(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Doctor Management",
            font=("Arial", 22, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=25, pady=15)

        form = tk.LabelFrame(
            self.main_frame,
            text="Add Doctor",
            bg="#f5f7fa",
            font=("Arial", 12, "bold")
        )

        form.pack(fill="x", padx=25)

        labels = [
            "Name",
            "Specialization",
            "Phone",
            "Room",
            "Availability"
        ]

        self.doctor_entries = {}

        for i, label in enumerate(labels):

            tk.Label(
                form,
                text=label,
                bg="#f5f7fa"
            ).grid(
                row=0,
                column=i * 2,
                padx=5,
                pady=12
            )

            entry = tk.Entry(
                form,
                width=15
            )

            entry.grid(
                row=0,
                column=i * 2 + 1,
                padx=5
            )

            self.doctor_entries[label] = entry

        tk.Button(
            form,
            text="Add Doctor",
            bg="#4caf50",
            fg="white",
            command=self.add_doctor
        ).grid(
            row=1,
            column=0,
            columnspan=10,
            pady=10
        )

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        columns = (
            "ID",
            "Name",
            "Specialization",
            "Phone",
            "Room",
            "Availability"
        )

        self.doctor_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.doctor_tree.heading(
                col,
                text=col
            )

        self.doctor_tree.pack(
            fill="both",
            expand=True
        )

        tk.Button(
            self.main_frame,
            text="Delete Selected Doctor",
            bg="#d32f2f",
            fg="white",
            command=self.delete_doctor
        ).pack(pady=(0, 15))

        self.load_doctors()

    def add_doctor(self):

        data = {
            key: entry.get().strip()
            for key, entry in self.doctor_entries.items()
        }

        if not data["Name"]:
            messagebox.showwarning(
                "Missing",
                "Doctor name is required."
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO doctors
            (name, specialization, phone, room, availability)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["Name"],
            data["Specialization"],
            data["Phone"],
            data["Room"],
            data["Availability"]
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Doctor added successfully."
        )

        self.doctor_page()

    def load_doctors(self):

        for item in self.doctor_tree.get_children():
            self.doctor_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                specialization,
                phone,
                room,
                availability
            FROM doctors
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:
            self.doctor_tree.insert(
                "",
                "end",
                values=row
            )

    def delete_doctor(self):

        selected = self.doctor_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select",
                "Select a doctor first."
            )
            return

        values = self.doctor_tree.item(
            selected[0]
        )["values"]

        doctor_id = values[0]

        if not messagebox.askyesno(
            "Confirm",
            "Delete this doctor?"
        ):
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM doctors WHERE id=?",
            (doctor_id,)
        )

        conn.commit()
        conn.close()

        self.load_doctors()

    # ========================================================
    # APPOINTMENT PAGE
    # ========================================================

    def appointment_page(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Appointment Management",
            font=("Arial", 22, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=25, pady=15)

        form = tk.LabelFrame(
            self.main_frame,
            text="Book Appointment",
            bg="#f5f7fa",
            font=("Arial", 12, "bold")
        )

        form.pack(fill="x", padx=25)

        # Patient
        tk.Label(
            form,
            text="Patient",
            bg="#f5f7fa"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.patient_combo = ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )

        self.patient_combo.grid(
            row=0,
            column=1,
            padx=10
        )

        # Doctor
        tk.Label(
            form,
            text="Doctor",
            bg="#f5f7fa"
        ).grid(row=0, column=2, padx=10)

        self.doctor_combo = ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )

        self.doctor_combo.grid(
            row=0,
            column=3,
            padx=10
        )

        # Date
        tk.Label(
            form,
            text="Date",
            bg="#f5f7fa"
        ).grid(row=1, column=0, padx=10, pady=10)

        self.app_date = tk.Entry(
            form,
            width=33
        )

        self.app_date.insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        self.app_date.grid(
            row=1,
            column=1
        )

        # Time
        tk.Label(
            form,
            text="Time",
            bg="#f5f7fa"
        ).grid(row=1, column=2)

        self.app_time = tk.Entry(
            form,
            width=33
        )

        self.app_time.insert(0, "10:00")

        self.app_time.grid(
            row=1,
            column=3
        )

        # Reason
        tk.Label(
            form,
            text="Reason",
            bg="#f5f7fa"
        ).grid(row=2, column=0, padx=10)

        self.app_reason = tk.Entry(
            form,
            width=33
        )

        self.app_reason.grid(
            row=2,
            column=1
        )

        tk.Button(
            form,
            text="Book Appointment",
            bg="#ff9800",
            fg="white",
            command=self.book_appointment
        ).grid(
            row=3,
            column=0,
            columnspan=4,
            pady=15
        )

        # Load combo boxes
        self.load_patient_combo()
        self.load_doctor_combo()

        # Table
        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        columns = (
            "ID",
            "Patient",
            "Doctor",
            "Date",
            "Time",
            "Reason",
            "Status"
        )

        self.appointment_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.appointment_tree.heading(
                col,
                text=col
            )
            self.appointment_tree.column(
                col,
                width=120
            )

        self.appointment_tree.pack(
            fill="both",
            expand=True
        )

        tk.Button(
            self.main_frame,
            text="Cancel Selected Appointment",
            bg="#d32f2f",
            fg="white",
            command=self.cancel_appointment
        ).pack(pady=(0, 15))

        self.load_appointments()

    def load_patient_combo(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name FROM patients ORDER BY name"
        )

        rows = cursor.fetchall()

        conn.close()

        self.patient_data = rows

        self.patient_combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in rows
        ]

        if rows:
            self.patient_combo.current(0)

    def load_doctor_combo(self):

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name FROM doctors ORDER BY name"
        )

        rows = cursor.fetchall()

        conn.close()

        self.doctor_data = rows

        self.doctor_combo["values"] = [
            f"{row[0]} - {row[1]}"
            for row in rows
        ]

        if rows:
            self.doctor_combo.current(0)

    def book_appointment(self):

        if not self.patient_combo.get():
            messagebox.showwarning(
                "Missing",
                "Please add/select a patient."
            )
            return

        if not self.doctor_combo.get():
            messagebox.showwarning(
                "Missing",
                "Please add/select a doctor."
            )
            return

        patient_id = int(
            self.patient_combo.get().split(" - ")[0]
        )

        doctor_id = int(
            self.doctor_combo.get().split(" - ")[0]
        )

        date = self.app_date.get().strip()
        time = self.app_time.get().strip()
        reason = self.app_reason.get().strip()

        if not date or not time:
            messagebox.showwarning(
                "Missing",
                "Date and time are required."
            )
            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id
            FROM appointments
            WHERE doctor_id=?
            AND date=?
            AND time=?
            AND status='Scheduled'
        """, (
            doctor_id,
            date,
            time
        ))

        if cursor.fetchone():
            conn.close()

            messagebox.showerror(
                "Unavailable",
                "Doctor already has an appointment at this time."
            )

            return

        cursor.execute("""
            INSERT INTO appointments
            (patient_id, doctor_id, date, time, reason, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            doctor_id,
            date,
            time,
            reason,
            "Scheduled"
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Appointment booked successfully."
        )

        self.appointment_page()

    def load_appointments(self):

        for item in self.appointment_tree.get_children():
            self.appointment_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                a.id,
                p.name,
                d.name,
                a.date,
                a.time,
                a.reason,
                a.status
            FROM appointments a
            LEFT JOIN patients p
                ON a.patient_id = p.id
            LEFT JOIN doctors d
                ON a.doctor_id = d.id
            ORDER BY a.date DESC, a.time DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:
            self.appointment_tree.insert(
                "",
                "end",
                values=row
            )

    def cancel_appointment(self):

        selected = self.appointment_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select",
                "Select an appointment first."
            )
            return

        values = self.appointment_tree.item(
            selected[0]
        )["values"]

        appointment_id = values[0]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE appointments
            SET status='Cancelled'
            WHERE id=?
        """, (appointment_id,))

        conn.commit()
        conn.close()

        self.load_appointments()

    # ========================================================
    # BILLING
    # ========================================================

    def billing_page(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Billing Management",
            font=("Arial", 22, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=25, pady=15)

        form = tk.LabelFrame(
            self.main_frame,
            text="Create Bill",
            bg="#f5f7fa",
            font=("Arial", 12, "bold")
        )

        form.pack(fill="x", padx=25)

        tk.Label(
            form,
            text="Patient",
            bg="#f5f7fa"
        ).grid(row=0, column=0, padx=10, pady=10)

        self.bill_patient = ttk.Combobox(
            form,
            width=30,
            state="readonly"
        )

        self.bill_patient.grid(
            row=0,
            column=1,
            padx=10
        )

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name FROM patients ORDER BY name"
        )

        patients = cursor.fetchall()

        conn.close()

        self.bill_patient["values"] = [
            f"{p[0]} - {p[1]}"
            for p in patients
        ]

        if patients:
            self.bill_patient.current(0)

        fields = [
            ("Consultation", "consultation"),
            ("Medicine", "medicine"),
            ("Room", "room"),
            ("Tests", "tests")
        ]

        self.bill_entries = {}

        for i, (label, key) in enumerate(fields):

            tk.Label(
                form,
                text=label,
                bg="#f5f7fa"
            ).grid(
                row=1,
                column=i * 2,
                padx=5,
                pady=10
            )

            entry = tk.Entry(
                form,
                width=12
            )

            entry.insert(0, "0")

            entry.grid(
                row=1,
                column=i * 2 + 1
            )

            self.bill_entries[key] = entry

        tk.Button(
            form,
            text="Generate Bill",
            bg="#9c27b0",
            fg="white",
            command=self.generate_bill
        ).grid(
            row=2,
            column=0,
            columnspan=8,
            pady=15
        )

        # Bills table

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        columns = (
            "ID",
            "Patient",
            "Consultation",
            "Medicine",
            "Room",
            "Tests",
            "Total",
            "Date",
            "Status"
        )

        self.bill_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.bill_tree.heading(
                col,
                text=col
            )

        self.bill_tree.pack(
            fill="both",
            expand=True
        )

        self.load_bills()

    def generate_bill(self):

        if not self.bill_patient.get():
            messagebox.showwarning(
                "Missing",
                "Select a patient."
            )
            return

        try:

            consultation = float(
                self.bill_entries["consultation"].get()
            )

            medicine = float(
                self.bill_entries["medicine"].get()
            )

            room = float(
                self.bill_entries["room"].get()
            )

            tests = float(
                self.bill_entries["tests"].get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid",
                "Enter valid amounts."
            )

            return

        total = (
            consultation +
            medicine +
            room +
            tests
        )

        patient_id = int(
            self.bill_patient.get().split(" - ")[0]
        )

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO bills
            (patient_id, consultation, medicine,
             room, tests, total, date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            patient_id,
            consultation,
            medicine,
            room,
            tests,
            total,
            datetime.now().strftime("%Y-%m-%d"),
            "Unpaid"
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Bill Generated",
            f"Total Bill: ₹{total:.2f}"
        )

        self.billing_page()

    def load_bills(self):

        for item in self.bill_tree.get_children():
            self.bill_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                b.id,
                p.name,
                b.consultation,
                b.medicine,
                b.room,
                b.tests,
                b.total,
                b.date,
                b.status
            FROM bills b
            LEFT JOIN patients p
                ON b.patient_id = p.id
            ORDER BY b.id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:
            self.bill_tree.insert(
                "",
                "end",
                values=row
            )

    # ========================================================
    # MEDICINE PAGE
    # ========================================================

    def medicine_page(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Medicine Management",
            font=("Arial", 22, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=25, pady=15)

        form = tk.LabelFrame(
            self.main_frame,
            text="Add Medicine",
            bg="#f5f7fa",
            font=("Arial", 12, "bold")
        )

        form.pack(fill="x", padx=25)

        fields = [
            "Name",
            "Category",
            "Quantity",
            "Price",
            "Expiry"
        ]

        self.medicine_entries = {}

        for i, field in enumerate(fields):

            tk.Label(
                form,
                text=field,
                bg="#f5f7fa"
            ).grid(
                row=0,
                column=i * 2,
                padx=5,
                pady=10
            )

            entry = tk.Entry(
                form,
                width=15
            )

            entry.grid(
                row=0,
                column=i * 2 + 1
            )

            self.medicine_entries[field] = entry

        tk.Button(
            form,
            text="Add Medicine",
            bg="#00897b",
            fg="white",
            command=self.add_medicine
        ).grid(
            row=1,
            column=0,
            columnspan=10,
            pady=10
        )

        table_frame = tk.Frame(self.main_frame)
        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        columns = (
            "ID",
            "Name",
            "Category",
            "Quantity",
            "Price",
            "Expiry"
        )

        self.medicine_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.medicine_tree.heading(
                col,
                text=col
            )

        self.medicine_tree.pack(
            fill="both",
            expand=True
        )

        tk.Button(
            self.main_frame,
            text="Delete Selected Medicine",
            bg="#d32f2f",
            fg="white",
            command=self.delete_medicine
        ).pack(pady=(0, 15))

        self.load_medicines()

    def add_medicine(self):

        data = {
            key: entry.get().strip()
            for key, entry in self.medicine_entries.items()
        }

        if not data["Name"]:
            messagebox.showwarning(
                "Missing",
                "Medicine name is required."
            )
            return

        try:

            quantity = int(
                data["Quantity"] or 0
            )

            price = float(
                data["Price"] or 0
            )

        except ValueError:

            messagebox.showerror(
                "Invalid",
                "Quantity must be integer and price must be numeric."
            )

            return

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO medicines
            (name, category, quantity, price, expiry)
            VALUES (?, ?, ?, ?, ?)
        """, (
            data["Name"],
            data["Category"],
            quantity,
            price,
            data["Expiry"]
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Success",
            "Medicine added successfully."
        )

        self.medicine_page()

    def load_medicines(self):

        for item in self.medicine_tree.get_children():
            self.medicine_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                category,
                quantity,
                price,
                expiry
            FROM medicines
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        conn.close()

        for row in rows:
            self.medicine_tree.insert(
                "",
                "end",
                values=row
            )

    def delete_medicine(self):

        selected = self.medicine_tree.selection()

        if not selected:
            messagebox.showwarning(
                "Select",
                "Select medicine first."
            )
            return

        values = self.medicine_tree.item(
            selected[0]
        )["values"]

        medicine_id = values[0]

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM medicines WHERE id=?",
            (medicine_id,)
        )

        conn.commit()
        conn.close()

        self.load_medicines()

    # ========================================================
    # SEARCH PAGE
    # ========================================================

    def search_page(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.main_frame,
            text="Patient Search",
            font=("Arial", 22, "bold"),
            bg="#f5f7fa"
        ).pack(anchor="w", padx=25, pady=20)

        search_frame = tk.Frame(
            self.main_frame,
            bg="#f5f7fa"
        )

        search_frame.pack(
            fill="x",
            padx=25
        )

        tk.Label(
            search_frame,
            text="Search:",
            bg="#f5f7fa",
            font=("Arial", 12)
        ).pack(side="left")

        self.search_entry = tk.Entry(
            search_frame,
            width=40,
            font=("Arial", 12)
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        tk.Button(
            search_frame,
            text="Search",
            bg="#2196f3",
            fg="white",
            command=self.search_patients
        ).pack(side="left")

        columns = (
            "ID",
            "Name",
            "Age",
            "Gender",
            "Phone",
            "Address",
            "Blood",
            "Disease"
        )

        self.search_tree = ttk.Treeview(
            self.main_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.search_tree.heading(
                col,
                text=col
            )
            self.search_tree.column(
                col,
                width=120
            )

        self.search_tree.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=20
        )

        self.search_entry.bind(
            "<Return>",
            lambda event: self.search_patients()
        )

        self.search_patients()

    def search_patients(self):

        search = self.search_entry.get().strip()

        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                age,
                gender,
                phone,
                address,
                blood_group,
                disease
            FROM patients
            WHERE name LIKE ?
               OR phone LIKE ?
               OR disease LIKE ?
               OR blood_group LIKE ?
            ORDER BY id DESC
        """, (
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%",
            "%" + search + "%"
        ))

        rows = cursor.fetchall()

        conn.close()

        for row in rows:
            self.search_tree.insert(
                "",
                "end",
                values=row
            )


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":

    initialize_database()

    root = tk.Tk()

    app = HospitalApp(root)

    root.mainloop()
