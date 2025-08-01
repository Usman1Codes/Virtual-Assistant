import { Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import SettingsPage from './pages/SettingsPage';
import DashboardPage from './pages/DashboardPage';
import NotFoundPage from './pages/NotFoundPage';

export default function App() {
  return (
    <Routes>
      {/* The Homepage does not have the sidebar layout */}
      <Route path="/" element={<HomePage />} />

      {/* These routes are nested inside the Layout with the sidebar */}
      <Route element={<Layout />}>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/settings" element={<SettingsPage />} />
      </Route>
      
      {/* Catch-all route for 404 Not Found */}
      <Route path="*" element={<NotFoundPage />} />
    </Routes>
  );
}