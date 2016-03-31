#include <SoftwareSerial.h>

#define DEBUG true
int count = 1;

SoftwareSerial esp8266(2, 3); // make RX Arduino line is pin 2, make TX Arduino line is pin 3.
// This means that you need to connect the TX line from the esp to the Arduino's pin 2
// and the RX line from the esp to the Arduino's pin 3
void setup()
{
  Serial.begin(115200);
  esp8266.begin(115200); // your esp's baud rate might be different


  sendData("AT", 2000, DEBUG);
  sendData("AT+GMR", 2000, DEBUG);
  //sendData("AT+RST\r\n", 2000, DEBUG); // reset module
  
  /*sendData("AT+CWMODE=2\r\n", 1000, DEBUG); // configure as access point
  sendData("AT+CIFSR\r\n", 1000, DEBUG); // get ip address
  sendData("AT+CIPMUX=1\r\n", 1000, DEBUG); // configure for multiple connections
  sendData("AT+CIPSERVER=1,80\r\n", 1000, DEBUG); // turn on server on port 80
  */
}

void loop()
{
  Serial.println(count);
  count++;
  delay(1000);
}


String sendData(String command, const int timeout, boolean debug)
{
  String response = "";

  esp8266.println(command); // send the read character to the esp8266

  long int time = millis();

  while ( (time + timeout) > millis())
  {
    while (esp8266.available())
    {

      // The esp has data so display its output to the serial window
      char c = esp8266.read(); // read the next character.
      response += c;
    }
  }

  if (debug)
  {
    Serial.println(response);
  }

  return response;
}
