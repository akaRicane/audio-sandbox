import React from 'react';
import ReactDOM from 'react-dom';
import Navigation from './navigation.js';
import Header from './header.js';
import Graph from './graph.js';
import '../../css/style.css';


class Main extends React.Component {
  render() {
    return (
      <main>
        <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8"> 
          <Graph />
        </div>
      </main>
    )
  }
};


ReactDOM.render(
  <div>
    <Navigation />
    <Header />
    <Main />
  </div>,
  document.getElementById('main')
);
