from flask import Flask, request, jsonify
import pandas as pd
from cleaning import clean_data
from flask_cors import CORS

app=Flask(__name__)

CORS(app)

#upload csv
@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({"error":"No file found"}), 400
    
    file = request.files['file']

    try:
        df = pd.read_csv(file,low_memory=False)
    except Exception as e:
        return jsonify({"error":f"Could not read CSV: {str(e)}"}) , 400
    
    cleaned_df, summary = clean_data(df)
    sample = cleaned_df.head(5).to_dict(orient='records')

    return jsonify({
        "message": "File cleaned successfully!",
        "summary": summary,
        "sample_data": sample
    })

if __name__ == '__main__':
    app.run(debug=True)
