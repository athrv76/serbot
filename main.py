import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import serial
import time
import math
import numpy as np
import csv  # Added for data logging

# --- Configuration ---
SERIAL_PORT = '/dev/ttyUSB0'  
BAUD_RATE = 115200 
MODEL_PATH = 'hand_landmarker.task' 
SIMULATION_MODE = True  # Set to False when you get the physical hardware

# --- Setup Serial / Simulation ---
arduino = None
if not SIMULATION_MODE:
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2) 
        print(f"Connected to Arduino on {SERIAL_PORT}")
    except Exception as e:
        print(f"Warning: Could not connect to Arduino: {e}")
        SIMULATION_MODE = True

if SIMULATION_MODE:
    print("Running in SIMULATION MODE. Hardware disabled. Logging data to CSV...")

# --- Setup MediaPipe ---
base_options = python.BaseOptions(model_asset_path=MODEL_PATH)
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.7,
    min_tracking_confidence=0.7,
    running_mode=vision.RunningMode.VIDEO 
)
detector = vision.HandLandmarker.create_from_options(options)

# --- CALIBRATION VARIABLES ---
is_calibrated = False
init_wrist_x = 0.0
init_wrist_y = 0.0
init_pitch_rad = 0.0
init_roll_rad = 0.0

# --- STATE & FILTER VARIABLES ---
pos_shoulder = 90.0
pos_elbow = 90.0
pos_wrist = 90.0

# EMA Filter variables (To match your paper's claims)
EMA_ALPHA = 0.3  
smoothed_angles = [90, 90, 90, 90, 90] 

# --- SENSITIVITY & SPEED ---
MOVE_SPEED = 0.5  
TILT_DEADZONE = 10.0  
Y_DEADZONE = 0.05  

# --- Setup Data Logging ---
csv_filename = 'teleop_results.csv'
csv_file = open(csv_filename, mode='w', newline='')
csv_writer = csv.writer(csv_file)
# Write header row for the research data
csv_writer.writerow(['Timestamp_ms', 'Inference_Latency_ms', 'Raw_Wrist_X', 'Raw_Wrist_Y', 'Cmd_Base', 'Cmd_Shoulder', 'Cmd_Elbow', 'Cmd_Wrist', 'Cmd_Gripper'])

# --- Main Loop ---
cap = cv2.VideoCapture(0)
print("Starting camera... Show your hand to calibrate neutral position!")

frame_timestamp_ms = 0 
start_time = time.time()

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    
    frame_timestamp_ms += 33 
    
    # --- PERFORMANCE TRACKING (For Paper Results) ---
    t0 = time.perf_counter()
    results = detector.detect_for_video(mp_image, frame_timestamp_ms)
    t1 = time.perf_counter()
    
    inference_latency_ms = (t1 - t0) * 1000  # Latency in milliseconds

    if results.hand_landmarks:
        landmarks = results.hand_landmarks[0]

        wrist = landmarks[0]
        thumb_tip = landmarks[4]
        index_mcp = landmarks[5]   
        index_tip = landmarks[8]
        middle_mcp = landmarks[9]  
        pinky_mcp = landmarks[17]  

        dx_pitch = middle_mcp.x - wrist.x
        dy_pitch = middle_mcp.y - wrist.y
        current_pitch_rad = math.atan2(dy_pitch, dx_pitch)

        dx_roll = pinky_mcp.x - index_mcp.x
        dy_roll = pinky_mcp.y - index_mcp.y
        current_roll_rad = math.atan2(dy_roll, dx_roll)

        if not is_calibrated:
            init_wrist_x = wrist.x
            init_wrist_y = wrist.y
            init_pitch_rad = current_pitch_rad
            init_roll_rad = current_roll_rad
            pos_shoulder = 90.0
            pos_elbow = 90.0
            pos_wrist = 90.0
            is_calibrated = True
            print("NEUTRAL POSITION LOCKED!")

        # 1. Base (Yaw)
        deadzone_x = 0.05 
        if wrist.x < (init_wrist_x - deadzone_x):
            base_speed = 80 
        elif wrist.x > (init_wrist_x + deadzone_x):
            base_speed = 100 
        else:
            base_speed = 90 

        # 2. Shoulder (Up/Down)
        delta_y = wrist.y - init_wrist_y 
        if delta_y > Y_DEADZONE: 
            pos_shoulder -= MOVE_SPEED 
        elif delta_y < -Y_DEADZONE:
            pos_shoulder += MOVE_SPEED 

        # 3. Elbow (Pitch)
        delta_pitch = math.degrees(current_pitch_rad - init_pitch_rad)
        if delta_pitch > TILT_DEADZONE:
            pos_elbow -= MOVE_SPEED
        elif delta_pitch < -TILT_DEADZONE:
            pos_elbow += MOVE_SPEED

        # 4. Wrist (Roll)
        delta_roll = math.degrees(current_roll_rad - init_roll_rad)
        if delta_roll > TILT_DEADZONE:
            pos_wrist -= MOVE_SPEED
        elif delta_roll < -TILT_DEADZONE:
            pos_wrist += MOVE_SPEED

        # 5. Gripper
        pinch_dist = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
        gripper_angle = np.interp(pinch_dist, [0.02, 0.15], [0, 180])

        # Clip bounds
        pos_shoulder = np.clip(pos_shoulder, 0, 180)
        pos_elbow = np.clip(pos_elbow, 0, 180)
        pos_wrist = np.clip(pos_wrist, 0, 180)
        
        raw_angles = [
            base_speed, 
            pos_shoulder, 
            pos_elbow, 
            pos_wrist, 
            np.clip(gripper_angle, 0, 180)
        ]

        # Apply EMA Filter (To match Section V.B in your paper)
        for i in range(5):
            smoothed_angles[i] = (EMA_ALPHA * raw_angles[i]) + ((1 - EMA_ALPHA) * smoothed_angles[i])

        final_angles = [int(a) for a in smoothed_angles]

        # --- DATA LOGGING ---
        current_time_ms = (time.time() - start_time) * 1000
        csv_writer.writerow([
            round(current_time_ms, 2), 
            round(inference_latency_ms, 2), 
            round(wrist.x, 4), 
            round(wrist.y, 4), 
            final_angles[0], final_angles[1], final_angles[2], final_angles[3], final_angles[4]
        ])

        # Send to Arduino (if not simulating)
        data_string = f"<{final_angles[0]},{final_angles[1]},{final_angles[2]},{final_angles[3]},{final_angles[4]}>\n"
        
        if not SIMULATION_MODE and arduino is not None:
            arduino.write(data_string.encode('utf-8'))
        
        # Visuals
        cv2.putText(frame, f"Latency: {inference_latency_ms:.1f} ms", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'c' to Re-Center | 'q' to Quit", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)

        points_to_draw = [wrist, thumb_tip, index_mcp, index_tip, middle_mcp, pinky_mcp]
        for p in points_to_draw:
            cx, cy = int(p.x * w), int(p.y * h)
            cv2.circle(frame, (cx, cy), 8, (0, 255, 255), cv2.FILLED)
        
        t_x, t_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
        i_x, i_y = int(index_tip.x * w), int(index_tip.y * h)
        cv2.line(frame, (t_x, t_y), (i_x, i_y), (255, 0, 0), 3)

    else:
        cv2.putText(frame, "Waiting for hand...", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.imshow('Hand Tracking Control (Logging)', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        is_calibrated = False 
        print("Recalibrating...")

print(f"Experiment finished. Results saved to {csv_filename}")
cap.release()
cv2.destroyAllWindows()
csv_file.close()

if arduino is not None:
    arduino.close()
