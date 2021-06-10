import React, { useState } from 'react';
import SineGenerator from './SineGenerator'
import NoiseGenerator from './NoiseGenerator'
import SweepGenerator from './SweepGenerator'

const DynamicSignalTypePanel = props => {

    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    if (props.signalType == 'sine')
        return <SineGenerator
            format={props.format}
            size={props.size}
            signalType={props.signalType}
            rate={props.rate}
            labelsCallback={labelsCallback}
            dataCallback={dataCallback}
        />
    if (props.signalType == 'noise')
        return <NoiseGenerator
            format={props.format}
            size={props.size}
            signalType={props.signalType}
            rate={props.rate}
            labelsCallback={labelsCallback}
            dataCallback={dataCallback}
        />
    if (props.signalType == 'sweep')
        return <SweepGenerator/>
    else return (<p>choose signal type</p>);
};

export default DynamicSignalTypePanel;
