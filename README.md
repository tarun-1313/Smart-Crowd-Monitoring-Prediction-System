# 🚀 Smart Crowd Monitoring & Prediction System using YOLOv8, IoT & Machine Learning

> AI-powered real-time crowd monitoring, analysis, and prediction system using **YOLOv8, ESP32 IoT sensors, XGBoost, and Streamlit Dashboard** with automated **WhatsApp & Email alerts**.

---

# 📌 Project Overview

The **Smart Crowd Monitoring & Prediction System** is an intelligent surveillance and analytics platform developed for real-time crowd monitoring in public areas such as:

- Railway Stations
- Airports
- Shopping Malls
- Stadiums
- Colleges
- Smart Cities
- Festivals & Public Events

The system combines:

- Computer Vision
- Machine Learning
- IoT Sensors
- Real-Time Analytics
- Alert Automation

to detect current crowd density and predict future crowd conditions proactively.

---

# 🧠 Key Features

## ✅ Real-Time Crowd Detection
- YOLOv8-based person detection
- Real-time crowd counting
- Bounding-box visualization
- Live ESP32-CAM video streaming

## ✅ IoT Sensor Integration
- IR sensors for entry/exit detection
- Ultrasonic sensors for density estimation
- ESP32 microcontroller communication

## ✅ Crowd Prediction using Machine Learning
- Predicts future crowd count
- Uses historical + live crowd data
- Trained using multiple ML algorithms

## ✅ Interactive Streamlit Dashboard
- Live monitoring dashboard
- Occupancy gauge
- Crowd analytics
- Trend visualization
- Real-time graphs

## ✅ Smart Alert System
- WhatsApp alerts
- Email alerts
- Buzzer activation
- LED warning indicators

## ✅ Data Analytics
- Current vs predicted graphs
- Crowd density analytics
- Occupancy percentage
- Residual error analysis
- Model comparison charts

## ✅ CSV Export
- Download monitoring logs
- Export crowd analytics

---

# 🏗️ System Architecture

The system architecture integrates:

- ESP32
- ESP32-CAM
- IR Sensors
- Ultrasonic Sensors
- YOLOv8
- XGBoost
- Streamlit Dashboard
- Mobile Alert System

---

# ⚙️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Development |
| Streamlit | Interactive Dashboard |
| YOLOv8 | Real-Time Crowd Detection |
| OpenCV | Video Processing |
| ESP32 | IoT Communication |
| ESP32-CAM | Live Video Streaming |
| IR Sensors | Entry/Exit Detection |
| Ultrasonic Sensor | Density Measurement |
| XGBoost | Crowd Prediction |
| Random Forest | ML Comparison |
| Linear Regression | Baseline Prediction |
| LSTM | Time-Series Prediction |
| Twilio API | WhatsApp Alerts |
| SMTP | Email Alerts |
| Plotly | Occupancy Gauge |
| Pandas | Data Processing |
| Matplotlib | Visualization |
| Seaborn | Heatmaps |

---

# 🧠 Machine Learning Models Used

The project trained and evaluated multiple ML algorithms for crowd prediction:

| Model | Purpose |
|---|---|
| Linear Regression | Baseline prediction |
| Random Forest | Ensemble prediction |
| XGBoost | Final optimized prediction model |
| LSTM | Time-series crowd forecasting |

---

# 🥇 Best Model Used

## ✅ XGBoost (Final Selected Model)

XGBoost achieved the best overall performance among all models and was selected as the final deployed prediction model.

### Why XGBoost?
- Highest accuracy
- Lowest prediction error
- Better feature optimization
- Handles nonlinear crowd patterns effectively
- Fast inference for real-time deployment

---

# 📊 Model Accuracy Comparison

| Model | R² Score | RMSE | MAE |
|---|---|---|---|
| Linear Regression | 0.9420 | 1.0830 | 0.8716 |
| Random Forest | 0.9493 | 1.0131 | 0.8364 |
| **XGBoost** | **0.9498** | **1.0079** | **0.8339** |
| LSTM | 0.9473 | 1.0324 | 0.8475 |

---

# 📈 Model Evaluation

The project includes:

- Actual vs Predicted Graph
- Residual Error Distribution
- Crowd Distribution Analysis
- Final Accuracy Comparison

The XGBoost model achieved:
- **R² Score = 0.9498**
- Lowest RMSE
- Lowest MAE

