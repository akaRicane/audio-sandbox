import React, { useState } from 'react';
import axios from 'axios';


const RequestSignal = props => {

    const args = {
        rate: props.rate,
        signalDict: props.signalDict,
    };
    
    const callAxios = () => {

        console.log("*** New Requested Signal -- AXIOS ***")
        console.log(args);

        axios.post('/sine', args)
            .then(response => {
            const newLabels = response.data.labels;
            const newData = response.data.data;
            console.log("Data received");
            props.labelsCallback(newLabels);
            props.dataCallback(newData);
            })
            .catch(error => {
            console.log(error)
            });
    };

    return (
        <div>
            <button onClick={callAxios}>Generate</button>
        </div>
    );
};

export default RequestSignal;
