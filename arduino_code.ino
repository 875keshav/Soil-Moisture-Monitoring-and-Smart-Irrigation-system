#include <DHT.h>
#include<ESP8266WiFi.h>
#include<WiFiClient.h>
#include<ESP8266HTTPClient.h>
WiFiClient client;
HTTPClient http;

#define DHTPIN D3 
DHT dht(DHTPIN, DHT11);

const char *ssid =  "oppoa5";   //wifi-name  
const char *pass =  "12345678"; //wifi-password

void connect(void){
Serial.begin(9600);
WiFi.mode(WIFI_STA);
WiFi.begin(ssid, pass);
Serial.print("Connecting");
while(WiFi.status() !=WL_CONNECTED)
{
 Serial.print('.');
 delay(200);
 Serial.println(WiFi.localIP()); 
}

}


void setup(){
  Serial.begin(9600);
  dht.begin();
  connect();
}

String url;
String API="1UJ1TM8Z6T1W6OOA";    //Thingspeak write API
String field1="&field1=";
String field2="&field2=";
String field3="&field3=";
int data;
float h,t;

;
int httpcode;

void sendreq(int data,float h,float t){

url="http://api.thingspeak.com/update?api_key=";
url=url + API;
url=url + field1;
url= url + data;
url=url + field2;
url= url + h;
url=url + field3;
url= url + t;
http.begin(client,url);
Serial.println("Waiting"); 
httpcode=http.GET();
if(httpcode>0){
  Serial.println("Data sent");
  }
else{
  Serial.println("Error");  
}
http.end();
delay(300000);
  
}
void loop() {
  data=analogRead(A0);
   h = dht.readHumidity();
   t = dht.readTemperature();
sendreq(data,h,t); 
Serial.println(data);
Serial.println(h);
Serial.println(t);
delay(5000);
}
