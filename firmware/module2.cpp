/*
kod przeznaczony na esp32 dla skompilowania przez arduino ide
modul smart gniazda
*/

#include <WiFi.h>
#include <esp_now.h>

const int led = 3;       // gniazdo ON/OFF [cewka przekaznika]

const int button = 21;   // Przycisk
const int Rled = 19;     // led czerwony
const int Gled = 10;     // led zielony

const int gniazdo2 = 4;  // gniazdo 2 ON/OFF [cewka przekaznika 2]
const int button2 = 5;   // Przycisk 2
const int Rled2 = 7;     // led czerwony 2
const int Gled2 = 6;     // led zielony 2

int led_mode = 0;
bool last_button_state = false;
int gniazdo2_mode = 0;
bool last_button2_state = false;

uint8_t transmitterMAC[] = {0xDC, 0x1E, 0xD5, 0xE5, 0xB8, 0x40}; // MAC nadajnika
esp_now_peer_info_t peerInfo;

void sendLampState() {
  String stateMsg = (led_mode == 1) ? "LED_ON" : "LED_OFF";
  esp_err_t result = esp_now_send(transmitterMAC, (uint8_t *)stateMsg.c_str(), stateMsg.length());
  if (result == ESP_OK) {
    Serial.print("Odesłano stan: ");
    Serial.println(stateMsg);
  } else {
    Serial.println("Błąd wysyłania stanu");
  }
}
void sendGniazdoState(){
  String stateMsg = (gniazdo2_mode == 1) ? "GNIAZDO2_ON" : "GNIAZDO2_OFF";
  esp_err_t result = esp_now_send(transmitterMAC, (uint8_t *)stateMsg.c_str(), stateMsg.length());
  if (result == ESP_OK){
    Serial.print("Odesłano stan: ");
    Serial.println(stateMsg);
  } else {
    Serial.println("Błąd wysyłania stanu");
  }
}
void sendCurState() {
  String curStateMsg;

  if (led_mode == 1) {
    curStateMsg = "LED_ON";
  } else if (led_mode == 0) {
    curStateMsg = "LED_OFF";
  }

  esp_err_t result = esp_now_send(transmitterMAC, (uint8_t *)curStateMsg.c_str(), curStateMsg.length());
  if (result == ESP_OK) {
    Serial.print("Odesłano stan: ");
    Serial.println(curStateMsg);
  } else {
    Serial.println("Błąd wysyłania stanu");
  }
}

void webControl(){
  String stateMsg = "pong2";
  esp_err_t result = esp_now_send(transmitterMAC, (uint8_t *)stateMsg.c_str(), stateMsg.length());
  if (result == ESP_OK) {
    Serial.print("Odesłano stan: ");
    Serial.println(stateMsg);
  } else {
    Serial.println("Błąd wysyłania stanu");
  }
}

void OnDataRecv(const esp_now_recv_info_t *recvInfo, const uint8_t *incomingData, int len) {
  char buffer[20];
  if (len >= sizeof(buffer)) len = sizeof(buffer) - 1;
  memcpy(buffer, incomingData, len);
  buffer[len] = 0;

  String command = String(buffer);
  Serial.print("Otrzymano komendę: ");
  Serial.println(command);

  if (command == "ledon") {
    led_mode = 1;
    sendLampState();
  } else if (command == "ledoff") {
    led_mode = 0;
    sendLampState();
  } else if(command == "ping"){
    webControl();
  } else if(command == "status?mod2"){
    sendLampState();
  } else if(command == "gniazdoon"){
    gniazdo2_mode = 1;
    sendGniazdoState();
  } else if(command == "gniazdooff"){
    gniazdo2_mode = 0;
    sendGniazdoState();
  }
}

void setup() {
  pinMode(led, OUTPUT);
  pinMode(gniazdo2, OUTPUT);

  pinMode(button, INPUT_PULLUP);
  pinMode(button2, INPUT_PULLUP);

  pinMode(Rled, OUTPUT);
  pinMode(Gled, OUTPUT);
  pinMode(Rled2, OUTPUT);
  pinMode(Gled2, OUTPUT);


  Serial.begin(115200);

  digitalWrite(led, LOW);
  digitalWrite(gniazdo2, LOW);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect();

  if (esp_now_init() != ESP_OK) {
    Serial.println("Błąd inicjalizacji ESP-NOW");
    return;
  }

  // Odbiór
  esp_now_register_recv_cb(OnDataRecv);

  // Dodanie nadajnika jako peer
  memcpy(peerInfo.peer_addr, transmitterMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Nie można dodać peer-a nadajnika");
    return;
  }

  Serial.print("MAC odbiornika: ");
  Serial.println(WiFi.macAddress());
}

void loop() {
  bool button_state = (digitalRead(button) == LOW);
  bool button2_state = (digitalRead(button2) == LOW);

  if (button2_state && !last_button2_state){
    gniazdo2_mode = !gniazdo2_mode;
    sendGniazdoState();
    delay(200);
  }

  last_button2_state = button2_state;

  if (button_state && !last_button_state) {
    led_mode = !led_mode;
    sendLampState();
    delay(200);
  }

  last_button_state = button_state;

  digitalWrite(gniazdo2, (gniazdo2_mode == 1) ? HIGH : LOW);

  digitalWrite(led, (led_mode == 1) ? HIGH : LOW);

  if(led_mode == 1){
    digitalWrite(Gled, HIGH);
    digitalWrite(Rled,LOW);
  }else{
    digitalWrite(Gled, LOW);
    digitalWrite(Rled,HIGH);
  }

  if(gniazdo2_mode == 1){
    digitalWrite(Gled2, HIGH);
    digitalWrite(Rled2,LOW);
  }else{
    digitalWrite(Gled2, LOW);
    digitalWrite(Rled2,HIGH);
  }

}