import React, { useEffect, useState } from "react";
import "./Card.css";

function HLOButton() {
  const [canLogout, setCanLogout] = useState(true);

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_info");
    window.location.href = "http://127.0.0.1:3000";
  };

  useEffect(() => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      setCanLogout(false);
    }
  }, []);

  return (
    <div className="logout-div">
      <button onClick={handleLogout} className="logout" disabled={!canLogout}>
        Logout
      </button>
    </div>
  );
}

export default HLOButton;
