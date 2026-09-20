import tkinter as tk
from tkinter import ttk, messagebox
import secrets
import string
import pyperclip
from datetime import datetime


# ============================================================
# SECUREVAULT - ADVANCED PASSWORD GENERATOR
# ============================================================

class SecureVault:
    def __init__(self, root):

        self.root = root

        # ----------------------------------------------------
        # WINDOW
        # ----------------------------------------------------

        self.root.title("SecureVault | Advanced Password Security")
        self.root.geometry("1100x720")
        self.root.minsize(950, 650)
        self.root.configure(bg="#080D1C")

        self.history = []

        # ----------------------------------------------------
        # VARIABLES
        # ----------------------------------------------------

        self.length_var = tk.IntVar(value=16)

        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.ambiguous_var = tk.BooleanVar(value=True)

        self.password_var = tk.StringVar(
            value="Generate a secure password"
        )

        self.show_password_var = tk.BooleanVar(value=True)

        # ----------------------------------------------------
        # COLORS
        # ----------------------------------------------------

        self.bg = "#080D1C"
        self.sidebar = "#0D1428"
        self.card = "#111A32"
        self.card2 = "#151F3A"

        self.border = "#243253"

        self.white = "#F4F7FF"
        self.text = "#C8D2E8"
        self.muted = "#71809E"

        self.blue = "#4F7CFF"
        self.blue_dark = "#355DDB"

        self.green = "#39D98A"
        self.yellow = "#FFC857"
        self.red = "#FF5C70"

        # ----------------------------------------------------
        # STYLE
        # ----------------------------------------------------

        self.setup_styles()

        # ----------------------------------------------------
        # CREATE UI
        # ----------------------------------------------------

        self.create_header()
        self.create_main_area()

    # ========================================================
    # STYLES
    # ========================================================

    def setup_styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Modern.Horizontal.TScale",
            background=self.card
        )

    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.root,
            bg=self.sidebar,
            height=92
        )

        header.pack(fill="x")
        header.pack_propagate(False)

        # Logo
        logo = tk.Label(
            header,
            text="🔐",
            font=("Segoe UI Emoji", 28),
            bg=self.sidebar,
            fg=self.white
        )

        logo.pack(
            side="left",
            padx=(30, 12)
        )

        # Title area
        title_area = tk.Frame(
            header,
            bg=self.sidebar
        )

        title_area.pack(
            side="left",
            pady=14
        )

        tk.Label(
            title_area,
            text="SECUREVAULT",
            font=("Segoe UI", 22, "bold"),
            bg=self.sidebar,
            fg=self.white
        ).pack(anchor="w")

        tk.Label(
            title_area,
            text="Advanced Password Security Suite",
            font=("Segoe UI", 10),
            bg=self.sidebar,
            fg=self.muted
        ).pack(anchor="w")

        # Security badge
        badge = tk.Label(
            header,
            text="●  SECURE GENERATOR",
            font=("Segoe UI", 9, "bold"),
            bg="#102C25",
            fg=self.green,
            padx=15,
            pady=8
        )

        badge.pack(
            side="right",
            padx=30
        )

    # ========================================================
    # MAIN AREA
    # ========================================================

    def create_main_area(self):

        container = tk.Frame(
            self.root,
            bg=self.bg
        )

        container.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=25
        )

        # ====================================================
        # LEFT PANEL
        # ====================================================

        left = tk.Frame(
            container,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=1
        )

        left.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 12)
        )

        # ====================================================
        # RIGHT PANEL
        # ====================================================

        right = tk.Frame(
            container,
            bg=self.card,
            highlightbackground=self.border,
            highlightthickness=1
        )

        right.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(12, 0)
        )

        self.create_settings_panel(left)
        self.create_password_panel(right)

    # ========================================================
    # SETTINGS PANEL
    # ========================================================

    def create_settings_panel(self, parent):

        # Heading
        tk.Label(
            parent,
            text="Password Configuration",
            font=("Segoe UI", 18, "bold"),
            bg=self.card,
            fg=self.white
        ).pack(
            anchor="w",
            padx=28,
            pady=(26, 3)
        )

        tk.Label(
            parent,
            text="Customize your security requirements",
            font=("Segoe UI", 10),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=28,
            pady=(0, 24)
        )

        # ----------------------------------------------------
        # LENGTH
        # ----------------------------------------------------

        length_header = tk.Frame(
            parent,
            bg=self.card
        )

        length_header.pack(
            fill="x",
            padx=28
        )

        tk.Label(
            length_header,
            text="PASSWORD LENGTH",
            font=("Segoe UI", 9, "bold"),
            bg=self.card,
            fg=self.muted
        ).pack(side="left")

        self.length_value = tk.Label(
            length_header,
            text="16",
            font=("Segoe UI", 14, "bold"),
            bg=self.card,
            fg=self.blue
        )

        self.length_value.pack(side="right")

        self.length_scale = tk.Scale(
            parent,
            from_=8,
            to=40,
            orient="horizontal",
            variable=self.length_var,
            command=self.update_length,
            bg=self.card,
            fg=self.white,
            troughcolor="#263352",
            activebackground=self.blue,
            highlightthickness=0,
            bd=0,
            showvalue=False
        )

        self.length_scale.pack(
            fill="x",
            padx=24,
            pady=(5, 5)
        )

        tk.Label(
            parent,
            text="8 characters                         40 characters",
            font=("Segoe UI", 8),
            bg=self.card,
            fg=self.muted
        ).pack(
            fill="x",
            padx=28
        )

        self.separator(parent)

        # ----------------------------------------------------
        # CHARACTER TYPES
        # ----------------------------------------------------

        tk.Label(
            parent,
            text="CHARACTER TYPES",
            font=("Segoe UI", 9, "bold"),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=28,
            pady=(5, 12)
        )

        self.create_option(
            parent,
            "Uppercase letters",
            "A-Z",
            self.upper_var
        )

        self.create_option(
            parent,
            "Lowercase letters",
            "a-z",
            self.lower_var
        )

        self.create_option(
            parent,
            "Numbers",
            "0-9",
            self.number_var
        )

        self.create_option(
            parent,
            "Symbols",
            "!@#$",
            self.symbol_var
        )

        self.create_option(
            parent,
            "Exclude ambiguous characters",
            "Il1O0",
            self.ambiguous_var
        )

        # ----------------------------------------------------
        # GENERATE BUTTON
        # ----------------------------------------------------

        generate = tk.Button(
            parent,
            text="⚡   GENERATE SECURE PASSWORD",
            command=self.generate_password,
            font=("Segoe UI", 11, "bold"),
            bg=self.blue,
            fg="white",
            activebackground=self.blue_dark,
            activeforeground="white",
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=14
        )

        generate.pack(
            fill="x",
            padx=28,
            pady=(25, 10)
        )

        # ----------------------------------------------------
        # RESET BUTTON
        # ----------------------------------------------------

        reset = tk.Button(
            parent,
            text="↻   Reset Configuration",
            command=self.reset_settings,
            font=("Segoe UI", 9),
            bg=self.card2,
            fg=self.text,
            activebackground="#1D2947",
            activeforeground=self.white,
            relief="flat",
            bd=0,
            cursor="hand2",
            pady=9
        )

        reset.pack(
            fill="x",
            padx=28
        )

        # ----------------------------------------------------
        # SECURITY INFO
        # ----------------------------------------------------

        info = tk.Frame(
            parent,
            bg="#0C1428",
            highlightbackground=self.border,
            highlightthickness=1
        )

        info.pack(
            fill="x",
            padx=28,
            pady=22
        )

        tk.Label(
            info,
            text="🛡  SECURITY INFORMATION",
            font=("Segoe UI", 9, "bold"),
            bg="#0C1428",
            fg=self.blue
        ).pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        tk.Label(
            info,
            text="Passwords are generated locally using\n"
                 "Python's cryptographically secure secrets module.",
            font=("Segoe UI", 8),
            justify="left",
            bg="#0C1428",
            fg=self.muted
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 12)
        )

    # ========================================================
    # OPTION
    # ========================================================

    def create_option(
        self,
        parent,
        title,
        description,
        variable
    ):

        frame = tk.Frame(
            parent,
            bg=self.card
        )

        frame.pack(
            fill="x",
            padx=28,
            pady=5
        )

        check = tk.Checkbutton(
            frame,
            variable=variable,
            bg=self.card,
            activebackground=self.card,
            selectcolor="#263352",
            cursor="hand2"
        )

        check.pack(side="left")

        text_frame = tk.Frame(
            frame,
            bg=self.card
        )

        text_frame.pack(
            side="left",
            fill="x"
        )

        tk.Label(
            text_frame,
            text=title,
            font=("Segoe UI", 10, "bold"),
            bg=self.card,
            fg=self.text
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=description,
            font=("Segoe UI", 8),
            bg=self.card,
            fg=self.muted
        ).pack(anchor="w")

    # ========================================================
    # PASSWORD PANEL
    # ========================================================

    def create_password_panel(self, parent):

        tk.Label(
            parent,
            text="Generated Password",
            font=("Segoe UI", 18, "bold"),
            bg=self.card,
            fg=self.white
        ).pack(
            anchor="w",
            padx=28,
            pady=(26, 3)
        )

        tk.Label(
            parent,
            text="Your password is generated securely on your device",
            font=("Segoe UI", 10),
            bg=self.card,
            fg=self.muted
        ).pack(
            anchor="w",
            padx=28
        )

        # ----------------------------------------------------
        # PASSWORD DISPLAY
        # ----------------------------------------------------

        password_card = tk.Frame(
            parent,
            bg="#0C1428",
            highlightbackground=self.blue,
            highlightthickness=1
        )

        password_card.pack(
            fill="x",
            padx=28,
            pady=(25, 10)
        )

        self.password_entry = tk.Entry(
            password_card,
            textvariable=self.password_var,
            font=("Consolas", 16, "bold"),
            bg="#0C1428",
            fg=self.white,
            insertbackground=self.white,
            relief="flat",
            justify="center",
            bd=0
        )

        self.password_entry.pack(
            fill="x",
            padx=18,
            pady=17
        )

        # ----------------------------------------------------
        # BUTTON ROW
        # ----------------------------------------------------

        button_row = tk.Frame(
            parent,
            bg=self.card
        )

        button_row.pack(
            fill="x",
            padx=28,
            pady=5
        )

        copy_button = tk.Button(
            button_row,
            text="📋  Copy",
            command=self.copy_password,
            font=("Segoe UI", 10, "bold"),
            bg=self.blue,
            fg="white",
            activebackground=self.blue_dark,
            relief="flat",
            cursor="hand2",
            pady=10
        )

        copy_button.pack(
            side="left",
            fill="x",
            expand=True,
            padx=(0, 5)
        )

        show_button = tk.Button(
            button_row,
            text="👁  Show / Hide",
            command=self.toggle_password,
            font=("Segoe UI", 10),
            bg=self.card2,
            fg=self.text,
            activebackground="#1D2947",
            relief="flat",
            cursor="hand2",
            pady=10
        )

        show_button.pack(
            side="right",
            fill="x",
            expand=True,
            padx=(5, 0)
        )

        # ----------------------------------------------------
        # STRENGTH
        # ----------------------------------------------------

        strength_frame = tk.Frame(
            parent,
            bg=self.card
        )

        strength_frame.pack(
            fill="x",
            padx=28,
            pady=(22, 5)
        )

        tk.Label(
            strength_frame,
            text="PASSWORD STRENGTH",
            font=("Segoe UI", 9, "bold"),
            bg=self.card,
            fg=self.muted
        ).pack(side="left")

        self.strength_text = tk.Label(
            strength_frame,
            text="Not generated",
            font=("Segoe UI", 10, "bold"),
            bg=self.card,
            fg=self.muted
        )

        self.strength_text.pack(side="right")

        # Strength bar background
        self.strength_bar_bg = tk.Frame(
            parent,
            bg="#263352",
            height=8
        )

        self.strength_bar_bg.pack(
            fill="x",
            padx=28,
            pady=(3, 5)
        )

        self.strength_bar = tk.Frame(
            self.strength_bar_bg,
            bg=self.blue,
            height=8
        )

        self.strength_bar.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=0
        )

        # ----------------------------------------------------
        # HISTORY
        # ----------------------------------------------------

        history_header = tk.Frame(
            parent,
            bg=self.card
        )

        history_header.pack(
            fill="x",
            padx=28,
            pady=(20, 5)
        )

        tk.Label(
            history_header,
            text="RECENT PASSWORDS",
            font=("Segoe UI", 9, "bold"),
            bg=self.card,
            fg=self.muted
        ).pack(side="left")

        clear_button = tk.Button(
            history_header,
            text="Clear",
            command=self.clear_history,
            font=("Segoe UI", 8),
            bg=self.card,
            fg=self.muted,
            activebackground=self.card,
            activeforeground=self.white,
            relief="flat",
            cursor="hand2"
        )

        clear_button.pack(side="right")

        # History box
        history_frame = tk.Frame(
            parent,
            bg="#0C1428",
            highlightbackground=self.border,
            highlightthickness=1
        )

        history_frame.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=(3, 20)
        )

        self.history_list = tk.Listbox(
            history_frame,
            bg="#0C1428",
            fg=self.text,
            selectbackground="#243A73",
            selectforeground=self.white,
            font=("Consolas", 9),
            relief="flat",
            highlightthickness=0,
            bd=0,
            activestyle="none"
        )

        self.history_list.pack(
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        self.history_list.bind(
            "<Double-Button-1>",
            self.copy_selected_history
        )

    # ========================================================
    # SEPARATOR
    # ========================================================

    def separator(self, parent):

        tk.Frame(
            parent,
            bg=self.border,
            height=1
        ).pack(
            fill="x",
            padx=28,
            pady=20
        )

    # ========================================================
    # LENGTH
    # ========================================================

    def update_length(self, value):

        value = int(float(value))

        self.length_value.config(
            text=str(value)
        )

    # ========================================================
    # BUILD CHARACTER POOLS
    # ========================================================

    def build_pools(self):

        ambiguous = "Il1O0|`'\""

        pools = []

        if self.upper_var.get():
            pool = string.ascii_uppercase

            if self.ambiguous_var.get():
                pool = "".join(
                    c for c in pool
                    if c not in ambiguous
                )

            pools.append(pool)

        if self.lower_var.get():
            pool = string.ascii_lowercase

            if self.ambiguous_var.get():
                pool = "".join(
                    c for c in pool
                    if c not in ambiguous
                )

            pools.append(pool)

        if self.number_var.get():
            pool = string.digits

            if self.ambiguous_var.get():
                pool = "".join(
                    c for c in pool
                    if c not in ambiguous
                )

            pools.append(pool)

        if self.symbol_var.get():
            pool = string.punctuation

            if self.ambiguous_var.get():
                pool = "".join(
                    c for c in pool
                    if c not in ambiguous
                )

            pools.append(pool)

        return pools

    # ========================================================
    # GENERATE
    # ========================================================

    def generate_password(self):

        length = self.length_var.get()

        pools = self.build_pools()

        if not pools:

            messagebox.showerror(
                "Invalid Configuration",
                "Please select at least one character type."
            )

            return

        if length < len(pools):

            messagebox.showerror(
                "Password Too Short",
                "Increase the password length so every selected "
                "character type can be included."
            )

            return

        # Combined pool
        combined = "".join(pools)

        # Create one character from every selected type
        password_chars = [
            secrets.choice(pool)
            for pool in pools
        ]

        # Fill remaining positions
        remaining = length - len(password_chars)

        for _ in range(remaining):

            password_chars.append(
                secrets.choice(combined)
            )

        # Secure Fisher-Yates shuffle
        for i in range(
            len(password_chars) - 1,
            0,
            -1
        ):

            j = secrets.randbelow(i + 1)

            password_chars[i], password_chars[j] = (
                password_chars[j],
                password_chars[i]
            )

        password = "".join(password_chars)

        self.password_var.set(password)

        # Add history
        self.add_to_history(password)

        # Update strength
        self.update_strength(password)

    # ========================================================
    # HISTORY
    # ========================================================

    def add_to_history(self, password):

        timestamp = datetime.now().strftime("%H:%M:%S")

        record = f"{timestamp}   {password}"

        self.history.insert(
            0,
            record
        )

        if len(self.history) > 8:
            self.history.pop()

        self.history_list.delete(
            0,
            tk.END
        )

        for item in self.history:

            self.history_list.insert(
                tk.END,
                item
            )

    # ========================================================
    # COPY
    # ========================================================

    def copy_password(self):

        password = self.password_var.get()

        if not password or password == "Generate a secure password":

            messagebox.showwarning(
                "No Password",
                "Generate a password first."
            )

            return

        try:

            pyperclip.copy(password)

            self.show_status(
                "✓ Password copied to clipboard"
            )

        except Exception as error:

            messagebox.showerror(
                "Clipboard Error",
                str(error)
            )

    # ========================================================
    # STATUS MESSAGE
    # ========================================================

    def show_status(self, message):

        status = tk.Toplevel(self.root)

        status.title("SecureVault")

        status.geometry("360x120")

        status.configure(
            bg=self.card
        )

        status.resizable(
            False,
            False
        )

        status.transient(
            self.root
        )

        status.grab_set()

        tk.Label(
            status,
            text="✓",
            font=("Segoe UI", 25, "bold"),
            bg=self.card,
            fg=self.green
        ).pack(
            pady=(10, 0)
        )

        tk.Label(
            status,
            text=message,
            font=("Segoe UI", 10, "bold"),
            bg=self.card,
            fg=self.white
        ).pack()

        status.after(
            1300,
            status.destroy
        )

    # ========================================================
    # TOGGLE PASSWORD
    # ========================================================

    def toggle_password(self):

        if self.password_entry.cget("show") == "":

            self.password_entry.config(
                show="•"
            )

        else:

            self.password_entry.config(
                show=""
            )

    # ========================================================
    # STRENGTH
    # ========================================================

    def update_strength(self, password):

        score = 0

        # Length
        if len(password) >= 12:
            score += 1

        if len(password) >= 18:
            score += 1

        if len(password) >= 24:
            score += 1

        # Character diversity
        if any(c.isupper() for c in password):
            score += 1

        if any(c.islower() for c in password):
            score += 1

        if any(c.isdigit() for c in password):
            score += 1

        if any(c in string.punctuation for c in password):
            score += 1

        if score <= 3:

            text = "WEAK"
            width = 0.30
            color = self.red

        elif score <= 5:

            text = "MEDIUM"
            width = 0.60
            color = self.yellow

        else:

            text = "STRONG"
            width = 1.0
            color = self.green

        self.strength_text.config(
            text=f"{text}  •  {len(password)} characters",
            fg=color
        )

        self.strength_bar.config(
            bg=color
        )

        self.strength_bar.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=width
        )

    # ========================================================
    # COPY HISTORY
    # ========================================================

    def copy_selected_history(self, event=None):

        selection = self.history_list.curselection()

        if not selection:
            return

        item = self.history_list.get(
            selection[0]
        )

        # Remove timestamp
        parts = item.split(
            "   ",
            1
        )

        if len(parts) == 2:

            password = parts[1]

            pyperclip.copy(password)

            self.show_status(
                "✓ Selected password copied"
            )

    # ========================================================
    # CLEAR HISTORY
    # ========================================================

    def clear_history(self):

        self.history.clear()

        self.history_list.delete(
            0,
            tk.END
        )

    # ========================================================
    # RESET
    # ========================================================

    def reset_settings(self):

        self.length_var.set(16)

        self.upper_var.set(True)
        self.lower_var.set(True)
        self.number_var.set(True)
        self.symbol_var.set(True)
        self.ambiguous_var.set(True)

        self.length_value.config(
            text="16"
        )

        self.password_var.set(
            "Generate a secure password"
        )

        self.strength_text.config(
            text="Not generated",
            fg=self.muted
        )

        self.strength_bar.place(
            x=0,
            y=0,
            relheight=1,
            relwidth=0
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    application = SecureVault(root)

    root.mainloop()