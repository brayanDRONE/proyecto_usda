/**
 * StageSamplingPanel - Panel para configurar muestreo por etapa
 * 
 * Permite ingresar cantidad de cajas por pallet con validaciones SAG-USDA
 * Muestra indicadores en tiempo real según CAP. 3.9.2.1
 */

import { useState, useEffect } from 'react';
import './StageSamplingPanel.css';

function StageSamplingPanel({ 
  totalPallets, 
  totalBoxesLot, 
  boxesPerPallet, 
  onBoxesPerPalletChange 
}) {
  const [isExpanded, setIsExpanded] = useState(true);
  const [localBoxes, setLocalBoxes] = useState([]);
  const [validations, setValidations] = useState({
    totalMatch: false,
    minPallets: false,
    variationCheck: false,
    sixtyPercentRule: false,
    warnings: []
  });

  useEffect(() => {
    // Inicializar array de cajas
    const initial = boxesPerPallet && boxesPerPallet.length === totalPallets 
      ? boxesPerPallet 
      : Array(totalPallets).fill('');
    setLocalBoxes(initial);
  }, [totalPallets, boxesPerPallet]);

  useEffect(() => {
    // Calcular validaciones en tiempo real
    calculateValidations();
  }, [localBoxes, totalBoxesLot, totalPallets]);

  const calculateValidations = () => {
    const boxes = localBoxes.map(b => parseInt(b) || 0).filter(b => b > 0);
    const totalEntered = boxes.reduce((sum, val) => sum + val, 0);
    
    // Validación 1: Total coincide con tamaño del lote
    const totalMatch = totalEntered === totalBoxesLot;
    
    // Validación 2: Mínimo 6 pallets
    const minPallets = totalPallets >= 6;
    
    // Validación 3: Variación para ≤15 pallets (30%)
    let variationCheck = true;
    let sixtyPercentRule = true;
    const warnings = [];
    
    if (boxes.length > 0 && boxes.length === totalPallets) {
      const average = totalEntered / totalPallets;
      const maxVariation = average * 0.30;
      
      if (totalPallets <= 15) {
        // Revisar que todos los pallets estén dentro del 30% de variación
        const outOfRange = boxes.filter(b => Math.abs(b - average) > maxVariation);
        variationCheck = outOfRange.length === 0;
        
        if (!variationCheck) {
          warnings.push(`${outOfRange.length} pallet(s) exceden la variación permitida del 30%`);
        }
      }
      
      // Validación 4: Regla del 60% para ≥10 pallets
      if (totalPallets >= 10) {
        const threshold = average * 0.60;
        const belowThreshold = boxes.filter(b => b < threshold);
        sixtyPercentRule = belowThreshold.length <= 1;
        
        if (!sixtyPercentRule) {
          warnings.push(`${belowThreshold.length} pallets están bajo el 60% del promedio (máx: 1)`);
        }
      }
    }
    
    // Advertencia si el total es diferente
    if (totalEntered > 0 && totalEntered !== totalBoxesLot) {
      if (totalEntered < totalBoxesLot) {
        warnings.push(`Faltan ${totalBoxesLot - totalEntered} cajas por ingresar`);
      } else {
        warnings.push(`Hay ${totalEntered - totalBoxesLot} cajas de más`);
      }
    }
    
    setValidations({
      totalMatch,
      minPallets,
      variationCheck,
      sixtyPercentRule,
      warnings
    });
  };

  const handleBoxChange = (index, value) => {
    const newBoxes = [...localBoxes];
    newBoxes[index] = value;
    setLocalBoxes(newBoxes);
    
    // Notificar al componente padre
    const numericBoxes = newBoxes.map(b => parseInt(b) || 0);
    onBoxesPerPalletChange(numericBoxes);
  };

  const getTotalEntered = () => {
    return localBoxes.reduce((sum, val) => sum + (parseInt(val) || 0), 0);
  };

  const allValidationsPass = () => {
    return validations.totalMatch && 
           validations.minPallets && 
           validations.variationCheck && 
           validations.sixtyPercentRule;
  };

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className={`stage-sampling-panel ${isExpanded ? 'expanded' : 'collapsed'}`}>
      <div className="panel-header" onClick={toggleExpand}>
        <h4>
          <svg 
            width="20" 
            height="20" 
            viewBox="0 0 20 20" 
            fill="currentColor"
            className={`chevron ${isExpanded ? 'expanded' : ''}`}
          >
            <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
          </svg>
          Configuración de Muestreo por Etapa
        </h4>
        <span className="panel-subtitle">
          Ingrese la cantidad de cajas en cada pallet
        </span>
      </div>

      {isExpanded && (
        <div className="panel-content">
          {/* Indicadores de validación */}
          <div className="validation-indicators">
            <div className={`indicator ${validations.minPallets ? 'pass' : 'fail'}`}>
              <span className="indicator-icon">{validations.minPallets ? '✓' : '✗'}</span>
              <span>Mínimo 6 pallets (Total: {totalPallets})</span>
            </div>
            
            {totalPallets <= 15 && (
              <div className={`indicator ${validations.variationCheck ? 'pass' : 'fail'}`}>
                <span className="indicator-icon">{validations.variationCheck ? '✓' : '✗'}</span>
                <span>Variación máxima 30% del promedio</span>
              </div>
            )}
            
            {totalPallets >= 10 && (
              <div className={`indicator ${validations.sixtyPercentRule ? 'pass' : 'fail'}`}>
                <span className="indicator-icon">{validations.sixtyPercentRule ? '✓' : '✗'}</span>
                <span>Regla 60%: Máx. 1 pallet bajo el umbral</span>
              </div>
            )}
            
            <div className={`indicator ${validations.totalMatch ? 'pass' : 'warn'}`}>
              <span className="indicator-icon">{validations.totalMatch ? '✓' : '⚠'}</span>
              <span>
                Total: <strong>{getTotalEntered()}</strong> / {totalBoxesLot} cajas
              </span>
            </div>
          </div>

          {/* Advertencias */}
          {validations.warnings.length > 0 && (
            <div className="warnings-container">
              {validations.warnings.map((warning, idx) => (
                <div key={idx} className="warning-message">
                  <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  {warning}
                </div>
              ))}
            </div>
          )}

          {/* Tabla de cajas por pallet */}
          <div className="boxes-table-container">
            <table className="boxes-table">
              <thead>
                <tr>
                  <th>Pallet</th>
                  <th>Cantidad de Cajas</th>
                </tr>
              </thead>
              <tbody>
                {Array.from({ length: totalPallets }, (_, index) => (
                  <tr key={index}>
                    <td className="pallet-number">Pallet {index + 1}</td>
                    <td>
                      <input
                        type="number"
                        min="1"
                        value={localBoxes[index] || ''}
                        onChange={(e) => handleBoxChange(index, e.target.value)}
                        placeholder="Cajas"
                        className="box-input"
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Resumen */}
          <div className="summary-box">
            <div className="summary-item">
              <span className="label">Total Pallets:</span>
              <span className="value">{totalPallets}</span>
            </div>
            <div className="summary-item">
              <span className="label">Cajas Ingresadas:</span>
              <span className={`value ${validations.totalMatch ? 'success' : 'warning'}`}>
                {getTotalEntered()}
              </span>
            </div>
            <div className="summary-item">
              <span className="label">Tamaño del Lote:</span>
              <span className="value">{totalBoxesLot}</span>
            </div>
            <div className="summary-item">
              <span className="label">Estado:</span>
              <span className={`value ${allValidationsPass() ? 'success' : 'error'}`}>
                {allValidationsPass() ? '✓ Válido' : '✗ Revisar validaciones'}
              </span>
            </div>
          </div>

          {/* Información adicional */}
          <div className="info-box">
            <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
            </svg>
            <span>
              Se seleccionará el <strong>25%</strong> de los pallets ({Math.max(1, Math.ceil(totalPallets * 0.25))}) 
              aleatoriamente para el muestreo según normativa SAG-USDA.
            </span>
          </div>
        </div>
      )}
    </div>
  );
}

export default StageSamplingPanel;
