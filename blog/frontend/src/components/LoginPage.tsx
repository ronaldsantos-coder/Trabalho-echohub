import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { useAuth } from '@/contexts/AuthContext';
import { Eye, EyeOff, Lock, User } from 'lucide-react';

export const LoginPage = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const { login, loading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (username.trim() && password.trim()) {
      await login(username, password);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-primary-gradient p-4 relative overflow-hidden">
      {/* Background decoration */}
      <div className="absolute inset-0 bg-accent-gradient opacity-30" />
      <div className="absolute top-20 left-20 w-96 h-96 bg-primary/10 rounded-full blur-3xl animate-pulse" />
      <div className="absolute bottom-20 right-20 w-80 h-80 bg-primary/5 rounded-full blur-3xl animate-pulse delay-1000" />
      
      <Card className="w-full max-w-md relative backdrop-blur-sm bg-card/95 border-border shadow-elegant">
        <CardHeader className="text-center space-y-4">
          <div className="mx-auto w-16 h-16 bg-primary-gradient rounded-2xl flex items-center justify-center shadow-soft">
            <Lock className="w-8 h-8 text-primary-foreground" />
          </div>
          <CardTitle className="text-3xl font-bold bg-primary-gradient bg-clip-text text-transparent">
            Blog CMS
          </CardTitle>
          <CardDescription className="text-muted-foreground">
            Sign in to manage your blog posts
          </CardDescription>
        </CardHeader>
        
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-2">
              <Label htmlFor="username" className="text-foreground font-medium">
                Username
              </Label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <Input
                  id="username"
                  type="text"
                  placeholder="Enter your username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="pl-12 h-12 border-border bg-background/50 backdrop-blur-sm transition-smooth focus:shadow-soft"
                  required
                />
              </div>
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password" className="text-foreground font-medium">
                Password
              </Label>
              <div className="relative">
                <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <Input
                  id="password"
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="pl-12 pr-12 h-12 border-border bg-background/50 backdrop-blur-sm transition-smooth focus:shadow-soft"
                  required
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-2 top-1/2 transform -translate-y-1/2 h-8 w-8 p-0 hover:bg-transparent"
                >
                  {showPassword ? (
                    <EyeOff className="w-4 h-4 text-muted-foreground" />
                  ) : (
                    <Eye className="w-4 h-4 text-muted-foreground" />
                  )}
                </Button>
              </div>
            </div>
            
            <Button
              type="submit"
              disabled={loading || !username.trim() || !password.trim()}
              className="w-full h-12 bg-primary-gradient hover:opacity-90 transition-smooth font-semibold text-lg shadow-elegant hover:shadow-soft"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
};