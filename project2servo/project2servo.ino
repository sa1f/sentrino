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
char action;
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
  action = Serial.read();
  next = Serial.peek();
  if (isDigit(next)) { 
    next = Serial.read();
  }
  else {
    next = 1;
  }
  switch (action) {
    case 'l': rotateLeft(poslr, 3*next); break;
    case 'r': rotateRight(poslr, 3*next); break;
    case 'u': panUp(posud, 3*next); break;
    case 'd': panDown(posud, 3*next); break;
     
  }
}

void rotateLeft(int poslr, int next) {
  if (poslr+next <= 180) 
    myservolr.write((poslr+next));
  else 
    myservolr.write(180);
}

void rotateRight(int poslr, int next) {
  if (poslr-next >= 0) 
    myservolr.write((poslr-next));
  else
    myservolr.write(0);
}


void panUp(int posud, int next) {
  if (posud-next >= 0)
    myservoud.write((posud-next));
  else
    myservoud.write(0);
}

void panDown(int posud, int next) {
  if (posud+next <= 180)
    myservoud.write((posud+next));
  else
    myservoud.write(180);
}


