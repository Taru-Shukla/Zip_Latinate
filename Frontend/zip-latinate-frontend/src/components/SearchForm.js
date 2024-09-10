import React, { useState } from 'react';

const SearchForm = ({ name, setName, zipcode, setZipcode, handleSubmit }) => {
  const [zipcodeError, setZipcodeError] = useState(""); // State to track errors

  const validateZipcode = (value) => {
    // Check if the value is numeric and has exactly 5 digits
    const zipRegex = /^[0-9]{5}$/;
    if (!zipRegex.test(value)) {
      setZipcodeError("Zipcode must be numeric and 5 digits long.");
    } else {
      setZipcodeError("");
    }
    setZipcode(value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter your full name"
        required
      />
      <input
        type="text"
        value={zipcode}
        onChange={(e) => validateZipcode(e.target.value)}
        placeholder="Enter your zip code"
        required
      />
      {zipcodeError && <div className="error">{zipcodeError}</div>} {/* Show error message */}
    </form>
  );
};

export default SearchForm;
