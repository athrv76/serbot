
# SERBOT: YOLO-Based Automatic Waste Segregation Using a 4-DOF Robotic Arm

##  Overview

**SERBOT** is an AI-powered automatic waste segregation system that integrates computer vision, object detection, embedded systems, and robotic manipulation.

The system uses a USB webcam to capture images of waste objects. A Raspberry Pi processes the camera input using a YOLO-based object detection model to identify and localize waste belonging to three target categories: **plastic, paper, and metal**.

After detecting an object, the Raspberry Pi determines the appropriate handling action and communicates with an Arduino. The Arduino controls the servo motors of a 4-degree-of-freedom (4-DOF) robotic arm, which is designed to pick up the detected object and move it toward the corresponding collection bin.

The project explores how artificial intelligence and robotics can be combined to reduce manual sorting and support more efficient waste management.

##  Objectives

- Develop an object detection system for identifying plastic, paper, and metal waste.
- Integrate a YOLO-based detection model with a Raspberry Pi.
- Capture and process waste images using a USB webcam.
- Establish communication between the Raspberry Pi and Arduino.
- Control a 4-DOF robotic arm using servo motors.
- Develop a coordinate-mapping and robotic movement approach for object picking.
- Evaluate detection accuracy and the effectiveness of robotic waste segregation.
- Demonstrate the practical application of AI and robotics in waste management.

##  System Architecture

```text
                  Waste Object
                       |
                       v
                  USB Webcam
                       |
                       v
                  Raspberry Pi
                +---------------+
                | Image Capture |
                | YOLO Detection|
                | Classification|
                | Position Logic|
                +---------------+
                       |
                       v
              Serial Communication
                       |
                       v
                    Arduino
                       |
                       v
              Servo Motor Control
                       |
                       v
               4-DOF Robotic Arm
                       |
                       v
               Waste Collection Bins
                 /       |       \
             Plastic    Paper    Metal
```

The Raspberry Pi handles image processing and high-level decision-making, while the Arduino manages the robotic arm's low-level motor control.

## ⚙️ Working Methodology

### 1. Image Acquisition

A USB webcam captures images of waste objects placed within the robot's working area.

### 2. Object Detection

The Raspberry Pi processes the captured images using a YOLO-based object detection model. The model is intended to predict the class and bounding-box coordinates of each detected waste object.

### 3. Waste Classification

The detected objects are classified into the following categories:

- Plastic
- Paper
- Metal

The final classification performance depends on the trained model and the quality of the dataset.

### 4. Object Localization

The bounding-box information is used to estimate the location of the detected object in the camera image. A calibration or coordinate-mapping method is required to convert image coordinates into coordinates suitable for robotic movement.

### 5. Command Generation

The Raspberry Pi generates a control command based on the detected class and target position. The command is transmitted to the Arduino through a serial connection.

### 6. Robotic Arm Control

The Arduino interprets the received command and controls the servo motors of the 4-DOF robotic arm.

The intended pick-and-place sequence consists of:

1. Moving the arm toward the detected object.
2. Positioning the gripper.
3. Gripping the object.
4. Moving the object toward its designated bin.
5. Releasing the object.
6. Returning the arm to a suitable position for the next operation.

The exact movement sequence depends on the implemented control software and the physical configuration of the robotic arm.

### 7. Waste Segregation

The robotic arm is designed to place each detected object into the collection bin corresponding to its predicted category.

Correct segregation depends on both the detection result and the successful execution of the robotic movement.

##  Hardware Requirements

| Component | Function |
|---|---|
| Raspberry Pi | Runs the object detection and high-level control logic |
| Arduino | Controls the robotic arm actuators |
| USB Webcam | Captures images of waste objects |
| 4-DOF Robotic Arm | Performs object manipulation |
| Servo Motors | Drive the robotic arm joints and gripper |
| Power Supply | Provides the required power to the system |
| Collection Bins | Store segregated waste categories |
| Connecting Wires and Mounting Hardware | Support electrical connections and mechanical assembly |

**Note:** Exact component models, servo specifications, power ratings, and circuit connections should be documented according to the final hardware assembly.

##  Software and Technologies

| Technology | Purpose |
|---|---|
| Python | Computer vision and system integration |
| YOLO | Waste object detection and classification |
| OpenCV | Camera input and image processing |
| Raspberry Pi OS | Operating environment for the Raspberry Pi |
| Arduino IDE | Development and uploading of Arduino firmware |
| Serial Communication | Communication between the Raspberry Pi and Arduino |
| Git and GitHub | Version control and project collaboration |

