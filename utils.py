import csv
from datetime import datetime

def export_joint_positions(joint_positions):
    filename = "joint_data.csv"
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        now = datetime.now().strftime("%H:%M:%S")
        row = [now] + [coord for pair in joint_positions.values() for coord in pair]
        writer.writerow(row)
        print(f"📥 Saved to {filename}: {row}")
