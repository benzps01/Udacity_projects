import React from "react";
import "./Card.css";

function ToggleButton({ isOn, updateIsOn, onToggle }) {
  const toggleButton = () => {
    updateIsOn(!isOn);
    onToggle();
  };
  return (
    <div className="toggle-div">
      <button onClick={toggleButton} className="toggle-details">
        {isOn ? "Actors" : "Movies"}
      </button>
    </div>
  );
}

export default ToggleButton;
