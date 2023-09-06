import React, { useState } from "react";
import "./AddActorModal.css";

function AddActorModal(props) {
  const [newActorData, setNewActorData] = useState({
    name: "",
    age: "",
    gender: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewActorData({ ...newActorData, [name]: value });
  };

  const handleSubmit = () => {
    // Validate the input data here if needed

    // Pass the new actor data to the parent component
    props.onAdd(newActorData);

    // Clear the form and close the modal
    setNewActorData({ name: "", age: "", gender: "" });
    props.onClose();
  };

  return (
    <div className="modal-container">
      <div className="modal-content">
        <span className="close-button" onClick={props.onClose}>
          &times;
        </span>
        <h2>Add Actor</h2>
        <form>
          <div className="form-group">
            <label htmlFor="name">Name: </label>
            <input
              type="text"
              name="name"
              className="form-input"
              value={newActorData.name}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="age">Age: </label>
            <input
              type="text"
              name="age"
              className="form-input"
              value={newActorData.age}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="gender">Gender: </label>
            <input
              type="text"
              name="gender"
              className="form-input"
              value={newActorData.gender}
              onChange={handleChange}
            />
          </div>
        </form>
        <button onClick={handleSubmit} className="submit-button">
          Add Actor
        </button>
      </div>
    </div>
  );
}

export default AddActorModal;
