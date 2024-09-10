import React, { useState, useEffect } from "react";
import Map from "./components/Map.js";
import Auth from "./components/Auth.js";
import SavedSearches from "./components/SavedSearches.js";
import SearchForm from "./components/SearchForm.js";
import LogoutButton from "./LogoutButton.js";
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
    const [isRegistering, setIsRegistering] = useState(false); // To toggle between login and registration
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
                setToken(data.access_token);
            } else {
                alert(data.error); // Show error to user
            }
        } catch (error) {
            alert('Error during login');
        }
    };

    // Handle user registration
    const handleRegister = async (e) => {
        e.preventDefault();

        const registerData = {
            username: username,
            password: password
        };

        try {
            const response = await fetch(`${apiURL}/register`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(registerData),
            });
            const data = await response.json();
            if (response.ok) {
                alert("User registered successfully! Please log in.");
                setIsRegistering(false); // Switch to login after successful registration
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert('Error during registration');
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
            }
        } catch (error) {
            alert('An error occurred while processing the request.');
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
                    fetchSavedSearches(); // Refresh saved searches after saving
                    setName("");
                    setZipcode("");
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

    useEffect(() => {
        if (token) {
            fetchSavedSearches(); // Fetch saved searches when logged in
        }
    }, [token]);
    // Conditional styling for background color transition
    const appClass = isRegistering ? "App registering" : "App";
 

    return (
        <div className={appClass}>
            {/* Logout button on top-right corner */}
            {token && <LogoutButton handleLogout={handleLogout} />}

            <h1>ZipLatinate</h1>

            {/* Conditionally render login or register form */}
            {!token ? (
                <Auth
                    isRegistering={isRegistering}
                    setIsRegistering={setIsRegistering}
                    username={username}
                    setUsername={setUsername}
                    password={password}
                    setPassword={setPassword}
                    handleLogin={handleLogin}
                    handleRegister={handleRegister}
                />
            ) : (
                <div>
                    <SearchForm 
                        name={name}
                        setName={setName}
                        zipcode={zipcode}
                        setZipcode={setZipcode}
                        handleSubmit={handleSubmit}
                    />
                    <button onClick={handleSaveSearch}  style={{ position: "absolute", top: "300px", right: "400px" }}>Save Search</button>
                </div>
            )}

            {/* Output with county, population and map */}
            {pigLatinName && county && population && (
                <p>{`${pigLatinName}'s zip code is in ${county} County and has a population of ${population}.`}</p>
            )}

            {/* Saved Searches */}
            {savedSearches.length > 0 && (
                <SavedSearches 
                    savedSearches={savedSearches}
                    handleDeleteSearch={handleDeleteSearch}
                />
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
