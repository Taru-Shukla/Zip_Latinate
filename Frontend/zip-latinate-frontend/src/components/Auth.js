import React from 'react';

const Auth = ({ isRegistering, setIsRegistering, username, setUsername, password, setPassword, handleLogin, handleRegister }) => {
  return (
    <div>
      {isRegistering ? (
        <form onSubmit={handleRegister}>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
          <button type="submit">Create Account</button>
          <button type="button" onClick={() => setIsRegistering(false)}>Go to Login</button>
        </form>
      ) : (
        <form onSubmit={handleLogin}>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
            required
          />
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
            required
          />
          <button type="submit">Login</button>
          <button type="button" onClick={() => setIsRegistering(true)}>Create New User</button>
        </form>
      )}
    </div>
  );
};

export default Auth;
