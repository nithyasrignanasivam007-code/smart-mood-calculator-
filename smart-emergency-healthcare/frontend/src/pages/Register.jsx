import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, useSearchParams } from 'react-router-dom';

const Register = () => {
    const [searchParams] = useSearchParams();
    const initialRole = searchParams.get('role') || 'patient';

    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        full_name: '',
        role: initialRole,
        blood_type: ''
    });

    const { register } = useAuth();
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await register(formData);
            navigate('/dashboard');
        } catch (err) {
            setError('Registration failed. Username may be taken.');
        }
    };

    return (
        <div className="flex items-center justify-center py-20">
            <div className="glass-panel p-8 w-full max-w-lg">
                <h2 className="text-3xl font-bold mb-6 text-center">Create Account</h2>
                {error && <div className="bg-danger/20 text-danger p-3 rounded-lg mb-4">{error}</div>}
                <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="md:col-span-2">
                        <label className="block text-gray-400 mb-2">Role</label>
                        <select name="role" className="input-field bg-surface" value={formData.role} onChange={handleChange}>
                            <option value="patient">Patient</option>
                            <option value="donor">Blood Donor</option>
                            <option value="ambulance">Ambulance Driver</option>
                            <option value="hospital_admin">Hospital Admin</option>
                        </select>
                    </div>

                    <div className="md:col-span-2">
                        <label className="block text-gray-400 mb-2">Full Name</label>
                        <input name="full_name" type="text" className="input-field" required onChange={handleChange} />
                    </div>

                    <div>
                        <label className="block text-gray-400 mb-2">Username</label>
                        <input name="username" type="text" className="input-field" required onChange={handleChange} />
                    </div>

                    <div>
                        <label className="block text-gray-400 mb-2">Email</label>
                        <input name="email" type="email" className="input-field" required onChange={handleChange} />
                    </div>

                    <div className="md:col-span-2">
                        <label className="block text-gray-400 mb-2">Password</label>
                        <input name="password" type="password" className="input-field" required onChange={handleChange} />
                    </div>

                    {(formData.role === 'patient' || formData.role === 'donor') && (
                        <div className="md:col-span-2">
                            <label className="block text-gray-400 mb-2">Blood Type</label>
                            <select name="blood_type" className="input-field bg-surface" onChange={handleChange}>
                                <option value="">Select Blood Type</option>
                                <option value="A+">A+</option>
                                <option value="A-">A-</option>
                                <option value="B+">B+</option>
                                <option value="B-">B-</option>
                                <option value="O+">O+</option>
                                <option value="O-">O-</option>
                                <option value="AB+">AB+</option>
                                <option value="AB-">AB-</option>
                            </select>
                        </div>
                    )}

                    <button type="submit" className="md:col-span-2 btn-primary mt-4">Register Function</button>
                </form>
            </div>
        </div>
    );
};

export default Register;
