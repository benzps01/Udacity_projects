import ActorCard from "./ActorCard";
import MovieCard from "./MovieCard";
import React, { useEffect, useState } from "react";
import fetchActorDetails from "./ActorData";
import fetchMovieDetails from "./MovieData";
import AddActorModal from "./AddActorModal";
import AddMovieModal from "./AddMovieModal";
import axios from "axios";
import HUButton from "./SigninButton";
import ToggleButton from "./ToggleButton";

function App() {
  const [actorDetails, setActorDetails] = useState([]);
  const [movieDetails, setMovieDetails] = useState([]);
  const [isOn, setIsOn] = useState(false);
  const [isActorModalOpen, setIsActorModalOpen] = useState(false);
  const [isMovieModalOpen, setIsMovieModalOpen] = useState(false);
  const [refreshData, setRefreshData] = useState(false);

  useEffect(() => {
    fetchActorDetails()
      .then((data) => {
        setActorDetails(data);
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });
  }, [refreshData]);
  useEffect(() => {
    fetchMovieDetails()
      .then((data) => {
        setMovieDetails(data);
      })
      .catch((error) => {
        console.log("Error fetching data:", error);
      });
  }, [refreshData]);

  const updateIsOn = (newIsOn) => {
    setIsOn(newIsOn);
  };

  const updateMovieList = (updatedMovieList) => {
    setMovieDetails(updatedMovieList);
  };

  const updateActorList = (updatedActorList) => {
    setActorDetails(updatedActorList);
  };

  const openAddActorModal = () => {
    setIsActorModalOpen(true);
  };

  const closeAddActorModal = () => {
    setIsActorModalOpen(false);
  };

  const openAddMovieModal = () => {
    setIsMovieModalOpen(true);
  };

  const closeAddMovieModal = () => {
    setIsMovieModalOpen(false);
  };

  const handleToggle = () => {
    setRefreshData(!refreshData);
  };

  const addActor = (newActorData) => {
    axios
      .post(`http://127.0.0.1:5000/actors`, newActorData)
      .then((response) => {
        console.log("Actor added successfully:", response.data["actors_dict"]);
        updateActorList(response.data["actors_dict"]);
        closeAddActorModal();
      })
      .catch((error) => {
        console.error("Error adding actor:", error);
      });
  };
  const addMovie = (newMovieData) => {
    axios
      .post(`http://127.0.0.1:5000/movies`, newMovieData)
      .then((response) => {
        console.log("Movie added successfully:", response.data["movies_dict"]);
        updateMovieList(response.data["movies_dict"]);
        closeAddMovieModal();
      })
      .catch((error) => {
        console.error("Error adding Movie:", error);
      });
  };

  return (
    <div>
      <HUButton />
      <ToggleButton
        isOn={isOn}
        updateIsOn={updateIsOn}
        onToggle={handleToggle}
      />
      {isOn ? (
        <MovieCard
          movieDetails={movieDetails}
          updateMovieList={updateMovieList}
          openAddMovieModal={openAddMovieModal}
        />
      ) : (
        <ActorCard
          actorDetails={actorDetails}
          updateActorList={updateActorList}
          openAddActorModal={openAddActorModal}
        />
      )}
      {isActorModalOpen && (
        <AddActorModal
          isOpen={isActorModalOpen}
          onClose={closeAddActorModal}
          onAdd={addActor}
        />
      )}
      {isMovieModalOpen && (
        <AddMovieModal
          isOpen={isMovieModalOpen}
          onClose={closeAddMovieModal}
          onAdd={addMovie}
        />
      )}
    </div>
  );
}
export default App;
