// include the library code:
#include <LiquidCrystal.h>

LiquidCrystal lcd(5, 7, 8, 9, 10, 11);

void printMode();
void printSpeed();
void printDirection();
void printInformation();

// initialize the library with the numbers of the interface pins
void setup() {
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
}

void loop() 
{
  // prints the current robot data onto the LCD
  printMode();
  printInfo();  
  delay(1000);
}

void printMode()
{
  int MODE = 2;
  // set the cursor to column 0, line 0
  lcd.setCursor(0,0);

  // print "MODE"
  lcd.print("MODE: ");
  
  switch(MODE)
  {
    case(1): lcd.print("AUTO"); break;
    case(2): lcd.print("WIFI"); break;
    case(3): lcd.print("MOTION"); break;
  }
}

void printInfo()
{
   int status = 1;

   // Set the cursor to column 0, line 1
   lcd.setCursor(0,1);
   
   switch(status)
   {
    case(1): lcd.print("NOBODY DETECTED"); break;
    case(2): lcd.print("ENEMY DETECTED"); break;
    case(3): lcd.print("ALLY DETECTED"); break;
   }

}


