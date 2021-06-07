import React, { useState } from 'react';
import axios from 'axios';

const SaveAudio = props => {

    const [filepath, setFilepath] = useState("");
    const [filename, setFilename] = useState("test.wav");
    const [extension, setExtension] = useState("WAV");

    const args = {
        rate: props.rate,
        data: props.data,
        filepath: filepath,
        filename: filename,
        format: extension
    };

    const handleRequest = () => {
        axios.post('/saveFile', args)
            .then(alert("Successfully saved: " + filepath + '\\' + filename))
            .catch(error => {
            console.log(error)
            });
    };

    return(
        <div>
            <p>Save audio in file</p>
            <button
                type="button"
                className="p-2 my-2 bg-gray-500 text-white rounded-md"
                onClick={handleRequest}>
                Save
            </button>
            <select 
                onChange={evt => setFilepath(evt.target.value)}>
                <option value="to fill">Drou</option>
                <option value="C:\Users\phili\audio\audio\resources\bin">Ricane</option>
            </select>{"   |  "}
            <input
                placeholder="file path"
                value={filepath}
                onChange={evt => setFilepath(evt.target.value)}
                />
            <br />
            <input
                placeholder="file name"
                value={filename}
                onChange={evt => setFilename(evt.target.value)}
                />
            <select 
                onChange={evt => setExtension(evt.target.value)}>
                <option value="WAV">.wav</option>
                <option value="FLAC">.flac</option>
            </select>
        </div>
    );
};

export default SaveAudio;