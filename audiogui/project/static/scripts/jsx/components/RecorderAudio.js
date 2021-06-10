import React, { useState } from 'react';
import axios from 'axios';

const RecorderAudio = props => {

    const rateCallback = props.rateCallback;
    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    const [duration, setDuration] = useState(1.0)

    const args = {
        rate: props.rate,
        duration: duration
    };

    const handleRequest = () => {
        axios.post('/recAudio', args)
            .then(response => {
                rateCallback(response.data.rate);
                labelsCallback(response.data.labels);
                dataCallback(response.data.data);
            })
            .catch(error => {
                console.log(error)
            });
    };

    return (
        <div>
            <button
                type="button"
                className="p-2 my-2 bg-gray-500 text-white rounded-md"
                onClick={handleRequest}
            >
                Rec audio
            </button>
            <input
                placeholder="duration"
                value={duration}
                onChange={evt => setDuration(evt.target.value)} />
            <br />
        </div>
    );
};

export default RecorderAudio;
