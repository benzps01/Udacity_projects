import React, { useState } from 'react';
import axios from 'axios';
import './UpdateModal.css';

function UpdateMovieModal(props) {
  const [updatedMovie, setUpdatedMovie] = useState({
    title: props.movie.title,
    release_date: props.movie.release_date,
    genre: props.movie.genre,
    actor_id: props.movie.actor_id,
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setUpdatedMovie({
      ...updatedMovie,
      [name]: value,
    });
  };

  const token = localStorage.getItem('access_token');

  const axiosConfig = {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  };

  const handleUpdate = () => {
    axios
      .patch(
        `https://castingagency-backend.onrender.com/movies/${props.movie.id}`,
        updatedMovie,
        axiosConfig
      )
      .then((response) => {
        console.log('Update Successful', response.data);
        props.onClose();
        props.updateMovieList(response.data['movies_dict']);
      })
      .catch((error) => {
        console.log('Update Movie', error);
      });
  };

  return (
    <div className='update-movie-modal'>
      <h2>Update Movie Details</h2>
      <form>
        <div className='form-group'>
          <label htmlFor='Title'>Title:</label>
          <input
            type='text'
            id='title'
            name='title'
            value={updatedMovie.title}
            onChange={handleInputChange}
          />
          <label htmlFor='release_date'>Release Date:</label>
          <input
            type='text'
            id='release_date'
            name='release_date'
            value={updatedMovie.release_date}
            onChange={handleInputChange}
          />
          <label htmlFor='gender'>Genre:</label>
          <input
            type='text'
            id='genre'
            name='genre'
            value={updatedMovie.genre}
            onChange={handleInputChange}
          />
          <label htmlFor='actor_id'>ActorID:</label>
          <input
            type='number'
            id='actor_id'
            name='actor_id'
            value={updatedMovie.actor_id}
            onChange={handleInputChange}
          />
        </div>
        <div className='button-group'>
          <button type='button' onClick={handleUpdate}>
            Update
          </button>
          <button type='button' onClick={props.onClose}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default UpdateMovieModal;
