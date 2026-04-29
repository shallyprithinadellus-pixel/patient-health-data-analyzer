import streamlit as st
import random
import plotly.graph_objects as go
import pandas as pd
import smtplib
from email.message import EmailMessage
from datetime import datetime

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Patient Health Analyzer",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f5c6d8, #c9e4f5) !important;
    }

    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #aed6f1, #f9c0d4) !important;
    }

    /* Main Title Color */
    h1 {
        color: #1a1a2e !important;
        font-weight: 800 !important;
    }

    /* All Headings Color */
    h2, h3, h4 {
        color: #1a1a2e !important;
        font-weight: 700 !important;
    }

    /* Fix All Buttons */
    .stButton button {
        background-color: #1a6eb5 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        padding: 10px 20px !important;
    }

    /* Button Hover Effect */
    .stButton button:hover {
        background-color: #155a94 !important;
        color: #ffffff !important;
    }

    /* Fix Form Submit Button */
    .stFormSubmitButton button {
        background-color: #1a6eb5 !important;
        color: #ffffff !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }

    /* Fix Input Boxes */
    input[type="text"],
    input[type="number"],
    input[type="password"],
    textarea {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border: 1px solid #aed6f1 !important;
        border-radius: 8px !important;
    }

    /* Fix Number Input */
    [data-testid="stNumberInput"] input {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }

    /* Fix Date Input */
    [data-testid="stDateInput"] input {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border: 1px solid #aed6f1 !important;
        border-radius: 8px !important;
    }

    /* Fix Selectbox */
    [data-testid="stSelectbox"] div {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }

    /* Fix Labels */
    label {
        color: #1a1a2e !important;
        font-weight: 600 !important;
    }

    /* Fix Tab Names */
    .stTabs [data-baseweb="tab"] {
        color: #1a1a2e !important;
        font-weight: 600 !important;
        background-color: rgba(255,255,255,0.5) !important;
        border-radius: 8px 8px 0 0 !important;
    }

    /* Selected Tab */
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        font-weight: 700 !important;
    }

    /* Fix General Text */
    p, span, div {
        color: #1a1a2e !important;
    }

    /* Watermark Image */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("https://img.freepik.com/free-vector/medical-healthcare-blue-color_1017-26807.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        opacity: 0.35;
        z-index: 0;
        pointer-events: none;
    }
    </style>
