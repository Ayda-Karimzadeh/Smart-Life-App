# 🌿 Smart Life

**A data-driven personal growth and productivity system.**

Smart Life is a desktop productivity application designed to help users build better habits, manage goals, organize tasks, and understand their progress through analytics-driven insights.

Built with clean architecture and a focus on meaningful data, Smart Life turns daily actions into measurable progress.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-GUI-green?logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=sqlite)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts-orange?logo=plotly)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Overview

Many habit trackers only focus on daily check-ins. Smart Life goes further by supporting flexible habits, goals, tasks, and focus sessions in one integrated system.

Instead of only recording activities, Smart Life analyzes consistency, tracks progress over time, and provides a clearer picture of personal growth.

---

## 🚀 Features

- **📊 Dashboard**
  - Overview of today's habits, active goals, upcoming tasks, and recent activity.

- **🔥 Habit Tracking**
  - Support for both daily habits and flexible weekly habits.
  - Example: "Exercise 3 times per week".
  - Includes streak calculation, best streak tracking, weekly progress, and streak status analysis.

- **🎯 Goal Tracking**
  - Create personal goals.
  - Track milestones and completion progress.

- **✅ Task Management**
  - Create, update, complete, and organize tasks.
  - Support for deadlines and priorities.

- **⏱️ Time Tracking**
  - Pomodoro-style focus timer.
  - Preset sessions: 25, 45, 60, and 90 minutes.
  - Custom durations.
  - Progress visualization and automatic session saving.

- **📈 Analytics**
  - Habit consistency analysis.
  - Productivity scoring.
  - Weekly reports.
  - Visual insights using:
    - Line charts
    - Bar charts
    - Donut charts
    - Grouped bar charts
    - Radar charts
    - Heatmaps

- **🧭 Onboarding Wizard**
  - First-run setup experience.
  - Guides users through:
    - Welcome
    - Habit selection
    - Goal selection
    - Completion

- **🌙 Dark Theme**
  - A consistent modern dark interface across the application.

---

## 🧮 Productivity Score

Smart Life calculates a personal progress score based on four areas:

| Area | Weight |
|------|--------|
| Habits | 40% |
| Goals | 30% |
| Tasks | 20% |
| Focus Time | 10% |

This score is designed as a personal progress indicator to help users understand their consistency and improvement over time.

---

## 🏗️ Architecture

The project follows a clean layered architecture:

```
Smart-Life-App/
├── assets/          # Styling, icons, and static resources
├── core/            # Business logic and analytics engines
├── data/            # Local application data
├── database/        # SQLite schema, models, and database access
├── ui/              # PyQt6 pages, dialogs, charts, sidebar, onboarding
├── main.py          # Application entry point
└── requirements.txt
```

### Key Modules

- `core/streak_engine.py`
  - Daily and weekly streak calculations.
  - Best streak tracking.
  - Weekly habit status analysis.

- `core/analytics.py`
  - Consistency calculations.
  - Productivity score.
  - Weekly reports.
  - Strength and weakness analysis.

- `ui/charts.py`
  - Matplotlib charts integrated with PyQt6 using `FigureCanvasQTAgg`.

- `ui/dialogs.py`
  - Application dialogs and reusable UI components.

- `ui/onboarding.py`
  - First-launch onboarding workflow.

- `database/db_manager.py`
  - SQLite database management and CRUD operations.

- `database/models.py`
  - Data models and application entities.

---

## 🛠️ Tech Stack

- **Language:** Python
- **GUI Framework:** PyQt6
- **Database:** SQLite
- **Charts & Visualization:** Matplotlib

---

## ⚙️ Installation and Run (Windows)

### Prerequisites

- Windows 10 or newer
- Python 3.11 or newer installed and available through the `py` command
- Git, if cloning the repository from GitHub

### 1. Download the project

```powershell
git clone https://github.com/Ayda-Karimzadeh/Smart-Life-App.git
cd Smart-Life-App
```

If the project was downloaded as a ZIP file, extract it and open PowerShell in the folder that contains `main.py`.

### 2. Create and activate the virtual environment

Run these commands from the project root:

```powershell
py -3 -m venv venv
.\venv\Scripts\Activate.ps1
```

For Command Prompt (`cmd.exe`), activate it with:

```bat
venv\Scripts\activate.bat
```

After activation, the terminal prompt should start with `(venv)`.

### 3. Install the required packages

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

This installs the exact versions required by the project: PyQt6 6.11.0, Matplotlib 3.11.0, and NumPy 2.3.2.

### 4. Run the application

Make sure `(venv)` is still visible in the terminal, then run:

```powershell
python main.py
```

The application must be launched from the project root, where `main.py` is located. On the first launch, if no database exists, the onboarding wizard will guide users through creating their initial habits and goals.

### Optional: PowerShell activation policy

If PowerShell blocks `Activate.ps1`, run this command once in the current PowerShell window and activate the environment again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

---

## 🗺️ Roadmap

- [ ] Add data export (CSV/PDF reports)
- [ ] Add reminders and notifications
- [ ] Add customizable themes
- [ ] Add database backup and restore
- [ ] Add smarter personal insights
- [ ] Add cross-device synchronization
- [ ] Add AI-based habit recommendations

---

## 📌 Project Status

Smart Life is currently an MVP under active development.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

Feel free to open an issue or suggest improvements.

---

## 📄 License

This project is licensed under the MIT License.