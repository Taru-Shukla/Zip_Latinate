import React from 'react';

const SavedSearches = ({ savedSearches, handleDeleteSearch }) => {
  return (
    <div className="saved-searches">
      <h3>Saved Searches</h3>
      <ul>
        {savedSearches.map((search, index) => (
          <li key={index} className="saved-search-item">
            <div className="search-details">
              {search.name} ({search.zip_code}) - {search.county}, Population: {search.population}
            </div>
            <button className="delete-button" onClick={() => handleDeleteSearch(search.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SavedSearches;
