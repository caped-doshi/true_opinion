import React from 'react';
import Movie from './Movie';

function Movie_List() {
    const movie_list = [
        {
            name: "Movie"
        },
        {
            name: "Avengers"
        }
    ]

    const ml = movie_list.map(movie => <Movie movie_data={movie} />)
    return <div class="list"><ul>{ml}</ul></div>
}

export default Movie_List;