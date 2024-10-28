# Sistema de Monitoreo y Riego Inteligente para Plantas con Visualización en 3D

## Descripción del Proyecto
Este repositorio contiene un sistema integral de monitoreo y riego inteligente para plantas, diseñado para optimizar el uso de agua en función de datos en tiempo real. El sistema utiliza sensores de humedad en el suelo y simula trayectorias de riego tanto en 3D como en 2D para determinar el ángulo óptimo de las bombas de agua. Esto permite que el agua llegue precisamente a las áreas que necesitan hidratación, basándose en los niveles de humedad detectados en el suelo.

Este proyecto es ideal para desarrolladores y entusiastas de la tecnología agrícola interesados en sistemas de riego automatizado, simulación física y visualización de datos. Cada componente del repositorio puede ser utilizado de manera independiente o como parte de un sistema completo de monitoreo y análisis.

## Contenidos del Repositorio

### 1. Simulación de Trayectoria de Riego en 3D
   - Descripción: Una interfaz interactiva desarrollada con Three.js para simular la trayectoria parabólica del agua lanzada por las bombas. Utilizando los datos de humedad en el suelo, la simulación calcula el ángulo óptimo para que el agua alcance las áreas específicas de la planta que necesitan riego.
   - Tecnologías: JavaScript, Three.js
   - Archivo principal: `simulacion.html`

### 2. Recolección y Envío de Datos desde un ESP32
   - Descripción: Código en Arduino para el microcontrolador ESP32, que recopila datos de sensores de temperatura y humedad en tiempo real y los envía a un servidor TCP. Esta funcionalidad es esencial para aplicaciones de monitoreo remoto en entornos IoT, permitiendo un control continuo sobre los niveles de humedad en el suelo.
   - Tecnologías: Arduino, ESP32
   - Archivo principal: `Esp32_collect_send_data.ino`

### 3. Servidor TCP y Dashboard en Tiempo Real
   - Descripción: Una aplicación basada en Flask y Dash que recibe datos de los sensores en tiempo real, los almacena en un DataFrame de pandas y muestra métricas en un dashboard interactivo. Los gráficos en tiempo real permiten tomar decisiones informadas sobre el riego, con visualización de indicadores como la temperatura y humedad del suelo.
   - Tecnologías: Python, Flask, Dash, Plotly
   - Archivo principal: `import socket.py`

### 4. Simulación de Trayectoria en 2D
   - Descripción: Script en Python que utiliza Matplotlib y SciPy para simular la trayectoria de riego en un espacio bidimensional. Este script permite ajustar parámetros como el ángulo y la velocidad de lanzamiento para que el riego sea lo más preciso posible, adaptándose a las necesidades de la planta según los datos de humedad.
   - Tecnologías: Python, Matplotlib, SciPy
   - Archivo principal: `tract.py`

## Cómo Ejecutar el Proyecto

### Requisitos
- Python: Asegúrate de tener Python 3.x instalado en tu sistema.
- Instalación de Dependencias: Puedes instalar todas las dependencias necesarias utilizando el archivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Instrucciones

1. Servidor TCP y Dashboard en Tiempo Real:
   - Navega a la carpeta del proyecto que contiene `import socket.py`.
   - Ejecuta el servidor TCP y el dashboard con el siguiente comando:

```bash
python import\ socket.py
```

   - Accede al dashboard en `http://localhost:8050` para ver los datos en tiempo real.

2. Simulación de Trayectoria en 2D:
   - Ejecuta el script `tract.py` en Python:

```bash
python tract.py
```


   - Esto abrirá una ventana de Matplotlib con la simulación en 2D de la trayectoria de riego.

3. Simulación de Trayectoria de Riego en 3D:
   - Abre `simulacion.html` en un navegador compatible para ver la simulación en 3D de la trayectoria del agua.

## Estructura de Archivos

- `simulacion.html` - Simulación de trayectoria de riego en 3D con Three.js.
- `Esp32_collect_send_data.ino` - Código para el microcontrolador ESP32 que envía datos de sensores.
- `import socket.py` - Servidor TCP que recibe datos y los visualiza en un dashboard en tiempo real.
- `tract.py` - Simulación de trayectoria en 2D utilizando Matplotlib y SciPy.
- `config.h` - Archivo de configuración (excluido del repositorio) para las credenciales de WiFi y la IP del servidor en el ESP32.


## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.
