import { NavLink, Outlet } from 'react-router-dom';
import { Settings, LayoutDashboard, Bot } from 'lucide-react';
import { Toaster } from 'react-hot-toast';

const NavItem = ({ to, children, label }) => (
  <NavLink
    to={to}
    className={({ isActive }) =>
      `flex flex-col items-center justify-center p-4 rounded-lg transition-colors duration-200 ${
        isActive ? 'bg-primary/20 text-primary' : 'text-text-secondary hover:bg-surface'
      }`
    }
  >
    {children}
    <span className="text-xs mt-1">{label}</span>
  </NavLink>
);

export default function Layout() {
  return (
    <div className="flex h-screen bg-background">
      {/* Toaster for notifications */}
      <Toaster position="bottom-right" toastOptions={{
        style: {
          background: '#333',
          color: '#fff',
        },
      }} />

      {/* Sidebar */}
      <aside className="w-24 bg-surface/50 flex flex-col items-center p-4 space-y-6">
        <div className="text-primary p-2">
          <Bot size={32} />
        </div>
        <nav className="flex flex-col space-y-4">
          <NavItem to="/dashboard" label="Dashboard"><LayoutDashboard /></NavItem>
          <NavItem to="/settings" label="Settings"><Settings /></NavItem>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto p-8">
        <Outlet /> {/* Child pages will be rendered here */}
      </main>
    </div>
  );
}