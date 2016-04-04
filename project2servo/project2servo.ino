#include <LiquidCrystal.h>
#include <Servo.h>

//LiquidCrystal screen(8, 9, 10, 11, 12, 13); //RS, EN, D4, D5, D6, D7

Servo yaw;    //ASSIGNED PIN 9 : For controlling left-right movement
Servo pitch;  //ASSIGNED PIN 10 : For controlling up-down movement

//VALUE CONSTANTS
const int CENTER_MOST = 90;
const int RIGHT_MOST = 0;
const int LEFT_MOST = 180;

//LCD CONSTANTS
const int FIRST_COL = 0;
const int TOP_ROW = 1;
const int BOTTOM_ROW = 1;

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
    servo.write((pos - motorStep >= RIGHT_MOST) ? pos - motorStep : 0);  
  }else{
    servo.write((pos + motorStep <= LEFT_MOST) ? pos + motorStep : 0);  
  }
}


/**
 * FOR DEBUGGING PURPOSE ONLY, DELETE THIS BEFORE SUBMITTING CODE
 */
/*void testLoop(){
  screen.clear();
  screen.print("TURNING LEFT");
  turnServo(yaw,true, 30);
  delay(1000);
  
  screen.clear();
  screen.print("TURNING RIGHT");
  turnServo(yaw,false, 30);
  delay(1000);

  screen.clear();
  screen.print("TURNING UP");
  turnServo(pitch,true, 30);
  delay(1000);

  screen.clear();
  screen.print("TURNING DOWN");
  turnServo(pitch,false, 30);
  delay(1000);
}*/


/**
 * Set-ups required before the main loop
 */
void setup() {
  Serial.begin(9600);
  
  //screen.begin(16, 2);
  audio_setup();
  
  yaw.attach(9);
  pitch.attach(10);
  
  yaw.write(CENTER_MOST);
  pitch.write(CENTER_MOST);
}


/**
 * The main loop of our program
 */
void loop() {
  /*if (Serial.available()){ 
    switch (Serial.read()) {
      case 'l': turnServo(yaw, true, 3); break;
      case 'r': turnServo(yaw, false, 3); break;
      case 'u': turnServo(pitch, true, 3); break;
      case 'd': turnServo(pitch, false, 3); break;
    }
  }8*/
  audio_loop();
}
