import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Activity, Menu, X, User as UserIcon, LogOut } from 'lucide-react';
import { useState } from 'react';

const Layout = ({ children }) => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const handleLogout = () => {
        logout();
        navigate('/');
    };

    return (
        <div className="min-h-screen bg-background relative overflow-hidden">
            {/* Background blobs */}
            <div className="absolute top-0 left-0 w-96 h-96 bg-primary/20 rounded-full blur-3xl -z-10 animate-blob"></div>
            <div className="absolute bottom-0 right-0 w-96 h-96 bg-secondary/20 rounded-full blur-3xl -z-10 animate-blob animation-delay-2000"></div>

            <nav className="glass-panel sticky top-4 mx-4 z-50 px-6 py-4 flex justify-between items-center">
                <Link to="/" className="flex items-center gap-2 text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-secondary">
                    <Activity className="text-secondary" />
                    <span>LifeLink Class</span>
                </Link>

                <div className="hidden md:flex items-center gap-6">
                    <Link to="/" className="hover:text-primary transition-colors">Home</Link>
                    <Link to="/about" className="hover:text-primary transition-colors">About</Link>
                    <Link to="/services" className="hover:text-primary transition-colors">Services</Link>
                    {user ? (
                        <div className="flex items-center gap-4">
                            <span className="text-sm text-gray-400">Hi, {user.full_name}</span>
                            <Link to="/dashboard" className="px-4 py-2 bg-primary/20 text-primary rounded-lg hover:bg-primary/30 transition-all">
                                Dashboard
                            </Link>
                            <button onClick={handleLogout} className="p-2 hover:text-danger transition-colors">
                                <LogOut size={20} />
                            </button>
                        </div>
                    ) : (
                        <div className="flex items-center gap-4">
                            <Link to="/login" className="px-4 py-2 hover:bg-white/5 rounded-lg transition-colors">Login</Link>
                            <Link to="/register" className="px-4 py-2 bg-gradient-to-r from-primary to-accent rounded-lg font-semibold hover:shadow-lg transition-all">
                                Get Started
                            </Link>
                        </div>
                    )}
                </div>

                {/* Mobile Menu Toggle */}
                <button className="md:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
                    {isMenuOpen ? <X /> : <Menu />}
                </button>
            </nav>

            {/* Mobile Menu */}
            {isMenuOpen && (
                <div className="md:hidden absolute top-20 left-4 right-4 glass-panel p-6 flex flex-col gap-4 z-40">
                    <Link to="/" onClick={() => setIsMenuOpen(false)}>Home</Link>
                    {!user && (
                        <>
                            <Link to="/login" onClick={() => setIsMenuOpen(false)}>Login</Link>
                            <Link to="/register" onClick={() => setIsMenuOpen(false)}>Register</Link>
                        </>
                    )}
                    {user && (
                        <>
                            <Link to="/dashboard" onClick={() => setIsMenuOpen(false)}>Dashboard</Link>
                            <button onClick={handleLogout} className="text-left text-danger">Logout</button>
                        </>
                    )}
                </div>
            )}

            <main className="p-4 md:p-8 max-w-7xl mx-auto">
                {children}
            </main>
        </div>
    );
};

export default Layout;
