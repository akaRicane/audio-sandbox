import os
import sys
from flask.helpers import make_response
import sounddevice as sd
import numpy as np
from flask import Flask, json, render_template, jsonify, request
sys.path.append(os.getcwd())
from lib import audiogenerator as generator  # noqa E402
from lib import audiofile, config, tool  # noqa E402

app = Flask(__name__)

RATE = 44100


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sine', methods=['POST'])
def generateSine():
    print("\n*** Generate sine ***")
    args_dict = request.get_json()

    rate = np.float32(args_dict["rate"])
    f0 = np.float32(args_dict["f0"])
    gain = np.float32(args_dict["gain"])
    print(f"rate: {rate} | f0: {f0} | gain: {gain}")

    sine = generator.Sine(rate=rate, f0=f0, gain=gain)
    return jsonify(
        {'data': sine.signal.tolist(), 'labels': sine.vect.tolist()})


@app.route('/multisine', methods=['POST'])
def generateMultiSine():
    print("\n*** Generate multisine ***")
    args_dict = request.get_json()

    f_list = np.array(args_dict["f_list"], dtype=np.float32)
    gain_list = np.array(args_dict["gain_list"], dtype=np.float32)
    print(f"F_LIST: {f_list}  "
          f"|  GAINS : {gain_list}")

    msine = generator.MultiSine(rate=RATE, f_list=f_list, gain_list=gain_list)
    return data_formatting_signals(msine)


@app.route('/noise', methods=['GET'])
def generateNoise():
    print("\n*** Generate noise\n")
    noise = generator.Noise(rate=RATE, gain=0.5)
    return data_formatting_signals(noise)


@app.route('/loadFile', methods=['GET'])
def loadFile():
    print("\n*** Loading file\n")
    data, rate = audiofile.load_from_filepath(config.AUDIO_FILE_JOYCA)
    return data_formatting_file(data)


@app.route('/writeFile', methods=['GET'])
def writeFile():
    print("\n*** Writting audio file\n")
    filepath = request.args.get("fullpath")
    data = request.args.get("data")
    rate = request.args.get("rate")
    print(rate)
    print(filepath)
    print(data)
    data = audiofile.load_from_filepath(config.AUDIO_FILE_ACID)
    success = True
    msg = {success: success}
    print("\nNIKE TA DARONE\n")
    return jsonify(msg)


@app.route('/playAudio', methods=['GET'])
def playAudio():
    print("\n*** Playing audio from web\n")
    data = request.args.get("data")
    # data, rate = audiofile.load_from_filepath(config.AUDIO_FILE_JOYCA)
    print(f'signal data {data}')
    sd.play(np.array(data), 44100)
    # sd.wait()
    success = True
    msg = {success: success}
    print("\nNIKE TA DARONE\n")
    return jsonify(msg)


def return_success_formatting(success):
    pass


def data_formatting_signals(signal):
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


def data_formatting_file(signal):
    data = []
    print("\n\n FORMATTING FILE DATA BEFORE SEND REACT\n\n")
    for index in range(len(signal)):
        if index % 30 == 0:
            # print(f"{signal.vect[index]} : {signal.signal[index]}")
            data.append({
                "label": float(index),
                "value": signal[index][0]
            })
        else:
            data.append({
                "label": "",
                "value": signal[index][0]
            })
    print("\nBYE FLASK\n")
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
