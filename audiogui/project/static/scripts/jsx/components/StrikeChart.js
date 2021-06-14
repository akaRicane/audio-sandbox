import React, { useEffect, useRef, useState } from "react";
import Chart from 'chart.js';

const StrikeChart = props => {

    return (
        <div>
            <canvas id="myChart" width="400" height="400"></canvas>
            <script>
                ctx = document.getElementById('myChart').getContext('2d');
                myChart = new Chart(ctx, {
                    type: "line",
                    showPoints: false,
                    data: {
                    //Bring in data
                    labels: props.labels,
                        datasets: [
                        {
                    label: props.title,
                            data: props.data,
                            fill: true,
                            borderColor: colorLine,
                            backgroundColor: colorFill
                        }
                        ]
                    },
                    options: {
                    animation: false,
                        responsive: false,
                        maintainAspectRatio: true,
                        elements: {
                    point: {
                    radius: 0
                        }
                        },
                        scales: {
                    xAxes: [{
                    gridLines: {
                    display: true,
                            color: '#2A3459'
                            }
                        }],
                        yAxes: [{
                    ticks: {
                    beginAtZero: true
                            },
                            gridLines: {
                    display: true,
                            color: '#2A3459'
                            }
                        }]
                        }
                    }
                    });
        </script>
        </div>
    );
};

export default StrikeChart;