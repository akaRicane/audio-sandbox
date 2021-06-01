import React from 'react';
import Navigation from './navigation.js';
import Main from './main';
import Graph from './graph';
import '../../css/style.css';

function App() {
    return (
      <div className="app">
        <Navigation />
        <Graph />
      </div>
    );
}

export default App;