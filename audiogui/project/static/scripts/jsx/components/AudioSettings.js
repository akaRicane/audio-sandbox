import React, { useState } from 'react';


const AudioSettings = props => {

    const [rate, setRate] = useState(props.currentRate);
    const [buffer, setBuffer] = useState(props.currentBuffer);

    const updateSettings = () => {
        props.callback({ rate: rate, buffer: buffer})
    }

    return (
        <div>
            <label>
                <h1>Audio Settings</h1>
                <ul>
                    <li>
                      rate: {rate}
                    </li>
                    <li>
                      buffer: {buffer}
                    </li>
                </ul>
                Rate  :
                <select 
                    value={rate}
                    onChange={evt => setRate(evt.target.value)}>
                    <option selected value={"44100"}>44100 Hz</option>
                    <option value={"48000"}>48000 Hz</option>
                    <option value={"96000"}>96000 Hz</option>
                </select>
                <br />
                <button onClick={updateSettings}>Save settings</button>
                <br />
            </label>
            <br />
        </div>
    );
};

export default AudioSettings;