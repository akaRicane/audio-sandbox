import React, { useState } from 'react';
import axios from 'axios';

const PlayerAudio = props => {

    const [activity, setActivity] = useState('stop');
    const [icon, setIcon] = useState(0)

    const args = {
        rate: props.rate,
        data: props.data
    };
    
    const handleClick = () => {
        if (activity == 'stop') {
            setActivity('play')
            handleRequest();
        }

        if (activity == 'play') 
            setActivity('stop')
    };

    const handleRequest = () => {
        axios.post('/playAudio', args)
            .then(response => {
                setActivity('stop');
            })
            .catch(error => {
            console.log(error)
            });
    };
    
    return(
        <div>
            <p>Player audio // {activity}</p>
            <button
                type="button"
                className="p-2 my-2 bg-gray-500 text-white rounded-md"
                onClick={handleClick}>
                Play
                </button>
        </div>
    );
};

export default PlayerAudio;
