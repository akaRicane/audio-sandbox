import React from "react";
import { Link } from 'react-router-dom';

class Wiki extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Link to="/wiki">
        <div>
          <h1>WIKI PAGE</h1>
        </div>
      </Link>
    )
  }
};

export default Wiki;