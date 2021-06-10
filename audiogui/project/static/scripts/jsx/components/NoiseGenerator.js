import React, { useState } from 'react';
import RequestSignal from './RequestSignal.js'

const NoiseGenerator = props => {

    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    const [shape, setShape] = useState('uniform');

    const [noiseDict, setNoiseDict] = useState({
        gain: 0.5
    });

    return(
        <div class="bg-blue-500 bg-opacity-100">
            <label>
                Noise Generator !
                <br />
                Noise shape  :
                <select 
                    value={shape}
                    onChange={evt => setShape(evt.target.value)}>
                    <option selected value='uniform'>uniform noise</option>
                    <option value='white'>white noise</option>
                    <option value='pink'>pink noise</option>
                </select>
            </label>
            <br />
            <RequestSignal
                format={props.format}
                size={props.size}
                signalType={props.signalType}
                rate={props.rate}
                labelsCallback={labelsCallback}
                dataCallback={dataCallback}
                signalDict={noiseDict}
            />
        </div>
    );
};

export default NoiseGenerator;
