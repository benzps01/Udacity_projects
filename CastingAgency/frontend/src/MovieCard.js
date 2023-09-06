import axios from "axios";
import "./Card.css";

function MovieCard(props) {
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
          <div className="AU">
            <button className="add-details" onClick={props.openAddMovieModal}>
              Add Movie
            </button>
            <button className="update-details">Update Movie</button>
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
    </div>
  );
}

export default MovieCard;
