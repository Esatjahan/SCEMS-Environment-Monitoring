# SCEMS - Smart Community Environment Monitoring System

## 1. Introduction

- Problem background (Gazipur industrial area, issues)
- Objectives of SCEMS
- Scope (simulation-only, no physical hardware)

## 2. System Architecture

- High-level block diagram:
  - User side (simulation input)
  - Simulation engine
  - Backend dashboard 
- Description of each block

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

## 8. Big Idea & Future Work (Bonus)

- Environmental & social impact
- How SCEMS can scale in real community
- Possible ML/AI/cloud/blockchain extensions 

## 9. Links

- GitHub Repository: https://github.com/Esatjahan/SCEMS-Environment-Monitoring
- Wokwi Project: (https://wokwi.com/projects/448685686274316289)
- Demo Video (Google Drive): (to be added)