demonstrating highly accurate crowd prediction performance.

---

# 🎥 Crowd Detection Methodology

## Step 1 — Video Capture
ESP32-CAM captures real-time video stream.

## Step 2 — YOLOv8 Detection
YOLOv8 detects and counts people from frames in real time.

## Step 3 — Sensor Data Collection
IR and ultrasonic sensors collect movement and density data.

## Step 4 — Crowd Density Estimation
Vision + sensor data are combined for improved counting accuracy.

## Step 5 — ML Prediction
XGBoost predicts future crowd density using:
- Camera Count
- IR Count
- Density
- Previous Crowd Count
- Crowd Change Rate

## Step 6 — Alert Generation
Alerts are generated if crowd exceeds threshold.

---

# 📊 Dashboard Features

## 🎥 Live Monitoring
- Real-time video feed
- YOLO detection overlay
- Live crowd count

## 📈 Crowd Analytics
- Current crowd
- Predicted crowd
- Occupancy %
- Density score

## 📊 Occupancy Gauge
Visual occupancy indicator using Plotly.

## 📋 Data Table
Recent monitoring records and logs.

## 📉 Trend Analysis
Current vs predicted crowd graph.

## 🚨 Alert Panel
- High-risk notifications
- Email alerts
- WhatsApp alerts
- Buzzer activation

---

# 🚨 Alert System

The system sends automatic alerts when crowd exceeds threshold.

### Alert Channels
- WhatsApp
- Email
- Buzzer
- LED Indicators

### Safety Mechanism
- Alert cooldown implemented
- Prevents spam notifications

---

# 📂 Dataset Information

| Feature | Description |
|---|---|
| Timestamp | Time of data |
| IR_Count | IR sensor count |
| Camera_Count | Camera detected crowd |
| Total_Count | Combined crowd count |
| Density | Crowd density |
| Next_Count | Future crowd count |

---

# 📦 Project Structure

```bash
Smart-Crowd-Monitoring/
│
├── Camera/
│   ├── app.py
│
├── Pickel file/
│   ├── best_xgb.pkl
│
├── notebooks/
│   ├── crowd_prediction_training.ipynb
│   ├── crowd_analysis.ipynb
│
├── screenshots/
│   ├── dashboard.png
│   ├── detection.png
│
├── dataset/
│   ├── crowd_dataset.csv
│
├── requirements.txt
├── README.md
└── LICENSE


▶️ Installation
Clone Repository
git clone https://github.com/yourusername/smart-crowd-monitoring.git
cd smart-crowd-monitoring
📦 Install Dependencies
pip install -r requirements.txt
▶️ Run Project
streamlit run app.py
📋 Required Libraries
pip install streamlit ultralytics opencv-python pandas matplotlib seaborn plotly requests joblib twilio scikit-learn xgboost
📓 Jupyter Notebooks

The project also includes Jupyter notebooks for:

Data preprocessing
Feature engineering
Model training
Hyperparameter tuning
Crowd prediction analysis
XGBoost training
📈 Results

The system successfully achieved:

Accurate real-time crowd detection
High prediction accuracy
Automated alerts
Real-time analytics dashboard

XGBoost performed best after hyperparameter tuning using GridSearchCV.

🔮 Future Enhancements
🔪 Weapon Detection
🧠 AI Anomaly Detection
📱 Mobile App
☁ Cloud Deployment
🛰 Drone-based Surveillance
👥 Multi-camera Support
🏙 Smart City Integration
😀 Face Recognition
🎯 Applications
Smart Cities
Crowd Safety Systems
Railway Stations
Airports
Stadiums
Shopping Malls
Festivals
Emergency Management
Public Surveillance
👨‍💻 Authors
Tarun Hemraj Chaudhari

📚 References
IoT and Machine Learning based Smart Emergency Management System
Chipless RFID Based Crowd Monitoring for Hajj Pilgrimage
Synthetic Data Generation for Crowd Management using Deep Learning
CNN-Based Real-Time People Counting System
Anomaly Detection in Crowded Environments using Deep Learning
⭐ GitHub Topics
python
streamlit
yolov8
computer-vision
machine-learning
iot
crowd-monitoring
opencv
xgboost
esp32
smart-surveillance
deep-learning
📜 License

This project is developed for educational and research purposes.
