import React, { useState } from "react";
import "./AddActorModal.css";

function AddMovieModal(props) {
  const [newMovieData, setNewMovieData] = useState({
    title: "",
    release_date: "",
    genre: "",
    actor_id: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setNewMovieData({ ...newMovieData, [name]: value });
  };

  const handleSubmit = () => {
    // Validate the input data here if needed

    // Pass the new actor data to the parent component
    props.onAdd(newMovieData);

    // Clear the form and close the modal
    setNewMovieData({ title: "", release_date: "", genre: "", actor_id: "" });
    props.onClose();
  };

  return (
    <div className="modal-container">
      <div className="modal-content">
        <span className="close-button" onClick={props.onClose}>
          &times;
        </span>
        <h2>Add Movie</h2>
        <form>
          <div className="form-group">
            <label htmlFor="title">Title: </label>
            <input
              type="text"
              name="title"
              className="form-input"
              value={newMovieData.title}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="release_date">Release Date: </label>
            <input
              type="text"
              name="release_date"
              className="form-input"
              value={newMovieData.release_date}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="genre">Genre: </label>
            <input
              type="text"
              name="genre"
              className="form-input"
              value={newMovieData.genre}
              onChange={handleChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="actor_id">Actor ID: </label>
            <input
              type="text"
              name="actor_id"
              className="form-input"
              value={newMovieData.actor_id}
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

export default AddMovieModal;
