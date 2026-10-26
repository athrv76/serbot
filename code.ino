#include <Servo.h>

Servo baseServo;
Servo shoulderServo;
Servo elbowServo;
Servo wristServo;
Servo gripperServo;

const byte numChars = 32;
char receivedChars[numChars];
boolean newData = false;

// --- DEBUG FLAG ---
// Set to true to test in Arduino Serial Monitor.
// Set to false when running the Python script for maximum speed.
bool DEBUG_MODE = false; 

void setup() {
  Serial.begin(115200); 
  
  baseServo.attach(3);
  shoulderServo.attach(5);
  elbowServo.attach(6);
  wristServo.attach(9);
  gripperServo.attach(10);
  
  baseServo.write(90); 
  shoulderServo.write(90);
  elbowServo.write(90);
  wristServo.write(90);
  gripperServo.write(90);

  if (DEBUG_MODE) {
    Serial.println("Arduino Ready. Type a command like: <90,120,90,90,45>");
  }
}

void loop() {
  recvWithStartEndMarkers();
  
  if (newData == true) {
    if (DEBUG_MODE) {
      Serial.print("Raw String Received: ");
      Serial.println(receivedChars);
    }
    
    parseAndMove();
    newData = false; 
  }
}

void recvWithStartEndMarkers() {
  static boolean recvInProgress = false;
  static byte ndx = 0;
  char startMarker = '<';
  char endMarker = '>';
  char rc;

  while (Serial.available() > 0 && newData == false) {
    rc = Serial.read();

    if (recvInProgress == true) {
      if (rc != endMarker) {
        receivedChars[ndx] = rc;
        ndx++;
        if (ndx >= numChars) { ndx = numChars - 1; } 
      } else {
        receivedChars[ndx] = '\0'; // terminate the string
        recvInProgress = false;
        ndx = 0;
        newData = true;
      }
    } else if (rc == startMarker) {
      recvInProgress = true;
    }
  }
}

void parseAndMove() {
  char * strtokIndx; 

  // Parse Base
  strtokIndx = strtok(receivedChars, ",");
  if (strtokIndx == NULL) return; // Safety check
  int valBase = atoi(strtokIndx);

  // Parse Shoulder
  strtokIndx = strtok(NULL, ",");
  if (strtokIndx == NULL) return; 
  int valShoulder = atoi(strtokIndx);

  // Parse Elbow
  strtokIndx = strtok(NULL, ",");
  if (strtokIndx == NULL) return; 
  int valElbow = atoi(strtokIndx);

  // Parse Wrist
  strtokIndx = strtok(NULL, ",");
  if (strtokIndx == NULL) return; 
  int valWrist = atoi(strtokIndx);

  // Parse Gripper
  strtokIndx = strtok(NULL, ",");
  if (strtokIndx == NULL) return; 
  int valGripper = atoi(strtokIndx);

  if (DEBUG_MODE) {
    Serial.print("Parsed Integers -> Base:"); Serial.print(valBase);
    Serial.print(" Shoulder:"); Serial.print(valShoulder);
    Serial.print(" Elbow:"); Serial.print(valElbow);
    Serial.print(" Wrist:"); Serial.print(valWrist);
    Serial.print(" Gripper:"); Serial.println(valGripper);
    Serial.println("-------------------------------------------------");
  }

  // Move the servos
  baseServo.write(valBase);
  shoulderServo.write(valShoulder);
  elbowServo.write(valElbow);
  wristServo.write(valWrist);
  gripperServo.write(valGripper);

  // Flush buffer
  while(Serial.available() > 0) {
    char t = Serial.read(); 
  }
}