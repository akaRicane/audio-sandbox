import os
import sys
from flask import Flask, render_template, jsonify, request
sys.path.append(os.getcwd())
from lib import audiogenerator

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data', methods=['GET'])
def getData():
    print("***", request)
    time, value = audiogenerator.generateSine(
        f0=float(request.args.get("f0"))
    )

    data = []
    for index in range(len(time)):
        data.append({
            "label": time[index],
            "value": value[index]
        })

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
