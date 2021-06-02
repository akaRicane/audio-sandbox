import React, { useState } from "react";
import axios from 'axios';
import Chart from 'chart.js';
import { Link } from 'react-router-dom';

class LineGraph extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidUpdate() {
    console.log(this.props.data);
    this.lineChart.data.labels = this.props.labels;
    this.lineChart.data.datasets[0].label = this.props.title;
    this.lineChart.data.datasets[0].data = this.props.data;
    this.lineChart.update();
  }

  componentDidMount() {
    const ctx = document.getElementById("myChart");
    ctx.height = 200;
    ctx.width = 500;

    this.lineChart = new Chart(ctx, {
      type: "line",
      data: {
        //Bring in data
        labels: this.props.labels,
        datasets: [
          {
            label: this.props.title,
            data: this.props.data,
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          yAxes: [{
            ticks: {
              beginAtZero: true
            }
          }]
        }
      }
    });
  }

  render() {
    return <canvas id="myChart" width={8000} />;
  }
}


class Graph extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: [],
      labels: [],
      f_list: ["440", "650", "1111"],
      rate: "44100",
      type: null,
      directory: "C:\\Users\\phili\\audio\\audio\\resources\\bin\\",
      filename: "test_save.wav",
      fullpath: "C:\\Users\\phili\\audio\\audio\\resources\\bin\\test_save.wav"
    };
  }

  generateSine() {
    console.log("Generating sine")

    const args = {
      rate: 44100,
      f0: this.state.f_list[0],
      gain: 0.98
    }
    console.log(args);

    axios.post('/sine', args)
      .then(response => {
        const labels = response.data.labels;
        const data = response.data.data;
        this.setState({ labels: labels, data: data, type: 'Sine' });
      })
      .catch(error => {
        console.log(error)
      });
  };

  generateMultiSine() {
    console.log("Generating multi sine")
    
    const args = {
      rate: this.state.rate,
      f_list: this.state.f_list,
      gain_list: [0.3, 0.3, 0.3]
    }
    console.log(args);

    axios.post('/multisine', args)
      .then(response => {
        const labels = response.data.labels;
        const data = response.data.data;
        this.setState({ labels: labels, data: data, type: 'MultiSine' });
      })
      .catch(error => {
        console.log(error)
      });
  };

  generateNoise(){
    console.log("Generating noise")
    
    const args = {
      rate: this.state.rate,
      gain: 0.95
    }
    console.log(args);

    axios.post('/noise', args)
      .then(response => {
        const labels = response.data.labels;
        const data = response.data.data;
        this.setState({ labels: labels, data: data, type: 'Noise' });
      })
      .catch(error => {
        console.log(error)
      });
  }


  loadFile() {
    console.log("Loading file")
    
    const args = {
      filepath: this.state.fullpath
    }
    console.log(args);

    axios.post('/loadFile', args)
      .then(response => {
        const rate = response.data.rate;
        const labels = response.data.labels;
        const data = response.data.data;
        this.setState({ rate: rate, labels:labels, data: data, type: 'File' });
      })
    .catch(error => {
      console.log(error)
    });
  }


  writeFile(){
    console.log("Loading file")
    
    const args = {
      rate: this.state.rate,
      data: this.state.data,
      directory: this.state.directory,
      filename: this.state.filename,
    }
    console.log(args);

    axios.post('/writeFile', args)
      .then(response => {
        alert("Successfully saved")
      })
      .catch(error => {
        console.log(error)
      });
  }


  playAudio() {
    console.log("Playing file")
    
    const args = {
      rate: this.state.rate,
      data: this.state.data,
      }
    console.log(args);
    
    axios.post('/playAudio', args)
      .catch(error => {
        console.log(error)
      });
  }


  handleFListChange(event, idx) {
    const value = event.target.value;
    const temp_list = this.state.f_list;
    temp_list[idx] = value;
    this.setState({ f_list: temp_list });
    if (idx == 0){
      this.setState({ f0: value });
      this.generateSine()
    }
  }

  handleWriteDirectoryChange(event) {
    const directory = event.target.value;
    this.setState({directory: directory});
    this.concatenateFullpath()
  }
  
  handleWriteFileNameChange(event) {
    const filename = event.target.value;
    this.setState({filename: filename});
    this.concatenateFullpath()
  }

  concatenateFullpath() {
    if (this.state.filename != null && this.state.directory != null)
      char = '{this.state.directory}${this.state.filename}'
      this.setState({ fullpath: char})
  }


  render() {
    return (
      <Link to="/graph">
        <div>
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.generateSine()}
          >
            Generate sine
            </button>
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.generateMultiSine()}
          >
            Generate multisine
            </button>
          <br />
          <div className="grid grid-cols-4">
            <input
              className="col-start-1 col-span-1"
              type="range" min="20" max="20000" step="10"
              value={this.state.f0}
              onChange={evt => this.handleFListChange(evt, 0)}
            />
          </div>
          <div>
            f_list:
            <input
              name="f0_frequency"
              value={this.state.f_list[0]}
              onChange={evt => this.handleFListChange(evt, 0)}/>
            {/* <br /> */}
            <input 
              placeholder="f1"
              value={this.state.f_list[1]}
              onChange={evt => this.handleFListChange(evt, 1)}/>
            <input
              placeholder="f2"
              value={this.state.f_list[2]}
              onChange={evt => this.handleFListChange(evt, 2)}/>
            (Hz)
          </div>
          <br />
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.generateNoise()}
          >
            Generate noise
          </button>
          <br />
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.writeFile()}
          >
            Save audio
          </button>
          <input
            placeholder="directory"
            value={this.state.directory}
            onChange={evt => this.handleWriteDirectoryChange(evt)}/>
          <input
            placeholder="filename + extension"
            value={this.state.filename}
            onchange={evt => this.handleWriteFileNameChange(evt)}/>
          <br />
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.loadFile()}
          >
            Load audio file
          </button>
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.playAudio()}
          >
            Play audio
          </button>
          <div>
            <LineGraph
              data={this.state.data}
              labels={this.state.labels}
              title={this.state.type}
          /></div>
        </div>
        <br />
        <label>
          f0 = {this.state.f0} Hz <br/>
          f_list = {this.state.f_list[0]},
          {this.state.f_list[1]}, {this.state.f_list[2]} <br/>
          rate = {this.state.rate} Hz <br/>
          success = {this.state.success} <br/>
          type = {this.state.type} <br/>
          fullpath = {this.state.fullpath}
        </label>      
      
      </Link>
    )
  }
};

export default Graph