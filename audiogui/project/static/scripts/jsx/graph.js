import React, { useState } from "react";
import { Link } from 'react-router-dom';
import AudioSettings from "./components/AudioSettings.js";
import SignalGenerator from "./components/SignalGenerator.js";


function Sandbox() {
  
  const [settings, setSettings] = useState(
    {
      rate: "44100",
      buffer: "1024"
    }
  );

  const [labels, setLabels] = useState({});
  const [data, setData] = useState({});


  const updateSettings = (newSettings) => {
    console.log("New audio settings " + newSettings);
    setSettings(newSettings)
    console.log(settings)
  }

  const updateLabels = (newLabels) => {
    setData(newLabels)
    console.log("Labels updated")
  }

  const updateData = (newData) => {
    setData(newData)
    console.log("Data updated")
  }

  return (
    <Link to="/">
      <AudioSettings
        currentRate={settings.rate}
        currentBuffer={settings.buffer}
        settingsCallback={updateSettings}/>
      <br />
      <SignalGenerator 
        rate={settings.rate}
        labels={labels}
        data={data}
        labelsCallback={updateLabels}
        dataCallback={updateData}
        />
      <div>
        <br /><br />
        <p>State visualizer</p>
        <p>Rate: {"rate" in settings ? settings["rate"] : "No rate"}</p>
        <p>Buffer: {"buffer" in settings ? settings["buffer"] : "No buffer"}</p>
        <p>Data length: {data.length}</p>
      </div>
    
    </Link>
  )
};

export default Sandbox