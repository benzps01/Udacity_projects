import React, { useState } from "react";
import axios from "axios";
import "./Card.css";
import UpdateActorModal from "./UpdateActorModal";

function ActorCard(props) {
  const [selectedActor, setSelectedActor] = useState(null);

  const handleUpdateClick = (actor) => {
    setSelectedActor(actor);
  };

  const handleDelete = (actor_id) => {
    axios
      .delete(`http://127.0.0.1:5000/actors/${actor_id}`)
      .then((response) => {
        console.log("Delete Successful", response.data);

        const updateActorList = props.actorDetails.filter(
          (actor) => actor.id !== actor_id
        );
        props.updateActorList(updateActorList);
      })
      .catch((error) => {
        console.log("Delete Actor", error);
      });
  };

  return (
    <>
      {props.actorDetails.map((actor, actorIndex) => (
        <div className="card">
          <div className="actor-content" key={actorIndex}>
            <u>Actor - Details:</u>
            <p>Name: {actor.name}</p>
            <p>Age: {actor.age}</p>
            <p>Gender: {actor.gender}</p>
          </div>
          <div className="AU">
            <button className="add-details" onClick={props.openAddActorModal}>
              Add Actor
            </button>
            <button
              className="update-details"
              onClick={() => handleUpdateClick(actor)}
            >
              Update Actor
            </button>
          </div>
          <div className="Delete">
            <button
              className="delete-details"
              onClick={() => handleDelete(actor.id)}
            >
              Delete Actor
            </button>
          </div>
        </div>
      ))}
      {selectedActor && (
        <UpdateActorModal
          actor={selectedActor}
          onClose={() => setSelectedActor(null)}
          updateActorList={props.updateActorList}
        />
      )}
    </>
  );
}
export default ActorCard;
