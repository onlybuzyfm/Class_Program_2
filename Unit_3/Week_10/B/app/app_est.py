from flask import Flask, request, jsonify, render_template
import pandas as pd
import plotly.express as px
import plotly
import plotly.graph_objs as go
import math
import numpy as np

app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])

def upload_csv():
    if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
    
    file=request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format. Only CSV files are supported.'}), 400
    
    try: 
         df = pd.read_csv(file)
         data = df.iloc[:, 1:]
         # descritive stadistics
         stats = data.describe().round(2).to_dict()
         
         #print(stats)
         
         # Graphication
         col1 = data.columns[0]
         col2 = data.columns[1]
         col3 = data.columns[2]
         
         df_aux = pd.DataFrame()
         n = len(col1)  # Número de datos
         k = math.ceil(np.log2(n) + 1)  # Fórmula de Sturges
         
        # print(k)
        
         df_aux['bins'] = pd.cut(df[col1], bins=k)  # Aquí definimos 10 intervalos
         
         grouped = df_aux['bins'].value_counts()
         
        # print(grouped)
         
         fig_1=go.Figure()
         
         fig_1.add_trace(go.Bar(
            x=grouped.index.astype(str),
            y=grouped.values,
            marker_color="blue"
         ))
         
         fig_1.update_layout(title="Gráfico de Barras", xaxis_title=col1)
         
         fig_2=go.Figure()
         
         fig_2.add_trace(go.Scatter(
            x=df[col1].head(50),
            y=df[col2].head(50),
            mode="markers",  # Modo para mostrar solo puntos
            marker=dict(size=10, color="green", symbol="triangle-up")  # Personalización de puntos
         ))
         
         fig_3=go.Figure()
         
         fig_3.add_trace( go.Box(
            y=df[col3], # Muestra la media y la desviación estándar
            marker=dict(color='blue')  # Color de los puntos
            ))  # Personalización de puntos
            
         
         graph_1=fig_1.to_json()
        # print(graph_1)
         graph_2=fig_2.to_json()
         
         graph_3=fig_3.to_json()
         
         return jsonify({
             "stats": stats,
             "graph_1":graph_1,
             "graph_2":graph_2,
             "graph_3":graph_3
         })
         
    
    except Exception as e:
         return jsonify({'error': str(e)}), 500
     

if __name__ == '__main__':
    app.run(debug=True)
    

    

