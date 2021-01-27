import { useState, useEffect } from 'react';
import React, { Component } from 'react';
import FloatingLabelInput from 'react-floating-label-input';
import './App.css';
import wikiMapLogo from './WikiMap.png';

function App() {

  const [source, setSource] = useState("");
  const [dest, setDest] = useState("");
  const [path, setPath] = useState([]);
  const [error, setError] = useState(false);



  const handleChangeSrc = (e) => {
    setSource(e.target.value);
  }
  const handleChangeDest = (e) => {
    setDest(e.target.value);
  }

  const handleSubmit = async (e) => {
    //pass source and dest into api
      e.preventDefault();
      //call api function
      const srcRes = await fetch(`/title?title=${source}`);
      const [srcId, srcTitle]  = (await srcRes.json()).page;
      const destRes = await fetch(`/title?title=${dest}`);
      const [destId, destTitle]= (await destRes.json()).page;

      //add check for empty list


      const res = await fetch(`./path?src-id=${srcId}&dest-id=${destId}`);
      //sort this path based on length
      const paths = (await res.json()).path;
      if (paths.length !== 0){
        setPath(paths[0]);
        setError(false);
      } else {
        setPath([]);
        setError(true);
      }
      //[einstein, atomic_bomb, world war 2]        
  }

  return (
    <div className="App">
      <header className="Header">
        <a href="#"><img src={wikiMapLogo} className="logoSize"/></a>
        <p>Finding links for you in the Wiki world.</p>
      </header>
      <div className="container">
        <div className="input-field">
            <FloatingLabelInput className="input" label="Source" id="source" onChange={handleChangeSrc} />
        </div>
        <div className="resultTable">
          {
            error &&
            <p>No path exists</p>
          }
          {path && path.map(title => {
            return(
            <p key={title}><a href={`https://en.wikipedia.org/wiki/${title}`} className="linkColour" target="_blank">{title}</a></p>
            )
          })}
        </div>
        <div className="input-field">
            <FloatingLabelInput className="input" label="Destination" id="destination" onChange={handleChangeDest} />
            <button className="Button-style" onClick={handleSubmit}>Find</button>
        </div>
      </div>           
    </div>
  );
}

export default App;