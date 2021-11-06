import React from 'react';
import { useParams } from 'react-router-dom';
import movies from './movies.json';

const Movie_Statistics =() => {
    console.log("Hello");
    const {name} = useParams();

    for(var i = 0; i < movies.length; i++){
        console.log(movies[i]);
    }

    return (
        <h4>Movie : {name}</h4>
    );
}

export default Movie_Statistics;