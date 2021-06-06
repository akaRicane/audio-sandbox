import React, { useState } from 'react';
import RequestSignal from './RequestSignal.js'

const SineGenerator = props => {
    
    const labelsCallback = props.labelsCallback;
    const dataCallback = props.dataCallback;

    const [pendingFreq, setPendingFreq] = useState(1234);
    const [pendingGain, setPendingGain] = useState(0.98);
    const [count, setCount] = useState(1);

    const [sineDict, setSineDict] = useState([
        {id: count, freq: 440, gain: 1.0}
    ]);

    const handleDelete = id => {
        const newTree = sineDict.slice();
        newTree.splice(id, 1);
        setSineDict(newTree);
    }

    const handleAddSine = () => {
        setCount(count + 1);
        const newTree = sineDict.slice();
        newTree.push({ id: count, freq: pendingFreq, gain: pendingGain})
        setSineDict(newTree);
    }

    return (
        <div class="bg-blue-500 bg-opacity-100">
            <label>
                Sine Generator Motherfucker !<br />
                <ul>
                    {sineDict.map(freq => 
                        <li>
                            <button
                            type="button"
                            className="p-2 my-2 bg-gray-500 text-white rounded-md"
                            onClick={() => handleDelete(freq.id)}
                            >X</button>
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
            <RequestSignal
                format={props.format}
                size={props.size}
                signalType={props.signalType}
                rate={props.rate}
                labelsCallback={labelsCallback}
                dataCallback={dataCallback}
                signalDict={sineDict}
            />
        </div>
    );
};

export default SineGenerator;
