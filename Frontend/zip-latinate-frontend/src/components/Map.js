import React from 'react';
import {MapContainer, TileLayer, Marker, Popup} from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import markerIcon from 'leaflet/dist/images/marker-icon.png';
import markerShadow from 'leaflet/dist/images/marker-shadow.png';

const Map = ({position, county}) => {
    const defaultIcon = L.icon({
        iconUrl: markerIcon,
        shadowUrl: markerShadow,
    });

    return (
        <MapContainer center={position} zoom={10} style={{height: "400px", width: "100%"}}>
            <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
            <Marker position={position} icon={defaultIcon}>
                <Popup>
                    {county}
                </Popup>
            </Marker>
        </MapContainer>
    );
};

export default Map;