import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
from PIL import Image, ImageTk
from io import BytesIO
from datetime import datetime
import os


# ============================================================
# CONFIGURATION
# ============================================================

API_KEY_FILE = "api_key.txt"

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


# ============================================================
# COLORS
# ============================================================

BG = "#08111f"
CARD = "#101d31"
CARD_LIGHT = "#16263f"
TEXT = "#f5f7fb"
MUTED = "#91a4bf"
ACCENT = "#4f8cff"
ACCENT_LIGHT = "#75a8ff"
BORDER = "#263957"
ERROR = "#ff6b6b"
SUCCESS = "#51d88a"


# ============================================================
# API KEY MANAGEMENT
# ============================================================

def get_api_key():
    """
    Reads the OpenWeatherMap API key from api_key.txt.
    If the file does not exist, ask the user to enter the key.
    """

    if os.path.exists(API_KEY_FILE):
        with open(API_KEY_FILE, "r", encoding="utf-8") as file:
            key = file.read().strip()

        if key:
            return key

    key = simpledialog.askstring(
        "OpenWeatherMap API Key",
        "Enter your OpenWeatherMap API key:",
        show="*"
    )

    if key:
        key = key.strip()

        with open(API_KEY_FILE, "w", encoding="utf-8") as file:
            file.write(key)

        return key

    return None


# ============================================================
# WEATHER APPLICATION
# ============================================================

