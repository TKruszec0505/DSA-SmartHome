/*
kod przeznaczony na esp32 dla skompilowania przez arduino ide
modul smart lampy
*/

#include <WiFi.h>
#include <esp_now.h>


const int led = 1;       // LED / lampa
const int button = 2;    // Przycisk lokalny

int led_mode = 0;
bool last_button_state = false;

uint8_t transmitterMAC[] = {0xDC, 0x1E, 0xD5, 0xE5, 0xB8, 0x40}; // MAC nadajnika
esp_now_peer_info_t peerInfo;

void sendLampState() {
  String stateMsg = (led_mode == 1) ? "LAMP_ON" : "LAMP_OFF";
  esp_err_t result = esp_now_send(transmitterMAC, (uint8_t *)stateMsg.c_str(), stateMsg.length());
  if (result == ESP_OK) {
    Serial.print("Odesłano stan: ");
    Serial.println(stateMsg);
  } else {
    Serial.println("Błąd wysyłania stanu");
  }
}

void webControl(){
  String stateMsg = "pong1";
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

  if (command == "ON") {
    led_mode = 1;
    sendLampState();
  } else if (command == "OFF") {
    led_mode = 0;
    sendLampState();
  } else if (command == "ping"){
    webControl();
  }
}

void setup() {
  pinMode(led, OUTPUT);
  pinMode(button, INPUT_PULLUP);
  Serial.begin(115200);

  digitalWrite(led, LOW);

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

  if (button_state && !last_button_state) {
    led_mode = !led_mode;
    sendLampState();
    delay(200);
  }

  last_button_state = button_state;

  digitalWrite(led, (led_mode == 1) ? HIGH : LOW);
}