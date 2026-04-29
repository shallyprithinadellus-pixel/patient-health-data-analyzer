# 🩺 Patient Health Analyzer — Streamlit Dashboard

## Setup & Run

### Step 1 — Install dependencies
```
pip install -r healthApp\requirements.txt
```
If pip is not recognized on Windows, use:
```
python -m pip install -r requirements.txt
```

### Step 2 — Run the app
```


streamlit run healthApp\app.py --server.headless true
```
If streamlit is not recognized, use:
```
python -m streamlit run app.py
```

Opens at: http://localhost:8501

---

## Login Credentials
- Name     : Reshmaan
- Password : RINSSPD

---

## Features
- Login page with password protection
- Sidebar: patient details (name, age, gender, guardian info)
- Tab 1 — Vital Signs: enter old & new readings, see status + summary table
- Tab 2 — Symptom Checker: tick symptoms, see disease risk alerts
- Tab 3 — Charts: grouped bar, old/new bars, change delta chart
