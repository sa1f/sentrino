/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservolr;  // create servo object to control a servo
Servo myservoud;
// twelve servo objects can be created on most boards

int poslr;
int posud;
int action;
int next;

void setup() {
  Serial.begin(9600);
  myservolr.attach(9);  // attaches the servo on pin 9 to the servo object
  myservoud.attach(10);
  myservolr.write(90);
  myservoud.write(90);
 
}

void loop() {
  poslr = myservolr.read();
  posud = myservoud.read();
  if (Serial.available()){ 
    action = Serial.read();
    /*
    next = Serial.peek();
    if (isDigit(next)) { 
      next = Serial.read();
    }  
    else {
      next = 1;
    }
    */
    switch (action) {
      case 'l': rotateLeft(poslr); break;
      case 'r': rotateRight(poslr); break;
      case 'u': panUp(posud); break;
      case 'd': panDown(posud); break;
       
    }
  }
}

void rotateLeft(int poslr) {
  if (poslr+3 <= 180) 
    myservolr.write((poslr+3));
  else 
    myservolr.write(180);
}

void rotateRight(int poslr) {
  if (poslr-3 >= 0) 
    myservolr.write((poslr-3));
  else
    myservolr.write(0);
}


void panUp(int posud) {
  if (posud-3 >= 0)
    myservoud.write((posud-3));
  else
    myservoud.write(0);
}

void panDown(int posud) {
  if (posud+3 <= 180)
    myservoud.write((posud+3));
  else
    myservoud.write(180);
}


