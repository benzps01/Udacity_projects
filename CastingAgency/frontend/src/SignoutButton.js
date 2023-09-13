import React, { useEffect, useState } from 'react';
import './Card.css';

function HLOButton() {
  const [canLogout, setCanLogout] = useState(true);

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    document.cookie =
      'access_token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

    localStorage.removeItem('user_info');
    document.cookie =
      'user_info=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';

    window.location.href = 'https://castingagency-frontend.onrender.com';
  };

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setCanLogout(false);
    }
  }, []);

  return (
    <div className='logout-div'>
      <button onClick={handleLogout} className='logout' disabled={!canLogout}>
        Logout
      </button>
    </div>
  );
}

export default HLOButton;
