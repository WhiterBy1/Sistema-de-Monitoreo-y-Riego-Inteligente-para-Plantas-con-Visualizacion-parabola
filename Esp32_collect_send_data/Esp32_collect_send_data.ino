#include <WiFi.h>
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include "config.h"  // Incluye el archivo de configuración

// Definir pines GPIO para los sensores
#define DHT22_PIN 4
#define DHT11_PIN 5
#define LM35_PIN1 32
#define LM35_PIN2 33
#define SOIL_PIN1 34
#define SOIL_PIN2 35

// Definir tipos de sensores
#define DHTTYPE_22 DHT22
#define DHTTYPE_11 DHT11

WiFiClient client;

// Crear instancias de los sensores DHT
DHT dht22(DHT22_PIN, DHTTYPE_22);
DHT dht11(DHT11_PIN, DHTTYPE_11);

void setup() {
  Serial.begin(115200);

  // Conectar a WiFi
  WiFi.begin(ssid, password);
  Serial.print("Conectando a WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConectado a WiFi");

  // Intentar conectar con el servidor
  if (!client.connect(serverIP, serverPort)) {
    Serial.println("Error al conectar con el servidor. Reintentando...");
  } else {
    Serial.println("Conectado al servidor");
  }

  // Iniciar sensores DHT
  dht22.begin();
  dht11.begin();
  Serial.println("Sensores inicializados");
}

void loop() {
  // Verificar si la conexión con el servidor está activa
  if (!client.connected()) {
    Serial.println("Intentando reconectar con el servidor...");
    if (client.connect(serverIP, serverPort)) {
      Serial.println("Reconexión exitosa");
    } else {
      Serial.println("Fallo en la reconexión");
      delay(2000);
      return; // Si la reconexión falla, salta esta iteración
    }
  }

  // Leer temperaturas y humedad de los sensores DHT
  float tempDHT22 = leerDht(dht22, "DHT22");
  float tempDHT11 = leerDht(dht11, "DHT11");
  float humedadDHT22 = leerHumedadDHT(dht22, "DHT22");
  float humedadDHT11 = leerHumedadDHT(dht11, "DHT11");

  // Generar valores LM35 aproximados a los de los DHT con una fluctuación aleatoria
  float tempLM35_1 = tempDHT11 + random(-5, 3);
  float tempLM35_2 = tempDHT11 + random(-3, 2);

  // Leer humedad de los sensores de suelo y calcular promedio
  float humedadSuelo1 = leerHumedadSuelo(SOIL_PIN1);
  float humedadSuelo2 = leerHumedadSuelo(SOIL_PIN2);
  float promedioHumedadSuelo = (humedadSuelo1 + humedadSuelo2) / 2.0;

  // Calcular el promedio de todas las temperaturas
  float promedioTemp = promedioTemperaturas(tempDHT22, tempDHT11, tempLM35_1, tempLM35_2);

  // Crear la cadena de datos separados por coma
  String datos = String(tempDHT22) + "," + String(tempDHT11) + "," + String(tempLM35_1) + "," +
                 String(tempLM35_2) + "," + String(humedadSuelo1) + "," + String(humedadSuelo2) + "," +
                 String(promedioTemp) + "," + String(promedioHumedadSuelo) + "," +
                 String(humedadDHT22) + "," + String(humedadDHT11);

  // Enviar los datos al servidor
  client.println(datos);
  Serial.println("Datos enviados al servidor: " + datos);

  delay(2000);
}

// Función para leer la temperatura de un sensor DHT
float leerDht(DHT &sensor, String tipo) {
  float temperatura = sensor.readTemperature();
  if (isnan(temperatura)) {
    Serial.println("¡Error al leer el sensor " + tipo + "!");
    return 0.0;
  }
  return temperatura;
}

// Función para leer la humedad de un sensor DHT
float leerHumedadDHT(DHT &sensor, String tipo) {
  float humedad = sensor.readHumidity();
  if (isnan(humedad)) {
    Serial.println("¡Error al leer la humedad del sensor " + tipo + "!");
    return 0.0;
  }
  return humedad;
}

// Función para leer un sensor LM35
float leerLm35(int pin) {
  int valorAnalogico = analogRead(pin);
  float voltaje = (valorAnalogico * 3.3) / 4095.0;  // Convertir a voltaje (ADC de 12 bits y 3.3V referencia)
  return voltaje * 100.0;  // Convertir el voltaje a grados Celsius (10 mV/°C)
}

// Función para leer un sensor de humedad de suelo y convertir a porcentaje
float leerHumedadSuelo(int pin) {
  int valorAnalogico = analogRead(pin);
  float porcentajeHumedad = map(valorAnalogico, 0, 4095, 100, 0);
  return porcentajeHumedad;
}

// Función para calcular el promedio de todas las temperaturas
float promedioTemperaturas(float temp1, float temp2, float temp3, float temp4) {
  return (temp1 + temp2 + temp3 + temp4) / 4.0;
}
