import cv2
import mediapipe as mp
import csv
import time
from datetime import datetime

# Define required joints and thresholds
JOINTS = {
    "left_shoulder": 11,
    "right_shoulder": 12,
    "left_hip": 23,
    "right_hip": 24,
    "left_knee": 25,
    "right_knee": 26,
    "left_ankle": 27,
    "right_ankle": 28,
}
REQUIRED_VISIBILITY = 0.5

# Sample expected coordinate ranges for validation
EXPECTED_COORDINATES = {
    "left_hip": (300, 700),
    "right_hip": (300, 700),
    "left_knee": (300, 1000),
    "right_knee": (300, 1000),
    "left_ankle": (300, 1100),
    "right_ankle": (300, 1100),
}

# Helper function to check if a joint is visible
def is_visible(landmark):
    return landmark.visibility >= REQUIRED_VISIBILITY

# Initialize MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(0)

print("✅ MediaPipe is working\nPress 'q' or wait 10 seconds to quit and analyze...")

last_joint_data = {}
start_time = time.time()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty frame.")
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if results.pose_landmarks:
        for name, index in JOINTS.items():
            landmark = results.pose_landmarks.landmark[index]
            if is_visible(landmark):
                cx, cy = int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])
                last_joint_data[name] = (cx, cy)
                cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)
            else:
                last_joint_data[name] = None

        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

    cv2.imshow("Pose Detection", image)

    # Exit on 'q' or after 10 seconds
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
    elif time.time() - start_time > 10:
        print("⏰ Auto shutdown after 10 seconds.")
        break

cap.release()
cv2.destroyAllWindows()

# Save to CSV
timestamp = datetime.now().strftime("%H:%M:%S")
with open("joint_data.csv", mode='a', newline='') as file:
    writer = csv.writer(file)
    row = [timestamp]
    for joint in JOINTS:
        coords = last_joint_data.get(joint)
        if coords:
            row.extend(coords)
        else:
            row.extend(["None", "None"])
    writer.writerow(row)
print(f"\n📥 Saved to joint_data.csv: {row}")

# Post-process and compare
print("\n🔍 Analyzing pose data...")
errors = []
for joint, expected in EXPECTED_COORDINATES.items():
    actual = last_joint_data.get(joint)
    if actual is None:
        errors.append(f"❌ {joint} not visible.")
    else:
        ax, ay = actual
        ex, ey = expected
        if not (ex - 50 <= ax <= ex + 50) or not (ey - 50 <= ay <= ey + 50):
            errors.append(f"⚠️ {joint} out of range: actual=({ax},{ay}) expected~({ex},{ey})")

if errors:
    print("\n🚫 Pose validation failed:")
    for error in errors:
        print(error)
else:
    print("\n✅ Pose validation passed successfully.")
