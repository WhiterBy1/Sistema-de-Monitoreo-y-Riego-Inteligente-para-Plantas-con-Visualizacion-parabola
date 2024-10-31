import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Parámetros
g = 9.81  # Gravedad (m/s²)
v0 = 25  # Velocidad inicial (m/s)
x_target = float(input("Ingrese la distancia en el eje x donde quiere que la altura sea 0: "))
escala_vectores = float(input("Ingrese el valor de escala para los vectores de velocidad (prueba distintos valores): "))

# Comprobar si el objetivo es alcanzable con la velocidad inicial dada
s = (g * x_target) / (v0 ** 2)
if abs(s) > 1:
    print("El objetivo está fuera del alcance máximo para la velocidad inicial dada.")
    exit()

# Calcular el ángulo óptimo usando física
theta_rad = 0.5 * np.arcsin(s)
angulo_optimo = np.degrees(theta_rad)

# Mostrar resultados del debug
print(f"El ángulo óptimo para que la altura en x = {x_target} sea 0 es aproximadamente: {angulo_optimo:.2f}°")
# Cálculo del ángulo óptimo usando física
theta_rad = 0.5 * np.arcsin((g * x_target) / (v0 ** 2))
angulo_optimo = np.degrees(theta_rad)

# Parámetros para la ecuación de la parábola
tan_theta = np.tan(theta_rad)
cos_theta_squared = np.cos(theta_rad) ** 2

# Mostrar la ecuación de la parábola en la terminal
print(f"Ecuación de la parábola: y = {tan_theta:.3f} * x - ({g / (2 * v0**2 * cos_theta_squared):.3f}) * x^2")

# Generar puntos para la trayectoria con el ángulo óptimo
angle_rad = theta_rad
t_max = (2 * v0 * np.sin(angle_rad)) / g  # Tiempo total de vuelo
t_vals = np.linspace(0, t_max, 500)  # Valores de tiempo

# Calcular posiciones (x, y) en función del tiempo
x_vals = v0 * np.cos(angle_rad) * t_vals
y_vals = v0 * np.sin(angle_rad) * t_vals - (0.5 * g * t_vals**2)
y_vals = np.maximum(y_vals, 0)  # Asegurarse de que y no sea negativo (no caer por debajo del suelo)

# Configurar la figura de Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(0, x_target * 1.5)
ax.set_ylim(0, max(y_vals) * 1.5)
ax.set_xlabel("Distancia (m)")
ax.set_ylabel("Altura (m)")
ax.set_title(f"Trayectoria Parabólica (Ángulo = {angulo_optimo:.2f}°)")

# Elementos de la animación
trajectory_line, = ax.plot([], [], 'b-', lw=2)  # Línea de trayectoria
position_dot, = ax.plot([], [], 'ro')  # Punto de la posición

# Texto para mostrar datos
time_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
velocity_text = ax.text(0.02, 0.90, '', transform=ax.transAxes)

# Vectores de velocidad (quiver), etiquetas y vector de posición
vectors = []
labels = []

# Función de inicialización
def init():
    trajectory_line.set_data([], [])
    position_dot.set_data([], [])
    time_text.set_text('')
    velocity_text.set_text('')
    # Limpiar los vectores y etiquetas
    global vectors, labels
    for vec in vectors:
        vec.remove()
    for lbl in labels:
        lbl.remove()
    vectors = []
    labels = []
    return trajectory_line, position_dot, time_text, velocity_text

