import { useState, useEffect } from 'react';
import api from '../api/axios';
import { AlertTriangle, MapPin, Activity } from 'lucide-react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Fix Leaflet marker icons
import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

const PatientDashboard = () => {
    const [activeEmergency, setActiveEmergency] = useState(null);
    const [loading, setLoading] = useState(false);
    const [location, setLocation] = useState(null);

    useEffect(() => {
        // Check for existing emergency
        checkActiveEmergency();
        // Get location
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    setLocation({
                        lat: position.coords.latitude,
                        lng: position.coords.longitude
                    });
                },
                (err) => console.error(err)
            );
        }
    }, []);

    const checkActiveEmergency = async () => {
        try {
            const { data } = await api.get('/my-emergency');
            if (data && data.length > 0) {
                // Find one that is not completed
                const active = data.find(e => e.status !== 'COMPLETED');
                if (active) setActiveEmergency(active);
            }
        } catch (error) {
            //   console.error(error);
        }
    };

    const requestEmergency = async (type) => {
        if (!location) {
            alert("Please enable location services.");
            return;
        }
        setLoading(true);
        try {
            const { data } = await api.post('/emergency', {
                latitude: location.lat,
                longitude: location.lng,
                emergency_type: type
            });
            setActiveEmergency(data);
        } catch (error) {
            console.error(error);
            alert("Failed to request emergency.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col gap-8">
            <div className="glass-panel p-8">
                <h2 className="text-3xl font-bold mb-4 flex items-center gap-3">
                    <Activity className="text-primary" /> Patient Emergency Center
                </h2>
                {location ? <p className="text-success text-sm mb-4">Location Detected: {location.lat.toFixed(4)}, {location.lng.toFixed(4)}</p> : <p className="text-warning text-sm mb-4">Detecting Location...</p>}

                {!activeEmergency ? (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
                        <button
                            onClick={() => requestEmergency('General')}
                            disabled={loading || !location}
                            className="bg-danger hover:bg-red-600 text-white p-10 rounded-2xl shadow-xl flex flex-col items-center gap-4 transition-all transform hover:scale-105 disabled:opacity-50"
                        >
                            <AlertTriangle size={64} />
                            <span className="text-2xl font-bold">SOS - GENERAL EMERGENCY</span>
                        </button>
                        <button
                            onClick={() => requestEmergency('Cardiac')}
                            disabled={loading || !location}
                            className="bg-orange-500 hover:bg-orange-600 text-white p-10 rounded-2xl shadow-xl flex flex-col items-center gap-4 transition-all transform hover:scale-105 disabled:opacity-50"
                        >
                            <Activity size={64} />
                            <span className="text-2xl font-bold">CARDIAC ARREST</span>
                        </button>
                    </div>
                ) : (
                    <div className="bg-surface/50 p-6 rounded-xl border border-primary/50 animate-pulse">
                        <h3 className="text-2xl font-bold text-primary mb-2">Emergency Active</h3>
                        <p>Status: <span className="font-bold text-white">{activeEmergency.status}</span></p>
                        <p>ID: #{activeEmergency.id}</p>
                        {activeEmergency.assigned_hospital_id && (
                            <p className="text-success mt-2">Hospital Assigned! Proceeding to location.</p>
                        )}
                    </div>
                )}
            </div>

            {/* Map Section */}
            <div className="h-[500px] glass-panel p-2 overflow-hidden relative">
                <h3 className="absolute top-6 left-6 z-10 bg-black/50 px-3 py-1 rounded text-sm font-bold">Live Tracking</h3>
                {location && (
                    <MapContainer center={[location.lat, location.lng]} zoom={13} scrollWheelZoom={false} className="map-container">
                        <TileLayer
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                        />
                        <Marker position={[location.lat, location.lng]}>
                            <Popup>
                                You are here.
                            </Popup>
                        </Marker>
                    </MapContainer>
                )}
            </div>
        </div>
    );
};

export default PatientDashboard;
