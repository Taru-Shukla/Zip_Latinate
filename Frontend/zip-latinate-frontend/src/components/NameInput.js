import React, {useState} from 'react';

const NameInput = ({ onConvert }) => {
    const [name, setName] = useState("");

    const handleConvert = () => {
        onConvert(name);
    };

    return (
        <div>
            <input type = "text"
                   value={name}
                   onChange={(e)=>setName(e.target.value)}
                   placeholder = "Enter your full name"
            />
            <button onClick={handleConvert}>Convert to Pig Latin</button>
        </div>
    );
};

export default NameInput;