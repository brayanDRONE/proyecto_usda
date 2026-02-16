/**
 * DiagramaPallet - Componente para visualizar un pallet con sus cajas
 * 
 * Muestra una grilla visual de un pallet con numeración correlativa
 * y resalta las cajas seleccionadas para muestreo.
 */

import { useState } from 'react';
import './DiagramaPallet.css';

function DiagramaPallet({ palletData, basePallet, alturaPallet }) {
  const [selectedBox, setSelectedBox] = useState(null);

  const handleBoxClick = (caja) => {
    setSelectedBox(selectedBox?.numero === caja.numero ? null : caja);
  };

  const handleCloseTooltip = () => {
    setSelectedBox(null);
  };

  return (
    <div className="diagrama-pallet-container">
      {/* Encabezado del pallet */}
      <div className="pallet-header">
        <h3>Pallet {palletData.numero_pallet}</h3>
        <div className="pallet-info">
          <span className="info-badge">
            Cajas: {palletData.inicio_caja} - {palletData.fin_caja}
          </span>
          <span className={`info-badge ${palletData.total_cajas_muestra > 0 ? 'badge-muestra' : 'badge-vacio'}`}>
            {palletData.total_cajas_muestra > 0 
              ? `${palletData.total_cajas_muestra} muestra${palletData.total_cajas_muestra > 1 ? 's' : ''}`
              : 'Sin muestras'}
          </span>
        </div>
      </div>

      {/* Grilla de cajas */}
      <div 
        className="pallet-grid"
        style={{ 
          gridTemplateColumns: `repeat(${basePallet}, 1fr)`,
          gridTemplateRows: `repeat(${alturaPallet}, 1fr)`
        }}
      >
        {palletData.cajas.map((caja) => {
          // Calcular row desde abajo (capa 1 en la parte inferior)
          const rowFromTop = caja.capa;
          const rowFromBottom = alturaPallet - rowFromTop + 1;
          const col = ((caja.numero_local - 1) % basePallet) + 1;
          
          return (
            <div
              key={caja.numero}
              className={`box-cell ${caja.seleccionada ? 'box-selected' : ''}`}
              onClick={() => handleBoxClick(caja)}
              title={`Caja ${caja.numero} - Capa ${caja.capa}`}
              style={{
                gridRow: rowFromBottom,
                gridColumn: col
              }}
            >
              <span className="box-number">{caja.numero}</span>
              {caja.seleccionada && (
                <span className="box-indicator">✓</span>
              )}
            </div>
          );
        })}
      </div>

      {/* Leyenda */}
      <div className="pallet-legend">
        <div className="legend-item">
          <div className="legend-box legend-box-normal"></div>
          <span>Normal</span>
        </div>
        <div className="legend-item">
          <div className="legend-box legend-box-muestra"></div>
          <span>Muestra</span>
        </div>
      </div>

      {/* Tooltip de información */}
      {selectedBox && (
        <div className="box-tooltip">
          <div className="tooltip-header">
            <h4>Información de Caja</h4>
            <button className="tooltip-close" onClick={handleCloseTooltip}>×</button>
          </div>
          <div className="tooltip-content">
            <div className="tooltip-row">
              <span className="tooltip-label">Número de Caja:</span>
              <span className="tooltip-value">{selectedBox.numero}</span>
            </div>
            <div className="tooltip-row">
              <span className="tooltip-label">Capa:</span>
              <span className="tooltip-value">{selectedBox.capa}</span>
            </div>
            <div className="tooltip-row">
              <span className="tooltip-label">Pallet:</span>
              <span className="tooltip-value">{palletData.numero_pallet}</span>
            </div>
            <div className="tooltip-row">
              <span className="tooltip-label">Estado:</span>
              <span className={`tooltip-value ${selectedBox.seleccionada ? 'status-muestra' : 'status-normal'}`}>
                {selectedBox.seleccionada ? 'MUESTRA' : 'NORMAL'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default DiagramaPallet;
