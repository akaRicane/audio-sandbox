import React, { useState } from "react";
import axios from 'axios';
import { Link } from 'react-router-dom';
import SignalGenerator from "./components/SignalGenerator.js";
import LineGraph from "./components/LineGraph.js";
import AudioSettings from "./components/AudioSettings.js";


function Graph() {
  
  const [settings, setSettings] = useState(
    {
      rate: "44100",
      buffer: "1024"
    }
  );


  const updateSettings = (newSettings) => {
    console.log("New audio settings " + newSettings);
    setSettings(newSettings)
    console.log(settings)
}

  return (
    <Link to="/">
      <AudioSettings
        currentRate={settings.rate}
        currentBuffer={settings.buffer}
        callback={updateSettings}/>
      <div>
        <p>Rate: {"rate" in settings ? settings["rate"] : "No rate"}</p>
        <p>Buffer: {"buffer" in settings ? settings["buffer"] : "No buffer"}</p>
      </div>
    
    </Link>
  )
};

export default Graph