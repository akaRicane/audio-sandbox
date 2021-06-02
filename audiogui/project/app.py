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

    rate = np.float64(args_dict["rate"])
    f0 = np.float64(args_dict["f0"])
    gain = np.float64(args_dict["gain"])
    print(f"rate: {rate} | f0: {f0} | gain: {gain}")

    sine = generator.Sine(rate=rate, f0=f0, gain=gain)
    return jsonify(
        {'data': sine.signal.tolist(), 'labels': sine.vect.tolist()})


@app.route('/multisine', methods=['POST'])
def generateMultiSine():
    print("\n*** Generate multisine ***")
    args_dict = request.get_json()

    rate = np.float64(args_dict["rate"])
    f_list = np.array(args_dict["f_list"], dtype=np.float64)
    gain_list = np.array(args_dict["gain_list"], dtype=np.float64)
    print(f"rate: {rate} | F_LIST: {f_list}  "
          f"|  GAINS : {gain_list}")

    msine = generator.MultiSine(rate=rate, f_list=f_list, gain_list=gain_list)
    return jsonify(
        {'data': msine.signal.tolist(), 'labels': msine.vect.tolist()})


@app.route('/noise', methods=['POST'])
def generateNoise():
    print("\n*** Generate noise ***")
    args_dict = request.get_json()

    rate = np.float64(args_dict["rate"])
    gain = np.float64(args_dict["gain"])
    print(f"rate: {rate} | gain: {gain}")

    noise = generator.Noise(rate=rate, gain=gain)
    return jsonify(
        {'data': noise.signal.tolist(), 'labels': noise.vect.tolist()})


@app.route('/loadFile', methods=['POST'])
def loadFile():
    print("\n*** Loading file")
    args_dict = request.get_json()

    filepath = args_dict["filepath"]
    print(f"filepath: {filepath}")

    data, rate = audiofile.load_from_filepath(config.AUDIO_FILE_JOYCA)

    labels = []
    mono_data = []
    for idx in range(len(data)):
        labels.append(idx)
        if isinstance(data[idx], np.float64):
            # it is a mono file
            mono_data.append(data[idx])
        else:
            mono_data.append(data[idx][0])

    return jsonify(
        {'data': mono_data, 'labels': labels, 'rate': rate})


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


@app.route('/playAudio', methods=['POST'])
def playAudio():
    print("\n*** Playing audio from web\n")
    args_dict = request.get_json()

    rate = args_dict["rate"]
    data = np.array(args_dict["data"], dtype=np.float64)

    sd.play(data, rate)
    sd.wait()
    return jsonify({'success': True})


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
