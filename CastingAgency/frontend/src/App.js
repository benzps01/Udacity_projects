import ActorCard from "./ActorCard";
import MovieCard from "./MovieCard";
import React, { useEffect, useState } from "react";
import fetchActorDetails from "./ActorData";
import fetchMovieDetails from "./MovieData";
import ToggleButton from "./ToggleButton";

function App() {
  const [actorDetails, setActorDetails] = useState([]);
  const [movieDetails, setMovieDetails] = useState([]);
  const [isOn, setIsOn] = useState(false);

  useEffect(() => {
    fetchActorDetails()
      .then((data) => {
        setActorDetails(data);
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });
  }, []);
  useEffect(() => {
    fetchMovieDetails()
      .then((data) => {
        setMovieDetails(data);
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });
  }, []);

  const updateIsOn = (newIsOn) => {
    setIsOn(newIsOn);
  };
  return (
    <div>
      <ToggleButton isOn={isOn} updateIsOn={updateIsOn} />
      {isOn ? (
        <MovieCard movieDetails={movieDetails} />
      ) : (
        <ActorCard actorDetails={actorDetails} />
      )}
    </div>
  );
}

export default App;
