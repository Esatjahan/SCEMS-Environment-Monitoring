"""
sensors_simulation.py

Generates synthetic sensor frames for SCEMS.
This can be used standalone (for testing) or imported by the dashboard.
"""

import random
import time
from typing import Dict, Any

from threshold_engine import SensorFrame, evaluate_all


def generate_random_frame() -> SensorFrame:
    """
    Generate one random but realistic sensor frame.
    You can tune ranges to match Gazipur scenario.
    """
    soil = random.uniform(10, 70)          # %
    temp = random.uniform(24, 46)          # °C
    hum = random.uniform(40, 90)           # %
    aqi = random.randint(30, 350)          # 0-500
    crowd = random.choice([3, 5, 10, 20, 25])
    pir_active = random.choice([True, False])
    sound_level = random.randint(0, 100)
    ldr_raw = random.randint(0, 1023)

    # simple night/day decision from LDR:
    is_night = ldr_raw < 300
    storm_dark_day = (ldr_raw < 400 and not is_night)

    frame = SensorFrame(
        soil_moisture=soil,
        temperature=temp,
        humidity=hum,
        aqi=aqi,
        crowd_estimate=crowd,
        pir_active=pir_active,
        sound_level=sound_level,
        ldr_raw=ldr_raw,
        is_night=is_night,
        storm_dark_day=storm_dark_day,
    )
    return frame


def frame_to_dict(frame: SensorFrame, eval_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Helper: convert frame + evaluation result into one flat dict (for logs/CSV).
    """
    base = {
        "soil_moisture": frame.soil_moisture,
        "temperature": frame.temperature,
        "humidity": frame.humidity,
        "aqi": frame.aqi,
        "crowd_estimate": frame.crowd_estimate,
        "pir_active": frame.pir_active,
        "sound_level": frame.sound_level,
        "ldr_raw": frame.ldr_raw,
        "is_night": frame.is_night,
        "storm_dark_day": frame.storm_dark_day,
    }
    base.update(eval_result)
    return base


def demo_print_loop(num_frames: int = 5, delay_sec: float = 1.0):
    """
    Small demo: generates N frames and prints them with evaluation.
    """
    for i in range(num_frames):
        frame = generate_random_frame()
        eval_result = evaluate_all(frame)
        merged = frame_to_dict(frame, eval_result)
        print(f"Frame {i+1}/{num_frames}:")
        for k, v in merged.items():
            print(f"  {k}: {v}")
        print("-" * 40)
        time.sleep(delay_sec)


if __name__ == "__main__":
    # Run a simple demo when this file is executed directly.
    demo_print_loop(num_frames=5, delay_sec=0.5)
