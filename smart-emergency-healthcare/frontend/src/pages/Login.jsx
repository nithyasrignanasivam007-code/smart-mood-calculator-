import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate } from 'react-router-dom';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { login } = useAuth();
    const navigate = useNavigate();
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await login(username, password);
            navigate('/dashboard');
        } catch (err) {
            setError('Invalid credentials');
        }
    };

    return (
        <div className="flex items-center justify-center py-20">
            <div className="glass-panel p-8 w-full max-w-md">
                <h2 className="text-3xl font-bold mb-6 text-center">Welcome Back</h2>
                {error && <div className="bg-danger/20 text-danger p-3 rounded-lg mb-4">{error}</div>}
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                    <div>
                        <label className="block text-gray-400 mb-2">Username</label>
                        <input
                            type="text"
                            className="input-field"
                            value={username} onChange={(e) => setUsername(e.target.value)}
                            required
                        />
                    </div>
                    <div>
                        <label className="block text-gray-400 mb-2">Password</label>
                        <input
                            type="password"
                            className="input-field"
                            value={password} onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn-primary mt-4">Login</button>
                </form>
            </div>
        </div>
    );
};

export default Login;
