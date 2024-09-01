import React, {useState} from "react";
import NameInput from '../src/components/NameInput.js';
import ZipcodeInput from '../src/components/ZipcodeInput.js';
import Map from "../src/components/Map.js";
import './App.css';

function App(){
  const[pigLatinName, setPigLatinName] = useState("");
  const[mapData, setMapData] = useState(null);
  const apiURL = process.env.FRONTEND_URL;

  const handleNameConvert = async (name) => {
    try {
        const response = await fetch(`${apiURL}/convert_name`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name }),
        });

        if (response.ok) {
            const text = await response.text();
            console.log(text);
            const data = text ? JSON.parse(text) : {};
            setPigLatinName(data.pig_latin_name || "Conversion failed");
        } else {
            alert('Failed to convert name');
        }
    } catch (error) {
        console.error("Error converting name:", error);
        alert('An error occurred while converting the name.');
    }
};


  const handleZipcodeFetch = async (zipcode) =>{
      const response = await fetch(`${apiURL}/zipcode_info`,{
          method:'POST',
          headers:{
              'Content-Type':'application/json',
          },
          body: JSON.stringify({zip_code: zipcode}),
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Received data:", data);  // Debugging print
        const position = [data.latitude, data.longitude];
        setMapData({ position, county: data.county });
    } else {
        const errorData = await response.json();
        alert(errorData.error);
    }
  };

  return(
      <div className="App">
          <h1>ZipLatinate</h1>
          <NameInput onConvert={handleNameConvert}/>
          {pigLatinName && <p>Pig Latin Name:{pigLatinName}</p>}
          <ZipcodeInput onFetchInfo={handleZipcodeFetch} />
          {mapData && <Map position={mapData.position} county={mapData.county}/>}
      </div>
  );
}

export default App;
