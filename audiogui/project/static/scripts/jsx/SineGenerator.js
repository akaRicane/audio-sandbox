import React, { Component } from 'react';
import axios from 'axios';
import '../../css/style.css';

class SineGenerator extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            freqs: []
        };
    }

    render() {
        return (
            <label>
                Sine Generator Motherfucker !<br />
                
            </label>
    )}
};

export default SineGenerator