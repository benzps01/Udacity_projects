import React from "react";

function ToggleButton({ isOn, updateIsOn }) {
  const toggleButton = () => {
    updateIsOn(!isOn);
  };
  return (
    <div>
      <button onClick={toggleButton}>{isOn ? "Actors" : "Movies"}</button>
    </div>
  );
}

export default ToggleButton;
