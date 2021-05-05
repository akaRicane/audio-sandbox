import React from 'react';
import Navigation from './navigation.js';
import Main from './main';
import '../../css/style.css';

function App() {
    return (
      <div className="app">
        <Navigation />
        <Main />
      </div>
    );
}

export default App;