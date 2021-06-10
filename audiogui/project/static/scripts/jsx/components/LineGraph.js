import React, { Component } from 'react';
import Chart from 'chart.js';

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
      return (
        <div>
            <canvas id="myChart" width={8000} />
        </div>
      )}
  }

export default LineGraph