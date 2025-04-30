from flask import Flask, jsonify
from flask_cors import CORS
import random
from datetime import datetime

app = Flask(__name__)
CORS(app) 

@app.route('/iot-data')
def get_iot_data():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    temp = round(random.uniform(20.0, 35.0), 2)
    humidity = round(random.uniform(30.0, 70.0), 2)

    data = {
        'timestamp': now,
        'temperature': temp,
        'humidity': humidity
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)