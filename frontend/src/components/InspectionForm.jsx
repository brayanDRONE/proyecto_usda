/**
 * InspectionForm - Formulario de captura de datos de inspección
 */

import { useState, useEffect } from 'react';
import { apiService } from '../services/api';
import './InspectionForm.css';

function InspectionForm({ onSamplingGenerated, onSubscriptionError }) {
  const [establishments, setEstablishments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const [formData, setFormData] = useState({
    exportador: '',
    establishment: '',
    inspector_sag: '',
    contraparte_sag: '',
    especie: '',
    numero_lote: '',
    tamano_lote: '',
    tipo_muestreo: 'NORMAL',
    tipo_despacho: '',
    cantidad_pallets: '',
  });

  const especies = [
    'Uva de Mesa',
    'Arándanos',
    'Cerezas',
    'Manzanas',
    'Peras',
    'Kiwis',
    'Ciruelas',
    'Duraznos',
    'Nectarines',
  ];

  const tiposDespacho = [
    'Inmediato',
    'Pendiente',
    'A Distancia',
  ];

  useEffect(() => {
    loadEstablishments();
  }, []);

  const loadEstablishments = async () => {
    try {
      const data = await apiService.getEstablishments();
      setEstablishments(data);
    } catch (err) {
      console.error('Error al cargar establecimientos:', err);
      setError('No se pudieron cargar los establecimientos');
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    setError(null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Validaciones básicas
    if (!formData.establishment) {
      setError('Debe seleccionar un establecimiento');
      return;
    }

    if (parseInt(formData.tamano_lote) <= 0) {
      setError('El tamaño del lote debe ser mayor a 0');
      return;
    }

    if (parseInt(formData.cantidad_pallets) <= 0) {
      setError('La cantidad de pallets debe ser mayor a 0');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const payload = {
        ...formData,
        establishment: parseInt(formData.establishment),
        tamano_lote: parseInt(formData.tamano_lote),
        cantidad_pallets: parseInt(formData.cantidad_pallets),
      };

      const response = await apiService.generateSampling(payload);

      if (response.success) {
        onSamplingGenerated(response.data);
      } else {
        setError(response.message || 'Error al generar el muestreo');
      }
    } catch (err) {
      console.error('Error:', err);
      
      // Verificar si es error de suscripción
      if (err.response?.status === 403 || err.response?.data?.error === 'SUBSCRIPTION_EXPIRED') {
        onSubscriptionError();
      } else {
        setError(
          err.response?.data?.message || 
          err.response?.data?.details ||
          'Error al generar el muestreo. Por favor intente nuevamente.'
        );
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card inspection-form-card">
      <div className="card-header">
        <h2>Nueva Inspección</h2>
        <p>Complete los datos de la inspección para generar el muestreo automático</p>
      </div>

      <form onSubmit={handleSubmit} className="inspection-form">
        {/* Información General */}
        <div className="form-section">
          <h3 className="section-title">Información General</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="exportador">Exportador *</label>
              <input
                type="text"
                id="exportador"
                name="exportador"
                value={formData.exportador}
                onChange={handleChange}
                required
                placeholder="Nombre del exportador"
              />
            </div>

            <div className="form-group">
              <label htmlFor="establishment">Planta/Establecimiento *</label>
              <select
                id="establishment"
                name="establishment"
                value={formData.establishment}
                onChange={handleChange}
                required
              >
                <option value="">Seleccione...</option>
                {establishments.map(est => (
                  <option key={est.id} value={est.id}>
                    {est.planta_fruticola}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="inspector_sag">Inspector SAG *</label>
              <input
                type="text"
                id="inspector_sag"
                name="inspector_sag"
                value={formData.inspector_sag}
                onChange={handleChange}
                required
                placeholder="Nombre del inspector"
              />
            </div>

            <div className="form-group">
              <label htmlFor="contraparte_sag">Contraparte SAG *</label>
              <input
                type="text"
                id="contraparte_sag"
                name="contraparte_sag"
                value={formData.contraparte_sag}
                onChange={handleChange}
                required
                placeholder="Nombre de la contraparte"
              />
            </div>
          </div>
        </div>

        {/* Detalles del Lote */}
        <div className="form-section">
          <h3 className="section-title">Detalles del Lote</h3>
          
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="especie">Especie *</label>
              <select
                id="especie"
                name="especie"
                value={formData.especie}
                onChange={handleChange}
                required
              >
                <option value="">Seleccione...</option>
                {especies.map(esp => (
                  <option key={esp} value={esp}>{esp}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="numero_lote">Número de Lote *</label>
              <input
                type="text"
                id="numero_lote"
                name="numero_lote"
                value={formData.numero_lote}
                onChange={handleChange}
                required
                placeholder="Ej: LOT-2026-001"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="tamano_lote">Tamaño del Lote (cajas) *</label>
              <input
                type="number"
                id="tamano_lote"
                name="tamano_lote"
                value={formData.tamano_lote}
                onChange={handleChange}
                required
                min="1"
                placeholder="Ej: 2332"
              />
            </div>

            <div className="form-group">
              <label htmlFor="cantidad_pallets">Cantidad de Pallets *</label>
              <input
                type="number"
                id="cantidad_pallets"
                name="cantidad_pallets"
                value={formData.cantidad_pallets}
                onChange={handleChange}
                required
                min="1"
                placeholder="Ej: 48"
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="tipo_muestreo">Tipo de Muestreo *</label>
              <select
                id="tipo_muestreo"
                name="tipo_muestreo"
                value={formData.tipo_muestreo}
                onChange={handleChange}
                required
              >
                <option value="NORMAL">Normal</option>
                <option value="POR_ETAPA">Por Etapa</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="tipo_despacho">Tipo de Despacho *</label>
              <select
                id="tipo_despacho"
                name="tipo_despacho"
                value={formData.tipo_despacho}
                onChange={handleChange}
                required
              >
                <option value="">Seleccione...</option>
                {tiposDespacho.map(tipo => (
                  <option key={tipo} value={tipo}>{tipo}</option>
                ))}
              </select>
            </div>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}

        <div className="form-actions">
          <button 
            type="submit" 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? (
              <>
                <span className="spinner"></span>
                Generando Muestreo...
              </>
            ) : (
              'Generar Muestreo'
            )}
          </button>
        </div>
      </form>
    </div>
  );
}

export default InspectionForm;
