#include "esp_camera.h"
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <VL53L0X.h>

// ================= WIFI =================
const char* ssid = "SAI";
const char* password = "Sai@1234";

// ================= SERVER =================
String serverUrl = "http://10.37.156.72:8080/upload";
// ================= PINS =================
#define BUTTON_PIN 12
#define MOTOR_PIN 13
#define SDA_PIN 14
#define SCL_PIN 15

// ================= SENSOR =================
VL53L0X sensor;

// ================= CAMERA CONFIG =================
#define PWDN_GPIO_NUM     32
#define RESET_GPIO_NUM    -1
#define XCLK_GPIO_NUM      0
#define SIOD_GPIO_NUM     26
#define SIOC_GPIO_NUM     27
#define Y9_GPIO_NUM       35
#define Y8_GPIO_NUM       34
#define Y7_GPIO_NUM       39
#define Y6_GPIO_NUM       36
#define Y5_GPIO_NUM       21
#define Y4_GPIO_NUM       19
#define Y3_GPIO_NUM       18
#define Y2_GPIO_NUM        5
#define VSYNC_GPIO_NUM    25
#define HREF_GPIO_NUM     23
#define PCLK_GPIO_NUM     22

// ================= SETUP =================
void setup() {
  Serial.begin(115200);

  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(MOTOR_PIN, OUTPUT);
  digitalWrite(MOTOR_PIN, LOW);

  // I2C
  Wire.begin(SDA_PIN, SCL_PIN);

  // Sensor init
  if (!sensor.init()) {
    Serial.println("VL53L0X not detected!");
    while (1);
  }
  sensor.setTimeout(500);
  sensor.startContinuous();

  // Camera init
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;

  config.frame_size = FRAMESIZE_VGA;
  config.jpeg_quality = 12;
  config.fb_count = 1;

  esp_camera_init(&config);

  // WiFi connect
  WiFi.begin(ssid, password);
  Serial.print("Connecting WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected");
}

// ================= SEND IMAGE =================
void sendImage() {
  camera_fb_t * fb = esp_camera_fb_get();

  if (!fb) {
    Serial.println("Camera failed");
    return;
  }

  WiFiClient client;
  HTTPClient http;

  http.begin(client, serverUrl);

  String boundary = "----123456789";
  http.addHeader("Content-Type", "multipart/form-data; boundary=" + boundary);

  String bodyStart = "--" + boundary + "\r\n";
  bodyStart += "Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n";
  bodyStart += "Content-Type: image/jpeg\r\n\r\n";

  String bodyEnd = "\r\n--" + boundary + "--\r\n";

  int totalLen = bodyStart.length() + fb->len + bodyEnd.length();
  http.addHeader("Content-Length", String(totalLen));

  WiFiClient * stream = http.getStreamPtr();

  http.POST("");

  stream->print(bodyStart);
  stream->write(fb->buf, fb->len);
  stream->print(bodyEnd);

  Serial.println("Image Sent");

  int responseCode = http.GET();
  Serial.print("Response: ");
  Serial.println(responseCode);

  String response = http.getString();
  Serial.println(response);

  esp_camera_fb_return(fb);
  http.end();
}

// ================= LOOP =================
void loop() {

  int distance = sensor.readRangeContinuousMillimeters();

  Serial.print("Distance: ");
  Serial.println(distance);

  // 🔴 OBSTACLE DETECTED
  if (distance < 500) {
    Serial.println("Obstacle!");

    // Vibration
    digitalWrite(MOTOR_PIN, HIGH);
    delay(200);
    digitalWrite(MOTOR_PIN, LOW);

    // Capture + send
    sendImage();

    delay(3000);
  }

  // 🔘 BUTTON TRIGGER
  if (digitalRead(BUTTON_PIN) == LOW) {
    Serial.println("Button Pressed");

    sendImage();
    delay(2000);
  }

  delay(200);
}