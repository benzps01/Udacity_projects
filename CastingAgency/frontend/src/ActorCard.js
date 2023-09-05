import React from "react";
import "./Card.css";

function ActorCard(props) {
  const handleDelete() {

  }

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
          <div className="DU">
            <button className="update-details" onClick="handleDelete">Update Actor</button>
            <button className="delete-details">Delete Actor</button>
          </div>
        </div>
      ))}
    </>
  );
}
export default ActorCard;