""", unsafe_allow_html=True)
# ── Credentials ──────────────────────────────────────────────────────────────
CORRECT_PATIENT  = "SANTU"
CORRECT_PASSWORD = "RINSSPD"

# ── Session State ────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ══════════════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS  
# ══════════════════════════════════════════════════════════════════════════════

def check_heart_rate(value):
    if value < 60:
        return "🟡 Very Low"
    elif 60 <= value <= 100:
        return "🟢 Normal"
    else:
        return "🔴 Very High"

def check_bp(value):
    if value < 90:
        return "🟡 Very Low"
    elif 90 <= value <= 120:
        return "🟢 Normal"
    else:
        return "🔴 Very High"

def check_temperature(value):
    if value < 36:
        return "🟡 Very Low"
    elif 36 <= value <= 37.5:
        return "🟢 Normal"
    else:
        return "🔴 Very High"

def check_bmi(value):
    if value < 18.5:
        return "🟡 Very Low"
    elif value >= 18.5:
        return "🟢 Normal"
    else:
        return "🔴 Very High"

def check_sugar(value):
    if value < 120:
        return "🟡 Very Low"
    elif value == 120:
        return "🟢 Perfect Normal"
    else:
        return "🔴 Very High"

def check_diseases(symptoms):
    results = []

    # HEART DISEASE
    if symptoms["chestpain"] and symptoms["breathing_problem"] and symptoms["fatigue"]:
        results.append(("🫀 Heart Disease", "error",
            "May be heart attack will come in future according to your symptoms. Consult the doctor.",
            "PRECAUTION: Walking, avoid junk food"))

    # DIABETES
    if symptoms["frequent_urination"] and symptoms["excessive_thirst"] and symptoms["fatigue"]:
        results.append(("🩸 Diabetes", "error",
            "May be diabetes according to your symptoms. Consult the doctor.",
            "PRECAUTION: Reduce sweets, walking"))

    # NEUROLOGICAL DISORDER
    if symptoms["memory_loss"] and symptoms["tremors"] and symptoms["fatigue"]:
        results.append(("🧠 Neurological Disorder", "warning",
            "May be neurological disorder according to your symptoms. Consult the doctor.",
            "PRECAUTION: Avoid mobile/TV, (7-8) hours sleep"))

    # INFECTION DISEASE
    if symptoms["cough"] and symptoms["body_pain"] and symptoms["fever"] and symptoms["fatigue"]:
        results.append(("🦠 Infection Disease", "warning",
            "May be infection disease according to your symptoms. Consult the doctor.",
            "PRECAUTION: Personal hygiene, wear mask"))

    # RESPIRATORY DISEASE
    if symptoms["cough"] and symptoms["breathing_problem"] and symptoms["fatigue"]:
        results.append(("🫁 Respiratory Disease", "warning",
            "May be respiratory disease according to your symptoms. Consult the doctor.",
            "PRECAUTION: Avoid smoking and pollution area"))

    # CANCER
    if symptoms["weight_loss"] and symptoms["lump"] and symptoms["fatigue"]:
        results.append(("🔴 Cancer Risk", "error",
            "May be Cancer according to your symptoms. Consult the doctor.",
            "PRECAUTION: Avoid tobacco, health screening (yearly once)"))

    # MENTAL STRESS
    if symptoms["anxiety"] and symptoms["sleeping_problem"]:
        results.append(("🧘 Psychological Problem", "warning",
            "May be psychological problem according to your symptoms. Consult the doctor.",
            "PRECAUTION: Meditation/yoga, reduce stress"))

    # JAUNDICE / KIDNEY
    if symptoms["swelling_legs"] and symptoms["yellow_skin"]:
        results.append(("🟡 Jaundice / Liver Issue", "warning",
            "May be jaundice according to your symptoms. Consult the doctor.",
            "PRECAUTION: Don't take medicine unnecessarily, take plenty of water"))

    return results


# ── Helper Functions ─────────────────────────────────────────────────────────

def add_message(content, category="General"):
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.session_state.messages.insert(0, {
        "Time"    : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Category": category,
        "Message" : content,
    })


def send_email_notification(recipient, subject, body, sender, password, smtp_server="smtp.gmail.com", smtp_port=587):
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"]    = sender
        msg["To"]      = recipient
        msg.set_content(body)
        with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as smtp:
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(msg)
        return True, "Email sent successfully."
    except Exception as exc:
        return False, str(exc)


def suggest_nearby_hospitals(location: str):
    location = location.strip().lower()

    if "bangalore" in location or "bengaluru" in location:
        return [
            "Manipal Hospital — Old Airport Road, Bangalore",
            "Apollo Hospital — Bannerghatta Road, Bangalore",
            "Fortis Hospital — Cunningham Road, Bangalore",
            "Columbia Asia Hospital — Hebbal, Bangalore",
            "Narayana Health — Bommasandra, Bangalore",
        ]
    if "mumbai" in location:
        return [
            "KEM Hospital — Parel, Mumbai",
            "Lilavati Hospital — Bandra West, Mumbai",
            "Kokilaben Dhirubhai Ambani Hospital — Andheri West, Mumbai",
            "Breach Candy Hospital — Bhulabhai Desai Road, Mumbai",
            "Tata Memorial Hospital — Parel, Mumbai",
        ]
    if "delhi" in location:
        return [
            "AIIMS — Ansari Nagar, New Delhi",
            "Apollo Hospital — Sarita Vihar, Delhi",
            "Fortis Hospital — Shalimar Bagh, Delhi",
            "Max Super Speciality Hospital — Saket, Delhi",
            "Sir Ganga Ram Hospital — Rajinder Nagar, Delhi",
        ]
    if "kolkata" in location:
        return [
            "SSKM Hospital — AJC Bose Road, Kolkata",
            "Apollo Gleneagles Hospital — Canal Circular Road, Kolkata",
            "Fortis Hospital — Anandapur, Kolkata",
            "Belle Vue Clinic — Lindsay Street, Kolkata",
            "Peerless Hospital — Pancha Sayar, Kolkata",
        ]
    if "chennai" in location:
        return [
            "Apollo Hospital — Greams Road, Chennai",
            "Government General Hospital — Park Town, Chennai",
            "Fortis Malar Hospital — Adyar, Chennai",
            "MIOT International — Manapakkam, Chennai",
            "Sri Ramachandra Hospital — Porur, Chennai",
        ]
    if "trichy" in location or "tiruchirappalli" in location or "tiruchirapalli" in location:
        return [
            "Mahatma Gandhi Memorial Government Hospital — Puthur, Trichy",
            "Kavery Hospital — Cantonment, Trichy",
            "Vasan Health Care — Thillai Nagar, Trichy",
            "Sri Ramakrishna Hospital — K.K. Nagar, Trichy",
            "Vijaya Hospital — Ariyamangalam, Trichy",
        ]
    if "salem" in location:
        return [
            "Salem Government Hospital — Saradha College Road, Salem",
            "SKS Hospital — Alagapuram, Salem",
            "Shanmuga Hospital — Steel Plant Road, Salem",
            "Vinayaka Mission Hospital — Sankari Main Road, Salem",
            "Apollo Clinic — Junction Main Road, Salem",
        ]
    if "madurai" in location:
        return [
            "Government Rajaji Hospital — Panagal Road, Madurai",
            "Meenakshi Mission Hospital — Lake Area, Madurai",
            "Apollo Hospitals — Alagarkovil Road, Madurai",
            "Velammal Medical College Hospital — Anuppanadi, Madurai",
            "Devaki Hospital — North Veli Street, Madurai",
        ]
    if "coimbatore" in location:
        return [
            "Coimbatore Medical College Hospital — Trichy Road, Coimbatore",
            "PSG Hospitals — Avinashi Road, Coimbatore",
            "G. Kuppuswamy Naidu Memorial Hospital — Pappanaickenpalayam, Coimbatore",
            "Kovai Medical Center — Avinashi Road, Coimbatore",
            "Sri Ramakrishna Hospital — Trichy Road, Coimbatore",
        ]
    return [
        "Nearest General Hospital",
        "Emergency Care Center",
        "24/7 Medical Clinic"
    ]

def build_health_email_body(name, age, gender, vitals, disease_results):
    lines = [
        f"Live Health Update for {name}",
        f"Age: {age}",
        f"Gender: {gender}",
        "",
        "Vital Signs:",
    ]
    for metric, value in vitals.items():
        lines.append(f"- {metric}: {value}")
    lines.append("")
    if disease_results:
        lines.append("Detected health concerns:")
        for disease, _, message, precaution in disease_results:
            lines.append(f"- {disease}: {message}")
            lines.append(f"  Precaution: {precaution}")
    else:
        lines.append("No immediate disease risk detected. Keep following health advice.")
    lines.append("")
    lines.append("This is an automated health condition update.")
    return "\n".join(lines)


def should_send_health_email(subject, body):
    if not st.session_state.get("send_auto_email"):
        return False
    if not st.session_state.get("recipient_email") or not st.session_state.get("sender_email") or not st.session_state.get("sender_password"):
        return False
    last_subject = st.session_state.get("last_health_email_subject")
    last_body    = st.session_state.get("last_health_email_body")
    return subject != last_subject or body != last_body


def try_auto_send_health_email(name, age, gender, vitals, disease_results):
    recipient   = st.session_state.get("recipient_email")
    sender      = st.session_state.get("sender_email")
    password    = st.session_state.get("sender_password")
    smtp_server = st.session_state.get("smtp_server", "smtp.gmail.com")
    smtp_port   = st.session_state.get("smtp_port", 587)

    if not recipient or not sender or not password or not st.session_state.get("send_auto_email"):
        return

    has_risk = bool(disease_results) or any(
        status not in ["🟢 Normal", "🟢 Perfect Normal"]
        for status in [
            check_heart_rate(vitals["Heart Rate"]),
            check_bp(vitals["Blood Pressure"]),
            check_temperature(vitals["Temperature"]),
            check_bmi(vitals["BMI"]),
            check_sugar(vitals["Blood Sugar"]),
        ]
    )
    if not has_risk:
        return

    subject = f"Live Health Alert for {name}"
    body    = build_health_email_body(name, age, gender, vitals, disease_results)

    if not should_send_health_email(subject, body):
        return

    success, message = send_email_notification(recipient, subject, body, sender, password, smtp_server, smtp_port)
    st.session_state["last_health_email_subject"] = subject
    st.session_state["last_health_email_body"]    = body

    if success:
        add_message(f"Automatic email sent to {recipient}.", category="Email Alert")
        st.success("📧 Automatic health email sent.")
    else:
        add_message(f"Automatic email failed: {message}", category="Email Error")
        st.error(f"❌ Email send failed: {message}")


def get_prescription(hr, bp, sugar, temp):
    issues       = []
    prescription = []

    if hr > 100:
        issues.append("High Heart Rate")
        prescription.append("• Take rest immediately")
        prescription.append("• Avoid caffeine and stress")
        prescription.append("• Consult cardiologist")
    if hr < 60:
        issues.append("Low Heart Rate")
        prescription.append("• Sit down and rest")
        prescription.append("• Drink warm water")
        prescription.append("• Consult doctor immediately")
    if bp > 120:
        issues.append("High Blood Pressure")
        prescription.append("• Avoid salty foods")
        prescription.append("• Take prescribed BP medicine")
        prescription.append("• Do deep breathing exercises")
    if bp < 90:
        issues.append("Low Blood Pressure")
        prescription.append("• Drink more water")
        prescription.append("• Eat small frequent meals")
        prescription.append("• Avoid standing up quickly")
    if sugar > 140:
        issues.append("High Blood Sugar")
        prescription.append("• Avoid sweets immediately")
        prescription.append("• Drink plenty of water")
        prescription.append("• Take diabetes medicine")
    if temp > 37.5:
        issues.append("High Temperature / Fever")
        prescription.append("• Take paracetamol")
        prescription.append("• Drink plenty of fluids")
        prescription.append("• Rest and avoid cold water")

    return issues, prescription


def show_email_setup():
    st.title("📧 Email Notification Setup")
    st.caption("Setup your email to receive automatic health alerts!")
    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("📧 Gmail Setup")
        st.info("💡 Enter your Gmail to receive automatic health alerts!")

        sender_email    = st.text_input("Your Gmail Address",
                          placeholder="yourname@gmail.com")
        sender_password = st.text_input("Gmail App Password",
                          placeholder="16 digit app password",
                          type="password")
        receiver_email  = st.text_input("Patient Gmail Address",
                          placeholder="patient@gmail.com")

        st.warning("⚠️ Use Gmail App Password — NOT your normal password!")

        if st.button("✅ Save & Continue", use_container_width=True, type="primary"):
            if sender_email and sender_password and receiver_email:
                st.session_state.sender_email    = sender_email
                st.session_state.sender_password = sender_password
                st.session_state.recipient_email = receiver_email
                st.session_state.send_auto_email = True
                st.session_state.email_setup     = True
                st.success("✅ Email setup saved! Redirecting...")
                st.rerun()
            else:
                st.error("❌ Please fill all email details!")

        if st.button("⏭️ Skip for Now", use_container_width=True):
            st.session_state.email_setup = True
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    st.title("🩺 Patient Health Analyzer")
    st.subheader("Please log in to continue")
    st.divider()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.subheader("🔐 Login")
        username = st.text_input("Patient Name", placeholder="Enter your name")
        password = st.text_input("Password", type="password", placeholder="Enter your password")

        if st.button("Login", use_container_width=True, type="primary"):
            if username == CORRECT_PATIENT and password == CORRECT_PASSWORD:
                st.session_state.logged_in   = True
                st.session_state.patient_name = username
                st.rerun()
            else:
                st.error("❌ Wrong name or password. Try again.")

        st.info("💡 Demo Login — Name: **SANTU** | Password: **RINSSPD**")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN DASHBOARDS
# ══════════════════════════════════════════════════════════════════════════════
def show_dashboard():

    # ── Sidebar: Patient Details ─────────────────────────────────────────────
    with st.sidebar:
     st.title("🩺 Health Analyzer")
     st.divider()

     st.subheader("👤 Patient Details")
     name     = st.text_input("Patient Name", value="SANTU")
     age      = st.text_input("Age",          value="25")
     gender   = st.selectbox("Gender",        ["Male", "Female", "Other"])
     guardian = st.text_input("Guardian Name", value="")
     phone    = st.text_input("Guardian Phone", value="")
     email    = st.text_input("Guardian Email", value="")

     st.divider()
     st.write(f"**Name:** {name}")
     st.write(f"**Age:** {age}")
     st.write(f"**Gender:** {gender}")
     if guardian: st.write(f"**Guardian:** {guardian}")
     if phone:    st.write(f"**Phone:** {phone}")
     if email:    st.write(f"**Email:** {email}")

     st.divider()
     st.subheader("🚨 Emergency Numbers")
     st.write("🏥 Ambulance: **108**")
     st.write("👮 Police: **100**")
     st.write("🔥 Fire: **101**")
     st.write("🩺 Doctor Helpline: **104**")

     st.divider()
     st.subheader("🏥 Nearby Hospital")
     location = st.text_input("Your City / Area", value="", placeholder="Enter your city or area")
     if location:
            hospitals = suggest_nearby_hospitals(location)
            st.write("**Suggested nearby hospitals:**")
            for hospital in hospitals:
                st.write(f"- {hospital}")
     else:
         st.info("Enter your location to get nearby hospital suggestions.")

     st.divider()
     st.subheader("💧 Water Intake Today")
     glasses = st.slider("Glasses of water drank", 0, 12, 4)
     if glasses < 4:
            st.error("🔴 Drink more water!")
     elif glasses < 8:
            st.warning("🟡 Almost there, drink more!")
     else:
            st.success("✅ Great! Well hydrated!")

            st.divider()
     if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    # ── Page Title ───────────────────────────────────────────────────────────
    st.title("🩺 Patient Health Analyzer")
    health_tips = [
    "💧 Drink at least 8 glasses of water daily",
    "🚶 Walk 30 minutes every day",
    "🥦 Eat more vegetables and fruits",
    "😴 Sleep 7-8 hours every night",
    "🧘 Do meditation to reduce stress",
    "🚭 Avoid smoking and alcohol",
    "🏃 Exercise regularly to stay fit",
    "🩺 Visit doctor for yearly checkup",
]
    st.info(f"💡 Daily Health Tip: {random.choice(health_tips)}")
    st.caption(f"Patient: **{name}** | Age: **{age}** | Gender: **{gender}**")
    st.divider()

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Vitals", "🔬 Symptoms", "📊 Charts", "🏥 Health Monitor", "📋 Medical Records"])
    # ════════════════ TAB 1 — VITAL SIGNS ════════════════════════════════════
    with tab1:
        st.subheader("Enter Vital Signs — Old & New Readings")
        st.divider()

        col_old, col_new = st.columns(2)

        with col_old:
            st.subheader("📁 Old (Previous) Reading")
            heartrate_old  = st.number_input("Heart Rate (bpm)",      min_value=0, max_value=300, value=72,   key="hr_old")
            bp_old         = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=300, value=110,  key="bp_old")
            temperature_old= st.number_input("Temperature (°C)",      min_value=30.0, max_value=45.0, value=36.6, step=0.1, key="tmp_old")
            bmi_old        = st.number_input("Weight / BMI (kg)",     min_value=0.0, max_value=200.0, value=22.5, step=0.1, key="bmi_old")
            sugar_old      = st.number_input("Blood Sugar (mg/dL)",   min_value=0, max_value=600, value=115,  key="sug_old")

        with col_new:
            st.subheader("📁 New (Current) Reading")
            heartrate_new  = st.number_input("Heart Rate (bpm)",      min_value=0, max_value=300, value=78,   key="hr_new")
            bp_new         = st.number_input("Blood Pressure (mmHg)", min_value=0, max_value=300, value=118,  key="bp_new")
            temperature_new= st.number_input("Temperature (°C)",      min_value=30.0, max_value=45.0, value=37.1, step=0.1, key="tmp_new")
            bmi_new        = st.number_input("Weight / BMI (kg)",     min_value=0.0, max_value=200.0, value=23.0, step=0.1, key="bmi_new")
            sugar_new      = st.number_input("Blood Sugar (mg/dL)",   min_value=0, max_value=600, value=120,  key="sug_new")

        st.divider()
        st.subheader("📊 Health Analysis Results")

        # OLD Results
        st.write("#### 🗂️ Old Reading — Analysis")
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Heart Rate",    f"{heartrate_old} bpm",   check_heart_rate(heartrate_old))
        c2.metric("Blood Pressure",f"{bp_old} mmHg",         check_bp(bp_old))
        c3.metric("Temperature",   f"{temperature_old} °C",  check_temperature(temperature_old))
        c4.metric("BMI",           f"{bmi_old} kg",          check_bmi(bmi_old))
        c5.metric("Blood Sugar",   f"{sugar_old} mg/dL",     check_sugar(sugar_old))

        st.divider()

        # NEW Results
        st.write("#### 🗂️ New Reading — Analysis")
        d1, d2, d3, d4, d5 = st.columns(5)
        d1.metric(label="Heart Rate",     value=f"{heartrate_new} bpm",    delta=int(heartrate_new - heartrate_old))
        d1.caption(check_heart_rate(heartrate_new))
        d2.metric(label="Blood Pressure", value=f"{bp_new} mmHg",          delta=int(bp_new - bp_old))
        d2.caption(check_bp(bp_new))
        d3.metric(label="Temperature",    value=f"{temperature_new} °C",   delta=round(temperature_new - temperature_old, 1))
        d3.caption(check_temperature(temperature_new))
        d4.metric(label="BMI",            value=f"{bmi_new} kg",           delta=round(bmi_new - bmi_old, 1))
        d4.caption(check_bmi(bmi_new))
        d5.metric(label="Blood Sugar",    value=f"{sugar_new} mg/dL",      delta=int(sugar_new - sugar_old))
        d5.caption(check_sugar(sugar_new))

        st.divider()

        # Summary Table
        st.write("#### 📋 Summary Table")
        df = pd.DataFrame({
            "Metric"      : ["Heart Rate", "Blood Pressure", "Temperature", "BMI", "Blood Sugar"],
            "Old Value"   : [heartrate_old, bp_old, temperature_old, bmi_old, sugar_old],
            "Old Status"  : [check_heart_rate(heartrate_old), check_bp(bp_old),
                             check_temperature(temperature_old), check_bmi(bmi_old), check_sugar(sugar_old)],
            "New Value"   : [heartrate_new, bp_new, temperature_new, bmi_new, sugar_new],
            "New Status"  : [check_heart_rate(heartrate_new), check_bp(bp_new),
                             check_temperature(temperature_new), check_bmi(bmi_new), check_sugar(sugar_new)],
            "Change"      : [
                heartrate_new - heartrate_old,
                bp_new - bp_old,
                round(temperature_new - temperature_old, 1),
                round(bmi_new - bmi_old, 1),
                sugar_new - sugar_old,
            ],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ════════════════ TAB 2 — SYMPTOM CHECKER ════════════════════════════════
    with tab2:
        st.subheader("🔬 Symptom Checker")
        st.caption("Check all symptoms that apply to the patient.")
        st.divider()

        col1, col2, col3 = st.columns(3)
        with col1:
            fatigue            = st.checkbox("😴 Tiredness / Fatigue")
            chestpain          = st.checkbox("💔 Chest Pain")
            breathing_problem  = st.checkbox("😮‍💨 Breathing Problem")
            frequent_urination = st.checkbox("🚽 Frequent Urination")
            excessive_thirst   = st.checkbox("💧 Excessive Thirst")
            memory_loss        = st.checkbox("🧠 Memory Loss / Forgetfulness")
        with col2:
            tremors            = st.checkbox("🤝 Tremors / Shivering")
            body_pain          = st.checkbox("🤕 Body Pain")
            cough              = st.checkbox("😷 Persistent Cough")
            weight_loss        = st.checkbox("⚖️ Unexplained Weight Loss")
            lump               = st.checkbox("🔴 Lump Formation")
            headache           = st.checkbox("🤯 Severe Headache")
        with col3:
            anxiety            = st.checkbox("😰 Anxiety")
            sleeping_problem   = st.checkbox("😶 Sleeping Problem")
            swelling_legs      = st.checkbox("🦵 Swelling in Legs")
            yellow_skin        = st.checkbox("🟡 Yellow Skin")
            fever              = st.checkbox("🌡️ Prolonged Fever")

        st.divider()
        st.subheader("🏥 Disease Risk Analysis")

        symptoms = {
            "fatigue": fatigue, "chestpain": chestpain,
            "breathing_problem": breathing_problem, "frequent_urination": frequent_urination,
            "excessive_thirst": excessive_thirst, "memory_loss": memory_loss,
            "tremors": tremors, "body_pain": body_pain,
            "cough": cough, "weight_loss": weight_loss,
            "lump": lump, "headache": headache,
            "anxiety": anxiety, "sleeping_problem": sleeping_problem,
            "swelling_legs": swelling_legs, "yellow_skin": yellow_skin,
            "fever": fever,
        }

        disease_results = check_diseases(symptoms)

        if not disease_results:
            st.success("✅ No critical disease risk patterns detected based on current symptoms.")
        else:
            for disease, level, message, precaution in disease_results:
                if level == "error":
                    st.error(f"**{disease}**\n\n{message}\n\n💡 {precaution}")
                elif level == "warning":
                    st.warning(f"**{disease}**\n\n{message}\n\n💡 {precaution}")

            if st.button("⚕️ Send Disease Alert Message"):
                alert_text = "Disease Alert Message: " + " ".join(
                    [f"{disease} detected. {message}" for disease, _, message, _ in disease_results]
                )
                add_message(alert_text, category="Disease Prescription")
                st.success("✅ Disease alert message sent to the patient.")

        vitals = {
            "Heart Rate": heartrate_new,
            "Blood Pressure": bp_new,
            "Temperature": temperature_new,
            "BMI": bmi_new,
            "Blood Sugar": sugar_new,
        }
        try_auto_send_health_email(name, age, gender, vitals, disease_results)

        if not disease_results:
            st.info("🌿 Keep maintaining a healthy lifestyle with regular checkups.")

    # ════════════════ TAB 3 — CHARTS ═════════════════════════════════════════
    with tab3:
        st.subheader("📊 Old vs New — Vital Signs Charts")
        st.divider()

        metric_labels = ["Heart Rate", "Blood Pressure", "Temperature", "BMI", "Blood Sugar"]
        old_values    = [heartrate_old, bp_old, temperature_old, bmi_old, sugar_old]
        new_values    = [heartrate_new, bp_new, temperature_new, bmi_new, sugar_new]

        # ── Grouped Bar Chart (Old vs New) ───────────────────────────────────
        st.write("#### 📊 Comparison Bar Chart — Old vs New")
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(name="Old Report", x=metric_labels, y=old_values, marker_color="steelblue"))
        fig1.add_trace(go.Bar(name="New Report", x=metric_labels, y=new_values, marker_color="tomato"))
        fig1.update_layout(
            barmode="group",
            xaxis_title="Vital Sign",
            yaxis_title="Value",
            legend_title="Reading",
            height=400,
        )
        st.plotly_chart(fig1, use_container_width=True)

        st.divider()

        col_l, col_r = st.columns(2)

        # ── Old Report Bar ───────────────────────────────────────────────────
        with col_l:
            st.write("#### 🗂️ Old Report")
            fig2 = go.Figure(go.Bar(
                x=metric_labels, y=old_values,
                marker_color="steelblue",
                text=old_values, textposition="outside",
            ))
            fig2.update_layout(xaxis_title="Vital Sign", yaxis_title="Value", height=380)
            st.plotly_chart(fig2, use_container_width=True)

        # ── New Report Bar ───────────────────────────────────────────────────
        with col_r:
            st.write("#### 🗂️ New Report")
            fig3 = go.Figure(go.Bar(
                x=metric_labels, y=new_values,
                marker_color="tomato",
                text=new_values, textposition="outside",
            ))
            fig3.update_layout(xaxis_title="Vital Sign", yaxis_title="Value", height=380)
            st.plotly_chart(fig3, use_container_width=True)

        st.divider()

        # ── Change / Delta Chart ─────────────────────────────────────────────
        st.write("#### 📈 Change Chart (New − Old)")
        deltas = [round(new_values[i] - old_values[i], 2) for i in range(len(old_values))]
        colors = ["green" if d <= 0 else "red" for d in deltas]
        fig4 = go.Figure(go.Bar(
            x=metric_labels, y=deltas,
            marker_color=colors,
            text=[f"+{d}" if d > 0 else str(d) for d in deltas],
            textposition="outside",
        ))
        fig4.update_layout(
            xaxis_title="Vital Sign",
            yaxis_title="Change",
            height=380,
        )
        st.plotly_chart(fig4, use_container_width=True)
    # ════════════════ TAB 4 — HEALTH MONITOR ════════════════════════════════════
    # ════════════════ TAB 4 — HEALTH MONITOR ════════════════════════════════════
    with tab4:
     st.subheader("🏥 Health Monitor")
     st.divider()

     # ── Health Alert System ──────────────────────────────────────────────
     st.subheader("🔔 Health Alert")
     col_a1, col_a2, col_a3 = st.columns(3)
     with col_a1:
        alert_hr = st.number_input("Heart Rate", min_value=0, max_value=300, value=80, key="alert_hr")
     with col_a2:
        alert_bp = st.number_input("Blood Pressure", min_value=0, max_value=300, value=110, key="alert_bp")
     with col_a3:
        alert_sugar = st.number_input("Blood Sugar", min_value=0, max_value=600, value=120, key="alert_sugar")

     if alert_hr > 100 or alert_bp > 120 or alert_sugar > 140:
         st.error("🚨 ALERT! Vitals are abnormal! Please consult a doctor immediately!")
         issues, prescription = get_prescription(alert_hr, alert_bp, alert_sugar, 37.0)
         if issues:
             st.write("#### 💊 Auto Prescription")
             for p in prescription:
                 st.write(p)
         if st.session_state.get("recipient_email"):
             email_body = f"""
     🏥 HEALTH ALERT NOTIFICATION
     =============================
     Patient Name : {name}
     Age          : {age}
     Gender       : {gender}
     Date & Time  : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

     ⚠️ ISSUES DETECTED:
     {chr(10).join(f"• {issue}" for issue in issues)}

     💊 PRESCRIPTION & ADVICE:
     {chr(10).join(prescription)}

     📊 ABNORMAL VITALS:
     - Heart Rate     : {alert_hr} bpm
     - Blood Pressure : {alert_bp} mmHg
     - Blood Sugar    : {alert_sugar} mg/dL

     🏥 Please consult a doctor immediately!
     =============================
     Sent by Patient Health Analyzer App
             """
             last_sent     = st.session_state.get("last_alert_sent", "")
             current_alert = f"{alert_hr}{alert_bp}{alert_sugar}"
             if current_alert != last_sent:
                 with st.spinner("📧 Sending automatic alert email..."):
                     success, msg = send_email_notification(
                         recipient = st.session_state.recipient_email,
                         subject   = f"🚨 Health Alert — {name}",
                         body      = email_body,
                         sender    = st.session_state.sender_email,
                         password  = st.session_state.sender_password,
                     )
                 if success:
                     st.session_state.last_alert_sent = current_alert
                     st.success(f"✅ Alert email automatically sent to {st.session_state.recipient_email}!")
                     add_message(email_body, category="Health Alert")
                 else:
                     st.error(f"❌ Email failed! {msg}")
             else:
                 st.success(f"✅ Alert already sent to {st.session_state.recipient_email}!")
         else:
             st.warning("⚠️ No email setup! Please logout and setup email first!")

     elif alert_hr < 60 or alert_bp < 90:
         st.warning("⚠️ WARNING! Vitals are low! Please take rest!")
         if st.session_state.get("recipient_email"):
             low_body = f"""
     ⚠️ LOW VITALS WARNING
     =============================
     Patient Name : {name}
     Age          : {age}
     Date & Time  : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

     ⚠️ LOW VITALS DETECTED:
     - Heart Rate     : {alert_hr} bpm
     - Blood Pressure : {alert_bp} mmHg

     💊 ADVICE:
     - Sit down and rest immediately
     - Drink warm water
     - Eat small meals
     - Consult doctor if not improving

     🏥 Please take rest and monitor vitals!
     =============================
     Sent by Patient Health Analyzer App
             """
             last_low_sent = st.session_state.get("last_low_sent", "")
             current_low   = f"{alert_hr}{alert_bp}"
             if current_low != last_low_sent:
                 with st.spinner("📧 Sending low vitals alert..."):
                     success, msg = send_email_notification(
                         recipient = st.session_state.recipient_email,
                         subject   = f"⚠️ Low Vitals Warning — {name}",
                         body      = low_body,
                         sender    = st.session_state.sender_email,
                         password  = st.session_state.sender_password,
                     )
                 if success:
                     st.session_state.last_low_sent = current_low
                     st.success(f"✅ Low vitals alert sent to {st.session_state.recipient_email}!")
                 else:
                     st.error(f"❌ Email failed! {msg}")
             else:
                 st.success("✅ Low vitals alert already sent!")
         else:
             st.warning("⚠️ No email setup! Please logout and setup email first!")

     else:
         st.success("✅ All vitals are normal! You are healthy!")

     st.divider()
     # ── Medicine Reminder ────────────────────────────────────────────────
     st.subheader("💊 Medicine Reminder")

     if "medicines" not in st.session_state:
        st.session_state.medicines = []

     col_m1, col_m2, col_m3 = st.columns(3)
     with col_m1:
        med_name = st.text_input("Medicine Name", placeholder="Ex: Paracetamol")
     with col_m2:
        med_time = st.selectbox("Reminder Time", ["Morning", "Afternoon", "Evening", "Night"])
     with col_m3:
        med_dose = st.text_input("Dosage", placeholder="Ex: 1 tablet")

     if st.button("➕ Add Medicine"):
        if med_name and med_dose:
            st.session_state.medicines.append({
                "Medicine": med_name,
                "Time": med_time,
                "Dose": med_dose,
                "Done": False
            })
            add_message(
                f"Medicine Reminder: Take {med_dose} of {med_name} in the {med_time}.",
                category="Medicine Reminder"
            )
            st.success(f"✅ Medicine **{med_name}** added and reminder sent!")
        else:
            st.warning("⚠️ Please enter medicine name and dosage!")

     # Show medicines with checkbox
     if st.session_state.medicines:
        st.write("#### 💊 Medicine List")
        st.caption("✅ Check the box when medicine is taken — it will be deleted!")
        to_delete = []
        for i, med in enumerate(st.session_state.medicines):
            col1, col2 = st.columns([1, 5])
            with col1:
                done = st.checkbox("Done", key=f"med_{i}")
            with col2:
                st.write(f"💊 **{med['Medicine']}** — {med['Dose']} — {med['Time']}")
            if done:
                to_delete.append(i)

        # Delete completed medicines
        if to_delete:
            st.session_state.medicines = [
                med for i, med in enumerate(st.session_state.medicines)
                if i not in to_delete
            ]
            st.success("✅ Medicine taken and removed!")
            st.rerun()

     st.divider()

     
     # ── BMI & Fitness ────────────────────────────────────────────────────
     st.subheader("🏋️ BMI & Fitness")
     col_b1, col_b2 = st.columns(2)
     with col_b1:
        bmi_weight = st.number_input("Weight (kg)", min_value=1, max_value=200, value=60, key="bmi_weight")
     with col_b2:
        bmi_height = st.number_input("Height (cm)", min_value=50, max_value=250, value=170, key="bmi_height")

     bmi_result = round(bmi_weight / ((bmi_height / 100) ** 2), 2)
     st.write(f"### Your BMI: **{bmi_result}**")

     if bmi_result < 18.5:
        st.warning("⚠️ Underweight — Eat more nutritious food")
        st.info("💡 Eat protein rich foods like eggs, milk, nuts")
        st.info("💡 Do light weight training")
     elif 18.5 <= bmi_result <= 24.9:
        st.success("✅ Normal Weight — Keep it up!")
        st.info("💡 Walk 30 minutes daily")
        st.info("💡 Drink 8 glasses of water")
     elif 25 <= bmi_result <= 29.9:
        st.warning("⚠️ Overweight — Start exercising")
        st.info("💡 Do cardio exercise daily")
        st.info("💡 Avoid junk food and sweets")
     else:
        st.error("🔴 Obese — Consult a doctor immediately")
        st.info("💡 Start with light walking")
        st.info("💡 Avoid oily and fatty foods")

   # ════════════════ TAB 5 — MEDICAL RECORDS ═══════════════════════════════════
    with tab5:
     st.subheader("📋 Medical Records")
     st.divider()

     # ── Doctor Appointment ───────────────────────────────────────────────
     st.subheader("🩺 Doctor Appointment")

     if "appointments" not in st.session_state:
        st.session_state.appointments = []

     col_d1, col_d2, col_d3 = st.columns(3)
     with col_d1:
        doc_name = st.text_input("Doctor Name", placeholder="Ex: Dr. Smith")
     with col_d2:
        doc_date = st.date_input("Appointment Date")
     with col_d3:
        doc_reason = st.text_input("Reason", placeholder="Ex: Regular Checkup")

     if st.button("📅 Save Appointment"):
        if doc_name and doc_reason:
            st.session_state.appointments.append({
                "Doctor": doc_name,
                "Date": str(doc_date),
                "Reason": doc_reason,
                "Done": False
            })
            st.success(f"✅ Appointment saved with **{doc_name}**!")
        else:
            st.warning("⚠️ Please enter doctor name and reason!")

     # Show appointments with checkbox
     if st.session_state.appointments:
        st.write("#### 📅 Appointment List")
        st.caption("✅ Check the box when appointment is completed — it will be deleted!")
        to_delete_app = []
        for i, app in enumerate(st.session_state.appointments):
            col1, col2 = st.columns([1, 5])
            with col1:
                done = st.checkbox("Done", key=f"app_{i}")
            with col2:
                st.write(f"🩺 **{app['Doctor']}** — {app['Date']} — {app['Reason']}")
            if done:
                to_delete_app.append(i)

        # Delete completed appointments
        if to_delete_app:
            st.session_state.appointments = [
                app for i, app in enumerate(st.session_state.appointments)
                if i not in to_delete_app
            ]
            st.success("✅ Appointment completed and removed!")
            st.rerun()

     st.divider()

    

     # ── Patient History Tracker ──────────────────────────────────────────
     st.subheader("📊 Patient History Tracker")
     st.caption("Track your health readings over time!")

     if "history" not in st.session_state:
        st.session_state.history = []

     col_h1, col_h2, col_h3 = st.columns(3)
     with col_h1:
        hist_date  = st.date_input("Date", key="hist_date")
        hist_hr    = st.number_input("Heart Rate",     min_value=0, max_value=300, value=80,  key="hist_hr")
     with col_h2:
        hist_bp    = st.number_input("Blood Pressure", min_value=0, max_value=300, value=110, key="hist_bp")
        hist_sugar = st.number_input("Blood Sugar",    min_value=0, max_value=600, value=120, key="hist_sugar")
     with col_h3:
        hist_temp  = st.number_input("Temperature",    min_value=30.0, max_value=45.0, value=36.6, step=0.1, key="hist_temp")
        hist_note  = st.text_input("Note", placeholder="Ex: After exercise")

     if st.button("➕ Add to History"):
        st.session_state.history.append({
            "Date"    : str(hist_date),
            "HR"      : hist_hr,
            "BP"      : hist_bp,
            "Sugar"   : hist_sugar,
            "Temp"    : hist_temp,
            "Note"    : hist_note
        })
        st.success("✅ Health reading added to history!")

     if st.session_state.history:
        st.write("#### 📋 Health History")
        hist_df = pd.DataFrame(st.session_state.history)
        st.dataframe(hist_df, use_container_width=True, hide_index=True)

        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.success("✅ History cleared!")
# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    show_login()
elif not st.session_state.get("email_setup", False):
    show_email_setup()
else:
    show_dashboard()
