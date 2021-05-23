import os
import sys
from flask import Flask, render_template, jsonify, request
sys.path.append(os.getcwd())
from lib import audiogenerator as generator  # noqa E402

app = Flask(__name__)

RATE = 44100


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sine', methods=['GET'])
def generateSine():
    print("***", request)
    f0 = request.args.get("f0")
    print(f0)
    sine = generator.Sine(rate=RATE, f0=float(f0), gain=0.8)
    return data_formatting(sine)


@app.route('/multisine', methods=['GET'])
def generateMultiSine():
    msine = generator.MultiSine(
        rate=RATE, f_list=[100, 440, 1000],
        gain_list=[0.2, 0.8, 0.35], )
    return data_formatting(msine)


@app.route('/noise', methods=['GET'])
def generateNoise():
    noise = generator.Noise(rate=RATE, gain=0.5)
    print(noise)
    return data_formatting(noise)


def data_formatting(signal):
    data = []
    for index in range(len(signal.vect)):
        # print(signal.signal[index])
        if index % 8 == 0:
            data.append({
                "label": signal.vect[index],
                "value": signal.signal[index]
            })
        else:
            data.append({
                "label": "",
                "value": signal.signal[index]
            })
    # print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
