import os, sys
from flask import Flask, render_template, jsonify
sys.path.append(os.getcwd())
from lib import audio
from lib import audiogenerator as generator

app = Flask(__name__)

RATE = 44100

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sine', methods=['GET'])
def generateSine():
    sine = generator.Sine(rate=RATE, f0=440, gain=0.8)
    return data_formatting(sine)


@app.route('/noise', methods=['GET'])
def generateNoise():
    noise = generator.Noise(rate=RATE, gain=0.5)
    return data_formatting(noise)


def data_formatting(signal):
    data = []
    for index in range(len(signal.vect)):
        data.append({
            "label": signal.vect[index],
            "value": signal.signal[index]
        })
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
