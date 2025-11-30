/*
 * Sistema de Monitoreo de Tanque - VERSIÓN NO BLOQUEANTE
 * Lógica original con correcciones de fuga - VERSIÓN CORREGIDA
 */

const int TRIG_PIN = 9;
const int ECHO_PIN = 10;
const int RAIN_SENSOR_PIN = A0;

// ===== CONFIGURACIÓN (AJUSTA ESTOS 2 VALORES) =====
const float ALTURA_TANQUE = 10.0;
const float DISTANCIA_SENSOR = 5.0;

// CONTROL DE TIEMPO (Optimizado para monitoreo de tanques)
unsigned long tiempoAnterior = 0;
const long intervalo = 1000; // Enviar datos cada 1 segundo (frecuencia óptima)

// Variables
long duracion;
float distancia;
float nivelAgua;
float porcentaje;
int humedadSensor;
int lecturasOK = 0;
int lecturasError = 0;

void setup() {
  Serial.begin(9600); // <-- BAUDRATE: 9600 para estabilidad
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RAIN_SENSOR_PIN, INPUT);
  
  Serial.println("Sistema Iniciado");
}

void loop() {
  // 1. Usamos millis() para controlar el envío sin bloquear
  unsigned long tiempoActual = millis();

  if (tiempoActual - tiempoAnterior >= intervalo) {
    tiempoAnterior = tiempoActual;
    leerSensoresYEnviar();
  }
  
  // Si tuvieras otras tareas (ej. encender un LED), irían aquí
  // y se ejecutarían sin esperar al sensor.
}

void leerSensoresYEnviar() {
  // Lógica de medición
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  duracion = pulseIn(ECHO_PIN, HIGH, 30000);
  bool sensorOK = (duracion > 0);
  
  if (sensorOK) {
    distancia = duracion * 0.034 / 2.0;
    if (distancia < 2 || distancia > 400) sensorOK = false;
  }
  
  if (sensorOK) {
    nivelAgua = ALTURA_TANQUE - (distancia - DISTANCIA_SENSOR);
    if (nivelAgua < 0) nivelAgua = 0;
    if (nivelAgua > ALTURA_TANQUE) nivelAgua = ALTURA_TANQUE;
    porcentaje = (nivelAgua / ALTURA_TANQUE) * 100.0;
    lecturasOK++;
  } else {
    nivelAgua = -1;
    porcentaje = -1;
    distancia = -1;
    lecturasError++;
  }
  
  String estado;
  if (!sensorOK) estado = "SinSensor";
  else if (porcentaje >= 70) estado = "Lleno";
  else if (porcentaje >= 30) estado = "Medio";
  else if (porcentaje >= 15) estado = "Bajo";
  else estado = "MuyBajo";
  
  humedadSensor = analogRead(RAIN_SENSOR_PIN);
  String estadoFuga;
  
  // ===== LÓGICA DE FUGA CORREGIDA (INVERTIDA) =====
 // 🔧 LÓGICA CORREGIDA - Más realista
if (humedadSensor < 200) {           // 0-199 = MUY MOJADO (FugaAlta)
    estadoFuga = "FugaAlta";          
} else if (humedadSensor < 400) {    // 200-399 = MOJADO (FugaMedia)  
    estadoFuga = "FugaMedia";         
} else {                             // 400-1023 = SECO (NoFuga)
    estadoFuga = "NoFuga";            
}
  
  // ===== ENVIAR DATOS POR SERIAL =====
  Serial.print("NIVEL:"); Serial.print(sensorOK ? nivelAgua : -1, 1);
  Serial.print(",PERC:"); Serial.print(sensorOK ? porcentaje : -1, 1);
  Serial.print(",ESTADO:"); Serial.print(estado);
  Serial.print(",HUM:"); Serial.print(humedadSensor);
  Serial.print(",FUGA:"); Serial.print(estadoFuga);
  Serial.print(",VALIDO:"); Serial.print(sensorOK ? "1" : "0");
  Serial.print(",DIST:"); Serial.print(sensorOK ? distancia : -1, 1);
  Serial.print(",OK:"); Serial.print(lecturasOK);
  Serial.print(",ERR:"); Serial.println(lecturasError);
}



