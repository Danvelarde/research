

const int Led1 = 13;


void setup() 
{
  pinMode(Led1, OUTPUT);

  Serial.begin(9600);
  while (! Serial); // Wait untilSerial is ready - Leonardo
  Serial.println("Enter 0 to turn off LED and 1 to turn on LED");
}

void loop() 
{
  if (Serial.available())
  {
    char ch = Serial.read();
    if (ch == 'f') //respong with light vale
    {
      digitalWrite(Led1,LOW);
    
      delay(10);
      Serial.println("Led Turned OFF");
    }    
    if (ch == 'o')
    {
      digitalWrite(Led1,HIGH);
      delay(10);
      Serial.println("Led Turned ON");
    }
  }
}
