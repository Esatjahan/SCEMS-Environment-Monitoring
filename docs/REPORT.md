# Mst.Esat Jahan Akhi
# SCEMS - Smart Community Environment Monitoring System

## 1. Introduction

- Problem background (Gazipur industrial area, issues)
- Objectives of SCEMS
- Scope (simulation-only, no physical hardware)

The Hi-Tech industrial area in Gazipur is facing serious environmental
and safety challenges such as poor air quality, rapid temperature rise,
unstable soil moisture, overcrowded public transport stops and night-time
security risks.

The SCEMS (Smart Community Environment Monitoring System) project
implements a **simulation-based multi-sensor platform** that can monitor:

- Soil moisture (for irrigation and plant health)
- Temperature & humidity (for worker heat stress)
- Air Quality Index (AQI)
- Crowd density at public locations
- Security events (PIR + sound)
- Ambient light levels for adaptive street lighting

In this implementation, all sensors are simulated using **Wokwi (Arduino)**
and **Python-based backend** without any physical hardware, which makes it
easy to test multiple scenarios for the contest.

## 2. System Architecture

- High-level block diagram:
  - User side (simulation input)
  - Simulation engine
  - Backend dashboard 
- Description of each block

The overall SCEMS architecture has three main layers:

1. **Sensor Simulation Layer (Wokwi / Arduino)**
   - Multiple virtual sensors are connected to an Arduino UNO in Wokwi:
     - Soil moisture (potentiometer → A0)
     - AQI mock sensor (potentiometer → A1)
     - Sound level (potentiometer → A2)
     - LDR + resistor (light sensor → A3)
     - DHT22 (temperature + humidity → D2)
     - HC-SR04 ultrasonic sensor (crowd distance → D3/D4)
     - PIR sensor (motion → D5)
     - LED (adaptive street light → D6)
   - The Arduino code (`wokwi/code.ino`) generates a frame of sensor readings
     and evaluates basic thresholds for each frame.

2. **Backend Simulation & Threshold Engine (Python)**
   - `threshold_engine.py` defines a `SensorFrame` dataclass and all
     threshold rules for soil, heat, AQI, crowd, security and lighting.
   - `sensors_simulation.py` generates synthetic frames that follow the
     same ranges as the Arduino side and calls `evaluate_all()`.
   - `log_to_csv.py` creates historical logs in `logs/system_logs.csv`.

3. **Dashboard & Analytics Layer (Streamlit)**
   - `dashboard_app.py` runs a Streamlit web app that:
     - Generates multiple synthetic frames
     - Evaluates alerts using the threshold engine
     - Displays live data table and multiple trend charts
     - Shows alert priority distribution and latest alert snapshot.


## 3. Sensor Simulation Pipeline

- Soil moisture
- Temperature & humidity
- AQI (mocked)
- Crowd density (ultrasonic)
- Security (PIR + sound)
- Adaptive lighting (LDR)
- Tools used: Wokwi + Python scripts

## 4. Threshold Rules & Algorithms

- Soil moisture thresholds (Alert/Warning/OK)
- Heat index formula + stress levels
- AQI classification categories
- Crowd density levels
- Security logic (PIR + sound)
- Night lighting logic (LDR)
- Noise filtering (EMA/Kalman if used) 

## 5. Dashboard UI Flow & Analytics

- Description of dashboard pages
- Real-time charts
- Alert state panel
- Health analytics
- Event summary graphs 

## 6. Test Cases & Results

- Section A test cases (A1–A6) – table of inputs vs outputs 
- Section B alert logic test scenarios
- Screenshots of successful runs

## 7. Logs & Graphs

- Sample log format (CSV fields)
- Historical trend graphs
- Discussion of patterns

A separate Python script `backend/log_to_csv.py` is used to generate
historical logs for the SCEMS system.

- Each log frame includes:
  - Raw sensor values (soil_moisture, temperature, humidity, aqi, crowd_estimate, etc.)
  - Evaluated statuses (soil_status, heat_status, aqi_status, crowd_status,
    security_status, light_status)
  - A global priority label (LOW / MEDIUM / HIGH / CRITICAL)
  - A timestamp (ISO format)

- The logs are saved in: `logs/system_logs.csv`

These logs can be used to:

- Plot historical trends such as:
  - Temperature vs time
  - Soil moisture vs time
  - AQI vs time
  - Crowd estimate vs time
- Analyse how often each alert level appears over a given period.
- Support future work such as ML-based prediction or anomaly detection.

## 8. Big Idea & Future Work (Bonus)

- Environmental & social impact
- How SCEMS can scale in real community
- Possible ML/AI/cloud/blockchain extensions 

## 9. Links

- GitHub Repository: https://github.com/Esatjahan/SCEMS-Environment-Monitoring
- Wokwi Project: (https://wokwi.com/projects/448685686274316289)
- Demo Video (Google Drive): (to be added)
