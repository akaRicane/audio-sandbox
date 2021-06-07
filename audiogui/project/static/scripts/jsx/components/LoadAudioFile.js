import React, { useState } from 'react';
import axios from 'axios';


const LoadAudioFile = props => {

    const rateCallback = props.rateCallback;
    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    const [filepath, setFilepath] = useState("")

    const args = {
        rate: props.rate,
        filepath: filepath
    };

    const handleRequest = () => {
        console.log("Loading file ...");
        axios.post('/loadFile', args)
            .then(response => {
                rateCallback(response.data.rate);
                labelsCallback(response.data.labels);
                dataCallback(response.data.data);
            })
            .catch(error => {
            console.log(error)
            });
    }

    return(
        <div>
            <p>Load audio from file</p>
            <button
                type="button"
                className="p-2 my-2 bg-gray-500 text-white rounded-md"
                onClick={handleRequest}>
                Load
            </button>
            <input
                placeholder="file path"
                value={filepath}
                onChange={evt => setFilepath(evt.target.value)}
                />
        </div>
    );
};

export default LoadAudioFile;