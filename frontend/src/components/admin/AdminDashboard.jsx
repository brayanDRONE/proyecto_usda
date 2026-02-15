/**
 * AdminDashboard - Panel de control para superadministrador
 */

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import apiService from '../../services/api';
import './AdminDashboard.css';

function AdminDashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      setError(null);

      const statsData = await apiService.getAdminStats();
      setStats(statsData);
    } catch (err) {
      console.error('Error loading dashboard:', err);
      setError('Error al cargar los datos del dashboard');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner-large"></div>
        <p>Cargando dashboard...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard-error">
        <p>{error}</p>
        <button onClick={loadDashboardData} className="btn btn-primary">
          Reintentar
        </button>
      </div>
    );
  }

  return (
    <div className="admin-dashboard">
      {/* Header */}
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <h1>Panel de Administración</h1>
            <p>Sistema de Inspecciones SAG-USDA</p>
          </div>
          <div className="header-right">
            <div className="user-info">
              <div className="user-avatar">
                {user?.username?.[0]?.toUpperCase() || 'A'}
              </div>
              <div className="user-details">
                <span className="user-name">{user?.username}</span>
                <span className="user-role">Superadministrador</span>
              </div>
            </div>
            <button onClick={handleLogout} className="btn btn-secondary btn-sm">
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="dashboard-main">
        <div className="dashboard-container">
          {/* Quick Actions */}
          <div className="quick-actions">
            <button 
              onClick={() => navigate('/admin/establishments')}
              className="btn btn-primary"
            >
              Gestionar Establecimientos
            </button>
          </div>

          {/* Stats Cards */}
          <div className="stats-grid">
            <div className="stat-card stat-total">
              <div className="stat-icon">
                <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zM3 10a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1v-6zM14 9a1 1 0 00-1 1v6a1 1 0 001 1h2a1 1 0 001-1v-6a1 1 0 00-1-1h-2z" />
                </svg>
              </div>
              <div className="stat-content">
                <h3>Total Establecimientos</h3>
                <p className="stat-value">{stats?.total_establishments || 0}</p>
              </div>
            </div>

            <div className="stat-card stat-active">
              <div className="stat-icon">
                <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="stat-content">
                <h3>Activos</h3>
                <p className="stat-value">{stats?.active_establishments || 0}</p>
                <button 
                  onClick={() => navigate('/admin/establishments?filter=active')}
                  className="stat-link"
                >
                  Ver detalles →
                </button>
              </div>
            </div>

            <div className="stat-card stat-expiring">
              <div className="stat-icon">
                <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="stat-content">
                <h3>Por Vencer (7 días)</h3>
                <p className="stat-value">{stats?.expiring_establishments || 0}</p>
                <button 
                  onClick={() => navigate('/admin/establishments?filter=expiring_soon')}
                  className="stat-link"
                >
                  Ver detalles →
                </button>
              </div>
            </div>

            <div className="stat-card stat-expired">
              <div className="stat-icon">
                <svg width="24" height="24" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="stat-content">
                <h3>Expirados</h3>
                <p className="stat-value">{stats?.expired_establishments || 0}</p>
                <button 
                  onClick={() => navigate('/admin/establishments?filter=expired')}
                  className="stat-link"
                >
                  Ver detalles →
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

export default AdminDashboard;
