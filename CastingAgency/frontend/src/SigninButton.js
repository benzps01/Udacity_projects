import React, { useEffect, useState } from 'react';
import './Card.css';

function HUButton() {
  const [refreshData, setRefreshData] = useState(false);
  const [canLogin, setCanLogin] = useState(true);

  const loginURL = `https://${process.env.REACT_APP_AUTH0_DOMAIN}/authorize?audience=${process.env.REACT_APP_API_IDENTIFIER}&response_type=token&client_id=${process.env.REACT_APP_CLIENT_ID}&redirect_uri=${process.env.REACT_APP_CALLBACKURL}`;
  const loginButton = () => {
    window.location.href = loginURL;
  };

  useEffect(() => {
    const hashParams = new URLSearchParams(window.location.hash.substring(1));
    const accessToken = hashParams.get('access_token');

    if (accessToken) {
      localStorage.setItem('access_token', accessToken);
      setRefreshData(true);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    if (token) {
      setCanLogin(false);
    }
  }, []);

  const handleLO = () => {
    setRefreshData(!refreshData);
  };

  return (
    <div className='login-div'>
      <button
        onClick={loginButton}
        className='login'
        onLog={handleLO}
        disabled={!canLogin}
      >
        Login
      </button>
    </div>
  );
}

export default HUButton;
