"""
threshold_engine.py

This module contains all the threshold rules and alert logic
for the SCEMS project (matches Section B of the contest).
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SensorFrame:
    """
    A single snapshot of all sensor readings.
    Units are chosen to roughly match the Arduino/Wokwi side.
    """
    soil_moisture: float        # percentage (0-100)
    temperature: float          # °C
    humidity: float             # %
    aqi: int                    # Air Quality Index (0-500 approx)
    crowd_estimate: int         # estimated number of people
    pir_active: bool            # motion detected
    sound_level: int            # 0-100 relative
    ldr_raw: int                # 0-1023 raw value
    is_night: bool              # derived from LDR/time
    storm_dark_day: bool        # dark daylight / storm condition


def evaluate_soil(frame: SensorFrame) -> Dict[str, Any]:
    """
    Soil moisture threshold logic (Section A1 + B1).
    """
    soil = frame.soil_moisture
    if soil <= 15:
        status = "IRRIGATION_ALERT"
    elif soil <= 30:
        status = "WARNING"
    elif 50 <= soil <= 60:
        status = "NO_WATERING_NEEDED"
    else:
        status = "STABLE"

    return {
        "soil_status": status,
        "soil_value": soil,
    }


def evaluate_heat(frame: SensorFrame) -> Dict[str, Any]:
    """
    Temperature + humidity → heat stress / emergency logic (Section A2).
    """
    t = frame.temperature
    h = frame.humidity

    if t is None:
        status = "TEMP_SENSOR_ERROR"
        heat_index = None
    else:
        # simple approximation of heat index (same idea as Arduino side)
        heat_index = t + (0.1 * h / 10.0)
        if t >= 45:
            status = "EMERGENCY_CONDITION"
        elif t >= 36:
            status = "HEAT_STRESS_ALERT"
        elif t < 25:
            status = "NORMAL"
        else:
            status = "ELEVATED"

        if t >= 32 and h >= 70:
            status += "_HEAT_INDEX_WARNING"

    return {
        "heat_status": status,
        "temperature": t,
        "humidity": h,
        "heat_index": heat_index,
    }


def evaluate_aqi(frame: SensorFrame) -> Dict[str, Any]:
    """
    AQI classification (Section A3).
    """
    aqi = frame.aqi

    if aqi >= 300:
        status = "HEALTH_RISK_ALERT"
    elif aqi >= 180:
        status = "POOR_AIR"
    elif 40 <= aqi <= 80:
        status = "STABLE_REPORTING"
    else:
        status = "GOOD"

    return {
        "aqi_status": status,
        "aqi_value": aqi,
    }


def evaluate_crowd(frame: SensorFrame) -> Dict[str, Any]:
    """
    Crowd density classification (Section A4).
    """
    c = frame.crowd_estimate

    if c >= 20:
        status = "SHUTTLE_ALERT"
    elif c <= 5:
        status = "NORMAL_CROWD"
    else:
        status = "MEDIUM_CROWD"

    return {
        "crowd_status": status,
        "crowd_estimate": c,
    }


def evaluate_security(frame: SensorFrame) -> Dict[str, Any]:
    """
    Security alert logic using PIR + Sound (Section A5).
    """
    pir = frame.pir_active
    sound = frame.sound_level
    night = frame.is_night

    sound_high = sound > 60

    if pir and sound_high:
        status = "SECURITY_ALERT"
    elif pir and not sound_high:
        status = "IGNORE_PIR_ONLY"
    elif not pir and sound_high:
        status = "IGNORE_SOUND_ONLY"
    else:
        status = "NO_ALERT"

    if night and status == "SECURITY_ALERT":
        status = "SECURITY_ALERT_ESCALATED"

    return {
        "security_status": status,
        "pir_active": pir,
        "sound_level": sound,
    }


def evaluate_lighting(frame: SensorFrame) -> Dict[str, Any]:
    """
    Adaptive lighting logic using LDR + night/storm flags (Section A6).
    """
    night = frame.is_night
    storm = frame.storm_dark_day

    if night:
        status = "NIGHT_MODE_LIGHT_ON"
        light_on = True
    elif storm:
        status = "STORM_DARK_DAY_LIGHT_ON"
        light_on = True
    else:
        status = "DAY_MODE_LIGHT_OFF"
        light_on = False

    return {
        "light_status": status,
        "light_on": light_on,
        "ldr_raw": frame.ldr_raw,
    }


def evaluate_all(frame: SensorFrame) -> Dict[str, Any]:
    """
    Main threshold detection engine (Section B1 + B2).
    Returns a combined dict with all sensor statuses + a global priority.
    """
    result = {}
    result.update(evaluate_soil(frame))
    result.update(evaluate_heat(frame))
    result.update(evaluate_aqi(frame))
    result.update(evaluate_crowd(frame))
    result.update(evaluate_security(frame))
    result.update(evaluate_lighting(frame))

    # Simple priority example:
    # Highest → heat emergency, then security, then AQI, then others.
    priority = "LOW"

    if "EMERGENCY_CONDITION" in result.get("heat_status", ""):
        priority = "CRITICAL"
    elif "SECURITY_ALERT" in result.get("security_status", ""):
        priority = "HIGH"
    elif result.get("aqi_status") in ("HEALTH_RISK_ALERT", "POOR_AIR"):
        priority = "MEDIUM"

    result["global_priority"] = priority

    return result
