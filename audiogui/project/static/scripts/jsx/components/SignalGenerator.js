import React, { useState } from 'react';
import DynamicSignalTypePanel from './DynamicSignalTypePanel.js'

const SignalGenerator = props => {

    const [format, setFormat] = useState('duration');
    const [size, setSize] = useState(1.0);
    const [signalType, setSignalType] = useState('sine');

    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    const handleChangeFormat = newFormat => {
        setFormat(newFormat);
        if (newFormat == 'max_size') {    
            // duration default is 1.5 sec
            setSize(1024);
        }
        else {
            // max size default is 1024 points
            setSize(1.0);
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
                        <option value="max_size">max_size</option>
                        <option selected value="duration">duration</option>
                    </select>
                    <br />
                    Size  :
                    <input
                        placeholder="1.0 seconds"
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
