/**
 * ConfiguracionDiagramaView - Vista para configurar base y altura de cada pallet
 * 
 * Permite al usuario ingresar configuración individual para cada pallet
 * antes de generar los diagramas.
 */

import { useState, useEffect } from 'react';
import './ConfiguracionDiagramaView.css';

function ConfiguracionDiagramaView({ inspection, onConfigured, onClose }) {
  const [configurations, setConfigurations] = useState([]);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    initializeConfigurations();
  }, [inspection]);

  const initializeConfigurations = () => {
    // Determinar qué pallets configurar
    let palletsToConfig = [];
    
    if (inspection.tipo_muestreo === 'POR_ETAPA') {
      // Solo pallets seleccionados
      palletsToConfig = inspection.selected_pallets || [];
    } else {
      // Todos los pallets
      palletsToConfig = Array.from({ length: inspection.cantidad_pallets }, (_, i) => i + 1);
    }

    // Inicializar con valores vacíos o existentes
    const existingConfigs = inspection.pallet_configurations || [];
    const configMap = {};
    existingConfigs.forEach(c => {
      configMap[c.numero_pallet] = c;
    });

    // Obtener boxes_per_pallet para valores por defecto
    const boxesPerPallet = inspection.boxes_per_pallet || [];

    const configs = palletsToConfig.map(numPallet => {
      if (configMap[numPallet]) {
        return configMap[numPallet];
      }
      
      // Si existe boxes_per_pallet, usar ese valor como cantidad_cajas por defecto
      const cantidadCajasDefault = boxesPerPallet[numPallet - 1] || '';
      
      return {
        numero_pallet: numPallet,
        base: '',
        cantidad_cajas: cantidadCajasDefault
      };
    });

    setConfigurations(configs);
  };

  const handleConfigChange = (index, field, value) => {
    const newConfigs = [...configurations];
    newConfigs[index][field] = value;
    setConfigurations(newConfigs);
    setError(null);
  };

  const applyToAll = () => {
    const firstConfig = configurations[0];
    if (!firstConfig.base || !firstConfig.cantidad_cajas) {
      setError('Ingrese base y cantidad de cajas en el primer pallet para aplicar a todos');
      return;
    }

    const newConfigs = configurations.map(config => ({
      ...config,
      base: firstConfig.base,
      cantidad_cajas: firstConfig.cantidad_cajas
    }));

    setConfigurations(newConfigs);
  };

  const validateConfigurations = () => {
    for (const config of configurations) {
      if (!config.base || !config.cantidad_cajas) {
        return 'Debe ingresar base y cantidad de cajas para todos los pallets';
      }
      if (parseInt(config.base) < 1 || parseInt(config.cantidad_cajas) < 1) {
        return 'Base y cantidad de cajas deben ser mayores a 0';
      }
    }
    return null;
  };

  const handleSave = async () => {
    const validationError = validateConfigurations();
    if (validationError) {
      setError(validationError);
      return;
    }

    setSaving(true);
    setError(null);

    try {
      const token = localStorage.getItem('access_token');
      const payload = {
        configurations: configurations.map(c => ({
          numero_pallet: c.numero_pallet,
          base: parseInt(c.base),
          cantidad_cajas: parseInt(c.cantidad_cajas)
        }))
      };

      const response = await fetch(
        `http://localhost:8000/api/muestreo/configurar-pallets/${inspection.id}/`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(payload)
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.message || 'Error al guardar configuraciones');
      }

      if (!data.success) {
        throw new Error(data.message);
      }

      // Notificar éxito
      onConfigured();
    } catch (err) {
      console.error('Error saving configurations:', err);
      setError(err.message);
    } finally {
      setSaving(false);
    }
  };

  const getTotalCajas = () => {
    return configurations.reduce((sum, config) => {
      const cantidad = parseInt(config.cantidad_cajas) || 0;
      return sum + cantidad;
    }, 0);
  };

  return (
    <div className="configuracion-overlay">
      <div className="configuracion-modal">
        {/* Header */}
        <div className="configuracion-header">
          <div>
            <h2>Configuración de Diagramas de Pallets</h2>
            <p className="configuracion-subtitle">
              Ingrese base (cajas por capa) y cantidad total de cajas por pallet
            </p>
          </div>
          <button className="btn-close" onClick={onClose}>×</button>
        </div>

        {/* Info del lote */}
        <div className="configuracion-info">
          <div className="info-alert">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            <div>
              <strong>Lote: {inspection.numero_lote}</strong>
              <div>
                {inspection.tipo_muestreo === 'POR_ETAPA' 
                  ? `Configurando ${configurations.length} pallets seleccionados (de ${inspection.cantidad_pallets} totales)`
                  : `Configurando ${configurations.length} pallets`
                }
              </div>
              {inspection.boxes_per_pallet && inspection.boxes_per_pallet.length > 0 && (
                <div style={{ marginTop: '8px', fontSize: '0.9em', color: '#059669' }}>
                  ℹ️ Las cantidades de cajas están pre-cargadas según los valores ingresados en el formulario. 
                  Asegúrese de que coincidan para mantener consistencia con el muestreo.
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Botón aplicar a todos */}
        <div className="configuracion-actions-top">
          <button className="btn btn-secondary" onClick={applyToAll}>
            📋 Aplicar Primer Pallet a Todos
          </button>
          <div className="total-cajas-display">
            Total cajas: <strong>{getTotalCajas()}</strong>
          </div>
        </div>

        {/* Tabla de configuraciones */}
        <div className="configuracion-content">
          <div className="config-table-container">
            <table className="config-table">
              <thead>
                <tr>
                  <th>Pallet</th>
                  <th>Base (cajas por capa)</th>
                  <th>Cantidad de Cajas</th>
                  <th>Capas Calculadas</th>
                </tr>
              </thead>
              <tbody>
                {configurations.map((config, index) => {
                  const base = parseInt(config.base) || 0;
                  const cantidad = parseInt(config.cantidad_cajas) || 0;
                  const capas = base > 0 && cantidad > 0 ? Math.ceil(cantidad / base) : 0;
                  
                  return (
                    <tr key={config.numero_pallet}>
                      <td className="pallet-number-cell">
                        <span className="pallet-badge">Pallet {config.numero_pallet}</span>
                      </td>
                      <td>
                        <input
                          type="number"
                          min="1"
                          value={config.base}
                          onChange={(e) => handleConfigChange(index, 'base', e.target.value)}
                          placeholder="Ej: 8"
                          className="config-input"
                        />
                      </td>
                      <td>
                        <input
                          type="number"
                          min="1"
                          value={config.cantidad_cajas}
                          onChange={(e) => handleConfigChange(index, 'cantidad_cajas', e.target.value)}
                          placeholder="Ej: 28"
                          className="config-input"
                        />
                      </td>
                      <td className="total-cell">
                        <span className={`total-badge ${capas > 0 ? 'has-value' : ''}`}>
                          {capas || '-'}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Error */}
        {error && (
          <div className="configuracion-error">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            {error}
          </div>
        )}

        {/* Footer */}
        <div className="configuracion-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Cancelar
          </button>
          <button 
            className="btn btn-success" 
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? (
              <>
                <span className="spinner"></span>
                Guardando...
              </>
            ) : (
              <>
                ✓ Guardar y Ver Diagramas
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

export default ConfiguracionDiagramaView;
