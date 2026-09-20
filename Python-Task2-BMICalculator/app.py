import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt

from database import (
    initialize_database,
    save_bmi_record,
    get_user_records
)


# ==========================================================
# BMI LOGIC
# ==========================================================

def calculate_bmi(height, weight):
    height_m = height / 100
    return round(weight / (height_m * height_m), 2)


def get_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    return "Obese"


def get_message(category):

    messages = {
        "Underweight":
            "Your BMI is below the standard range. Focus on balanced nutrition and healthy habits.",

        "Normal":
            "Your BMI is within the standard healthy range. Keep maintaining your healthy lifestyle!",

        "Overweight":
            "Your BMI is above the standard range. Regular activity and balanced nutrition may help.",

        "Obese":
            "Your BMI is in the obesity range. Consider discussing your health goals with a professional."
    }

    return messages[category]


# ==========================================================
# MAIN APPLICATION
# ==========================================================

class BMIApp:

    def __init__(self, root):

        self.root = root

        self.root.title("BMI Health Pulse")
        self.root.geometry("1180x760")
        self.root.minsize(1050, 700)

        self.bg = "#F5F7FB"
        self.sidebar = "#111827"
        self.sidebar_hover = "#1F2937"
        self.primary = "#14B8A6"
        self.primary_dark = "#0F766E"
        self.text = "#172033"
        self.muted = "#718096"
        self.card = "#FFFFFF"
        self.border = "#E5E7EB"

        self.current_bmi = None
        self.current_category = None

        self.root.configure(bg=self.bg)

        initialize_database()

        self.setup_styles()
        self.create_layout()

    # ======================================================
    # STYLES
    # ======================================================

    def setup_styles(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Modern.TEntry",
            font=("Segoe UI", 11),
            padding=10,
            fieldbackground="#F8FAFC",
            borderwidth=0
        )

        style.configure(
            "Modern.TCombobox",
            font=("Segoe UI", 11),
            padding=9
        )

        style.configure(
            "Treeview",
            background="white",
            foreground=self.text,
            rowheight=36,
            fieldbackground="white",
            font=("Segoe UI", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#F1F5F9",
            foreground=self.text,
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", "#CCFBF1")],
            foreground=[("selected", self.text)]
        )

    # ======================================================
    # MAIN LAYOUT
    # ======================================================

    def create_layout(self):

        self.create_sidebar()

        self.content = tk.Frame(
            self.root,
            bg=self.bg
        )

        self.content.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.create_topbar()

        self.create_dashboard()

    # ======================================================
    # SIDEBAR
    # ======================================================

    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            bg=self.sidebar,
            width=235
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        # Logo
        logo_frame = tk.Frame(
            sidebar,
            bg=self.sidebar
        )

        logo_frame.pack(
            fill="x",
            padx=22,
            pady=(28, 35)
        )

        logo_icon = tk.Label(
            logo_frame,
            text="◉",
            font=("Segoe UI", 24, "bold"),
            bg=self.sidebar,
            fg=self.primary
        )

        logo_icon.pack(side="left")

        logo = tk.Label(
            logo_frame,
            text="BMI\nPULSE",
            font=("Segoe UI", 15, "bold"),
            justify="left",
            bg=self.sidebar,
            fg="white"
        )

        logo.pack(
            side="left",
            padx=10
        )

        # Menu
        self.sidebar_button(
            sidebar,
            "⌂   Dashboard",
            self.show_dashboard,
            True
        )

        self.sidebar_button(
            sidebar,
            "⚖   BMI Calculator",
            self.focus_calculator
        )

        self.sidebar_button(
            sidebar,
            "▥   BMI History",
            self.show_history
        )

        self.sidebar_button(
            sidebar,
            "⌁   BMI Analytics",
            self.show_graph
        )

        # Bottom information
        bottom = tk.Frame(
            sidebar,
            bg="#172033"
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=18
        )

        tk.Label(
            bottom,
            text="HEALTH TRACKER",
            font=("Segoe UI", 8, "bold"),
            bg="#172033",
            fg=self.primary
        ).pack(
            anchor="w",
            padx=12,
            pady=(12, 3)
        )

        tk.Label(
            bottom,
            text="Your health data is stored\nlocally using SQLite.",
            font=("Segoe UI", 8),
            justify="left",
            bg="#172033",
            fg="#CBD5E1"
        ).pack(
            anchor="w",
            padx=12,
            pady=(0, 12)
        )

    def sidebar_button(
        self,
        parent,
        text,
        command,
        active=False
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            bg="#193A3A" if active else self.sidebar,
            fg=self.primary if active else "#CBD5E1",
            activebackground=self.sidebar_hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            padx=25
        )

        button.pack(
            fill="x",
            pady=3,
            ipady=12
        )

    # ======================================================
    # TOP BAR
    # ======================================================

    def create_topbar(self):

        topbar = tk.Frame(
            self.content,
            bg="white",
            height=75
        )

        topbar.pack(
            fill="x"
        )

        topbar.pack_propagate(False)

        tk.Label(
            topbar,
            text="Health Dashboard",
            font=("Segoe UI", 17, "bold"),
            bg="white",
            fg=self.text
        ).pack(
            side="left",
            padx=30
        )

        status = tk.Frame(
            topbar,
            bg="#ECFDF5"
        )

        status.pack(
            side="right",
            padx=30
        )

        tk.Label(
            status,
            text="●",
            font=("Segoe UI", 10),
            bg="#ECFDF5",
            fg="#10B981"
        ).pack(
            side="left",
            padx=(10, 4),
            pady=8
        )

        tk.Label(
            status,
            text="SYSTEM READY",
            font=("Segoe UI", 8, "bold"),
            bg="#ECFDF5",
            fg="#047857"
        ).pack(
            side="left",
            padx=(0, 10)
        )

    # ======================================================
    # DASHBOARD
    # ======================================================

    def create_dashboard(self):

        self.dashboard = tk.Frame(
            self.content,
            bg=self.bg
        )

        self.dashboard.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        # Welcome
        welcome = tk.Frame(
            self.dashboard,
            bg=self.bg
        )

        welcome.pack(
            fill="x"
        )

        tk.Label(
            welcome,
            text="Welcome to BMI Pulse 👋",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(
            anchor="w"
        )

        tk.Label(
            welcome,
            text="Calculate your BMI and keep track of your health journey.",
            font=("Segoe UI", 10),
            bg=self.bg,
            fg=self.muted
        ).pack(
            anchor="w",
            pady=(3, 20)
        )

        # Statistic cards
        stats = tk.Frame(
            self.dashboard,
            bg=self.bg
        )

        stats.pack(
            fill="x"
        )

        self.bmi_stat = self.create_stat_card(
            stats,
            "CURRENT BMI",
            "--",
            "Your latest result"
        )

        self.status_stat = self.create_stat_card(
            stats,
            "BMI STATUS",
            "--",
            "Health category"
        )

        self.records_stat = self.create_stat_card(
            stats,
            "TOTAL RECORDS",
            "0",
            "Saved measurements"
        )

        self.create_stat_card(
            stats,
            "TRACKING",
            "ACTIVE",
            "Local SQLite storage"
        )

        # Main area
        lower = tk.Frame(
            self.dashboard,
            bg=self.bg
        )

        lower.pack(
            fill="both",
            expand=True,
            pady=(20, 0)
        )

        self.create_calculator_card(lower)

        self.create_result_card(lower)

        self.update_statistics()

    # ======================================================
    # STAT CARD
    # ======================================================

    def create_stat_card(
        self,
        parent,
        title,
        value,
        subtitle
    ):

        card = tk.Frame(
            parent,
            bg=self.card,
            bd=1,
            relief="solid",
            highlightbackground=self.border
        )

        card.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 12)
        )

        tk.Label(
            card,
            text=title,
            font=("Segoe UI", 8, "bold"),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 2)
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Segoe UI", 20, "bold"),
            bg=self.card,
            fg=self.text
        )

        value_label.pack(
            anchor="w",
            padx=18
        )

        tk.Label(
            card,
            text=subtitle,
            font=("Segoe UI", 8),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 14)
        )

        return value_label

    # ======================================================
    # CALCULATOR CARD
    # ======================================================

    def create_calculator_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.card,
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )

        tk.Label(
            card,
            text="Calculate Your BMI",
            font=("Segoe UI", 16, "bold"),
            bg=self.card,
            fg=self.text
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 2)
        )

        tk.Label(
            card,
            text="Enter your information below",
            font=("Segoe UI", 9),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=22,
            pady=(0, 18)
        )

        form = tk.Frame(
            card,
            bg=self.card
        )

        form.pack(
            fill="x",
            padx=22
        )

        # Name
        self.name_entry = self.form_field(
            form,
            "FULL NAME",
            0,
            0
        )

        # Age
        self.age_entry = self.form_field(
            form,
            "AGE",
            0,
            1
        )

        # Gender
        tk.Label(
            form,
            text="GENDER",
            font=("Segoe UI", 8, "bold"),
            bg=self.card,
            fg=self.muted
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(13, 5)
        )

        self.gender_combo = ttk.Combobox(
            form,
            values=["Female", "Male", "Other"],
            state="readonly",
            style="Modern.TCombobox"
        )

        self.gender_combo.current(0)

        self.gender_combo.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=(0, 7)
        )

        # Height
        self.height_entry = self.form_field(
            form,
            "HEIGHT (CM)",
            2,
            1
        )

        # Weight
        self.weight_entry = self.form_field(
            form,
            "WEIGHT (KG)",
            4,
            0
        )

        form.grid_columnconfigure(
            0,
            weight=1
        )

        form.grid_columnconfigure(
            1,
            weight=1
        )

        # Button
        calculate = tk.Button(
            card,
            text="CALCULATE BMI   →",
            command=self.calculate,
            font=("Segoe UI", 10, "bold"),
            bg=self.primary,
            fg="white",
            activebackground=self.primary_dark,
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            bd=0
        )

        calculate.pack(
            fill="x",
            padx=22,
            pady=(25, 20),
            ipady=11
        )

    # ======================================================
    # FORM FIELD
    # ======================================================

    def form_field(
        self,
        parent,
        label,
        row,
        column
    ):

        tk.Label(
            parent,
            text=label,
            font=("Segoe UI", 8, "bold"),
            bg=self.card,
            fg=self.muted
        ).grid(
            row=row,
            column=column,
            sticky="w",
            pady=(0, 5),
            padx=(0, 7)
        )

        entry = ttk.Entry(
            parent,
            style="Modern.TEntry"
        )

        entry.grid(
            row=row + 1,
            column=column,
            sticky="ew",
            padx=(0, 7)
        )

        return entry

    # ======================================================
    # RESULT CARD
    # ======================================================

    def create_result_card(self, parent):

        card = tk.Frame(
            parent,
            bg=self.card,
            bd=1,
            relief="solid"
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0)
        )

        tk.Label(
            card,
            text="Your Result",
            font=("Segoe UI", 16, "bold"),
            bg=self.card,
            fg=self.text
        ).pack(
            anchor="w",
            padx=22,
            pady=(20, 3)
        )

        tk.Label(
            card,
            text="Your latest BMI measurement",
            font=("Segoe UI", 9),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=22
        )

        self.result_bmi = tk.Label(
            card,
            text="--",
            font=("Segoe UI", 48, "bold"),
            bg=self.card,
            fg=self.primary
        )

        self.result_bmi.pack(
            pady=(18, 0)
        )

        self.result_status = tk.Label(
            card,
            text="WAITING FOR DATA",
            font=("Segoe UI", 11, "bold"),
            bg="#F1F5F9",
            fg=self.muted,
            padx=15,
            pady=7
        )

        self.result_status.pack()

        self.result_message = tk.Label(
            card,
            text="Calculate your BMI to see your health status.",
            font=("Segoe UI", 9),
            wraplength=330,
            justify="center",
            bg=self.card,
            fg=self.muted
        )

        self.result_message.pack(
            pady=14,
            padx=20
        )

        # BMI scale
        tk.Label(
            card,
            text="BMI RANGE",
            font=("Segoe UI", 8, "bold"),
            bg=self.card,
            fg=self.muted
        ).pack(
            pady=(5, 5)
        )

        scale = tk.Canvas(
            card,
            height=14,
            bg=self.card,
            highlightthickness=0
        )

        scale.pack(
            fill="x",
            padx=25
        )

        scale.create_rectangle(
            0, 2, 70, 12,
            fill="#60A5FA",
            outline=""
        )

        scale.create_rectangle(
            70, 2, 190, 12,
            fill="#34D399",
            outline=""
        )

        scale.create_rectangle(
            190, 2, 270, 12,
            fill="#FBBF24",
            outline=""
        )

        scale.create_rectangle(
            270, 2, 350, 12,
            fill="#F87171",
            outline=""
        )

        labels = tk.Frame(
            card,
            bg=self.card
        )

        labels.pack(
            fill="x",
            padx=20,
            pady=(2, 15)
        )

        for text in [
            "Underweight",
            "Normal",
            "Overweight",
            "Obese"
        ]:

            tk.Label(
                labels,
                text=text,
                font=("Segoe UI", 7),
                bg=self.card,
                fg=self.muted
            ).pack(
                side="left",
                expand=True
            )

        # Buttons
        buttons = tk.Frame(
            card,
            bg=self.card
        )

        buttons.pack(
            fill="x",
            padx=22,
            pady=(3, 15)
        )

        tk.Button(
            buttons,
            text="VIEW HISTORY",
            command=self.show_history,
            font=("Segoe UI", 9, "bold"),
            bg="#F1F5F9",
            fg=self.text,
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5),
            ipady=8
        )

        tk.Button(
            buttons,
            text="VIEW TREND",
            command=self.show_graph,
            font=("Segoe UI", 9, "bold"),
            bg="#CCFBF1",
            fg=self.primary_dark,
            relief="flat",
            cursor="hand2"
        ).pack(
            side="left",
            fill="x",
            expand=True,
            padx=(5, 0),
            ipady=8
        )

    # ======================================================
    # CALCULATE
    # ======================================================

    def calculate(self):

        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        gender = self.gender_combo.get()
        height = self.height_entry.get().strip()
        weight = self.weight_entry.get().strip()

        if not name or not age or not height or not weight:

            messagebox.showwarning(
                "Missing Information",
                "Please complete all the required fields."
            )

            return

        try:

            age = int(age)
            height = float(height)
            weight = float(weight)

            if age <= 0 or age > 120:
                raise ValueError

            if height < 50 or height > 250:
                raise ValueError

            if weight < 2 or weight > 300:
                raise ValueError

        except ValueError:

            messagebox.showerror(
                "Invalid Information",
                "Please enter valid values.\n\n"
                "Age: 1–120\n"
                "Height: 50–250 cm\n"
                "Weight: 2–300 kg"
            )

            return

        bmi = calculate_bmi(
            height,
            weight
        )

        category = get_category(bmi)

        self.current_bmi = bmi
        self.current_category = category

        # Result
        self.result_bmi.config(
            text=str(bmi)
        )

        self.result_status.config(
            text=category.upper()
        )

        self.result_message.config(
            text=get_message(category)
        )

        # Statistics
        self.bmi_stat.config(
            text=str(bmi)
        )

        self.status_stat.config(
            text=category
        )

        # Save
        saved = save_bmi_record(
            name,
            age,
            gender,
            height,
            weight,
            bmi,
            category
        )

        if saved:

            self.update_statistics()

            messagebox.showinfo(
                "BMI Saved",
                f"BMI: {bmi}\n"
                f"Status: {category}\n\n"
                f"Your result has been saved successfully."
            )

        else:

            messagebox.showerror(
                "Database Error",
                "The BMI was calculated but could not be saved."
            )

    # ======================================================
    # STATISTICS
    # ======================================================

    def update_statistics(self):

        name = self.name_entry.get().strip()

        if name:

            records = get_user_records(name)

            self.records_stat.config(
                text=str(len(records))
            )

    # ======================================================
    # HISTORY
    # ======================================================

    def show_history(self):

        name = self.name_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Name Required",
                "Enter your name first to view your history."
            )

            return

        records = get_user_records(name)

        if not records:

            messagebox.showinfo(
                "No History",
                "No BMI records found for this user."
            )

            return

        window = tk.Toplevel(self.root)

        window.title("BMI History")
        window.geometry("900x500")
        window.configure(bg=self.bg)

        tk.Label(
            window,
            text=f"Health History — {name}",
            font=("Segoe UI", 20, "bold"),
            bg=self.bg,
            fg=self.text
        ).pack(
            anchor="w",
            padx=30,
            pady=(25, 5)
        )

        tk.Label(
            window,
            text="Your saved BMI measurements",
            font=("Segoe UI", 9),
            bg=self.bg,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=30,
            pady=(0, 20)
        )

        frame = tk.Frame(
            window,
            bg="white"
        )

        frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        columns = (
            "date",
            "age",
            "gender",
            "height",
            "weight",
            "bmi",
            "category"
        )

        table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "date": "Date",
            "age": "Age",
            "gender": "Gender",
            "height": "Height",
            "weight": "Weight",
            "bmi": "BMI",
            "category": "Status"
        }

        for column in columns:

            table.heading(
                column,
                text=headings[column]
            )

            table.column(
                column,
                anchor="center",
                width=110
            )

        table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        for record in records:

            table.insert(
                "",
                "end",
                values=(
                    record["recorded_at"],
                    record["age"],
                    record["gender"],
                    f"{record['height']} cm",
                    f"{record['weight']} kg",
                    record["bmi"],
                    record["category"]
                )
            )

    # ======================================================
    # GRAPH
    # ======================================================

    def show_graph(self):

        name = self.name_entry.get().strip()

        if not name:

            messagebox.showwarning(
                "Name Required",
                "Enter your name first."
            )

            return

        records = get_user_records(name)

        if len(records) < 2:

            messagebox.showinfo(
                "Not Enough Data",
                "Complete at least two BMI calculations "
                "to generate your trend."
            )

            return

        records = list(reversed(records))

        dates = [
            record["recorded_at"]
            for record in records
        ]

        bmi_values = [
            record["bmi"]
            for record in records
        ]

        plt.figure(
            figsize=(10, 5)
        )

        plt.plot(
            dates,
            bmi_values,
            marker="o",
            linewidth=2
        )

        plt.axhline(
            18.5,
            linestyle="--",
            alpha=0.5
        )

        plt.axhline(
            25,
            linestyle="--",
            alpha=0.5
        )

        plt.title(
            f"BMI Progress — {name}",
            fontsize=16,
            fontweight="bold"
        )

        plt.xlabel(
            "Measurement Date"
        )

        plt.ylabel(
            "BMI"
        )

        plt.xticks(
            rotation=35,
            ha="right"
        )

        plt.grid(
            alpha=0.25
        )

        plt.tight_layout()

        plt.show()

    # ======================================================
    # NAVIGATION
    # ======================================================

    def show_dashboard(self):
        pass

    def focus_calculator(self):

        self.name_entry.focus()

    # ======================================================
    # RUN
    # ======================================================


if __name__ == "__main__":

    root = tk.Tk()

    application = BMIApp(root)

    root.mainloop()