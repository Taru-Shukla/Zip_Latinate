import React, { useState, useEffect } from "react";
import Map from "./components/Map.js";
import './App.css';

function App() {
    const [pigLatinName, setPigLatinName] = useState("");
    const [mapData, setMapData] = useState(null);
    const [county, setCounty] = useState("");
    const [population, setPopulation] = useState("");
    const [name, setName] = useState("");
    const [zipcode, setZipcode] = useState("");
    const [token, setToken] = useState(null); // Track the token state
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [savedSearches, setSavedSearches] = useState([]); // To store saved searches
    const apiURL = process.env.REACT_APP_API_URL;

    // Handle user login
    const handleLogin = async (e) => {
        e.preventDefault();

        const loginData = {
            username: username,
            password: password
        };

        try {
            const response = await fetch(`${apiURL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loginData),
            });
            const data = await response.json();
            if (response.ok) {
                console.log('Login successful');
                console.log('Token:', data.access_token);

                // Save the token in the state
                setToken(data.access_token);
            } else {
                console.log('Login failed:', data.error);
                alert(data.error); // Show error to user
            }
        } catch (error) {
            alert('Error during login');
        }
    };

    // Handle user logout
    const handleLogout = () => {
        setToken(null); // Clear the token
        setSavedSearches([]); // Clear saved searches
        setPigLatinName(""); // Reset the form data
        setMapData(null);
        setCounty("");
        setPopulation("");
        setName("");
        setZipcode("");
    };

    // Handle name and zipcode submission (not saving search here)
    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            // Convert Name to Pig Latin
            const nameResponse = await fetch(`${apiURL}/convert_name`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ name }),
            });

            if (nameResponse.ok) {
                const nameData = await nameResponse.json();
                setPigLatinName(nameData.pig_latin_name || "Conversion failed");
            } else {
                alert('Failed to convert name');
            }

            // Fetch Zipcode Info
            const zipcodeResponse = await fetch(`${apiURL}/zipcode_info`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ zip_code: zipcode }),
            });

            if (zipcodeResponse.ok) {
                const zipData = await zipcodeResponse.json();
                const position = [zipData.latitude, zipData.longitude];
                setMapData({ position, county: zipData.county });
                setCounty(zipData.county);
                setPopulation(zipData.population);
            } else {
                alert('Failed to fetch zipcode info');
            }
        } catch (error) {
            alert('An error occurred while processing the request.');
        }
    };

    // Handle saving the search
    const handleSaveSearch = async () => {
        if (token && county && population) { // Ensure search data is ready before saving
            try {
                const saveSearchResponse = await fetch(`${apiURL}/save_search`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`, // Pass JWT token for authentication
                    },
                    body: JSON.stringify({ name, zip_code: zipcode, county, population }), // Include county and population
                });

                if (saveSearchResponse.ok) {
                    alert("Search saved successfully!");

                    // Fetch saved searches to update the UI
                    fetchSavedSearches();
                } else {
                    alert("Failed to save search.");
                }
            } catch (error) {
                alert('Error saving search');
            }
        } else {
            alert("Please fetch name and zip code data first before saving the search.");
        }
    };

    // Fetch saved searches from the server
    const fetchSavedSearches = async () => {
        if (token) {
            try {
                const response = await fetch(`${apiURL}/get_searches`, {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`, // Send token in headers
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    setSavedSearches(data); // Store saved searches
                }
            } catch (error) {
                alert('Error fetching saved searches');
            }
        }
    };

    // Handle deleting a search
    const handleDeleteSearch = async (id) => {
        if (token) {
            try {
                const response = await fetch(`${apiURL}/delete_search/${id}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                    },
                });
                if (response.ok) {
                    alert("Search deleted successfully.");
                    fetchSavedSearches(); // Refresh the saved searches after deletion
                } else {
                    alert("Failed to delete search.");
                }
            } catch (error) {
                alert('Error deleting search');
            }
        }
    };

    useEffect(() => {
        if (token) {
            fetchSavedSearches(); // Fetch saved searches when logged in
        }
    }, [token]);

    return (
        <div className="App">
            <h1>ZipLatinate</h1>

            {/* Conditionally render login form or search form */}
            {!token ? (
                // Login Form
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
                </form>
            ) : (
                <div>
                    {/* Show Search form when the user is logged in */}
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
                        <button type="submit">Submit</button>
                    </form>

                    <button onClick={handleSaveSearch}>Save Search</button>
                    <button onClick={handleLogout}>Logout</button>
                </div>
            )}

            {/* Output with county, population and map */}
            {pigLatinName && county && population && (
                <p>{`${pigLatinName}'s zip code is in ${county} County and has a population of ${population}.`}</p>
            )}

            {/* Saved Searches */}
            {savedSearches.length > 0 && (
                <div>
                    <h3>Saved Searches</h3>
                    <ul>
                        {savedSearches.map((search, index) => (
                            <li key={index}>
                                {search.name} ({search.zip_code}) - {search.county}, Population: {search.population}
                                <button onClick={() => handleDeleteSearch(search.id)}>Delete</button>
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* Main Layout with Flexbox */}
            <div className="main-content">
                {/* Fun Facts Section */}
                <div className="fun-facts">
                    <h3>Did you know?</h3>
                    <p>Pig Latin is a fun way to alter English words. By moving the first consonant to the end and adding 'ay', you can create a playful version of your name!</p>
                    <p>It was commonly used as a secret language among kids and originated as a playful transformation of English in the 19th century.</p>
                </div>

                {/* Conditionally Render Map Section */}
                {mapData && (
                    <div className="map-container">
                        <Map position={mapData.position} county={mapData.county} />
                    </div>
                )}
            </div>
        </div>
    );
}

export default App;
