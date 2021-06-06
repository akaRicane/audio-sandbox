import React, { useState } from 'react';
import DynamicSignalTypePanel from './DynamicSignalTypePanel.js'

const SignalGenerator = props => {

    const [format, setFormat] = useState('max_size');
    const [size, setSize] = useState(1024);
    const [signalType, setSignalType] = useState('sine');

    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    const handleChangeFormat = newFormat => {
        setFormat(newFormat);
        if (newFormat == 'duration') {    
            // duration default is 1.5 sec
            setSize(1.5);
        }
        else {
            // max size default is 1024 points
            setSize(1024);
        };
    };

    const handleChangeSignalType = newSignalType => {
        setSignalType(newSignalType);
    };

    return(
        <div>
            <h1>Signal Generator</h1>
            <p>Input rate: {props.rate}</p>
            <form>
                <label>
                    Format  :
                    <select 
                        value={format}
                        onChange={evt => handleChangeFormat(evt.target.value)}>
                        <option selected value="max_size">max_size</option>
                        <option value="duration">duration</option>
                    </select>
                    <br />
                    Size  :
                    <input
                        placeholder="1024 points"
                        value={size}
                        onChange={evt => setSize(evt.target.value)}/>
                    (nb points or seconds)
                    <br />
                    Signal type  :
                    <select 
                        value={signalType}
                        onChange={evt => handleChangeSignalType(evt.target.value)}>
                        <option selected value="sine">Sine</option>
                        <option value="noise">Noise</option>
                    </select>
                </label>
                <br />
            </form>
            <br />
            <DynamicSignalTypePanel 
                format={format}
                size={size}
                signalType={signalType}
                rate={props.rate}
                labelsCallback={labelsCallback}
                dataCallback={dataCallback}
            />
        </div>
    );
};

export default SignalGenerator;
