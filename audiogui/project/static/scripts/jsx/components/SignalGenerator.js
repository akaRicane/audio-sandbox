import React, { Component, useState } from 'react';

const SignalGenerator = props => {

    const [format, setFormat] = useState('max_size');
    const [size, setSize] = useState(1024);
    const [signalType, setSignalType] = useState('Sine');

    return(
        <div>
            <h1>Signal Generator</h1>
            <p>Input rate: {props.rate}</p>
            <p>Format: {format}</p>
            <p>Size: {size}</p>
            <p>Signal type: {signalType}</p>
        </div>
    );
};

export default SignalGenerator;