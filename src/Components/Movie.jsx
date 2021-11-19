import React from 'react';
import {Link} from 'react-router-dom';

function Movie({movie_data}){
    return (
        <li>
            <span><Link className="App-link" to={'/path3/' + movie_data.name}>{movie_data.name}
            </Link></span>
        </li>
    )
}

export default Movie;