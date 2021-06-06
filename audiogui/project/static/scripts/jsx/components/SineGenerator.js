import React, { Component, useState } from 'react';
import axios from 'axios';


const SineGenerator = props => {
    
    const [pendingFreq, setPendingFreq] = useState(1234);
    const [pendingGain, setPendingGain] = useState(0.98);

    const [freqTree, setFreqTree] = useState([
        {id: 0, freq: 440, gain: 1.0},
        {id: 1, freq: 1000, gain: 0.8}
    ]);

    const makeRequest = () => {
        console.log("Generating sine")
    
        const args = {
          rate: props.rate,
          freqTree: freqTree,
        };
        console.log(args);
    
        axios.post('/sine', args)
          .then(response => {
            const newLabels = response.data.labels;
            const newData = response.data.data;
            console.log("Data received");
            props.labelsCallback(newLabels);
            props.dataCallback(newData);
          })
          .catch(error => {
            console.log(error)
          });
      };

    const handleDelete = id => {
        const newTree = freqTree.slice();
        newTree.splice(id, 1);
        setFreqTree(newTree)
    }

    const handleAddSine = () => {
        const newTree = freqTree.slice();
        newTree.push({ id: newTree.length, freq: pendingFreq, gain: pendingGain})
        setFreqTree(newTree)
    }

    const cleanSinesIds = () => {
        const id = 0;
        const param = this.state.param.slice();
        param.map(sine => {sine.pos = id; id++;})
        this.setState({ param: param})
    }

    return (
        <div class="bg-blue-500 bg-opacity-100">
            <label>
                Sine Generator Motherfucker !<br />
                <ul>
                    {freqTree.map(freq => 
                        <li>
                            <button
                            type="button"
                            className="p-2 my-2 bg-gray-500 text-white rounded-md"
                            onClick={() => handleDelete(freq.id)}
                            >X</button>
                            id: {freq.id}{"   |   "}
                            freq: {freq.freq}{"   Hz|   "}
                            gain: {freq.gain}{"     |   "}
                        </li>
                    )}
                    <form>
                        <button
                        type="button"
                        className="p-2 my-2 bg-gray-500 text-white rounded-md"
                        onClick={() => handleAddSine()}
                        >add</button>{"   "}
                        freq:
                        <input 
                            value={pendingFreq}
                            onChange={evt => setPendingFreq(evt.target.value)}/>{"Hz|   "}
                        gain: 
                        <input 
                            value={pendingGain}
                            onChange={evt => setPendingGain(evt.target.value)}/>{"|   "}    
                    </form>
                </ul>
            </label>
            <br />
            <button onClick={makeRequest}>Generate</button>
        </div>
    );
};

export default SineGenerator