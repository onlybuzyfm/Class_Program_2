from flask import Flask, request, jsonify, render_template
import pandas as pd 
import plotly.express as px
import plotly
import json 


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file= request.files['file']
    
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'Invalid file format. Only CSV files are supported.'}), 40
    
    try:
        df=pd.read_csv(file)
        data= df.iloc[:,1:]
        stats= data.describe().round(2).to_dict()
        print("Descriptive Stadistics Obtained")
        print(stats)
        return jsonify({'stats': stats})
    except Exception as e:
         return jsonify({'error': str(e)}), 500
     
     
if __name__ == '__main__':
    app.run(debug=True)
    

    

