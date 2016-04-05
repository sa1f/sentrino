#include <LiquidCrystal.h>
#include <Servo.h>
#include <Keypad.h>

LiquidCrystal screen(4, 5, 7, 8, 12, 13); //RS, EN, D4, D5, D6, D7

Servo yaw;    //ASSIGNED PIN 9 : For controlling left-right movement
Servo pitch;  //ASSIGNED PIN 10 : For controlling up-down movement

//VALUE CONSTANTS
const int CENTER_MOST = 90;
const int RIGHT_MOST = 0;
const int LEFT_MOST = 180;
/*
const int KEY_BUFFER_SIZE = 5;
char keyBuffer[KEY_BUFFER_SIZE];
int keyBufferHead = 0;

const byte ROWS = 4; //four rows
const byte COLS = 3; //three columns
char keys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};
byte rowPins[ROWS] = {19, 18, 17, 16}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {15, 14, 13}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );
*/
/**
   Rotate a given servo arm relative to its current position

   @param servo - The servo to rotate
   @param clockwise - Determines whether to rotate clockwise or not
   @param motorStep - How much to degree to rotate
*/
void turnServo(Servo servo, bool clockwise, int motorStep = 1) {
  int pos = servo.read();

  if (clockwise) {
    servo.write((pos - motorStep >= RIGHT_MOST) ? pos - motorStep : 0);
  } else {
    servo.write((pos + motorStep <= LEFT_MOST) ? pos + motorStep : 0);
  }
}


/**
   FOR DEBUGGING PURPOSE ONLY, DELETE THIS BEFORE SUBMITTING CODE
*/

void testLoop(){
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
}
/*
void resetKeycode() {
  keyBufferHead = 0;
  for (int i = 0; i < KEY_BUFFER_SIZE; i++) {
    keyBuffer[i] = NULL;
  }
}

void keypadEvent(KeypadEvent key) {
  if (key == '*' && keyBufferHead > 0) {
    keyBuffer[--keyBufferHead] = NULL;
  } else if (key == '#' || keyBufferHead == KEY_BUFFER_SIZE) {
    if (String(keyBuffer).equals("291")) {
      Serial.println("Correct");
    }else{
      Serial.println("Incorrect");
    }
    delay(2000);
    resetKeycode();
  } else{
    keyBuffer[keyBufferHead++] = key;
  }
}
*/
/**
   Set-ups required before the main loop
*/
void setup() {
  Serial.begin(9600);
  screen.begin(16, 2);
  //audio_setup();

  yaw.attach(9);
  pitch.attach(10);

  yaw.write(CENTER_MOST);
  pitch.write(CENTER_MOST);

  //resetKeycode();
}


/**
   The main loop of our program
*/
void loop() {
  /*if (Serial.available()){
    switch (Serial.read()) {
      case 'l': turnServo(yaw, true, 3); break;
      case 'r': turnServo(yaw, false, 3); break;
      case 'u': turnServo(pitch, true, 3); break;
      case 'd': turnServo(pitch, false, 3); break;
    }
    }*/
  testLoop();  
  /*char key = keypad.getKey();
  if (key != NULL) {
    keypadEvent(key);
  }*/
  

}

