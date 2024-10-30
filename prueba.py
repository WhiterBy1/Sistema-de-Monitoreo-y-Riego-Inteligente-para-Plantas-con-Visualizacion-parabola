import serial
import time
import matplotlib.pyplot as plt
import numpy as np

# Configura el puerto serial (cambia 'COM8' por el puerto adecuado en tu sistema)
arduino = serial.Serial('COM8', 9600)
time.sleep(2)  # Espera para que el puerto se estabilice

# Configuración de la visualización en tiempo real
angles = []
distances = []

plt.ion()  # Habilita el modo interactivo de Matplotlib
fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})

# Configura el gráfico
ax.set_ylim(0, 200)  # Ajusta el límite de distancia (ajusta según el alcance de tu sensor)
ax.set_theta_zero_location('N')  # El cero está al norte
ax.set_theta_direction(-1)  # Dirección de ángulo en sentido horario

try:
    while True:
        # Lee la distancia enviada desde el Arduino
        if arduino.in_waiting > 0:
            distance = float(arduino.readline().decode().strip())
            print(f"Distancia medida por el sensor: {distance} cm")

            # Pide al usuario ingresar el ángulo manualmente
            angle_deg = float(input("Ingresa el ángulo actual del sensor en grados (0-360): "))
            angle_rad = np.deg2rad(angle_deg)  # Convierte el ángulo a radianes

            # Agrega el ángulo y la distancia a las listas
            angles.append(angle_rad)
            distances.append(distance)

            # Limita el historial para que solo muestre los últimos 36 ángulos (360 grados a intervalos de 10 grados)
            if len(angles) > 36:
                angles.pop(0)
                distances.pop(0)

            # Borra y actualiza el gráfico
            ax.clear()
            ax.plot(angles, distances, marker='o', color='b')
            ax.set_ylim(0, 200)  # Limita el alcance de distancia en el gráfico

            # Refresca la visualización
            plt.draw()
            plt.pause(0.01)

except KeyboardInterrupt:
    print("Conexión terminada")
finally:
    arduino.close()
