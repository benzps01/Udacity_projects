import axios from 'axios';
import React, { useState, useEffect } from 'react';
import './Card.css';
import UpdateMovieModal from './UpdateMovieModal';
import jwt_decode from 'jwt-decode';

function MovieCard(props) {
  const [selectedMovie, setSelectedMovie] = useState(null);
  const [canAddMovie, setCanAddMovie] = useState(false);
  const [canDeleteMovie, setCanDeleteMovie] = useState(false);
  const [canUpdateMovie, setCanUpdateMovie] = useState(false);

  const baseURL = 'https://castingagency-frontend.onrender.com';

  const handleUpdateClick = (movie) => {
    setSelectedMovie(movie);
  };

  const token = localStorage.getItem('access_token');

  const axiosConfig = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const handleDelete = (movie_id) => {
    axios
      .delete(`${baseURL}/movies/${movie_id}`, axiosConfig)
      .then((response) => {
        console.log('Delete Successful', response.data);

        const updateMovieList = props.movieDetails.filter(
          (movie) => movie.id !== movie_id
        );
        props.updateMovieList(updateMovieList);
      })
      .catch((error) => {
        console.log('Delete Movie', error);
      });
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      const decodedToken = jwt_decode(token);

      if (decodedToken.permissions.includes('post:movies')) {
        setCanAddMovie(true);
      }
      if (decodedToken.permissions.includes('delete:movies')) {
        setCanDeleteMovie(true);
      }
      if (decodedToken.permissions.includes('patch:movies')) {
        setCanUpdateMovie(true);
      }
    }
  }, []);

  return (
    <div>
      <div className='add-modal'>
        <button
          className='add-details'
          onClick={props.openAddMovieModal}
          disabled={!canAddMovie}
        >
          Add Movie
        </button>
      </div>
      {props.movieDetails.map((movie, movieIndex) => (
        <div className='card' key={movieIndex}>
          <header className='card-header'>
            <p className='card-header-title'>{movie.title}</p>
          </header>
          <div className='movie-content'>
            <u>Movie - Details:</u>
            <p>Movie Id: {movie.id}</p>
            <p>Actor Id: {movie.actor_id}</p>
            <p>Release Date: {movie.release_date}</p>
            <p>Genre: {movie.genre}</p>
          </div>
          <div className='update-modal'>
            <button
              className='update-details'
              onClick={() => handleUpdateClick(movie)}
              disabled={!canUpdateMovie}
            >
              Update Movie
            </button>
          </div>
          <div className='Delete'>
            <button
              className='delete-details'
              onClick={() => handleDelete(movie.id)}
              disabled={!canDeleteMovie}
            >
              Delete Movie
            </button>
          </div>
        </div>
      ))}
      {selectedMovie && (
        <UpdateMovieModal
          movie={selectedMovie}
          onClose={() => setSelectedMovie(null)}
          updateMovieList={props.updateMovieList}
        />
      )}
    </div>
  );
}

export default MovieCard;
