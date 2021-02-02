from flask import Flask, render_template, jsonify
from lib import audio

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')


@app.route('/data', methods=['GET'])
def getData():
    signal = audio.AudioItem()
    signal.addSinusAsNewChannel()

    data = []
    for index in range(len(signal.data[0].t)):
        data.append({
            "label": signal.data[0].t[index],
            "value": signal.data[0].tamp[index]
        })

    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)
