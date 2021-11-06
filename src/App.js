import React, { useState, useEffect } from 'react';
import { BrowserRouter, Route, Link, Switch } from 'react-router-dom';
import logo from './logo.svg';
import Movie_List from './Components/Movie_List';
import Movie_Statistics from './Components/Movie_Statistics';
import './App.css';

function App() {

    return ( <
        div className = "App" >
        <
        header className = "App-header" >
        <
        BrowserRouter >
        <
        div >
        <
        div >
        <
        Link className = "App-link"
        to = "/" > Home < /Link> | <Link className="App-link" to="/page
        1 ">Page 1</Link> | <
        Link className = "App-link"
        to = "/page3" > Page 3 < /Link> <
        /div> <
        Switch >
        <
        Route exact path = "/" >
        <
        Movie_List / >
        <
        /Route> <
        Route path = "/page1" >
        <
        h2 > Welcome to page 1 < /h2> <
        /Route> <
        Route path = "/page3" >
        <
        h3 > Welcome to page 3 < /h3> <
        Route path = "/page3/:name" >
        <
        Movie_Statistics / >
        <
        /Route> <
        /Route> <
        /Switch> <
        /div> <
        /BrowserRouter> <
        /header> <
        /div>
    );
}

export default App;