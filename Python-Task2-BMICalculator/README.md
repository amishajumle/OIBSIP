# BMI Health Pulse

A modern desktop BMI tracking application developed using Python as part of the Oasis Infobyte Python Programming Internship.

## 📌 Project Overview

BMI Health Pulse is a graphical BMI calculator that allows users to calculate their Body Mass Index, understand their BMI category, save their measurements, view their health history, and visualize BMI progress over time.

The application uses a modern Tkinter interface with SQLite for local data storage and Matplotlib for BMI trend visualization.

## ✨ Features

* Modern desktop dashboard interface
* BMI calculation using height and weight
* User name, age and gender information
* BMI category classification
* Input validation and error handling
* SQLite database for storing BMI records
* Multiple user records
* BMI history table
* BMI trend visualization
* Health statistics dashboard
* Local data storage
* User-friendly interface

## 🛠️ Technologies Used

* Python
* Tkinter
* SQLite
* Matplotlib
* ttk
* Git & GitHub

## 📂 Project Structure

```text
Python-Task2-BMICalculator/
│
├── app.py
├── database.py
├── README.md
├── bmi_history.db
│
└── screenshots/
    ├── dashboard.png
    ├── bmi-result.png
    ├── history.png
    └── bmi-trend.png
```

## ⚙️ Installation

### 1. Install Python

Make sure Python is installed on your computer.

### 2. Install Matplotlib

Open the terminal inside the project folder and run:

```bash
py -m pip install matplotlib
```

### 3. Run the application

```bash
py app.py
```

## 🧮 How to Use

1. Launch the application.
2. Enter your full name.
3. Enter your age.
4. Select your gender.
5. Enter your height in centimeters.
6. Enter your weight in kilograms.
7. Click **Calculate BMI**.
8. View your BMI and health category.
9. Use **View History** to see previous measurements.
10. Add multiple measurements to generate a BMI trend graph.

## 📊 BMI Categories

| BMI Range    | Category    |
| ------------ | ----------- |
| Below 18.5   | Underweight |
| 18.5 – 24.9  | Normal      |
| 25 – 29.9    | Overweight  |
| 30 and above | Obese       |

## 💾 Database

The application uses SQLite to store:

* User name
* Age
* Gender
* Height
* Weight
* BMI
* BMI category
* Date and time of measurement

The database is created automatically when the application starts.

## 📈 BMI Trend

After recording at least two BMI measurements for a user, the application can generate a BMI progress graph using Matplotlib.

This allows users to visually track changes in their BMI over time.

## ⚠️ Error Handling

The application validates:

* Empty fields
* Invalid age
* Invalid height
* Invalid weight
* Database storage errors
* Insufficient records for trend visualization

## 🎓 Internship Task

**Organization:** Oasis Infobyte

**Track:** Python Programming

**Task:** Task 2 — BMI Calculator

**Project:** BMI Health Pulse

## 👩‍💻 Author

Amisha Jumle

IT Engineering Student

---

*This project was developed for educational and internship purposes.*
