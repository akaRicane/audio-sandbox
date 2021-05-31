import React, { Component } from 'react';
import axios from 'axios';


class NoiseGenerator extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: []
        }
    }

    render() {
        return(
            <label>
                Noise Generator biatche !
            </label>
    )}
};

export default NoiseGenerator