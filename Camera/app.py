import streamlit as st
import cv2
import requests
import pandas as pd
import time
from ultralytics import YOLO
from collections import deque
from datetime import datetime
import joblib
import plotly.graph_objects as go
from twilio.rest import Client
import smtplib
from email.mime.text import MIMEText

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Smart Crowd AI", layout="wide")

st.title("🚀 Smart Crowd Monitoring & Prediction System")

camera_url = "http://10.103.115.201:81/stream"
sensor_url = "http://10.103.115.154/data"

# ESP32 DEVICE URLS
buzzer_url = "http://10.103.115.154/buzzer?state="
green_led_url = "http://10.103.115.154/green?state="
yellow_led_url = "http://10.103.115.154/yellow?state="
red_led_url = "http://10.103.115.154/red?state="

# ---------------------------
# Twilio WhatsApp Config
# ---------------------------
TWILIO_SID = "YOUR_TWILIO_SID"
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"

WHATSAPP_FROM = "YOUR_TWILIO_WHATSAPP_NUMBER"   # Twilio sandbox
WHATSAPP_TO = "YOUR_PERSONAL_WHATSAPP_NUMBER"    # Your WhatsApp number

# ---------------------------
# Email Config
# ---------------------------
EMAIL_ADDRESS = "YOUR_EMAIL_ADDRESS"
EMAIL_PASSWORD = "YOUR_EMAIL_PASSWORD"
ALERT_EMAIL = "ALERT_RECEIVER_EMAIL_ADDRESS"

# ---------------------------
# SESSION STATE
# ---------------------------
if "logs" not in st.session_state:
    st.session_state.logs = []

if "history" not in st.session_state:
    st.session_state.history = deque(maxlen=20)

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = 0

if "buzzer_end_time" not in st.session_state:
    st.session_state.buzzer_end_time = 0

if "buzzer_active" not in st.session_state:
    st.session_state.buzzer_active = False

ALERT_COOLDOWN = 60

# ---------------------------
# LOAD MODELS
# ---------------------------
yolo_model = YOLO("yolov8n.pt")

predict_model = joblib.load(
    r"C:\Users\Admin\Downloads\Croud Mini project\Pickel file\best_xgb.pkl"
)

# ---------------------------
# CAMERA
# ---------------------------
cap = cv2.VideoCapture(camera_url)

# ---------------------------
# ALERT FUNCTIONS
# ---------------------------
def send_whatsapp(msg):

    try:

        Client(
            TWILIO_SID,
            TWILIO_AUTH_TOKEN
        ).messages.create(

            body=msg,
            from_=WHATSAPP_FROM,
            to=WHATSAPP_TO

        )

    except:
        pass


def send_email(msg):

    try:

        m = MIMEText(msg)

        m["Subject"] = "🚨 Crowd Alert"
        m["From"] = EMAIL_ADDRESS
        m["To"] = ALERT_EMAIL

        s = smtplib.SMTP("smtp.gmail.com", 587)

        s.starttls()

        s.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        s.sendmail(
            EMAIL_ADDRESS,
            ALERT_EMAIL,
            m.as_string()
        )

        s.quit()

    except:
        pass

# ---------------------------
# AI ALERT CONTROL
# ---------------------------
def control_ai_alerts(count):

    try:

        now = time.time()

        # -----------------------------
        # SEND CAMERA COUNT TO ESP32
        # -----------------------------
        try:

            requests.get(
                f"http://10.103.115.154/update?count={count}",
                timeout=0.5
            )

        except:
            pass

        # -----------------------------
        # RESET LEDS
        # -----------------------------
        requests.get(green_led_url + "off", timeout=1)
        requests.get(yellow_led_url + "off", timeout=1)
        requests.get(red_led_url + "off", timeout=1)

        # -----------------------------
        # 🟢 SAFE
        # -----------------------------
        if count < 5:

            requests.get(green_led_url + "on", timeout=1)

            requests.get(buzzer_url + "off", timeout=1)

            st.session_state.buzzer_active = False

        # -----------------------------
        # 🟡 MEDIUM
        # -----------------------------
        elif count < 10:

            requests.get(yellow_led_url + "on", timeout=1)

            requests.get(buzzer_url + "off", timeout=1)

            st.session_state.buzzer_active = False

        # -----------------------------
        # 🔴 HIGH (3 sec)
        # -----------------------------
        elif count < 15:

            requests.get(red_led_url + "on", timeout=1)

            if not st.session_state.buzzer_active:

                requests.get(buzzer_url + "on", timeout=1)

                st.session_state.buzzer_end_time = now + 3

                st.session_state.buzzer_active = True

        # -----------------------------
        # 🔴 VERY HIGH (5 sec)
        # -----------------------------
        elif count < 20:

            requests.get(red_led_url + "on", timeout=1)

            if not st.session_state.buzzer_active:

                requests.get(buzzer_url + "on", timeout=1)

                st.session_state.buzzer_end_time = now + 5

                st.session_state.buzzer_active = True

        # -----------------------------
        # 🚨 DANGER (CONTINUOUS)
        # -----------------------------
        else:

            requests.get(red_led_url + "on", timeout=1)

            requests.get(buzzer_url + "on", timeout=1)

            st.session_state.buzzer_active = False

        # -----------------------------
        # STOP TIMED BUZZER
        # -----------------------------
        if st.session_state.buzzer_active:

            if now >= st.session_state.buzzer_end_time:

                requests.get(
                    buzzer_url + "off",
                    timeout=1
                )

                st.session_state.buzzer_active = False

    except Exception as e:

        print("AI Alert Error:", e)