# Función de actualización para cada cuadro de la animación
def update(frame):
    t = t_vals[frame]
    x = x_vals[frame]
    y = y_vals[frame]
    
    # Actualizar la línea de trayectoria
    trajectory_line.set_data(x_vals[:frame], y_vals[:frame])
    
    # Actualizar el punto de posición
    position_dot.set_data([x], [y])
    
    # Calcular componentes de velocidad
    vx = v0 * np.cos(angle_rad)  # Velocidad en x constante
    vy = v0 * np.sin(angle_rad) - g * t  # Velocidad en y cambia con el tiempo
    v = np.sqrt(vx**2 + vy**2)  # Magnitud de la velocidad resultante

    # Actualizar los vectores de velocidad
    global vectors, labels
    for vec in vectors:
        vec.remove()
    for lbl in labels:
        lbl.remove()
    vectors = []
    labels = []

    # Vector de velocidad en x (rojo)
    vector_vx = ax.quiver(x, y, vx, 0, angles='xy', scale_units='xy', scale=escala_vectores, color='red')
    vectors.append(vector_vx)
    label_vx = ax.text(x + vx * 0.1, y, 'v_x', color='red', fontsize=8)
    labels.append(label_vx)

    # Vector de velocidad en y (verde)
    vector_vy = ax.quiver(x, y, 0, vy, angles='xy', scale_units='xy', scale=escala_vectores, color='green')
    vectors.append(vector_vy)
    label_vy = ax.text(x, y + vy * 0.1, 'v_y', color='green', fontsize=8)
    labels.append(label_vy)

    # Vector de velocidad resultante (negro)
    vector_v = ax.quiver(x, y, vx, vy, angles='xy', scale_units='xy', scale=escala_vectores, color='black')
    vectors.append(vector_v)
    label_v = ax.text(x + vx * 0.1, y + vy * 0.1, 'v', color='black', fontsize=8)
    labels.append(label_v)

    # Vector de posición (azul)
    vector_position = ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color='pink')
    vectors.append(vector_position)
    label_position = ax.text(x / 2, y / 2, '  Posición', color='pink', fontsize=8)
    labels.append(label_position)

    # Actualizar el texto de tiempo y velocidad
    time_text.set_text(f'Tiempo: {t:.2f} s')
    velocity_text.set_text(f'Velocidad total: {v:.2f} m/s, Velocidad en x: {vx:.2f} m/s, Velocidad en y: {vy:.2f} m/s')
    
    return trajectory_line, position_dot, time_text, velocity_text, *vectors, *labels

# Crear la animación
ani = animation.FuncAnimation(fig, update, frames=len(t_vals), init_func=init, blit=True, interval=0.1, repeat=False)

plt.legend(["Trayectoria"])

# Conectar el evento de clic para mostrar vectores en puntos específicos
def mostrar_vectores_en_punto(x, y, vx, vy):
    global vectors, labels
    # Limpiar los vectores y etiquetas anteriores
    for vec in vectors:
        vec.remove()
    for lbl in labels:
        lbl.remove()
    vectors = []
    labels = []

    # Vector de velocidad en x (rojo)
    vector_vx = ax.quiver(x, y, vx, 0, angles='xy', scale_units='xy', scale=escala_vectores, color='red')
    vectors.append(vector_vx) 
    label_vx = ax.text(x + vx * 0.1, y, 'v_x', color='red', fontsize=8)
    labels.append(label_vx)

    # Vector de velocidad en y (verde)
    vector_vy = ax.quiver(x, y, 0, vy, angles='xy', scale_units='xy', scale=escala_vectores, color='green')
    vectors.append(vector_vy)
    label_vy = ax.text(x, y + vy * 0.1, 'v_y', color='green', fontsize=8)
    labels.append(label_vy)

    # Vector de velocidad resultante (negro)
    vector_v = ax.quiver(x, y, vx, vy, angles='xy', scale_units='xy', scale=escala_vectores, color='black')
    vectors.append(vector_v)
    label_v = ax.text(x + vx * 0.1, y + vy * 0.1, 'v', color='black', fontsize=8)
    labels.append(label_v)

    # Vector de posición (azul)
    vector_position = ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color='blue')
    vectors.append(vector_position)
    label_position = ax.text(x / 2, y / 2, 'Posición', color='blue', fontsize=8)
    labels.append(label_position)

def on_click(event):
    # Si el clic está fuera de los límites de la gráfica, no hacer nada
    if event.xdata is None or event.ydata is None:
        return

    # Obtener la coordenada x del clic
    x_click = event.xdata

    # Encontrar el índice del punto más cercano en la trayectoria
    index = (np.abs(x_vals - x_click)).argmin()

    # Obtener las coordenadas (x, y) del punto más cercano
    x = x_vals[index]
    y = y_vals[index]
    t = t_vals[index]

    # Calcular componentes de velocidad en ese punto
    vx = v0 * np.cos(angle_rad)  # Velocidad en x constante
    vy = v0 * np.sin(angle_rad) - g * t  # Velocidad en y cambia con el tiempo

    # Actualizar el punto de posición
    position_dot.set_data([x], [y])

    # Mostrar vectores en el punto seleccionado
    mostrar_vectores_en_punto(x, y, vx, vy)

    # Actualizar el texto de tiempo y velocidad
    time_text.set_text(f'Tiempo: {t:.2f} s')
    velocity_text.set_text(f'Velocidad total: {np.sqrt(vx**2 + vy**2):.2f} m/s, Velocidad en x: {vx:.2f} m/s, Velocidad en y: {vy:.2f} m/s')

    plt.draw()

# Conectar el evento de clic a la función on_click
fig.canvas.mpl_connect('button_press_event', on_click)

plt.show()
