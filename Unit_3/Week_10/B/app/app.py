from flask import Flask, request, jsonify, render_template
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objs as go
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format. Only CSV files are supported.'}), 400

    # Read the CSV file
    try:
        df = pd.read_csv(file)
        
        data = df.iloc[:, 1:]

        # Compute statistics for each column
        stats = data.describe().round(2).to_dict()  # Generate descriptive statistics, rounded to 2 decimals

        # Generate a Plotly graph (example with the first column)
        
        
        col1 = data.columns[0]
        col2 = data.columns[1] if len(data.columns) > 1 else col1
        fig1 = go.Figure()
        fig1.add_trace(go.Bar(
            x=df[col1].head(10),
            y=df[col2].head(10),
            marker_color="blue"
        ))
        fig1.update_layout(title="Gráfico de Barras", xaxis_title=col1, yaxis_title=col2)

        # Gráfico 2: Primeras columnas como gráfico de líneas
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=df[col1].head(10),
            y=df[col2].head(10),
        ))
        fig2.update_layout(title="Gráfico de Líneas", xaxis_title=col1, yaxis_title=col2)

        # Convertir gráficos a JSON
        graph_1 = fig1.to_json()
        graph_2 = fig2.to_json()

        return jsonify({
            "stats": stats,
            "graph_1": graph_1,
            "graph_2": graph_2
        })

    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