The specific YOLO version, Python package versions, and trained model configuration are **yet to be confirmed**.

##  Object Detection Model

The object detection module is intended to identify and localize waste objects using a YOLO-based model.

### Target Classes

| Class ID | Waste Category |
|---|---|
| 0 | Plastic |
| 1 | Paper |
| 2 | Metal |

These class IDs are a proposed label mapping. The actual IDs must match the dataset configuration used during training.

### Model Training Workflow

1. Collect or select images representing the target waste categories.
2. Annotate the objects with bounding boxes.
3. Organize the dataset into training, validation, and test subsets.
4. Configure the selected YOLO model and dataset.
5. Train the model using the selected training configuration.
6. Validate the model and inspect its predictions.
7. Evaluate its performance on appropriate test data.
8. Deploy the trained model to the Raspberry Pi, subject to hardware compatibility.

### Evaluation Metrics

The following metrics can be used to evaluate the object detection model:

- **Precision:** Proportion of predicted positive detections that are correct.
- **Recall:** Proportion of ground-truth objects that are successfully detected.
- **Intersection over Union (IoU):** Measures the overlap between a predicted bounding box and its ground-truth box.
- **mAP@0.5:** Mean Average Precision at an IoU threshold of 0.50.
- **mAP@0.5:0.95:** Mean Average Precision averaged across IoU thresholds from 0.50 to 0.95.
- **Inference Time:** Time taken to process an image and generate detections.

Actual metric values will be reported after the selected model has been trained and evaluated.

##  Robotic Arm and Control

The robotic subsystem uses a 4-DOF arm controlled by an Arduino and servo motors.

The control pipeline is designed to connect the object detection output to the physical pick-and-place operation.

### Control Pipeline

```text
Detected Object
      |
      v
Extract Bounding Box
      |
      v
Estimate Object Position
      |
      v
Map Position to Robot Coordinates
      |
      v
Generate Movement Command
      |
      v
Send Command to Arduino
      |
      v
Move Arm and Operate Gripper
      |
      v
Place Object in Target Bin
```

### Coordinate Mapping and Inverse Kinematics

Image coordinates do not directly correspond to robotic joint angles. A calibration procedure is therefore needed to map camera observations to positions in the robot's workspace.

Depending on the physical arrangement, the control system may use:

- Camera calibration
- Image-to-workspace coordinate mapping
- Geometric calculations
- Inverse kinematics
- Joint-angle constraints
- Gripper actuation commands

The final mathematical model must be derived from the actual arm dimensions, joint arrangement, camera position, and workspace calibration. No specific kinematic solution is assumed here.

##  System Performance Evaluation

The complete system should be evaluated at both the computer-vision and robotic levels.

| Metric | Purpose |
|---|---|
| Detection Precision | Measures the correctness of predicted detections |
| Detection Recall | Measures how many actual objects are detected |
| mAP | Summarizes object detection performance |
| Inference Time | Measures the detection processing time |
| Pick Success Rate | Measures the proportion of successful object pickups |
| Correct-Bin Rate | Measures the proportion of objects placed in the intended bins |
| Positioning Error | Measures the difference between target and achieved positions |
| End-to-End Cycle Time | Measures the time required for a complete sorting operation |

For example, the pick success rate can be calculated as:

\[
\text{Pick Success Rate} =
\frac{\text{Successful Pick Attempts}}
{\text{Total Pick Attempts}}\times 100
\]

The correct-bin rate can be calculated as:

\[
\text{Correct-Bin Rate} =
\frac{\text{Objects Placed in Correct Bins}}
{\text{Total Objects Processed}}\times 100
\]

These metrics should be calculated from recorded experiments. No experimental scores are claimed in this README.

##  Repository Structure

The following is a suggested structure for organizing the project. File names should be updated to match the actual repository contents.

```text
serbot/
├── arduino/
│   └── robotic_arm.ino
├── raspberry_pi/
│   ├── detection.py
│   ├── coordinate_mapping.py
│   └── serial_communication.py
├── dataset/
│   └── README.md
├── models/
│   └── README.md
├── calibration/
│   └── README.md
├── results/
│   └── README.md
├── paper/
│   └── README.md
├── requirements.txt
└── README.md
```

Large datasets and trained model weights may be stored separately if they exceed GitHub's file-size limits. Their download instructions should be documented when available.

##  Installation and Setup

