import axios from "axios";
import React, { useState } from "react";
import "./Card.css";
import UpdateMovieModal from "./UpdateMovieModal";

function MovieCard(props) {
  const [selectedMovie, setSelectedMovie] = useState(null);

  const handleUpdateClick = (movie) => {
    setSelectedMovie(movie);
  };

  const handleDelete = (movie_id) => {
    axios
      .delete(`http://127.0.0.1:5000/movies/${movie_id}`)
      .then((response) => {
        console.log("Delete Successful", response.data);

        const updateMovieList = props.movieDetails.filter(
          (movie) => movie.id !== movie_id
        );
        props.updateMovieList(updateMovieList);
      })
      .catch((error) => {
        console.log("Delete Movie", error);
      });
  };

  return (
    <div>
      <div className="add-modal">
        <button className="add-details" onClick={props.openAddMovieModal}>
          Add Movie
        </button>
      </div>
      {props.movieDetails.map((movie, movieIndex) => (
        <div className="card" key={movieIndex}>
          <header className="card-header">
            <p className="card-header-title">{movie.title}</p>
          </header>
          <div className="movie-content">
            <u>Movie - Details:</u>
            <p>Release Date: {movie.release_date}</p>
            <p>Genre: {movie.genre}</p>
            <p>Actor Id: {movie.actor_id}</p>
          </div>
          <div className="update-modal">
            <button
              className="update-details"
              onClick={() => handleUpdateClick(movie)}
            >
              Update Movie
            </button>
          </div>
          <div className="Delete">
            <button
              className="delete-details"
              onClick={() => handleDelete(movie.id)}
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
