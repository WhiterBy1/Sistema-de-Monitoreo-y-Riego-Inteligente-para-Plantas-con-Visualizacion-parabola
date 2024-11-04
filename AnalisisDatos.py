import socketserver
import threading
import pandas as pd
import datetime
from flask import Flask
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# Datos recibidos (almacenados en un DataFrame para facilitar el análisis)
data_df = pd.DataFrame(columns=["timestamp", "temperatura_DHT22", "temperatura_DHT11", 
                                "temperatura_LM35_1", "temperatura_LM35_2", 
                                "humedad_suelo_1", "humedad_suelo_2", 
                                "humedad_suelo_3", "humedad_DHT22", "humedad_DHT11",
                                "promedio_temperatura"])

# Clase para manejar las conexiones al servidor
class SensorTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        global data_df
        while True:
            try:
                data = self.request.recv(1024).strip()
                if not data:
                    break

                message = data.decode('utf-8').strip()
                if not message:
                    continue

                print(f"Datos recibidos: {message}")

                # Separar los datos por comas
                try:
                    parts = message.split(",")
                    if len(parts) == 10:
                        # Convertir las partes a float
                        tempDHT22, tempDHT11, tempLM35_1, tempLM35_2, humedadSuelo1, humedadSuelo2, humedadSuelo3, humedadDHT22, humedadDHT11, promedioTemp = map(float, parts)
                        new_data = {
                            "timestamp": datetime.datetime.now(),
                            "temperatura_DHT22": tempDHT22,
                            "temperatura_DHT11": tempDHT11,
                            "temperatura_LM35_1": tempLM35_1,
                            "temperatura_LM35_2": tempLM35_2,
                            "humedad_suelo_1": humedadSuelo1,
                            "humedad_suelo_2": humedadSuelo2,
                            "humedad_suelo_3": humedadSuelo3,
                            "humedad_DHT22": humedadDHT22,
                            "humedad_DHT11": humedadDHT11,
                            "promedio_temperatura": promedioTemp
                        }
                        data_df = pd.concat([data_df, pd.DataFrame([new_data])], ignore_index=True)
                        if len(data_df) > 100:
                            data_df = data_df.iloc[-100:]
                    else:
                        print(f"Error: Número de partes incorrecto ({len(parts)}) en los datos recibidos: {message}")
                except ValueError as e:
                    print(f"Error al procesar los datos recibidos: {e}")

            except ConnectionResetError:
                print("Conexión restablecida por el cliente")
                break

# Configurar el servidor en un hilo separado
def start_tcp_server():
    server = socketserver.ThreadingTCPServer(("0.0.0.0", 12345), SensorTCPHandler)
    print("Servidor TCP escuchando en el puerto 12345...")
    server.serve_forever()

# Iniciar el servidor TCP en un hilo
tcp_thread = threading.Thread(target=start_tcp_server, daemon=True)
tcp_thread.start()

# Configurar la aplicación Dash
server = Flask(__name__)
app = Dash(__name__, server=server)

# Layout del Dashboard
app.layout = html.Div([
    html.H1("Dashboard de Sensores - Visualización Atractiva", style={"textAlign": "center"}),

    # Indicadores Resumen
    html.Div([
        html.Div([
            html.H4("Temperatura Máxima Registrada"),
            html.P(id="max-temp", style={"fontSize": "30px"})
        ], className="indicator"),
        html.Div([
            html.H4("Humedad Promedio Actual (%)"),
            html.P(id="avg-humidity", style={"fontSize": "30px"})
        ], className="indicator"),
        html.Div([
            html.H4("Cantidad de Datos Registrados"),
            html.P(id="data-count", style={"fontSize": "30px"})
        ], className="indicator"),
    ], className="summary-indicators", style={"display": "flex", "justifyContent": "space-around"}),

    # Gráfico de Temperaturas
    dcc.Graph(id="live-temperature-graph"),

    # Gráfico de Humedad
    dcc.Graph(id="live-humidity-graph"),

    # Intervalo para actualizar gráficos automáticamente
    dcc.Interval(
        id="interval-component",
        interval=2000,
        n_intervals=0
    )
], style={"margin": "20px"})

# Actualización de los gráficos y los indicadores
@app.callback(
    [
        Output("live-temperature-graph", "figure"),
        Output("live-humidity-graph", "figure"),
        Output("max-temp", "children"),
        Output("avg-humidity", "children"),
        Output("data-count", "children")
    ],
    [Input("interval-component", "n_intervals")]
)
def update_graphs(n):
    global data_df

    if data_df.empty:
        return go.Figure(), go.Figure(), "N/A", "N/A", "0"

    # Gráfico de Temperaturas
    temperature_fig = go.Figure()
    temperature_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["temperatura_DHT22"], mode='lines+markers', name="Temp DHT22 (°C)"))
    temperature_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["temperatura_DHT11"], mode='lines+markers', name="Temp DHT11 (°C)"))
    temperature_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["temperatura_LM35_1"], mode='lines+markers', name="Temp LM35_1 (°C)"))
    temperature_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["temperatura_LM35_2"], mode='lines+markers', name="Temp LM35_2 (°C)"))
    temperature_fig.update_layout(title="Temperaturas en Tiempo Real", xaxis_title="Tiempo", yaxis_title="Temperatura (°C)", template="plotly_dark")

    # Gráfico de Humedades
    humidity_fig = go.Figure()
    humidity_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["humedad_suelo_1"], mode='lines+markers', name="Humedad Suelo 1 (%)"))
    humidity_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["humedad_suelo_2"], mode='lines+markers', name="Humedad Suelo 2 (%)"))
    humidity_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["humedad_suelo_3"], mode='lines+markers', name="Humedad Suelo 3 (%)"))
    humidity_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["humedad_DHT22"], mode='lines+markers', name="Humedad DHT22 (%)"))
    humidity_fig.add_trace(go.Scatter(x=data_df["timestamp"], y=data_df["humedad_DHT11"], mode='lines+markers', name="Humedad DHT11 (%)"))
    humidity_fig.update_layout(title="Humedad en Tiempo Real", xaxis_title="Tiempo", yaxis_title="Humedad (%)", template="plotly_dark")

    # Indicadores Resumen
    max_temp = data_df[["temperatura_DHT22", "temperatura_DHT11", "temperatura_LM35_1", "temperatura_LM35_2"]].max().max()
    avg_humidity = data_df[["humedad_suelo_1", "humedad_suelo_2", "humedad_suelo_3", "humedad_DHT22", "humedad_DHT11"]].mean().mean()
    data_count = len(data_df)

    return temperature_fig, humidity_fig, f"{max_temp:.2f} °C", f"{avg_humidity:.2f} %", str(data_count)

# Ejecutar el servidor de Dash
if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)
