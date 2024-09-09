import React, { useState } from "react";
import Map from '../src/components/Map.js';
import './App.css';

function App() {
    const [pigLatinName, setPigLatinName] = useState("");
    const [mapData, setMapData] = useState(null);
    const [county, setCounty] = useState("");
    const [population, setPopulation] = useState("");
    const [name, setName] = useState("");
    const [zipcode, setZipcode] = useState("");
    const apiURL = process.env.REACT_APP_API_URL;

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

    return (
        <div className="App">
            <h1>ZipLatinate</h1>

            {/* Combined Name and Zipcode Input */}
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

            {/* Output with county, population and map */}
            {pigLatinName && county && population && (
                <p>{`${pigLatinName}'s zip code is in ${county} County and has a population of ${population}.`}</p>
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
