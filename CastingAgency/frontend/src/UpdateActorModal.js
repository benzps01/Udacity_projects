import React, { useState } from "react";
import axios from "axios";
import "./UpdateModal.css";

function UpdateActorModal(props) {
  const [updatedActor, setUpdatedActor] = useState({
    name: props.actor.name,
    age: props.actor.age,
    gender: props.actor.gender,
  });

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setUpdatedActor({
      ...updatedActor,
      [name]: value,
    });
  };

  const handleUpdate = () => {
    axios
      .patch(`http://127.0.0.1:5000/actors/${props.actor.id}`, updatedActor)
      .then((response) => {
        console.log("Update Successful", response.data);
        props.onClose();
        props.updateActorList(response.data["actors_dict"]);
      })
      .catch((error) => {
        console.log("Update Actor", error);
      });
  };

  return (
    <div className="update-actor-modal">
      <h2>Update Actor Details</h2>
      <form>
        <div className="form-group">
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={updatedActor.name}
            onChange={handleInputChange}
          />
          <label htmlFor="age">Age:</label>
          <input
            type="number"
            id="age"
            name="age"
            value={updatedActor.age}
            onChange={handleInputChange}
          />
          <label htmlFor="gender">Gender:</label>
          <input
            type="text"
            id="gender"
            name="gender"
            value={updatedActor.gender}
            onChange={handleInputChange}
          />
        </div>
        <div className="button-group">
          <button type="button" onClick={handleUpdate}>
            Update
          </button>
          <button type="button" onClick={props.onClose}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
}

export default UpdateActorModal;
