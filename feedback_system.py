import csv
import pyttsx3

# Set up Text-to-Speech engine
engine = pyttsx3.init()

# Feedback rule: expected Y-coordinate ranges for hips/knees (example ranges)
EXPECTED_Y = {
    "left_hip": (500, 700),
    "right_hip": (500, 700),
    "left_knee": (700, 1000),
    
    "right_knee": (700, 1000),
}

# Feedback logic
def get_feedback(joint_data):
    errors = []

    joints = ["left_hip", "right_hip", "left_knee", "right_knee"]
    for i, joint in enumerate(joints):
        y_index = 5 + (i * 2)  # skip timestamp + x values
        y_val = joint_data[y_index]

        if y_val == "None":
            errors.append(f"{joint} not visible")
        else:
            y = int(y_val)
            low, high = EXPECTED_Y[joint]
            if not (low <= y <= high):
                errors.append(f"{joint} out of expected range ({y})")

    if not errors:
        return "✅ Great posture! Keep going!"
    else:
        return "⚠️ " + "; ".join(errors)

# Speak feedback
def speak_feedback(message):
    print("🗣️ Feedback:", message)
    engine.say(message)
    engine.runAndWait()

# Read latest row from joint_data.csv
def read_latest_pose():
    with open("joint_data.csv", "r") as file:
        lines = list(csv.reader(file))
        if not lines:
            return None
        return lines[-1]  # get last line (latest)

# MAIN
latest_pose = read_latest_pose()
if latest_pose:
    feedback = get_feedback(latest_pose)
    speak_feedback(feedback)
else:
    print("⚠️ No pose data found.")
