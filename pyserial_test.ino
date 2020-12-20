#include <Wire.h>
#include <LiquidCrystal_I2C.h>
char serialData;
int pinB =13;
int pinR = 12;
int piezo = 7;
int freq = 1500;
int Door = 8;
void setup() {
  
Serial.begin(9600);
  pinMode(Door,OUTPUT);
  pinMode(pinB,OUTPUT);
  pinMode(pinR,OUTPUT);
  pinMode(piezo, OUTPUT);
  Serial.begin(9600);
}



void loop() {

if( Serial.available()>0 ){
  serialData = Serial.read();
  Serial.println( serialData);
  
  if (serialData == '1'){  
    
    //이때 문이 열리는 함수 만들고+ 파란 불 + signal: 맛있게 먹어라  
    digitalWrite(Door,HIGH);
    digitalWrite(pinB,HIGH);
    digitalWrite(pinR,LOW);
    LiquidCrystal_I2C lcd(39,16,2);
    lcd.begin();
    lcd.backlight();
    lcd.print("enjoy your meal");
  }
  else if (serialData == '0'){
    
    //이때 문이 닫히는 함수 + 빨간 불 + signal : 너 지금 스트레스 받았다
    digitalWrite(Door,LOW);
    digitalWrite(pinB,LOW);
    digitalWrite(pinR,HIGH);
    tone (piezo, freq);
    delay(2);
    noTone(piezo);
    
    LiquidCrystal_I2C lcd(39,16,2);
    lcd.begin();
    lcd.backlight();
    lcd.print("Stress eating!");
  }
  
  }
}
