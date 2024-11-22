import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Initialize DataFrame with simulated values
data_df = pd.DataFrame(columns=[
    "timestamp", "temperatura_DHT22", "temperatura_DHT11", 
    "temperatura_LM35_1", "temperatura_LM35_2", 
    "humedad_suelo_1", "humedad_suelo_2", "humedad_suelo_3", 
    "humedad_DHT22", "humedad_DHT11", "promedio_temperatura"
])

# Constants for sensor ranges
TEMP_MIN, TEMP_MAX = 15, 35
HUMIDITY_MIN, HUMIDITY_MAX = 20, 80
def create_color_legend():
    sensors = ["Humedad Suelo 1", "Humedad Suelo 2", "Humedad Suelo 3", "DHT22", "DHT11"]
    colors = ['#6C0694', '#ED9B19', '#5B11BB', '#93E59C', '#ECF08A']
    
    legend_items = []
    for sensor, color in zip(sensors, colors):
        legend_items.append(
            dbc.Row([
                dbc.Col(
                    html.Div(style={"width": "20px", "height": "20px", "backgroundColor": color, "marginRight": "10px"}),
                    width="auto"
                ),
                dbc.Col(html.Span(sensor), width="auto")
            ], className="mb-1")
        )
    
    return dbc.Card(
        dbc.CardBody(legend_items),
        className="mt-4"
    )
def generate_simulated_data():
    global data_df
    now = pd.Timestamp.now()
    base_temp = 25
    base_hum = 55
    simulated_data = {
        "timestamp": now,
        "temperatura_DHT22": np.random.uniform(base_temp - 1.5, base_temp + 1.5),
        "temperatura_DHT11": np.random.uniform(base_temp - 1.0, base_temp + 1.0),
        "temperatura_LM35_1": np.random.uniform(base_temp - 1.0, base_temp + 2.0),
        "temperatura_LM35_2": np.random.uniform(base_temp - 1.0, base_temp + 2.0),
        "humedad_suelo_1": np.random.uniform(base_hum - 5, base_hum + 5),
        "humedad_suelo_2": np.random.uniform(base_hum - 5, base_hum + 5),
        "humedad_suelo_3": np.random.uniform(base_hum - 5, base_hum + 5),
        "humedad_DHT22": np.random.uniform(base_hum - 3, base_hum + 3),
        "humedad_DHT11": np.random.uniform(base_hum - 3, base_hum + 3),
    }
    simulated_data["promedio_temperatura"] = np.mean([
        simulated_data["temperatura_DHT22"],
        simulated_data["temperatura_DHT11"],
        simulated_data["temperatura_LM35_1"],
        simulated_data["temperatura_LM35_2"]
    ])
    data_df = pd.concat([data_df, pd.DataFrame([simulated_data])], ignore_index=True)
    if len(data_df) > 100:
        data_df = data_df.iloc[-100:]

# Configure Dash application with dark theme
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Custom styles
COLORS = {
    'background': '#303030',
    'text': '#FFFFFF',
    'grid': '#555555',
    'warning': '#FFA500',
    'danger': '#FF4136',
    'success': '#2ECC40'
}

# Dashboard Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🌱 Sistema de Monitoreo de Invernadero Inteligente", 
                    className="text-center mb-4"),
            html.P("Monitoreo en tiempo real de temperatura y humedad para cultivos óptimos",
                   className="text-center text-muted mb-5")
        ])
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🌡️ Temperatura Promedio", className="card-title"),
                    html.P(id="avg-temp", className="card-text display-4")
                ])
            ], color="primary", inverse=True)
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("💧 Humedad Promedio", className="card-title"),
                    html.P(id="avg-humidity", className="card-text display-4")
                ])
            ], color="info", inverse=True)
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Muestras Registradas", className="card-title"),
                    html.P(id="data-count", className="card-text display-4")
                ])
            ], color="success", inverse=True)
        ], width=4),
    ], className="mb-4"),
    
    # Add this new row for the color legend
    dbc.Row([
        dbc.Col([
            html.H4("Leyenda de Sensores", className="mb-3"),
            create_color_legend()
        ], width=12)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="live-temperature-graph")
        ], width=12, className="mb-4"),
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id="live-humidity-graph")
        ], width=12, className="mb-4"),
    ]),

    dbc.Row([
        dbc.Col([
            html.H4("Estadísticas Detalladas", className="mb-3"),
            html.Div(id="detailed-stats")
        ], width=12)
    ]),

    dcc.Interval(id="interval-component", interval=2000, n_intervals=0)
], fluid=True, style={"backgroundColor": COLORS['background'], "color": COLORS['text']})



