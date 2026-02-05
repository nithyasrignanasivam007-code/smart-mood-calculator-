import { useState, useEffect } from 'react';
import api from '../api/axios';
import { Plus, Shield } from 'lucide-react';

const HospitalDashboard = () => {
    const [hospitals, setHospitals] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [formData, setFormData] = useState({
        name: '', latitude: 0, longitude: 0, address: '',
        icu_beds_total: 10, icu_beds_available: 5,
        doctors_available: 2, oxygen_cylinders: 20, ventilators: 5
    });

    useEffect(() => {
        fetchHospitals();
    }, []);

    const fetchHospitals = async () => {
        try {
            const { data } = await api.get('/hospitals');
            setHospitals(data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post('/hospitals', formData);
            setShowForm(false);
            fetchHospitals();
        } catch (err) {
            alert('Failed to add hospital');
        }
    };

    return (
        <div className="flex flex-col gap-8">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold">Hospital Management</h2>
                <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center gap-2">
                    <Plus size={20} /> Register New Hospital
                </button>
            </div>

            {showForm && (
                <div className="glass-panel p-6">
                    <h3 className="text-xl font-bold mb-4">Register Hospital</h3>
                    <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <input placeholder="Name" className="input-field" onChange={e => setFormData({ ...formData, name: e.target.value })} />
                        <input placeholder="Address" className="input-field" onChange={e => setFormData({ ...formData, address: e.target.value })} />
                        <input placeholder="Lat" type="number" className="input-field" onChange={e => setFormData({ ...formData, latitude: parseFloat(e.target.value) })} />
                        <input placeholder="Lng" type="number" className="input-field" onChange={e => setFormData({ ...formData, longitude: parseFloat(e.target.value) })} />
                        <input placeholder="ICU Beds" type="number" className="input-field" onChange={e => setFormData({ ...formData, icu_beds_available: parseInt(e.target.value) })} />
                        <input placeholder="Doctors" type="number" className="input-field" onChange={e => setFormData({ ...formData, doctors_available: parseInt(e.target.value) })} />
                        <button className="btn-primary md:col-span-2">Submit</button>
                    </form>
                </div>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {hospitals.map(hospital => (
                    <div key={hospital.id} className="glass-panel p-6 hover:border-primary/50 transition-colors">
                        <div className="flex items-start justify-between mb-4">
                            <div>
                                <h3 className="text-xl font-bold">{hospital.name}</h3>
                                <p className="text-sm text-gray-400">{hospital.address}</p>
                            </div>
                            <Shield className="text-primary" />
                        </div>

                        <div className="space-y-2">
                            <div className="flex justify-between">
                                <span>Readiness Score:</span>
                                <span className="font-bold text-accent">{hospital.readiness_score.toFixed(1)}</span>
                            </div>
                            <div className="flex justify-between">
                                <span>ICU Beds:</span>
                                <span className={hospital.icu_beds_available < 3 ? "text-danger" : "text-success"}>{hospital.icu_beds_available} / {hospital.icu_beds_total}</span>
                            </div>
                            <div className="flex justify-between">
                                <span>Doctors:</span>
                                <span>{hospital.doctors_available}</span>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default HospitalDashboard;
