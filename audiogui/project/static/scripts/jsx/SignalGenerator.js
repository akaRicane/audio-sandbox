import React, { Component, useState } from 'react';
import axios from 'axios';
import Chart from 'chart.js';
import { Link } from 'react-router-dom';
import SineGenerator from './components/SineGenerator'
import NoiseGenerator from './components/NoiseGenerator'
import '../../css/style.css';

function UniqueParameters(props){
    if (props.type == 'Sine')
        return <SineGenerator />
    if (props.type == 'Noise')
        return <NoiseGenerator/>
    if (props.type == null)
        return <label>Type is null</label>
    else
        return <label>Ca pue</label>
}

class SignalGenerator extends Component {
    constructor(props) {
        super(props);
        this.state = {
            commonProps: {
                rate: 44100,
                format: "max_size",
                size: 1024,
                type: null
            },
            uniqueProps: null
        };
    }

    sineWidget() {
    
        this.setState({ commonProps: {type: "Sine"}});

    }
    
    sweepWidget() {
    
        this.setState({ commonProps: {type: "Sweep"}});
    
    }
    
    noiseWidget() {
    
        this.setState({ commonProps: {type: "Noise"}});
    
    }

    handleChangeRate(event) {   
        const rate = event.target.value;
        this.setState({ commonProps: {rate}});
    }
    
    
    handleChangeFormat(event) {   
        const format = event.target.value;
        if (format == 'duration')    
            this.setState({ commonProps: {format, size: 1.5}})
        else
            this.setState({ commonProps: {format, size: 1024}})

    }


    handleChangeSize(event) {   
        const size = event.target.value;
        this.setState({ commonProps: {size}});
    }
    
    
    render() {
        return (
            <div>
                <h1>Signal Generator</h1>
                <button
                    type="button"
                    className="p-2 my-2 bg-gray-500 text-white rounded-md"
                    onClick={() => this.sineWidget()}>
                    Sine Generator
                </button>
                <button
                    type="button"
                    className="p-2 my-2 bg-gray-500 text-white rounded-md"
                    onClick={() => this.sweepWidget()}>
                    Sweep Generator
                </button>
                <button
                    type="button"
                    className="p-2 my-2 bg-gray-500 text-white rounded-md"
                    onClick={() => this.noiseWidget()}>
                    Noise Generator
                </button>
                <form>
                    <label>
                        Rate  :
                        <select 
                            value={this.state.commonProps.rate}
                            onChange={evt => this.handleChangeRate(evt)}>
                            <option selected value={44100}>44100 Hz</option>
                            <option value={48000}>48000 Hz</option>
                            <option value={96000}>96000 Hz</option>
                        </select>
                        <br />
                        Format  :
                        <select 
                            value={this.state.commonProps.format}
                            onChange={evt => this.handleChangeFormat(evt)}>
                            <option selected value="max_size">max_size</option>
                            <option value="duration">duration</option>
                        </select>
                        <br />
                        Size  :
                        <input
                            placeholder="1024 points"
                            value={this.state.commonProps.size}
                            onChange={evt => this.handleChangeSize(evt)}/>
                        (nb points or seconds)
                        <br />
                        Type: {this.state.commonProps.type}
                    </label>
                    <br />
                    <UniqueParameters type={this.state.commonProps.type}/>
                </form>
            </div>
        )
    }
};

export default SignalGenerator