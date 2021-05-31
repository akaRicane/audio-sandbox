import React, { Component } from 'react';
import axios from 'axios';
import '../../css/style.css';

class SineGenerator extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            param: [
                {id: 0, freq: 440, gain: 1.0},
                {id: 1, freq: 1000, gain: 0.8},
            ],
            nSines: 2
        };
    }

    handleDelete(id) {
        const param = this.state.param.slice();

        param.splice(id, 1);

        this.setState({ param: param})

    }

    render() {
        return (
            <label>
                <br />
                Sine Generator Motherfucker !<br />
                <ul>
                  {this.state.param.map(sine => 
                    <li>
                        id: {sine.id}{"   |   "}
                        freq: {sine.freq}{"   Hz|   "}
                        gain: {sine.gain}{"     |   "}
                        <button
                          type="button"
                          className="p-2 my-2 bg-gray-500 text-white rounded-md"
                          onClick={() => this.handleDelete(sine.id)}
                          >X</button>
                    </li>
                  )}
                </ul>
            </label>
    )}
};

export default SineGenerator