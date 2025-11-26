"""
log_to_csv.py

Generate multiple synthetic SCEMS frames, evaluate alerts,
and save everything into a CSV log file under ../logs/.
"""

import csv
import os
from datetime import datetime

from sensors_simulation import generate_random_frame, frame_to_dict
from threshold_engine import evaluate_all


def generate_logs(num_frames: int = 50, output_path: str = "../logs/system_logs.csv"):
    """
    Generate num_frames frames and save them to a CSV file.
    If the file does not exist, it creates a new one with headers.
    If it exists, it appends new rows.
    """
    rows = []

    for _ in range(num_frames):
        frame = generate_random_frame()
        eval_result = evaluate_all(frame)
        merged = frame_to_dict(frame, eval_result)
        merged["timestamp"] = datetime.now().isoformat(timespec="seconds")
        rows.append(merged)

    # Ensure logs directory exists (../logs)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    file_exists = os.path.isfile(output_path)

    with open(output_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())

        # If file not exists, write header first
        if not file_exists:
            writer.writeheader()

        for row in rows:
            writer.writerow(row)

    print(f"✅ Generated {num_frames} frames and saved to: {output_path}")


if __name__ == "__main__":
    # You can adjust num_frames if needed
    generate_logs(num_frames=100)
