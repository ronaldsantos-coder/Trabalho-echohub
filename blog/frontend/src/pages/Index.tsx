import { useAuth } from '@/contexts/AuthContext';
import { LoginPage } from '@/components/LoginPage';
import { Dashboard } from '@/components/Dashboard';

const Index = () => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-primary-gradient">
        <div className="text-center space-y-4">
          <div className="w-16 h-16 bg-primary-gradient rounded-2xl mx-auto animate-pulse" />
          <p className="text-primary-foreground font-medium">Loading...</p>
        </div>
      </div>
    );
  }

  return isAuthenticated ? <Dashboard /> : <LoginPage />;
};

export default Index;
