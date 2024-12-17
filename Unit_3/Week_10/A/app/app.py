from flask import Flask, request, jsonify, render_template
import pandas as pd
import plotly.express as px
import plotly
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
        first_column = df.columns[1]
        fig = px.scatter(df, x=df.index, y=first_column, title=f"Graph of {first_column}")
        graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

        return jsonify({'stats': stats, 'graph': graph_json})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
