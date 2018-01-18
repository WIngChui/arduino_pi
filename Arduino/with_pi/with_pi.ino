#include <SimpleDHT.h>
//#include <LiquidCrystal_I2C.h>
#include <Wire.h>

int pinDHT11 = 7;
int photocellPin = 13;
int photocellVal = 0;

//LiquidCrystal_I2C lcd(0x27,20,4);
SimpleDHT11 dht11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //lcd.init(); 
  //lcd.begin(16, 2);
}

void loop() {
  photocellVal = analogRead(photocellPin);
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(pinDHT11, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.write("Read DHT11 failed");
    return;
  }

  if (Serial.available() > 0) {
    char choice = Serial.read();
    switch(choice){
      case 'A':
        Serial.write("T:");send_TH(temperature);
        Serial.write("H:");send_TH(humidity);
        Serial.write("R:");Serial.print(photocellVal);
        break;
      case 'B':
        Serial.write(temperature);
        Serial.write(humidity);
        Serial.write(byte(photocellVal));
        break;
      case 'C':
        Serial.println(temperature);
        Serial.println(humidity);
        Serial.println(photocellVal);
        break;
      case 'P':
        Serial.print("temperature:");Serial.println((int)temperature);
        Serial.print("humidity:");Serial.println((int)humidity);
        Serial.print("light_resistance:");Serial.println(photocellVal);
        break;
    };
  }
}

void send_TH(byte val){
    byte tmp[] = {val};
    for (int i ;i<sizeof(tmp);i++){
        Serial.print(tmp[i]);
    }
}
/*
void on_lcd(int temperature, int humidity, int photocellVal){
  lcd.clear();
  //lcd.print("Temp : ");
  lcd.print(temperature);
  lcd.print(" *C  ");
  //lcd.print("Humidity : ");
  lcd.print(humidity);
  lcd.print("H");
  lcd.setCursor(0,1);
  lcd.print("LResistance:");
  lcd.print(photocellVal);
}
*/
