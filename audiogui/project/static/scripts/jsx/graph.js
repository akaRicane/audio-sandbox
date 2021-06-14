import React, { useState } from "react";
import { Link } from 'react-router-dom';
import AudioSettings from "./components/AudioSettings.js";
import LineGraph from "./components/LineGraph.js";
import LoadAudioFile from './components/LoadAudioFile';
import PlayerAudio from "./components/PlayerAudio.js";
import RecorderAudio from "./components/RecorderAudio.js";
import SaveAudio from './components/SaveAudio.js'
import SignalGenerator from "./components/SignalGenerator.js";

const Sandbox = () => {

  const [settings, setSettings] = useState(
    {
      rate: "44100",
      buffer: "1024"
    }
  );

  const [labels, setLabels] = useState({});
  const [data, setData] = useState({});

  const updateRate = (newRate) => {
    setSettings({ rate: newRate })
    console.log("Rate updated")
  };

  const updateSettings = (newSettings) => {
    setSettings(newSettings)
    console.log(settings)
  };

  const updateLabels = (newLabels) => {
    setLabels(newLabels)
    console.log("Labels updated")
  };

  const updateData = (newData) => {
    setData(newData)
    console.log("Data updated")
  };

  return (
    <Link to="/">
      <AudioSettings
        currentRate={settings.rate}
        currentBuffer={settings.buffer}
        settingsCallback={updateSettings} />
      <br />
      <SignalGenerator
        rate={settings.rate}
        labels={labels}
        data={data}
        labelsCallback={updateLabels}
        dataCallback={updateData}
      />
      <br />
      <LoadAudioFile
        rateCallback={updateRate}
        labelsCallback={updateLabels}
        dataCallback={updateData}
      />
      <br />
      <SaveAudio
        rate={settings.rate}
        data={data}
      />
      <br />
      <PlayerAudio
        rate={settings.rate}
        data={data}
      />
      <RecorderAudio
        rateCallback={updateRate}
        labelsCallback={updateLabels}
        dataCallback={updateData}
        rate={settings.rate}
      />
      <br />
      <div>
        <br /><br />
        <p>State visualizer</p>
        <p>Rate: {"rate" in settings ? settings["rate"] : "No rate"}</p>
        <p>Buffer: {"buffer" in settings ? settings["buffer"] : "No buffer"}</p>
        <p>Data length: {data.length}</p>
      </div>

    </Link>
  );
};

export default Sandbox;
