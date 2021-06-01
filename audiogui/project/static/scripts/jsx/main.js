import React from 'react';
import { Switch, Route } from 'react-router-dom';

import Graph from './graph';
import Wiki from './wiki';
import '../../css/style.css';


const Main = () => {
  return (
    <Switch>
      <Route exact path='/graph' component={Graph}></Route>
      <Route exact path='/wiki' component={Wiki}></Route>
    </Switch>
  );
}

export default Main;
