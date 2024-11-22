
# Sistema de Monitoreo y Simulación de Sensores con visualizacion de parabola

Este proyecto combina hardware y software para recolectar, analizar y simular datos físicos relacionados con sensores de temperatura, humedad y mecánica clásica. Se implementan conceptos de física, como trayectorias parabólicas y análisis de condiciones ambientales, aplicando tecnologías modernas como microcontroladores, Python y Dash para visualización en tiempo real. 

---

## Estructura del Proyecto

### Directorios y Archivos

- **Esp32_collect_send_data.ino**: Código para la recolección de datos en un ESP32 utilizando sensores como DHT22, DHT11, LM35 y sensores de humedad de suelo. Los datos se envían a un servidor.
- 
- **config.h**: Archivo de configuración para el ESP32, que incluye credenciales de red y parámetros del servidor.
- **AnalisisDatos.py**: Servidor Python que recibe, procesa y visualiza los datos en tiempo real utilizando Dash.
- **Datos_De_Prueba.py**: Script para generar datos simulados y probar el sistema sin hardware real.
- **Angulo_search.py**: Script para calcular distancias utilizando un sensor (o datos simulados), optimizando parámetros para trayectorias parabólicas.
- **tract.py**: Simulación de trayectorias parabólicas basada en física clásica. Calcula ángulos óptimos, ecuaciones de trayectoria y genera gráficos interactivos.
- **requirements.txt**: Lista de dependencias necesarias para el entorno Python.
- **simulacion.html**: Interfaz HTML que complementa las visualizaciones y simulaciones.
- **.gitignore**: Archivo para excluir archivos temporales, entornos virtuales y configuraciones específicas del IDE.       

---

## Detalles de los Archivos -- funcionalidad -- 

### Esp32_collect_send_data.ino

Este archivo configura un ESP32 para recolectar datos desde múltiples sensores y enviarlos a un servidor mediante comunicación WiFi.

#### Características

1. **Sensores Utilizados**:
   - **DHT22 y DHT11**: Miden temperatura y humedad.
   - **LM35**: Mide temperatura de manera analógica.
   - **Sensores de Suelo**: Miden humedad en el suelo.

2. **Conexión a WiFi**:
   Permite transmitir los datos recolectados al servidor remoto.

3. **Formato de Datos**:
   Los datos se formatean como una cadena CSV que incluye temperatura, humedad y promedios calculados.

4. **Cálculo de Promedios**:
   - Promedio de temperaturas de todos los sensores.
   - Promedio de humedades del suelo.

5. **Ciclo de Recolección**:
   Cada dos segundos, se recolectan y envían los datos.

---

### AnalisisDatos.py

Servidor desarrollado en Python que analiza los datos recibidos del ESP32. Incluye visualización en tiempo real mediante Dash.

#### Características

1. **Recepción de Datos**:
   Recibe cadenas CSV enviadas desde el ESP32 y las almacena en un DataFrame de pandas.

2. **Visualización en Tiempo Real**:
   Utiliza Dash y Plotly para mostrar:
   - Gráficos de temperatura y humedad.
   - Indicadores clave como temperatura máxima, humedad promedio y cantidad de datos registrados.

3. **Actualización Automática**:
   Los gráficos y estadísticas se actualizan automáticamente cada dos segundos.

4. **Interfaz**:
   Incluye una interfaz interactiva para analizar las tendencias y patrones en los datos recolectados.

---

### Datos_De_Prueba.py

Script diseñado para pruebas en ausencia del hardware real. Genera datos simulados con rangos definidos de temperatura y humedad.

#### Características

1. **Generación de Datos Simulados**:
   - Los datos se crean utilizando distribuciones aleatorias dentro de límites establecidos.
   - Incluye fluctuaciones naturales para simular condiciones reales.

2. **Visualización Similar al Servidor Real**:
   Reutiliza el mismo sistema de visualización en Dash para observar los datos simulados.

---

### Angulo_search.py

Script que calcula distancias utilizando un sensor conectado a un Arduino o valores simulados.

#### Características

1. **Cálculo de Distancia**:
   Procesa datos de sensores para calcular distancias promedio, esenciales para ajustar trayectorias parabólicas.

2. **Modo de Prueba**:
   Incluye un modo de simulación para generar datos en ausencia de hardware real.

3. **Aplicación Física**:
   Utiliza la distancia calculada como parámetro clave en simulaciones parabólicas.

---

### tract.py

Este script modela trayectorias parabólicas y visualiza los resultados, integrando conceptos clave de física mecánica.      

#### Características

1. **Cálculo del Ángulo Óptimo**:
   Utiliza física clásica para determinar el ángulo necesario para alcanzar un objetivo dado:
   ```
   θ = (1/2) * arcsin((g * x_target) / v0²)
   ```
   Donde:
   - **g**: Gravedad (9.81 m/s²).
   - **x_target**: Distancia objetivo en el eje x.
   - **v0**: Velocidad inicial.

2. **Ecuación de la Parábola**:
   Calcula la trayectoria en función de \(x\):
   ```
   y = tan(θ) * x - (g / (2 * v0² * cos²(θ))) * x²
   ```

3. **Visualización Interactiva**:
   - Grafica la trayectoria del proyectil.
   - Incluye vectores dinámicos que representan velocidad en \(x\), \(y\) y la resultante.

