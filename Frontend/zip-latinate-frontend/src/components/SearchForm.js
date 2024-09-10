import React from 'react';

const SearchForm = ({ name, setName, zipcode, setZipcode, handleSubmit }) => {
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
        onChange={(e) => setZipcode(e.target.value)}
        placeholder="Enter your zip code"
        required
      />
    </form>
  );
};

export default SearchForm;
