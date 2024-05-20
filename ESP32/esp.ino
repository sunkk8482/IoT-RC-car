#include <WiFi.h>
#include <IOXhop_FirebaseESP32.h>
#include <SPI.h>
#define FIREBASE_HOST "kfcproject-cf35a-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "kSzXuNXaSelXb1haZNZpXp2U5VNF3JHlHTuayT3p"
#define WIFI_SSID "Galaxy4"
#define WIFI_PASSWORD "12345678"
int trigPin = 25;
int echoPin = 26;

void setup() {

  Serial.begin(115200);
  
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  SPI.begin(SCK, MISO, MOSI, SS);
  SPI.setFrequency(16000000);
  digitalWrite(SS, LOW);


  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println();
  Serial.print("Connected: ");
  Serial.println(WiFi.localIP());
  
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}
uint8_t readData;
char command;
void loop() {
  String cmdPath = "commandTable";
  String cmdData = Firebase.getString(cmdPath);

  if (Firebase.failed()) {
    Serial.print("Getting cmd_string failed: ");
    Serial.println(Firebase.error());  
    return;
  }

  // Find the latest cmd_string
  String latestCmd;
  int startPos = cmdData.lastIndexOf("cmd_string");
  if (startPos != -1) {
    int startPosValue = cmdData.indexOf('"', startPos);
    int endPosValue = cmdData.indexOf('"', startPosValue + 3);
    latestCmd = cmdData.substring(startPosValue + 3, endPosValue);
  } else {
    Serial.println("No cmd_string found in data");
    return;
  }

  Serial.println(latestCmd);
  long duration, distance;
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 17 / 1000;
  Serial.print(distance);
  Serial.println("CM");
  
  if(distance>15){

  if( latestCmd.equals( "GO") ){
      readData = SPI.transfer('w');
  }
  if( latestCmd.equals("BACK") ){
      readData = SPI.transfer('x');
  }
  if( latestCmd.equals("LEFT")){
      readData = SPI.transfer('a');
  }
  if( latestCmd.equals ("MID") ){
      readData = SPI.transfer('s');
  }
  if( latestCmd.equals("RIGHT") ){
      readData = SPI.transfer('d');
  }
  if( latestCmd == "STOP" ){
      Serial.println("aaa");
      readData = SPI.transfer('f');
  }
  }
  else{
    readData = SPI.transfer('f');
  }

  delay(5);
}