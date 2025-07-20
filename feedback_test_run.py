from feedback_system import read_latest_pose, get_feedback, speak_feedback

# MAIN EXECUTION
if __name__ == "__main__":
    latest_pose = read_latest_pose()
    if latest_pose:
        feedback = get_feedback(latest_pose)
        speak_feedback(feedback)
    else:
        print("⚠️ No pose data found.")
