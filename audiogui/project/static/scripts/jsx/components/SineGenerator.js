import React, { Component } from 'react';
import axios from 'axios';


class SineGenerator extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            param: [
                {id: 0, freq: 440, gain: 1.0},
                {id: 1, freq: 1000, gain: 0.8},
            ],
            nSines: 2,
            pending_freq: 1492,
            pending_gain: 0.123
        };
    }

    handleDelete(id) {
        const param = this.state.param.slice();
        const newNumber = this.state.nSines - 1;
        param.splice(id, 1);

        this.setState({ param: param, nSines: newNumber});
        this.cleanSinesIds()
    }

    handleChangeNewGain(event){
        const gain = event.target.value;
        this.setState({ pending_gain: gain})
    }

    handleChangeNewFreq(event){
        const freq = event.target.value;
        this.setState({ pending_freq: freq})
    }

    handleAddSine() {
        const param = this.state.param.slice();
        const newId = this.state.nSines;
        param.push({ id: newId, freq: this.state.pending_freq, gain: this.state.pending_gain})
        const newNumber = this.state.nSines + 1;
        this.setState({ param: param, nSines: newNumber});
        this.cleanSinesIds();
    }

    cleanSinesIds() {
        const id = 0;
        const param = this.state.param.slice();
        param.map(sine => {sine.pos = id; id++;})
        this.setState({ param: param})
    }

    render() {
        return (
            <div class="bg-blue-500 bg-opacity-100">
                <label>
                    Sine Generator Motherfucker !<br />
                    <ul>
                        {this.state.param.map(sine => 
                            <li>
                                <button
                                type="button"
                                className="p-2 my-2 bg-gray-500 text-white rounded-md"
                                onClick={() => this.handleDelete(sine.id)}
                                >X</button>
                                id: {sine.id}{"   |   "}
                                freq: {sine.freq}{"   Hz|   "}
                                gain: {sine.gain}{"     |   "}
                            </li>
                        )}
                        <form>
                            <button
                            type="button"
                            className="p-2 my-2 bg-gray-500 text-white rounded-md"
                            onClick={() => this.handleAddSine()}
                            >add</button>{"   "}
                            freq:
                            <input 
                                value={this.state.pending_freq}
                                onChange={evt => this.state.handleChangeNewFreq(evt)}/>{"Hz|   "}
                            gain: 
                            <input 
                                value={this.state.pending_gain}
                                onChange={evt => this.handleChangeNewGain(evt)}/>{"|   "}    
                        </form>
                    </ul>
                </label>
            </div>
    )}
};

export default SineGenerator