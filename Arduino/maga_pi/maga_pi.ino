#include <SimpleDHT.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

int pinDHT11 = 2;
int photocellPin = A0;
int photocellVal = 0;
byte temperature = 0;
byte humidity = 0;
int err = SimpleDHTErrSuccess;

LiquidCrystal_I2C lcd(0x27,20,4);
SimpleDHT11 dht11;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  lcd.init(); 
  lcd.begin(16, 2);
}

void loop() {
  
  if (Serial.available() > 0) {
    char choice = Serial.read();
    switch(choice){
      case 'A':
          read_data();
          Serial.write("T:");send_TH(temperature);
          Serial.write("H:");send_TH(humidity);
          Serial.write("R:");Serial.print(photocellVal);
          on_lcd((int)temperature, (int)humidity, photocellVal);
          break;
      case 'B':
          read_data();
          Serial.write(temperature);
          Serial.write(humidity);
          Serial.write(photocellVal);
          on_lcd((int)temperature, (int)humidity, photocellVal);
          break;
      case 'C':
          read_data();
          Serial.println((int)temperature);
          Serial.println((int)humidity);
          Serial.println(photocellVal);
          on_lcd((int)temperature, (int)humidity, photocellVal);
          break;
      case 'D':
          read_data();
          Serial.print("temperature:");Serial.println((int)temperature);
          Serial.print("humidity:");Serial.println((int)humidity);
          Serial.print("light_resistance:");Serial.println(photocellVal);
          break;
     case 'P':
          on_lcd((int)temperature, (int)humidity, photocellVal);
          break;
     case 'O':
          lcd.backlight();
          break;
     case 'N':
          lcd.noBacklight();
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

void read_data(){
  photocellVal = analogRead(photocellPin);
  if ((err = dht11.read(pinDHT11, &temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.println("fail");
  }
}

void on_lcd(int temperature, int humidity, int photocellVal){
  lcd.clear();
  //lcd.print("Temp : ");
  lcd.print((int)temperature);
  lcd.print(" *C  ");
  //lcd.print("Humidity : ");
  lcd.print((int)humidity);
  lcd.print("H");
  lcd.setCursor(0,1);
  lcd.print("LResistance:");
  lcd.print(photocellVal);
}
