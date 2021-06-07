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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generateSignal', methods=['POST'])
def generateSignal():
    print("\n*** Generate signal ***")
    args_dict = request.get_json()

    format = args_dict["format"]
    value = np.float64(args_dict["size"])
    signalType = args_dict["signalType"]
    rate = np.int64(args_dict["rate"])
    signal_dict = args_dict["signalDict"]

    if signalType == 'sine':
        print("\n*** Generate sine ***")
        freq_list = []
        gain_list = []

        for item in signal_dict:
            freq_list.append(item["freq"])
            gain_list.append(item["gain"])

        print(f"rate: {rate} | F_LIST: {freq_list}  "
              f"|  GAINS : {gain_list}")

        signal = generator.MultiSine(rate=rate,
                                     f_list=freq_list,
                                     gain_list=gain_list,
                                     format=format,
                                     value=value)

    elif signalType == 'noise':
        print("\n*** Generate noise ***")
        gain = np.float64(signal_dict["gain"])

        print(f"rate: {rate} | gain: {gain}")

        signal = generator.Noise(rate=rate,
                                 gain=gain,
                                 format=format,
                                 value=value)

    else:
        print("\n*** Generate nothing sorry ***")

    return jsonify(
        {'data': signal.signal.tolist(), 'labels': signal.vect.tolist()})



@app.route('/loadFile', methods=['POST'])
def loadFile():
    print("\n*** Loading file")
    args_dict = request.get_json()

    filepath = args_dict["filepath"]
    print(f"filepath: {filepath}")

    data, rate = audiofile.load_from_filepath(filepath)

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


@app.route('/writeFile', methods=['POST'])
def writeFile():
    print("\n*** Writting audio file\n")
    args_dict = request.get_json()

    rate = np.int64(args_dict["rate"])
    data = np.array(args_dict["data"], dtype=np.float64)
    directory = args_dict["directory"]
    filename = args_dict["filename"]

    print(f"rate: {rate} | filename: {filename}")

    success = audiofile.write_in_audiofile(
        filepath=directory, filename=filename,
        format='WAV', audio_signal=data, rate=rate)

    return jsonify({"success": success})


@app.route('/playAudio', methods=['POST'])
def playAudio():
    print("\n*** Playing audio from web\n")
    args_dict = request.get_json()

    rate = np.int64(args_dict["rate"])
    data = np.array(args_dict["data"], dtype=np.float64)

    sd.play(data, rate)
    sd.wait()
    return jsonify({'success': True})


if __name__ == '__main__':
    app.run(debug=True)
