import React from 'react';
import ReactDOM from 'react-dom';
import App from './app';
import { BrowserRouter } from 'react-router-dom';

ReactDOM.render((
  <BrowserRouter>
    <App /> {/* The various pages will be displayed by the `Main` component. */}
  </BrowserRouter>
  ), document.getElementById('root')
);