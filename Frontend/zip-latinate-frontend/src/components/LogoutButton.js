import React from 'react';

const LogoutButton = ({ handleLogout }) => {
  return (
    <button onClick={handleLogout} style={{ position: "absolute", top: "10px", right: "10px" }}>
      Logout
    </button>
  );
};

export default LogoutButton;
