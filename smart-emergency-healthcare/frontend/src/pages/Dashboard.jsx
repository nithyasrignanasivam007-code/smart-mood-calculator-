import { useAuth } from '../context/AuthContext';
import PatientDashboard from './dashboards/PatientDashboard';
import HospitalDashboard from './dashboards/HospitalDashboard';
import BloodBankDashboard from './dashboards/BloodBankDashboard';

const Dashboard = () => {
    const { user } = useAuth();

    if (!user) return <div className="text-center mt-20">Please login</div>;

    return (
        <div className="w-full">
            {user.role === 'patient' && <PatientDashboard />}
            {user.role === 'hospital_admin' && <HospitalDashboard />}
            {user.role === 'blood_bank_admin' && <BloodBankDashboard />}

            {!['patient', 'hospital_admin', 'blood_bank_admin'].includes(user.role) && (
                <div className="text-center mt-20 glass-panel p-10">
                    <h2 className="text-2xl">Dashboard for {user.role} coming soon.</h2>
                </div>
            )}
        </div>
    );
};

export default Dashboard;
