# 🎓 Class Performance Dashboard

A Streamlit web app for analysing student performance across subjects.

## 📦 Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run class_performance_app.py
```

Then open http://localhost:8501 in your browser.

## 🗂️ Features

| Tab | Contents |
|-----|----------|
| 📋 Dataset | Full styled table, absence summary, CSV download |
| 🏆 Rankings & Toppers | Rank list, top 3 cards, subject-wise toppers |
| 📈 Student-wise Analysis | Bar chart for all / radar + bar for individual |
| 📚 Subject-wise Analysis | Distribution, trend, pass/fail pie, all subjects |
| 🥧 Overall Summary | Pie chart, heatmap, pass % table, box plot |

## 📁 Data

- A **built-in sample dataset** (20 students) is included — no upload needed.
- You can also upload your own **class_performance.csv** from the sidebar.

### CSV Format
Your CSV must have a `NAME` column and these subject columns:
```
NAME, Roll No, PPDS, EP, EM2, DS, UHV
```
Absent entries can be marked as `ab`, `Ab`, or `AB`.

## 🖥️ Requirements
- Python 3.8+
- See requirements.txt
