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
    this.lineChart.data.labels = this.props.data.map(d => d.label);
    this.lineChart.data.datasets[0].data = this.props.data.map(d => d.value);
    this.lineChart.update();
  }

  componentDidMount() {
    const ctx = document.getElementById("myChart");
    ctx.height = 500;
    ctx.width = 2500;

    this.lineChart = new Chart(ctx, {
      type: "line",
      data: {
        //Bring in data
        labels: this.props.data.map(d => d.label),
        datasets: [
          {
            label: this.props.title,
            data: this.props.data.map(d => d.value),
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
      rate: 44100,
      f0: 440,
      type: null
    };
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  generateSine() {
    axios.get('/sine', {params: {f0: this.state.f0}})
      .then(response => {
        this.setState({ data: response.data, type: 'Sine' });
      })
      .catch(error => {
        console.log(error)
      });
  };

  generateMultiSine() {
    axios.get('/multisine')
      .then(response => {
        this.setState({ data: response.data, type: 'MultiSine' });
      })
      .catch(error => {
        console.log(error)
      });
  };

  generateNoise(){
    axios.get('/noise')
      .then(response => {
        this.setState({ data: response.data });
      })
      .catch(error => {
        console.log(error)
      });
  }

  handleInputChange(event) {
    const value = event.target.value;
    this.setState({ f0: value });
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
          <br />
          <div className="grid grid-cols-4">
            <input
              className="col-start-2 col-span-2"
              type="range" min="20" max="20000" step="10"
              value={this.state.f0}
              onChange={evt => this.handleInputChange(evt)}
            />
          </div>
          <label>
            Frequency f0 :
            <input
              name="f0_frequency"
              value={this.state.f0}
              onChange={evt => this.handleInputChange(evt)}/>
            (Hz)
          </label>
          <br />
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.generateMultiSine()}
          >
            Generate multisine
            </button>
          <button
            type="button"
            className="p-2 my-2 bg-gray-500 text-white rounded-md"
            onClick={() => this.handleInputChange()}
          >
            Generate noise
          </button>
          <LineGraph
            data={this.state.data}
            title={this.state.type}
          />
        </div>
      </Link>
    )
  }
};

export default Graph