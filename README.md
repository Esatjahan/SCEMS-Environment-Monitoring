# Mst. Esat Jahan Akhi  
# SCEMS - Smart Community Environment Monitoring System

This repository contains the **software-only implementation** of  
**SCEMS (Smart Community Environment Monitoring System)**  
for the **UFTB Robotics Club – IoT & Robotics Contest 2025 (Senior Category)**.

---

## 📌 Problem Overview

Gazipur’s Hi-Tech Industrial Zone faces:
- Poor air quality  
- Rapid heat stress  
- Unstable soil moisture  
- Overcrowded public transport points  
- Night-time security risks  
- High energy waste due to static street lighting  

SCEMS monitors these factors using simulated virtual sensors in **Wokwi** and performs alert classification with a **Python backend**.

---

## 🗂 Project Structure

SCEMS-Gazipur/  
&nbsp;&nbsp;wokwi/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Arduino/Wokwi simulation  
&nbsp;&nbsp;backend/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Python threshold engine + dashboard  
&nbsp;&nbsp;docs/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Report + screenshots + final PDF  
&nbsp;&nbsp;logs/ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Stored CSV logs  
&nbsp;&nbsp;README.md

---

## 🎯 Contest Requirements Mapping

**Section A – Simulation (Wokwi + Arduino)**  
✔ A1 Soil moisture  
✔ A2 Temperature & humidity  
✔ A3 AQI mock sensor  
✔ A4 Crowd density  
✔ A5 Security (PIR + Sound)  
✔ A6 Adaptive lighting  

**Section B – Python Threshold Logic**  
✔ Full logic implemented in `threshold_engine.py`

**Section C – Integration & Dashboard**  
✔ Streamlit dashboard  
✔ Realtime charts  
✔ Priority evaluation  
✔ Logs to CSV

**Section D – Documentation**  
✔ REPORT.md  
✔ Screenshots  
✔ Final PDF  
✔ TASKS.md (progress record)

**Section E – Big Idea**  
✔ Simulation-based community monitoring concept

---

## 🚀 How to Run

### 🔹 Wokwi Simulation  

Circuit + Serial Monitor:  
https://wokwi.com/projects/448685686274316289  

### 🔹 Python Backend + Dashboard

(From project root)

1. Open terminal / Git Bash  
2. Run:

    cd backend  
    pip install -r requirements.txt  
    streamlit run dashboard_app.py  

---

## 🧪 Features Demonstrated

- Threshold engine for each sensor  
- Global priority evaluation (CRITICAL / HIGH / MEDIUM / LOW)  
- Temperature, humidity, AQI, soil, crowd analytics  
- CSV logging  
- Dashboard visualization  

---

## 🎬 Demo Video (Google Drive)

You can watch the full project demonstration here:

Demo Video Link:  
https://drive.google.com/drive/folders/1hMPlVeWZghY3mUDQZwAU2zho7XbX1x9D?usp=drive_link

---

## 📄 Final Report (PDF)

PDF File (inside this repo):  
docs/Final_Report/EsatJahan_SCEMS.pdf

---

## 🔗 Important Links

- GitHub Repository:  
  https://github.com/Esatjahan/SCEMS-Environment-Monitoring  

- Wokwi Project:  
  https://wokwi.com/projects/448685686274316289  

- Demo Video (Google Drive):  
  https://drive.google.com/drive/folders/1hMPlVeWZghY3mUDQZwAU2zho7XbX1x9D?usp=drive_link  

---

## 👩‍💻 Author

**Mst. Esat Jahan Akhi**

SCEMS — A complete environment monitoring prototype via software simulation.
