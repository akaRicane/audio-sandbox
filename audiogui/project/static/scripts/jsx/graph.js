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
      data: []
    };
  }

  handleClick() {
    axios.get('/data')
      .then(response => {
        this.setState({ data: response.data });
      })
      .catch(error => {
        console.log(error)
      });
  };

  render() {
    return (
      <div>
        <button
          type="button"
          className="p-2 my-2 bg-gray-500 text-white rounded-md"
          onClick={() => this.handleClick()}
        >
          Generate Graph
          </button>
        <LineGraph
          data={this.state.data}
          title="label"
        />
      </div>
    )
  }
};

export default Graph