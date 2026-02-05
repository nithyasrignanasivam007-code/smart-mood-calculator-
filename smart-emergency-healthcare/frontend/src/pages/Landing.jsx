import { Link } from 'react-router-dom';
import { Heart, Truck, Activity, Shield } from 'lucide-react';

const Landing = () => {
    return (
        <div className="flex flex-col items-center justify-center py-20 text-center">
            <div className="inline-block p-1 px-3 rounded-full bg-surface/50 border border-white/10 text-sm mb-6 text-primary">
                AI-Powered Emergency Response
            </div>
            <h1 className="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight">
                Seconds <span className="bg-clip-text text-transparent bg-gradient-to-r from-danger to-secondary">Save Lives</span>
            </h1>
            <p className="text-xl text-gray-400 max-w-2xl mb-10 leading-relaxed">
                The integrated intelligent coordination layer for Hospitals, Ambulances, and Blood Banks.
                Real-time tracking, AI readiness scoring, and instant connectivity.
            </p>

            <div className="flex flex-wrap gap-4 justify-center mb-20">
                <Link to="/register" className="btn-primary flex items-center gap-2">
                    <Activity size={20} /> Request Emergency Help
                </Link>
                <Link to="/register?role=hospital_admin" className="btn-secondary flex items-center gap-2">
                    Partner Hospital
                </Link>
            </div>

            {/* Features Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
                <FeatureCard
                    icon={<Truck className="text-primary w-8 h-8" />}
                    title="Smart Ambulance Routing"
                    desc="AI-optimized routes avoiding traffic with OSRM integration."
                />
                <FeatureCard
                    icon={<Heart className="text-danger w-8 h-8" />}
                    title="Blood Bank Coordination"
                    desc="Real-time blood tracking and automated shortage alerts."
                />
                <FeatureCard
                    icon={<Shield className="text-success w-8 h-8" />}
                    title="Hospital Readiness"
                    desc="Live ICU and ventilator availability tracking."
                />
            </div>
        </div>
    );
};

const FeatureCard = ({ icon, title, desc }) => (
    <div className="glass-panel p-8 text-left hover:scale-105 transition-transform duration-300">
        <div className="mb-4 bg-white/5 p-3 rounded-lg inline-block">{icon}</div>
        <h3 className="text-xl font-bold mb-2">{title}</h3>
        <p className="text-gray-400">{desc}</p>
    </div>
);

export default Landing;
