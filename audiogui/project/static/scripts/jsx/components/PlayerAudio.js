import React, { useState } from 'react';
import axios from 'axios';
import { PlayCircleOutlined, PauseCircleOutlined } from '@ant-design/icons';

const IconManager = props => {
    if (props.call == 'stop')    
        return(<PlayCircleOutlined />);
    if (props.call == 'play')
        return(<PauseCircleOutlined />);
};

const PlayerAudio = props => {

    const [activity, setActivity] = useState('stop');

    const args = {
        rate: props.rate,
        data: props.data
    };
    
    const handleActivity = () => {
        if (activity == 'stop') {
            setActivity('play');
            handleRequest();
        }

        if (activity == 'play') {
            setActivity('stop');
        }
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
                onClick={handleActivity}>
                <IconManager call={activity}/>
                </button>
        </div>
    );
};

export default PlayerAudio;
