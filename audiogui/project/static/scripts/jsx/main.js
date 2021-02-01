import React from 'react';
import axios from 'axios';
import Chart from "chart.js";


class LineGraph extends React.Component {
  constructor(props) {
    super(props);
  }

  componentDidMount() {
    const ctx = document.getElementById("myChart");

    new Chart(ctx, {
      type: "line",
      data: {
        //Bring in data
        labels: ["Jan", "Feb", "March"],
        datasets: [
          {
            label: "Sales",
            data: [86, 67, 91],
          }
        ]
      },
      options: {
        //Customize chart options
      }
    });
  }

  render() {
    return <canvas id="myChart" />;
  }
}


class GenerateButton extends React.Component {
  constructor(props) {
    super(props);
    this.data = [];
  }

  handleClick() {
    axios.get('/data')
      .then(response => {
        this.setState({ data: response.data });
        console.log(response.data);
      })
      .catch(error => {
        console.log(error)
      });
  };

  render() {
    return (
      <div>
        <button onClick={() => this.handleClick()}>
          Generate Graph
        </button>
        <LineGraph />
      </div>
    )
  }
};


ReactDOM.render(
  <div>
    <GenerateButton />
  </div>,
  document.getElementById('main')
);
