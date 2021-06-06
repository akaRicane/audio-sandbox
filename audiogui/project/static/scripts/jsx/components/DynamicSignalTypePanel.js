import React, { useState } from 'react';
import SineGenerator from './SineGenerator'
import NoiseGenerator from './NoiseGenerator'
import SweepGenerator from './SweepGenerator'

const DynamicSignalTypePanel = props => {
    console.log("Dynamic Signal Panel");
    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    if (props.signalType == 'sine')
        return <SineGenerator
            rate={props.rate}
            labelsCallback={labelsCallback}
            dataCallback={dataCallback}
        />
    if (props.signalType == 'noise')
        return <NoiseGenerator/>
    if (props.signalType == 'sweep')
        return <SweepGenerator/>
    else return (<p>choose signal type</p>);
};

export default DynamicSignalTypePanel;
