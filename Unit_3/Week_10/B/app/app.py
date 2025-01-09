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
        
        
        fig3 = go.Figure()
        
        fig3.add_trace(go.Box(
        y=df[col2],  # Reemplaza col1 con el nombre de la columna que deseas analizar
        name=col2    # Etiqueta del eje X o el nombre del boxplot
        ))
        
        fig3.update_layout(title="Gráfico de Caja y Bigotes", xaxis_title=col2)
        
        
        data_corr = df.iloc[:, 1:5]
        
        correlation_matrix = data_corr.corr()
        
        fig4 = go.Figure (
        data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale="Twilight",
        colorbar=dict(title="Correlation"),
        zmin=-1,  # Minimum correlation value
        zmax=1    # Maximum correlation value
        )
            )
        fig4.update_layout(
        title="Correlation Matrix Heatmap",
        xaxis_title="Features",
        yaxis_title="Features",
        xaxis=dict(tickangle=45),
        yaxis=dict(autorange="reversed"),  # Reverse y-axis for traditional matrix layout
        width=600,
        height=600
        )   
        

        # Convertir gráficos a JSON
        graph_1 = fig1.to_json()
        graph_2 = fig2.to_json()
        graph_3 = fig3.to_json()
        graph_4 = fig4.to_json()

        return jsonify({
            "stats": stats,
            "graph_1": graph_1,
            "graph_2": graph_2,
            "graph_3": graph_3,
            "graph_4": graph_4
        })

    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
