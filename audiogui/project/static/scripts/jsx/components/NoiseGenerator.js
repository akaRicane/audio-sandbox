import React, { Component } from 'react';
import axios from 'axios';


class NoiseGenerator extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            shape: 'uniform'
        }
    }
    
    handleChangeShape(event) {   
        const shape = event.target.value;
        this.setState({ shape: shape});
    }

    render() {
        return(
            <div class="bg-blue-500 bg-opacity-100">
                <label>
                    Noise Generator biatche !
                    <br />
                    Noise shape  :
                    <select 
                        value={this.state.shape}
                        onChange={evt => this.handleChangeShape(evt)}>
                        <option selected value='uniform'>uniform noise</option>
                        <option value='white'>white noise</option>
                        <option value='pink'>pink noise</option>
                    </select>
                </label>
            </div>
    )}
};

export default NoiseGenerator