# ---------------------------
# SIDEBAR
# ---------------------------
run = st.sidebar.toggle(
    "Start Monitoring",
    True
)

alert_threshold = st.sidebar.slider(
    "Alert Threshold",
    5,
    20,
    10
)

alerts_enabled = st.sidebar.checkbox(
    "Enable Alerts",
    True
)

max_capacity = st.sidebar.slider(
    "Max Capacity",
    20,
    200,
    50
)

# ---------------------------
# UI PLACEHOLDERS
# ---------------------------
video = st.empty()

metrics = st.empty()

trend_box = st.empty()

gauge = st.empty()

chart = st.empty()

table = st.empty()

# ---------------------------
# MAIN LOOP
# ---------------------------
while run:

    success, frame = cap.read()

    if not success:

        st.warning("Camera not connected")

        break

    frame = cv2.resize(
        frame,
        (640, 480)
    )

    results = yolo_model(frame)

    count = 0

    # ---------------------------
    # PERSON DETECTION
    # ---------------------------
    for r in results:

        for box in r.boxes:

            if int(box.cls[0]) == 0 and box.conf[0] > 0.5:

                count += 1

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

    # DISPLAY COUNT
    cv2.putText(
        frame,
        f"Count: {count}",
        (10, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        3
    )

    frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    video.image(frame)

    # ---------------------------
    # AI ALERT CONTROL
    # ---------------------------
    control_ai_alerts(count)

    # ---------------------------
    # SENSOR DATA
    # ---------------------------
    try:

        d = requests.get(
            sensor_url,
            timeout=0.5
        ).json()

        entry = d["entry"]

        exit_count = d["exit"]

        total = d["total"]

    except:

        entry = 0
        exit_count = 0
        total = 0

    # ---------------------------
    # HISTORY
    # ---------------------------
    st.session_state.history.append(count)

    prev = (
        st.session_state.history[-2]
        if len(st.session_state.history) > 1
        else count
    )

    density = count / max_capacity

    change = count - prev

    # ---------------------------
    # MODEL INPUT
    # ---------------------------
    df_input = pd.DataFrame({

        "IR_Count": [entry],

        "Camera_Count": [count],

        "Total_Count": [count],

        "Density": [density],

        "Prev_Total_Count": [prev],

        "Count_Change": [change]

    })

    # ---------------------------
    # FUTURE PREDICTION
    # ---------------------------
    try:

        future_growth = 0

        if change > 0:

            future_growth = abs(change) * 1.5

        elif change == 0:

            future_growth = 1

        else:

            future_growth = change * 0.5

        pred = int(count + future_growth)

        if pred < 0:
            pred = 0

    except:

        pred = count

    occupancy = (count / max_capacity) * 100

    # ---------------------------
    # ALERTS
    # ---------------------------
    now = time.time()

    if (
        alerts_enabled
        and count >= alert_threshold
        and now - st.session_state.last_alert_time > ALERT_COOLDOWN
    ):

        msg = (
            f"🚨 Crowd Alert\n\n"
            f"Current Count: {count}\n"
            f"Predicted Count: {pred}\n"
            f"Occupancy: {round(occupancy,2)}%"
        )

        send_whatsapp(msg)

        send_email(msg)

        st.session_state.last_alert_time = now

    # ---------------------------
    # UI METRICS
    # ---------------------------
    with metrics.container():

        st.subheader("📊 Crowd Monitoring Metrics")

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("📥 Entry", entry)

        c2.metric("📤 Exit", exit_count)

        c3.metric("📊 IR Total", total)

        c4.metric("🎥 Camera Count", count)

        d1, d2, d3, d4 = st.columns(4)

        d1.metric("🔮 Future Prediction", pred)

        d2.metric(
            "📈 Occupancy %",
            round(occupancy, 2)
        )

        d3.metric("📉 Change", change)

        d4.metric(
            "📌 Density",
            round(density, 2)
        )

    # ---------------------------
    # TREND
    # ---------------------------
    trend_box.info(

        f"Trend: {'📈 Increasing Crowd' if pred > count else '📉 Stable/Decreasing Crowd'}"

    )

    # ---------------------------
    # GAUGE
    # ---------------------------
    fig = go.Figure(

        go.Indicator(

            mode="gauge+number",

            value=occupancy,

            title={'text': "Occupancy %"},

            gauge={
                'axis': {
                    'range': [0, 100]
                }
            }

        )
    )

    gauge.plotly_chart(
        fig,
        use_container_width=True,
        key=f"gauge_{time.time()}"
    )

    # ---------------------------
    # LOGGING
    # ---------------------------
    t = datetime.now().strftime("%H:%M:%S")

    st.session_state.logs.append([
        t,
        count,
        pred,
        occupancy
    ])

    df = pd.DataFrame(

        st.session_state.logs,

        columns=[
            "Time",
            "Current",
            "Predicted",
            "Occupancy"
        ]
    )

    chart.line_chart(
        df.set_index("Time")
    )

        # ---------------------------
    # SAVE COMPLETE LOGS
    # ---------------------------
    df.to_csv(
        "crowd_logs.csv",
        index=False
    )

    # ---------------------------
    # SHOW LAST 20 ROWS ONLY
    # ---------------------------
    table.dataframe(
        df.tail(20),
        use_container_width=True
    )

   

    cv2.waitKey(1)