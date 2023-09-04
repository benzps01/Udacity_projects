import "./Card.css";

function Card() {
  return (
    <div className="card">
      <header className="card-header">
        <p className="card-header-title">Movie Title</p>
      </header>
      <div className="movie-content">
        <u>Movie - Details:</u>
        <p>Release Date:</p>
        <p>Genre:</p>
        <p>Actor Id:</p>
      </div>
      <div className="actor-content">
        <u>Actor - Details:</u>
        <p>Name:</p>
        <p>Age:</p>
        <p>Gender:</p>
      </div>
    </div>
  );
}

export default Card;
