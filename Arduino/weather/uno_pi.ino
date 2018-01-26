#include <LiquidCrystal_I2C.h> // LCD monitor
#include <Wire.h> 
#include <dht.h>

//Constants
#define DHTPIN 2     // what pin we're connected to
// Initialize DHT sensor for normal 16mhz Arduino
dht dht11;  

LiquidCrystal_I2C lcd(0x27, 16,2); // Initialize DHT sensor
int photocellPin = 0; // Analog pin 
int photocellVal = 0; // initialize Light Resistance value

float temperature = 0;
float humidity = 0;

void setup() {
  Serial.begin(9600);
  lcd.init(); 
  lcd.begin(16, 2);
}

void loop() {
  if (Serial.available() > 0) {
    char choice = Serial.read();
    switch(choice){
      case 'B':
          read_data();
          Serial.write(byte(temperature));
          Serial.write(byte(humidity));
          Serial.write(byte(photocellVal));
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

void read_data(){
  photocellVal = analogRead(photocellPin);
  int check = dht11.read11(DHTPIN);
    if (check == 0) {
        //Read data and store it to variables hum and temp
        humidity = dht11.humidity;
        temperature= dht11.temperature;
    }
    else {
        Serial.println("fail");
    }
}

void on_lcd(int temperature, int humidity, int photocellVal){
  lcd.clear();
  lcd.print((int)temperature);
  lcd.print(" *C  ");
  lcd.print((int)humidity);
  lcd.print("H");
  lcd.setCursor(0,1);
  lcd.print("LResistance:");
  lcd.print(photocellVal);
}
