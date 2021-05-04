import React from "react";
import axios from 'axios';
import Chart from 'chart.js';

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
      f0_frequency: null
    };
  }

  generateGraph() {
    axios.get('/data', {params: {f0: this.state.f0_frequency}})
      .then(response => {
        this.setState({ data: response.data });
      })
      .catch(error => {
        console.log(error)
      });
  };

  updateF0Value(newF0Value) {
    this.setState({
      f0_frequency: newF0Value
    });
  }

  on_changeF0Input(evt) {
    this.updateF0Value(evt.target.value);
    this.generateGraph()
  }

  render() {
    return (
      <div>
        <div className="grid grid-cols-4">
          <input
            className="col-start-2 col-span-2"
            type="range" min="1" max="500"
            value={this.state.f0_frequency}
            onChange={evt => this.on_changeF0Input(evt)}
          />
        </div>
        <LineGraph
          data={this.state.data}
          title="label"
        />
      </div>
    )
  }
};

export default Graph