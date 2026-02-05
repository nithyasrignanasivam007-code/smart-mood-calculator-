import { useState, useEffect } from 'react';
import api from '../api/axios';
import { Droplet, Plus } from 'lucide-react';

const BloodBankDashboard = () => {
    const [inventory, setInventory] = useState([]);
    const [showForm, setShowForm] = useState(false);
    const [newData, setNewData] = useState({ blood_type: 'A+', quantity: 0 });

    useEffect(() => {
        // fetchInventory(); // Mocking for now as backend endpoint might need specific implementation
        // For MVP, using mock data or I need to implement GET /blood-inventory
        setInventory([
            { id: 1, blood_type: 'A+', quantity: 12, expiry: '2026-03-01' },
            { id: 2, blood_type: 'O-', quantity: 3, expiry: '2026-02-28' },
        ]);
    }, []);

    const handleAdd = async (e) => {
        e.preventDefault();
        // Simulate API call
        setInventory([...inventory, { id: Date.now(), ...newData, expiry: '2026-04-01' }]);
        setShowForm(false);
    };

    return (
        <div className="flex flex-col gap-8">
            <div className="flex justify-between items-center">
                <h2 className="text-3xl font-bold flex items-center gap-2">
                    <Droplet className="text-danger" fill="currentColor" /> Blood Bank Inventory
                </h2>
                <button onClick={() => setShowForm(!showForm)} className="btn-primary">
                    Add Stock
                </button>
            </div>

            {showForm && (
                <div className="glass-panel p-6 max-w-md">
                    <form onSubmit={handleAdd} className="flex gap-4">
                        <select className="input-field bg-surface" onChange={e => setNewData({ ...newData, blood_type: e.target.value })}>
                            <option>A+</option><option>O-</option><option>B+</option>
                        </select>
                        <input type="number" className="input-field" placeholder="Qty" onChange={e => setNewData({ ...newData, quantity: parseInt(e.target.value) })} />
                        <button className="btn-secondary">Save</button>
                    </form>
                </div>
            )}

            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {inventory.map(item => (
                    <div key={item.id} className="glass-panel p-6 text-center border-b-4 border-danger">
                        <h3 className="text-2xl font-bold text-danger">{item.blood_type}</h3>
                        <p className="text-4xl font-extrabold my-2">{item.quantity}</p>
                        <p className="text-xs text-gray-400">Units Available</p>
                    </div>
                ))}
            </div>
        </div>
    );
};
export default BloodBankDashboard;
