/*
TK electronics DSA™
  Ten dokumentem jest dla najnowszej wersji oprogramowania modułu nadajnika płyty głownej DSA,
  przed skasowaniem lub modyfikowaniem kodu nalezy skopoiwac kod do "nadajnikDSA1" ktroy przechowuje
  starsze wersje oprogramowania.

  W celu wysłania wiadomości do serwera nalezy skorzystac z MySerial zamiast Serial poniewaz połączenie
  z węzłem odbywa się przez uart a nie usb.


*/

#include <WiFi.h>
#include <esp_now.h>

uint8_t receiverMAC1[] = {0xDC, 0x1E, 0xD5, 0xE5, 0xCE, 0x88}; // MAC pierwszego odbiornika   (LAMPA)
uint8_t receiverMAC2[] = {0x98, 0x88, 0xE0, 0xD1, 0x84, 0x70}; // MAC drugiego odbiornika     (GNIAZDKO)
uint8_t receiverMAC3[] = {0x98, 0x88, 0xE0, 0xD1, 0x7F, 0xB4}; // MAC trzeciego odbiornika    (SILNIK)

esp_now_peer_info_t peerInfo;

const int ledPin = 2;
HardwareSerial MySerial(1);

unsigned long lastPingTime = 0;
const unsigned long pingInterval = 500; // 05 sekund

void OnDataSent(const wifi_tx_info_t *tx_info, esp_now_send_status_t status) {
  Serial.print("Wysłano do: ");
  for (int i = 0; i < 6; i++) {
    Serial.printf("%02X", tx_info->des_addr[i]);
    if (i < 5) Serial.print(":");
  }

  Serial.print(" status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Sukces" : "Błąd");
}
void OnDataRecv(const esp_now_recv_info_t *recvInfo, const uint8_t *incomingData, int len) {
  char buffer[50];
  if (len >= sizeof(buffer)) len = sizeof(buffer) - 1;
  memcpy(buffer, incomingData, len);
  buffer[len] = 0;
  String command = String(buffer);
  /*
  if(command == "LAMP_ON"){
    MySerial.println("lamp_on");
  }else if (command == "LAMP_OFF"){
    MySerial.println("lamp_off");
  } else if(command == "LED_ON"){
    MySerial.println("led_on");
  } else if (command == "LED_OFF"){
    MySerial.println("led_off");
  } else if (command =="MOTOR_UP"){
    MySerial.println("motor_up");
  } else if (command == "MOTOR_DOWN"){
    MySerial.println("motor_down");
  }else if (command =="MOTOR_OFF"){
    MySerial.println("motor_off");
  }else if (command == "pong2"){
    MySerial.println("mod2active");
  }else if (command == "pong1"){
    MySerial.println("mod1active");
  }//else if (command.indexOf("Temp:") != -1){
    //MySerial.println("temp cos");
  else {
    MySerial.println(command);
  }
*/
  MySerial.println(command);
  Serial.print("Stan lampy odebrany: ");
  Serial.println(buffer);
}

void addPeer(uint8_t *mac) {
  memcpy(peerInfo.peer_addr, mac, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Nie można dodać peer-a!");
  }
}

void sendCommandToAll(String command) {
  esp_err_t result1 = esp_now_send(receiverMAC1, (uint8_t *)command.c_str(), command.length());
  esp_err_t result2 = esp_now_send(receiverMAC2, (uint8_t *)command.c_str(), command.length());
  esp_err_t result3 = esp_now_send(receiverMAC3, (uint8_t *)command.c_str(), command.length());

  if (result1 == ESP_OK) Serial.print("Wysłano do odbiornika 1: "); else Serial.println("Błąd wysyłania do odbiornika 1");
  if (result2 == ESP_OK) Serial.print("Wysłano do odbiornika 2: "); else Serial.println("Błąd wysyłania do odbiornika 2");
  if (result3 == ESP_OK) Serial.print("Wysłano do odbiornika 3: "); else Serial.println("Błąd wysyłania do odbiornika 3");
}

void setup() {
  Serial.begin(115200);
  MySerial.begin(9600, SERIAL_8N1, 5, 4); // RX, TX
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  if (esp_now_init() != ESP_OK) {
    Serial.println("Błąd inicjalizacji ESP-NOW");
    return;
  }

  // Dodawanie odbiorników
  addPeer(receiverMAC1);
  addPeer(receiverMAC2);
  addPeer(receiverMAC3);

  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);

  Serial.print("MAC nadajnika: ");
  Serial.println(WiFi.macAddress());
}

void loop() {
  static String lastCommand = "";

  // Obsługa komend z MySerial
  if (MySerial.available()) {
    String command = MySerial.readStringUntil('\n');
    command.trim();
    String commandToSend = "";

    if (command == "ledon") {
      digitalWrite(ledPin, HIGH);
      commandToSend = "ledon";
      MySerial.println("LED włączony");
    } else if (command == "ledoff") {
      digitalWrite(ledPin, LOW);
      commandToSend = "ledoff";
      MySerial.println("LED wyłączony");
    } else if (command == "lampon") {
      commandToSend = "ON";
    } else if (command == "lampoff") {
      commandToSend = "OFF";
    } else if (command == "motorup") {
      commandToSend = "motorup";
    } else if (command == "motordown") {
      commandToSend = "motordown";
    } else if (command == "motoroff") {
      commandToSend = "motoroff";
    }  else if(command == "status?mod2"){
      commandToSend = "status?mod2";
    } else if(command == "gniazdoon"){
      commandToSend = "gniazdoon";
    }else if(command == "gniazdooff"){
      commandToSend = "gniazdooff";
    }

    if (commandToSend.length() > 0 && commandToSend != lastCommand) {
      sendCommandToAll(commandToSend);
      lastCommand = commandToSend;
    }else {
      // jeśli żadna znana komenda, ustaw ping
      commandToSend = "ping";
    }
  }

  // Cyclical ping co 5 sekund, niezależnie od MySerial
  if (millis() - lastPingTime > pingInterval) {
    sendCommandToAll("ping");
    lastPingTime = millis();
  }

  delay(10); // minimalne opóźnienie dla stabilności
}