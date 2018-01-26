//Libraries
#include <dht.h>

//Constants
#define DHTPIN 2     // what pin we're connected to

// Initialize DHT sensor for normal 16mhz Arduino
dht DHT;

void setup()
{
    Serial.begin(9600);
}

void loop()
{
//Variables
int check;
float hum;  //Stores humidity value
float temp; //Stores temperature value

    check = DHT.read11(DHTPIN);
    if (check == 0) {
        //Read data and store it to variables hum and temp
        hum = DHT.humidity;
        temp= DHT.temperature;
        //Print temp and humidity values to serial monitor
        Serial.print("Humidity: ");
        Serial.print(hum);
        Serial.print(" %, Temp: ");
        Serial.print(temp);
        Serial.println(" Celsius");
    }
    else { 
        Serial.print("check=");
        Serial.println(check);
    }
    delay(2000); //Delay 2 sec.
}


