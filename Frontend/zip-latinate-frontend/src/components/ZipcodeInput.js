import React, { useState} from "react";

const ZipcodeInput = ({onFetchInfo}) => {
    const [zipcode, setZipcode] = useState("");

    const handleFetchInfo = (e) => {
        e.preventDefault();
            onFetchInfo(zipcode);
    };
    
    return(
        <div>
            <input type="text"
                   value={zipcode}
                   onChange={(e) => setZipcode(e.target.value)}
                   placeholder="Enter your zip code"
            />
            <button onClick={handleFetchInfo}>Fetch Zip Code Info</button>
        </div>
    );
};

export default ZipcodeInput;

