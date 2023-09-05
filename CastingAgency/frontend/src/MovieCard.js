import React from "react";
import "./Card.css";

function MovieCard(props) {
  return (
    <div>
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
          <div className="DU">
            <button className="update-details">Update Movie</button>
            <button className="delete-details">Delete Movie</button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default MovieCard;