4. **Interacción**:
   Permite seleccionar puntos específicos en el gráfico para mostrar valores detallados de tiempo, velocidad y posición.    

---
## Detalles de los Archivos -- Codigo -- 

## Esp32_collect_send_data.ino

Este código recolecta datos físicos (temperatura, humedad y humedad del suelo) desde sensores conectados a un ESP32 y los transmite a un servidor.

### Funcionamiento

1. **Conexión a WiFi**:
   Se conecta a una red para transmitir los datos recolectados.
   ```
   WiFi.begin(ssid, password);
   while (WiFi.status() != WL_CONNECTED) {
       delay(500);
   }
   ```

2. **Lectura de Sensores**:
   Los sensores DHT22 y DHT11 miden temperatura y humedad, mientras que los LM35 y sensores de suelo obtienen datos adicionales.
   ```
   float tempDHT22 = dht22.readTemperature();
   float humedadDHT22 = dht22.readHumidity();
   float humedadSuelo1 = analogRead(SOIL_PIN1);
   ```

3. **Cálculo de Promedios**:
   Calcula promedios de temperatura y humedad para análisis más precisos.
   ```
   float promedioTemp = (tempDHT22 + tempDHT11) / 2.0;
   ```

4. **Transmisión de Datos**:
   Los datos recolectados se envían al servidor en formato CSV.
   ```
   String datos = String(tempDHT22) + "," + String(humedadDHT22);
   client.println(datos);
   ```

---

## AnalisisDatos.py

Servidor Python que recibe y analiza datos enviados por el ESP32. Utiliza Dash para la visualización en tiempo real.        

### Funcionamiento

1. **Recepción de Datos**:
   Los datos recibidos por el servidor se almacenan en un DataFrame.
   ```
   data = self.request.recv(1024).strip()
   parts = message.split(",")
   data_df = pd.concat([data_df, pd.DataFrame([new_data])], ignore_index=True)
   ```

2. **Visualización**:
   Se crean gráficos interactivos para monitorear temperaturas y humedades en tiempo real.
   ```
   temperature_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["temperatura_DHT22"], mode='lines+markers'))      
   ```

3. **Indicadores Clave**:
   Muestra valores máximos, promedios y cantidad de datos registrados.
   ```
   max_temp = data_df[["temperatura_DHT22", "temperatura_DHT11"]].max().max()
   ```

---

## tract.py

Simula trayectorias parabólicas con un enfoque en la física mecánica. Calcula ángulos y ecuaciones clave.

### Funcionamiento

1. **Cálculo del Ángulo Óptimo**:
   Determina el ángulo necesario para alcanzar un objetivo dado:
   ```
   theta_rad = 0.5 * np.arcsin((g * x_target) / (v0 ** 2))
   ```

2. **Ecuación de la Parábola**:
   Describe la trayectoria en función de \(x\):
   ```
   y = tan(theta) * x - (g / (2 * v0**2 * cos(theta)**2)) * x**2
   ```

3. **Visualización**:
   Muestra la trayectoria y vectores dinámicos de velocidad:
   ```
   vector_vx = ax.quiver(x, y, vx, 0, angles='xy', scale_units='xy', scale=escala_vectores, color='red')
   ```

---


## Instalación

### Requisitos Previos

1. **Hardware**:
   - ESP32.
   - Sensores de temperatura y humedad (DHT22, DHT11, LM35, sensores de suelo).
   - Arduino para pruebas con `Angulo_search.py`.

2. **Software**:
   - Python 3.8 o superior.
   - IDE Arduino.

### Pasos

1. Clona el repositorio:
   ```
   git clone https://github.com/Sistema-de-Monitoreo-y-Riego-Inteligente-para-Plantas-con-Visualizacion-parabola
   ```

2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

3. Sube el código `Esp32_collect_send_data.ino` al ESP32 usando el IDE de Arduino.

---

## Uso

1. **Recolección de Datos**:
   - Ejecuta el código en el ESP32 para iniciar la recolección de datos.
   - Inicia el servidor Python ejecutando `AnalisisDatos.py`.

2. **Simulación de Datos**:
   - Usa `Datos_De_Prueba.py` para probar el sistema sin hardware real.

3. **Simulación de Trayectorias**:
   - Ejecuta `tract.py` para calcular y visualizar trayectorias parabólicas basadas en física clásica.

---

## Conexión Física y Mecánica

Este proyecto aplica conceptos de física clásica en tres áreas principales:

1. **Cinemática**:
   - Cálculo y simulación de trayectorias parabólicas.
   - Representación de vectores dinámicos de velocidad y posición.

2. **Termodinámica**:
   - Análisis de temperaturas y humedades recolectadas.
   - Relación entre las variables ambientales.

3. **Dinámica**:
   - Cálculo de fuerzas involucradas en movimientos proyectiles.
   - Uso de modelos matemáticos para describir el comportamiento del sistema.

---

## Contribuciones

Si deseas contribuir:

1. Haz un fork del repositorio.
2. Realiza tus cambios en una rama separada.
3. Envía un pull request detallando tus mejoras.

¡Gracias por usar este sistema de monitoreo y simulación! 🚀


