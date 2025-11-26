# Mst.Esat Jahan Akhi
# SCEMS - Smart Community Environment Monitoring System


This repository contains the **software-only implementation** of the  
**Smart Community Environment Monitoring System (SCEMS)** for the  
**UFTB Robotics Club Monthly IoT & Robotics Contest 2025 (Senior Category)**.

## 📌 Problem Overview

The Hi-Tech industrial area in Gazipur is facing:
- Poor air quality  
- Rapid temperature rise and worker heat stress  
- Unstable soil moisture damaging community crop beds  
- Night security risks  
- Overcrowded public transport stops  
- High energy waste due to inefficient street lighting   

SCEMS is a **simulation-based multi-sensor monitoring system** that tracks:
- Soil moisture  
- Temperature & humidity (heat stress)  
- Air Quality Index (AQI)  
- Crowd density (ultrasonic)  
- Security (PIR + sound)  
- Adaptive lighting (LDR)   

## 🗂 Project Structure

```text
SCEMS-Gazipur/
  wokwi/                 # Arduino/Wokwi circuit + simulation code
  backend/               # Python simulation engine + dashboard
  docs/                  # Report, diagrams, screenshots
  logs/                  # Sample log files (CSV)
  README.md
