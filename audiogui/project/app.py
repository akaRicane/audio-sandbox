import os
import sys
from flask import Flask, render_template, jsonify, request
sys.path.append(os.getcwd())
from lib import audiogenerator as generator  # noqa E402
from lib import audiofile  # noqa E402

app = Flask(__name__)

RATE = 44100


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sine', methods=['GET'])
def generateSine():
    print("\n*** Generate sine", request)
    f0 = request.args.get("f0")
    sine = generator.Sine(rate=RATE, f0=float(f0), gain=0.8)
    return data_formatting(sine)


@app.route('/multisine', methods=['GET'])
def generateMultiSine():
    print("\n*** Generate multisine", request)
    f_list = request.args.get("f_list")
    print(f_list)
    if f_list is None:
        f_list = [440, 650, 1111]
    msine = generator.MultiSine(
        rate=RATE, f_list=f_list, gain_list=[1, 1, 1])
    return data_formatting(msine)


@app.route('/noise', methods=['GET'])
def generateNoise():
    print("\n*** Generate noise\n")
    noise = generator.Noise(rate=RATE, gain=0.5)
    return data_formatting(noise)


@app.route('/writeFile', methods=['GET'])
def writeFile():
    print("\n*** Writting audio file\n")
    filepath = request.args.get("fullpath")
    data = request.args.get("data")
    rate = request.args.get("rate")
    print(data is not None)
    print(rate)
    print(filepath)
    data = [data, data]
    success = audiofile.write_in_audiofile(
        filepath="\\C:\\Users\\phili\\Downloads",
        filename="test_save.wav",
        format="WAV",
        audio_signal=data,
        rate=44100)
    msg = []
    msg.success = success
    print("\nBYE FLASK\n")
    return jsonify(msg)


def return_success_formatting(success):
    pass


def data_formatting(signal):
    data = []
    print("\n\n FORMATTING DATA BEFORE SEND REACT\n\n")
    for index in range(len(signal.vect)):
        if index % 8 == 0:
            # print(f"{signal.vect[index]} : {signal.signal[index]}")
            data.append({
                "label": float(signal.vect[index]),
                "value": signal.signal[index]
            })
        else:
            data.append({
                "label": "",
                "value": signal.signal[index]
            })
    print("\nBYE FLASK\n")
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