@app.callback(
    [Output("live-temperature-graph", "figure"),
     Output("live-humidity-graph", "figure"),
     Output("avg-temp", "children"),
     Output("avg-humidity", "children"),
     Output("data-count", "children"),
     Output("detailed-stats", "children")],
    [Input("interval-component", "n_intervals")]
)
def update_graphs(n):
    global data_df
    generate_simulated_data()

    common_layout = dict(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text']),
        margin=dict(l=60, r=30, t=50, b=50)
    )

    # Temperature Graph
    temp_fig = go.Figure()
    temp_fig.add_hrect(y0=TEMP_MIN, y1=TEMP_MAX, fillcolor="rgba(0, 255, 0, 0.1)", line_width=0, layer="below")
    
    temp_vars = ["temperatura_DHT22", "temperatura_DHT11", "temperatura_LM35_1", "temperatura_LM35_2"]
    colors = [ '#93E59C', '#ECF08A', '#45B7D1', '#FFA07A']
    
    for temp_var, color in zip(temp_vars, colors):
        temp_fig.add_trace(go.Scatter(
            x=data_df["timestamp"], y=data_df[temp_var],
            name=temp_var.replace('_', ' ').title(),
            line=dict(color=color, width=2), mode='lines+markers'
        ))

    temp_fig.update_layout(
        title="Monitoreo de Temperatura",
        yaxis=dict(range=[TEMP_MIN-5, TEMP_MAX+5], title="Temperatura (°C)"),
        xaxis=dict(title="Tiempo"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **common_layout
    )

    # Humidity Graph
    hum_fig = go.Figure()
    hum_fig.add_hrect(y0=HUMIDITY_MIN, y1=HUMIDITY_MAX, fillcolor="rgba(0, 0, 255, 0.1)", line_width=0, layer="below")
    
    hum_vars = ["humedad_suelo_1", "humedad_suelo_2", "humedad_suelo_3", "humedad_DHT22", "humedad_DHT11"]
    colors = ['#6C0694', '#ED9B19', '#5B11BB', '#93E59C', '#ECF08A']
    
    for hum_var, color in zip(hum_vars, colors):
        hum_fig.add_trace(go.Scatter(
            x=data_df["timestamp"], y=data_df[hum_var],
            name=hum_var.replace('_', ' ').title(),
            line=dict(color=color, width=2), mode='lines+markers'
        ))

    hum_fig.update_layout(
        title="Monitoreo de Humedad",
        yaxis=dict(range=[HUMIDITY_MIN-10, HUMIDITY_MAX+10], title="Humedad (%)"),
        xaxis=dict(title="Tiempo"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        **common_layout
    )

    # Calculate indicators
    avg_temp = data_df[temp_vars].mean().mean()
    avg_humidity = data_df[hum_vars].mean().mean()
    data_count = len(data_df)

    # Detailed statistics
    temp_stats = data_df[temp_vars].agg(['mean', 'min', 'max']).round(2)
    hum_stats = data_df[hum_vars].agg(['mean', 'min', 'max']).round(2)
    
    detailed_stats = html.Div([
        dbc.Row([
            dbc.Col([
                html.H5("Estadísticas de Temperatura"),
                dbc.Table.from_dataframe(temp_stats, striped=True, bordered=True, hover=True, dark=True)
            ], width=6),
            dbc.Col([
                html.H5("Estadísticas de Humedad"),
                dbc.Table.from_dataframe(hum_stats, striped=True, bordered=True, hover=True, dark=True)
            ], width=6),
        ])
    ])

    return temp_fig, hum_fig, f"{avg_temp:.1f}°C", f"{avg_humidity:.1f}%", str(data_count), detailed_stats

if __name__ == "__main__":
    app.run_server(debug=True, use_reloader=False)

# Note: This code won't run in this environment. It needs to be run in a proper Python environment with the required libraries installed.
print("Greenhouse Monitoring System improved with dark mode and additional statistics.")