class WeatherApp:

    def __init__(self, root):

        self.root = root

        self.root.title("Weatherly | Smart Weather Dashboard")
        self.root.geometry("1180x780")
        self.root.minsize(1050, 700)
        self.root.configure(bg=BG)

        self.api_key = get_api_key()

        self.current_city = ""
        self.current_data = None
        self.forecast_data = None

        self.unit = "C"

        self.weather_icon = None

        self.setup_variables()
        self.create_interface()

        if not self.api_key:
            self.show_error(
                "API key is required.\n"
                "Please restart the application and enter your API key."
            )


    # ========================================================
    # VARIABLES
    # ========================================================

    def setup_variables(self):

        self.city_var = tk.StringVar()
        self.temperature_var = tk.StringVar(value="--°")
        self.condition_var = tk.StringVar(value="Search for a city")
        self.feels_like_var = tk.StringVar(value="--°")
        self.humidity_var = tk.StringVar(value="--%")
        self.wind_var = tk.StringVar(value="-- km/h")
        self.pressure_var = tk.StringVar(value="-- hPa")
        self.visibility_var = tk.StringVar(value="-- km")
        self.location_var = tk.StringVar(value="Your weather at a glance")


    # ========================================================
    # MAIN INTERFACE
    # ========================================================

    def create_interface(self):

        # Main scrollable canvas
        self.canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )

        self.scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.main_frame = tk.Frame(
            self.canvas,
            bg=BG
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.main_frame,
            anchor="nw"
        )

        self.main_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_canvas
        )

        self.canvas.bind_all(
            "<MouseWheel>",
            self.mouse_scroll
        )

        # Build interface
        self.create_header()
        self.create_search_section()
        self.create_current_weather()
        self.create_details()
        self.create_hourly_forecast()
        self.create_daily_forecast()
        self.create_footer()


    # ========================================================
    # SCROLLING
    # ========================================================

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )


    def resize_canvas(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )


    def mouse_scroll(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )


    # ========================================================
    # HEADER
    # ========================================================

    def create_header(self):

        header = tk.Frame(
            self.main_frame,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=45,
            pady=(30, 15)
        )

        left = tk.Frame(
            header,
            bg=BG
        )

        left.pack(
            side="left"
        )

        logo = tk.Label(
            left,
            text="☁",
            font=("Segoe UI Emoji", 34),
            bg=BG,
            fg=ACCENT_LIGHT
        )

        logo.pack(
            side="left",
            padx=(0, 12)
        )

        title_frame = tk.Frame(
            left,
            bg=BG
        )

        title_frame.pack(
            side="left"
        )

        title = tk.Label(
            title_frame,
            text="WEATHERLY",
            font=("Segoe UI", 24, "bold"),
            bg=BG,
            fg=TEXT
        )

        title.pack(
            anchor="w"
        )

        subtitle = tk.Label(
            title_frame,
            text="Smart Weather Dashboard",
            font=("Segoe UI", 10),
            bg=BG,
            fg=MUTED
        )

        subtitle.pack(
            anchor="w"
        )

        self.unit_button = tk.Button(
            header,
            text="°C  |  °F",
            command=self.toggle_unit,
            font=("Segoe UI", 10, "bold"),
            bg=CARD_LIGHT,
            fg=TEXT,
            activebackground=ACCENT,
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2"
        )

        self.unit_button.pack(
            side="right"
        )


    # ========================================================
    # SEARCH SECTION
    # ========================================================

    def create_search_section(self):

        search_card = tk.Frame(
            self.main_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        search_card.pack(
            fill="x",
            padx=45,
            pady=10
        )

        search_inner = tk.Frame(
            search_card,
            bg=CARD
        )

        search_inner.pack(
            fill="x",
            padx=25,
            pady=20
        )

        label = tk.Label(
            search_inner,
            text="SEARCH LOCATION",
            font=("Segoe UI", 9, "bold"),
            bg=CARD,
            fg=MUTED
        )

        label.pack(
            anchor="w",
            pady=(0, 8)
        )

        search_row = tk.Frame(
            search_inner,
            bg=CARD
        )

        search_row.pack(
            fill="x"
        )

        self.city_entry = tk.Entry(
            search_row,
            textvariable=self.city_var,
            font=("Segoe UI", 14),
            bg="#0b1728",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.city_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 12)
        )

        self.city_entry.insert(
            0,
            "Mumbai"
        )

        self.search_button = tk.Button(
            search_row,
            text="🔍  SEARCH",
            command=self.search_weather,
            font=("Segoe UI", 10, "bold"),
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_LIGHT,
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )

        self.search_button.pack(
            side="right"
        )

        self.city_entry.bind(
            "<Return>",
            lambda event: self.search_weather()
        )


    # ========================================================
    # CURRENT WEATHER
    # ========================================================

    def create_current_weather(self):

        self.current_card = tk.Frame(
            self.main_frame,
            bg=CARD,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.current_card.pack(
            fill="x",
            padx=45,
            pady=10
        )

        content = tk.Frame(
            self.current_card,
            bg=CARD
        )

        content.pack(
            fill="x",
            padx=35,
            pady=30
        )

        # Left
        left = tk.Frame(
            content,
            bg=CARD
        )

        left.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.location_label = tk.Label(
            left,
            textvariable=self.location_var,
            font=("Segoe UI", 13, "bold"),
            bg=CARD,
            fg=TEXT
        )

        self.location_label.pack(
            anchor="w"
        )

        self.date_label = tk.Label(
            left,
            text=datetime.now().strftime("%A, %d %B %Y"),
            font=("Segoe UI", 10),
            bg=CARD,
            fg=MUTED
        )

        self.date_label.pack(
            anchor="w",
            pady=(4, 25)
        )

        temperature_row = tk.Frame(
            left,
            bg=CARD
        )

        temperature_row.pack(
            anchor="w"
        )

        self.icon_label = tk.Label(
            temperature_row,
            text="☀",
            font=("Segoe UI Emoji", 58),
            bg=CARD,
            fg=TEXT
        )

        self.icon_label.pack(
            side="left",
            padx=(0, 20)
        )

        self.temperature_label = tk.Label(
            temperature_row,
            textvariable=self.temperature_var,
            font=("Segoe UI", 55, "bold"),
            bg=CARD,
            fg=TEXT
        )

        self.temperature_label.pack(
            side="left"
        )

        self.condition_label = tk.Label(
            left,
            textvariable=self.condition_var,
            font=("Segoe UI", 13),
            bg=CARD,
            fg=MUTED
        )

        self.condition_label.pack(
            anchor="w",
            padx=(92, 0),
            pady=(0, 5)
        )

        # Right
        self.info_panel = tk.Frame(
            content,
            bg=CARD_LIGHT
        )

        self.info_panel.pack(
            side="right",
            padx=(30, 0)
        )

        self.create_info_row(
            self.info_panel,
            "Feels Like",
            self.feels_like_var,
            0
        )

        self.create_info_row(
            self.info_panel,
            "Humidity",
            self.humidity_var,
            1
        )

        self.create_info_row(
            self.info_panel,
            "Wind",
            self.wind_var,
            2
        )

        self.create_info_row(
            self.info_panel,
            "Pressure",
            self.pressure_var,
            3
        )

        self.create_info_row(
            self.info_panel,
            "Visibility",
            self.visibility_var,
            4
        )


    def create_info_row(
        self,
        parent,
        title,
        variable,
        row
    ):

        frame = tk.Frame(
            parent,
            bg=CARD_LIGHT
        )

        frame.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=20,
            pady=8
        )

        label = tk.Label(
            frame,
            text=title,
            font=("Segoe UI", 9),
            bg=CARD_LIGHT,
            fg=MUTED,
            width=12,
            anchor="w"
        )

        label.pack(
            side="left"
        )

        value = tk.Label(
            frame,
            textvariable=variable,
            font=("Segoe UI", 10, "bold"),
            bg=CARD_LIGHT,
            fg=TEXT,
            width=12,
            anchor="e"
        )

        value.pack(
            side="right"
        )


    # ========================================================
    # DETAILS
    # ========================================================

    def create_details(self):

        self.details_frame = tk.Frame(
            self.main_frame,
            bg=BG
        )

        self.details_frame.pack(
            fill="x",
            padx=45,
            pady=10
        )

        for title in [
            "☀ Sunrise",
            "☾ Sunset",
            "🌡 Weather"
        ]:

            card = tk.Frame(
                self.details_frame,
                bg=CARD,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.pack(
                side="left",
                fill="x",
                expand=True,
                padx=5
            )

            label = tk.Label(
                card,
                text=title,
                font=("Segoe UI", 9, "bold"),
                bg=CARD,
                fg=MUTED
            )

            label.pack(
                pady=(15, 5)
            )

            value = tk.Label(
                card,
                text="--",
                font=("Segoe UI", 15, "bold"),
                bg=CARD,
                fg=TEXT
            )

            value.pack(
                pady=(0, 15)
            )

            if "Sunrise" in title:
                self.sunrise_label = value

            elif "Sunset" in title:
                self.sunset_label = value

            else:
                self.weather_status_label = value


    # ========================================================
    # HOURLY FORECAST
    # ========================================================

    def create_hourly_forecast(self):

        section_title = tk.Label(
            self.main_frame,
            text="NEXT 6 HOURS",
            font=("Segoe UI", 15, "bold"),
            bg=BG,
            fg=TEXT
        )

        section_title.pack(
            anchor="w",
            padx=45,
            pady=(25, 10)
        )

        self.hourly_container = tk.Frame(
            self.main_frame,
            bg=BG
        )

        self.hourly_container.pack(
            fill="x",
            padx=40
        )


    def display_hourly_forecast(self, forecast_list):

        for widget in self.hourly_container.winfo_children():
            widget.destroy()

        hourly_items = forecast_list[:6]

        for item in hourly_items:

            card = tk.Frame(
                self.hourly_container,
                bg=CARD,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            dt = datetime.fromtimestamp(item["dt"])

            time_label = tk.Label(
                card,
                text=dt.strftime("%I %p"),
                font=("Segoe UI", 9, "bold"),
                bg=CARD,
                fg=MUTED
            )

            time_label.pack(
                pady=(15, 5)
            )

            icon = self.weather_symbol(
                item["weather"][0]["main"]
            )

            icon_label = tk.Label(
                card,
                text=icon,
                font=("Segoe UI Emoji", 25),
                bg=CARD,
                fg=TEXT
            )

            icon_label.pack(
                pady=5
            )

            temp = self.convert_temperature(
                item["main"]["temp"]
            )

            temp_label = tk.Label(
                card,
                text=f"{temp}°",
                font=("Segoe UI", 14, "bold"),
                bg=CARD,
                fg=TEXT
            )

            temp_label.pack(
                pady=(5, 15)
            )


    # ========================================================
    # DAILY FORECAST
    # ========================================================

    def create_daily_forecast(self):

        section_title = tk.Label(
            self.main_frame,
            text="5-DAY FORECAST",
            font=("Segoe UI", 15, "bold"),
            bg=BG,
            fg=TEXT
        )

        section_title.pack(
            anchor="w",
            padx=45,
            pady=(30, 10)
        )

        self.daily_container = tk.Frame(
            self.main_frame,
            bg=BG
        )

        self.daily_container.pack(
            fill="x",
            padx=40,
            pady=(0, 25)
        )


    def display_daily_forecast(self, forecast_list):

        for widget in self.daily_container.winfo_children():
            widget.destroy()

        daily_data = {}

        for item in forecast_list:

            date = datetime.fromtimestamp(
                item["dt"]
            ).strftime("%Y-%m-%d")

            if date not in daily_data:
                daily_data[date] = item

        days = list(daily_data.values())[:5]

        for item in days:

            card = tk.Frame(
                self.daily_container,
                bg=CARD,
                highlightbackground=BORDER,
                highlightthickness=1
            )

            card.pack(
                side="left",
                fill="both",
                expand=True,
                padx=5
            )

            dt = datetime.fromtimestamp(
                item["dt"]
            )

            day = tk.Label(
                card,
                text=dt.strftime("%a").upper(),
                font=("Segoe UI", 10, "bold"),
                bg=CARD,
                fg=MUTED
            )

            day.pack(
                pady=(15, 5)
            )

            date_label = tk.Label(
                card,
                text=dt.strftime("%d %b"),
                font=("Segoe UI", 8),
                bg=CARD,
                fg=MUTED
            )

            date_label.pack()

            icon = tk.Label(
                card,
                text=self.weather_symbol(
                    item["weather"][0]["main"]
                ),
                font=("Segoe UI Emoji", 30),
                bg=CARD,
                fg=TEXT
            )

            icon.pack(
                pady=8
            )

            temp = self.convert_temperature(
                item["main"]["temp"]
            )

            temp_label = tk.Label(
                card,
                text=f"{temp}°",
                font=("Segoe UI", 15, "bold"),
                bg=CARD,
                fg=TEXT
            )

            temp_label.pack(
                pady=(0, 15)
            )


    # ========================================================
    # FOOTER
    # ========================================================

    def create_footer(self):

        footer = tk.Label(
            self.main_frame,
            text="Weather data powered by OpenWeatherMap",
            font=("Segoe UI", 9),
            bg=BG,
            fg=MUTED
        )

        footer.pack(
            pady=(10, 35)
        )


    # ========================================================
    # SEARCH WEATHER
    # ========================================================

    def search_weather(self):

        city = self.city_var.get().strip()

        if not city:
            self.show_error(
                "Please enter a city name."
            )
            return

        if not self.api_key:
            self.show_error(
                "OpenWeatherMap API key is missing."
            )
            return

        self.search_button.config(
            text="LOADING...",
            state="disabled"
        )

        self.root.update_idletasks()

        try:

            current_params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }

            current_response = requests.get(
                CURRENT_WEATHER_URL,
                params=current_params,
                timeout=10
            )

            if current_response.status_code == 401:
                raise Exception(
                    "Invalid API key."
                )

            if current_response.status_code == 404:
                raise Exception(
                    "City not found. Please check the city name."
                )

            current_response.raise_for_status()

            self.current_data = current_response.json()

            forecast_params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }

            forecast_response = requests.get(
                FORECAST_URL,
                params=forecast_params,
                timeout=10
            )

            forecast_response.raise_for_status()

            self.forecast_data = forecast_response.json()

            self.current_city = city

            self.update_current_weather()
            self.display_hourly_forecast(
                self.forecast_data["list"]
            )
            self.display_daily_forecast(
                self.forecast_data["list"]
            )

        except requests.exceptions.Timeout:

            self.show_error(
                "The weather service took too long to respond."
            )

        except requests.exceptions.ConnectionError:

            self.show_error(
                "Internet connection error.\n"
                "Please check your internet connection."
            )

        except requests.exceptions.RequestException as error:

            self.show_error(
                f"Unable to retrieve weather data.\n\n{error}"
            )

        except Exception as error:

            self.show_error(
                str(error)
            )

        finally:

            self.search_button.config(
                text="🔍  SEARCH",
                state="normal"
            )


    # ========================================================
    # UPDATE CURRENT WEATHER
    # ========================================================

    def update_current_weather(self):

        data = self.current_data

        city = data["name"]
        country = data["sys"]["country"]

        self.location_var.set(
            f"{city}, {country}"
        )

        temperature = self.convert_temperature(
            data["main"]["temp"]
        )

        feels_like = self.convert_temperature(
            data["main"]["feels_like"]
        )

        self.temperature_var.set(
            f"{temperature}°"
        )

        self.feels_like_var.set(
            f"{feels_like}°"
        )

        self.condition_var.set(
            data["weather"][0]["description"].title()
        )

        self.humidity_var.set(
            f"{data['main']['humidity']}%"
        )

        wind_kmh = data["wind"]["speed"] * 3.6

        self.wind_var.set(
            f"{wind_kmh:.1f} km/h"
        )

        self.pressure_var.set(
            f"{data['main']['pressure']} hPa"
        )

        visibility_km = data.get(
            "visibility",
            0
        ) / 1000

        self.visibility_var.set(
            f"{visibility_km:.1f} km"
        )

        condition = data["weather"][0]["main"]

        self.icon_label.config(
            text=self.weather_symbol(condition)
        )

        self.weather_status_label.config(
            text=data["weather"][0]["description"].title()
        )

        sunrise = datetime.fromtimestamp(
            data["sys"]["sunrise"]
        ).strftime("%I:%M %p")

        sunset = datetime.fromtimestamp(
            data["sys"]["sunset"]
        ).strftime("%I:%M %p")

        self.sunrise_label.config(
            text=sunrise
        )

        self.sunset_label.config(
            text=sunset
        )


    # ========================================================
    # TEMPERATURE CONVERSION
    # ========================================================

    def convert_temperature(self, celsius):

        if self.unit == "C":
            return round(celsius)

        fahrenheit = (celsius * 9 / 5) + 32

        return round(fahrenheit)


    # ========================================================
    # UNIT TOGGLE
    # ========================================================

    def toggle_unit(self):

        if self.unit == "C":
            self.unit = "F"
        else:
            self.unit = "C"

        if self.current_data:

            self.update_current_weather()

            self.display_hourly_forecast(
                self.forecast_data["list"]
            )

            self.display_daily_forecast(
                self.forecast_data["list"]
            )


    # ========================================================
    # WEATHER SYMBOLS
    # ========================================================

    def weather_symbol(self, condition):

        symbols = {
            "Clear": "☀",
            "Clouds": "☁",
            "Rain": "🌧",
            "Drizzle": "🌦",
            "Thunderstorm": "⛈",
            "Snow": "❄",
            "Mist": "🌫",
            "Smoke": "🌫",
            "Haze": "🌫",
            "Dust": "🌫",
            "Fog": "🌫",
            "Sand": "🌫",
            "Ash": "🌫",
            "Squall": "💨",
            "Tornado": "🌪"
        }

        return symbols.get(
            condition,
            "🌤"
        )


    # ========================================================
    # ERROR MESSAGE
    # ========================================================

    def show_error(self, message):

        messagebox.showerror(
            "Weatherly - Error",
            message
        )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = WeatherApp(root)

    root.mainloop()