The exact installation commands depend on the selected YOLO version, Python environment, and Raspberry Pi operating system.

### 1. Clone the Repository

```bash
git clone https://github.com/athrv76/serbot.git
cd serbot
```

### 2. Set Up the Python Environment

On a compatible Python installation, create and activate a virtual environment:

```bash
python -m venv .venv
```

On Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

If a verified `requirements.txt` file is available:

```bash
pip install -r requirements.txt
```

The required packages and compatible versions must be added to `requirements.txt` based on the implementation. No unverified dependency list is assumed here.

### 4. Configure the Hardware

- Connect the USB webcam to the Raspberry Pi.
- Connect the Arduino to the Raspberry Pi.
- Connect the servo motors according to the verified circuit design.
- Ensure the motors receive an appropriate power supply.
- Upload the Arduino firmware.
- Verify camera input and serial communication before enabling automatic movement.

Avoid powering multiple servos directly from a Raspberry Pi GPIO pin. Use an appropriate power arrangement and ensure a common ground where required by the circuit design.

### 5. Configure the Detection Model

After selecting and training a compatible YOLO model:

- Store or locate the trained model weights.
- Configure the camera input.
- Set the correct class names and label mapping.
- Configure the serial port and communication format.
- Verify detections before connecting them to robotic movement.

### 6. Run the Application

The final run command depends on the Python entry point implemented in the repository.

For example, if the project contains `raspberry_pi/detection.py`, the command may be:

```bash
python raspberry_pi/detection.py
```

This is an example command, not a guarantee that the file currently exists. Update it after confirming the actual application entry point.

## Testing and Validation

The system should be tested in stages:

1. **Camera Test:** Verify that the USB webcam provides a stable image stream.
2. **Detection Test:** Evaluate predictions on representative plastic, paper, and metal objects.
3. **Serial Communication Test:** Confirm that commands are received correctly by the Arduino.
4. **Servo Test:** Verify joint movement and gripper operation independently.
5. **Calibration Test:** Check the mapping between image coordinates and the robot's workspace.
6. **Pick-and-Place Test:** Evaluate object pickup and placement for each category.
7. **End-to-End Test:** Measure complete sorting performance under repeatable conditions.

Record failures as well as successful trials to identify limitations and improve the system.

##  Limitations

Potential limitations that require evaluation include:

- Detection performance may vary with lighting, background, object shape, and camera angle.
- Overlapping objects may be difficult to detect and localize.
- Image coordinates require calibration before they can guide robotic movement.
- Servo precision, mechanical tolerances, and gripper design may affect pickup reliability.
- Model inference speed depends on the selected model and Raspberry Pi hardware.
- Incorrect classifications can lead to incorrect bin selection.
- Different object sizes and shapes may require changes to the gripping strategy.

These are anticipated engineering considerations, not claims that every limitation has already been observed in testing.

##  Future Scope

Possible future improvements include:

- Expanding the dataset to include more waste categories.
- Improving detection accuracy using additional training data.
- Optimizing inference for Raspberry Pi deployment.
- Adding feedback sensors to improve pickup reliability.
- Implementing collision avoidance and workspace constraints.
- Improving calibration and robotic positioning accuracy.
- Adding real-time performance logging and visualization.
- Evaluating the system across different object sizes, orientations, and lighting conditions.
- Investigating additional recyclable and non-recyclable waste categories.

##  Project Team

**Institution:** SRM Institute of Science and Technology  
**Department:** Department of Computing Technologies


##  References

1. J. Redmon, S. Divvala, R. Girshick, and A. Farhadi, "You Only Look Once: Unified, Real-Time Object Detection," *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 2016.
2. Ultralytics, "YOLO Performance Metrics." Available at: https://docs.ultralytics.com/guides/yolo-performance-metrics/
3. Ultralytics, "Model Validation with Ultralytics YOLO." Available at: https://docs.ultralytics.com/modes/val/
4. OpenCV Documentation. Available at: https://docs.opencv.org/
5. Arduino Documentation. Available at: https://docs.arduino.cc/

##  Research Documentation

The accompanying research paper is intended to describe the system architecture, dataset preparation, object detection methodology, robotic control strategy, calibration, performance evaluation, and experimental findings.

Research results should be added only after the corresponding experiments have been completed and documented.

##  License

No license has been specified yet. Add an appropriate license file if the project is intended for public reuse or distribution.

---

<p align="center">
  <strong>SERBOT — Bringing AI and Robotics to Smart Waste Segregation.</strong>
</p>
