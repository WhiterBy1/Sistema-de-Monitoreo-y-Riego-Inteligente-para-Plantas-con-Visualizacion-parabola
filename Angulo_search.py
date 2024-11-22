import serial
import time
import matplotlib.pyplot as plt
import numpy as np


def buscar_distancia( prueba:bool):
    distances = []
    if not prueba:
        arduino = serial.Serial('COM8', 9600)
        time.sleep(2)  # Espera para que el puerto se estabilice    
        # Configuración de la visualización en tiempo real
    
    try:
        while True:
            if not prueba:
                # Lee la distancia enviada desde el Arduino
                if arduino.in_waiting > 0:
                    distance = float(arduino.readline().decode().strip())
                    print(f"Distancia medida por el sensor: {distance} cm")
            else:
                distance = np.random.uniform(10, 20)  # Simula la distancia para pruebas sin Arduino
            # Agrega el ángulo y la distancia a las listas
            distances.append(distance)
            # Limita el historial para que solo muestre los últimos 120 leidas que equivale a un segundo y calcula su promedio
            if len(distances) > 120:
                prom_distances = sum(distances)/len(distances)
                return prom_distances


    except KeyboardInterrupt:
        print("Conexión terminada")
    finally:
        if not prueba:
            arduino.close()
