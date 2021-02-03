import React from 'react';
import axios from 'axios';
import Chart from 'chart.js';
import ReactDOM from 'react-dom';
import Sidebar from './sidebar.js';
import { Container, Row, Col, Card, Form, Button } from "react-bootstrap";
import { BrowserRouter as Router, Route, Link } from "react-router-dom";

// Importing the Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';


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


class GenerateButton extends React.Component {
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
        <Button onClick={() => this.handleClick()}>
          Generate Graph
        </Button>
        <LineGraph
          data={this.state.data}
          title="label"
        />
      </div>
    )
  }
};


ReactDOM.render(
  <Router>
    <Container fluid>
      <Row>
        <Col xs={2} id="sidebar-wrapper">
          <Sidebar />
        </Col>
        <Col id="page-content-wrapper">
          <GenerateButton />
        </Col>
      </Row>
    </Container>
  </Router>,
  document.getElementById('main')
);
