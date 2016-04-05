#include <LiquidCrystal.h>
#include <Servo.h>
#include <Keypad.h>

LiquidCrystal screen(4, 5, 12, 13, 7, 8); //RS, EN, D4, D5, D6, D7

Servo yaw;    //ASSIGNED PIN 9 : For controlling left-right movement
Servo pitch;  //ASSIGNED PIN 10 : For controlling up-down movement

const int ENEMY_LED = 6;
const int PIEZO_PIN = 11;

//VALUE CONSTANTS
const int CENTER_MOST = 90;
const int RIGHT_MOST = 0;
const int LEFT_MOST = 180;

//FOR KEYPAD ALARM DISABLING
const int KEY_BUFFER_SIZE = 16;
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
byte rowPins[ROWS] = {3, 14, 15, 16}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {17, 18, 19}; //connect to the column pinouts of the keypad

bool alarmIsOn = false;

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

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
 * Clear the keypad buffer and reset it to the start
 */
void resetKeycode() {
  keyBufferHead = 0;
  for (int i = 0; i < KEY_BUFFER_SIZE; i++) {
    keyBuffer[i] = NULL;
  }
}

/**
 * Handle a keypress event from the keypad to disable the alarm
 */
void keypadEvent(KeypadEvent key) {
  if (key == '*' && keyBufferHead > 0) {
    keyBuffer[--keyBufferHead] = NULL;
  } else if (key == '#' || keyBufferHead == KEY_BUFFER_SIZE) {
    screen.clear();
    if (String(keyBuffer).equals("291")) {
      screen.print("Alarm Disable");
      alarmIsOn = false;
      digitalWrite(ENEMY_LED, LOW);
      screen.setCursor(0, 1);
      screen.clear();
      screen.setCursor(0, 0);
    }else{
      screen.print("Incorrect Code");
    }
    delay(2000);
    resetKeycode();
  } else{
    keyBuffer[keyBufferHead++] = key;
  }
}

/**
   Set-ups required before the main loop
*/
void setup() {
  Serial.begin(9600);
  screen.begin(16, 2);
  
  pinMode(PIEZO_PIN, OUTPUT);
  pinMode(ENEMY_LED, OUTPUT);
  
  yaw.attach(10);
  pitch.attach(9);
  
  yaw.write(CENTER_MOST);
  pitch.write(CENTER_MOST);
 
  resetKeycode();
}


/**
   The main loop of our program
*/
void loop() {
  if (Serial.available()){ 
    switch (Serial.read()) {
      case 'l': turnServo(yaw, false, 2); break;
      case 'r': turnServo(yaw, true, 2); break;
      case 'u': turnServo(pitch, true, 1); break;
      case 'd': turnServo(pitch, false, 1); break;
      case 'a': alarmIsOn = true; break;
    }
  } 
  char key = keypad.getKey();
  if (key != NULL && alarmIsOn) {
    keypadEvent(key);
    screen.clear();
    screen.print("Enter Code: ");
    screen.setCursor(0, 1);
    screen.print(String(keyBuffer));
    screen.setCursor(0, 0);
  }

  if(alarmIsOn){
    tone(PIEZO_PIN, 440, 50);
    digitalWrite(ENEMY_LED, HIGH);
    delay(50);
    noTone(PIEZO_PIN);
    delay(50);
  }

}

