import React, { useEffect } from "react";
import "./Card.css";

function HUButton() {
  const auth0_domain = "capstone-fsnd-1234.us.auth0.com";
  const api_identifier = "casts";
  const client_id = "pWJFyxY4bglHX7UXThOfnPif5XquA29g";
  const callbackUrl = "http://127.0.0.1:3000";

  const loginURL = `https://${auth0_domain}/authorize?audience=${api_identifier}&response_type=token&client_id=${client_id}&redirect_uri=${callbackUrl}`;
  const loginButton = () => {
    window.location.href = loginURL;
  };

  useEffect(() => {
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const accessToken = hashParams.get("access_token");

    if (accessToken) {
      localStorage.setItem("access_token", accessToken);
      window.location.hash = "";
    }
  }, []);

  return (
    <div className="login-div">
      <button onClick={loginButton} className="login">
        Login
      </button>
    </div>
  );
}

export default HUButton;
