import React from "react";
import "./Card.css";

function ToggleButton({ isOn, updateIsOn }) {
  const toggleButton = () => {
    updateIsOn(!isOn);
  };
  return (
    <div className="submit-div">
      <button onClick={toggleButton} className="submit-details">
        {isOn ? "Actors" : "Movies"}
      </button>
    </div>
  );
}

export default ToggleButton;
