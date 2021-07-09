
#include <SoftwareSerial.h>
#include <MPU6050_tockn.h>
#include <Wire.h>

 
MPU6050 mpu(Wire);

int blueTx=2;   //Tx (보내는핀 설정)at
int blueRx=3;   //Rx (받는핀 설정)
SoftwareSerial mySerial(blueTx, blueRx);  //시리얼 통신을 위한 객체선언
int in1 = 9;
int in2 = 6;



void setup() {

  pinMode(9, OUTPUT);    
  pinMode(6, OUTPUT);


  mpu.begin();
  mpu.calcGyroOffsets(true);
  
  Serial.begin(9600);
  Wire.begin();
  mySerial.begin(9600); // 통신 속도 9600bps로 블루투스 시리얼 통신 시작 

}


void loop() {
//  read1 = mySerial.read();

if (mySerial.available()){
  char read1;
  read1 = mySerial.read();
  if(read1 == '1'){
    digitalWrite(6, HIGH);
    digitalWrite(9, LOW);//up
    delay(1000);
    }
  else if(read1 == '2'){
    digitalWrite(6, LOW);
    digitalWrite(9, HIGH);//down
    delay(1000);
    }
  else if(read1 == '3') {
    digitalWrite(6, LOW);
    digitalWrite(9, LOW);
    delay(1000);
    }
  
}

  mpu.update();
  mySerial.print("angleX : ");
  mySerial.print(mpu.getAngleX());
  mySerial.print("\tangleY : ");
  mySerial.print(mpu.getAngleY());
  mySerial.print("\tangleZ : ");
  mySerial.println(mpu.getAngleZ());
  delay(1000);


}
