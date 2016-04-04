#include <Servo.h>

Servo yaw;    //For controlling left-right movement
Servo pitch;  //For controlling up-down movement

//PIN CONSTANTS
const int YAW_PIN = 9;
const int PITCH_PIN = 10;

//VALUE CONSTANTS
const int CENTER = 90;
const int RIGHT = 0;
const int LEFT = 180;

/**
 * Rotate a given servo arm relative to its current position
 * 
 * @param servo - The servo to rotate
 * @param clockwise - Determines whether to rotate clockwise or not
 * @param motorStep - How much to degree to rotate
 */
void turnServo(Servo servo, bool clockwise, int motorStep=1){
  int pos = servo.read();
  
  if(clockwise){
    servo.write((pos - motorStep >= 0) ? pos - motorStep : 0);  
  }else{
    servo.write((pos + motorStep <= 180) ? pos + motorStep : 0);  
  }
}


/**
 * FOR DEBUGGING PURPOSE ONLY, DELETE THIS BEFORE SUBMITTING CODE
 */
void testLoop(){
  Serial.println("LEFT");
  turnServo(yaw,true, 30);
  delay(1000);

  Serial.println("RIGHT");
  turnServo(yaw,false, 30);
  delay(1000);

  Serial.println("UP");
  turnServo(pitch,true, 30);
  delay(1000);

  Serial.println("DOWN");
  turnServo(pitch,false, 30);
  delay(1000);
}


/**
 * Set-ups required before the main loop
 */
void setup() {
  Serial.begin(9600);
  
  yaw.attach(9);
  pitch.attach(10);
  
  yaw.write(90);
  pitch.write(90);
}


/**
 * The main loop of our program
 */
void loop() {
  if (Serial.available()){ 
    switch (Serial.read()) {
      case 'l': turnServo(yaw, true, 3); break;
      case 'r': turnServo(yaw, false, 3); break;
      case 'u': turnServo(pitch, true, 3); break;
      case 'd': turnServo(pitch, false, 3); break;
    }
  }
}
