/**
 * DiagramasPalletView - Vista para mostrar diagramas de todos los pallets
 * 
 * Obtiene los datos de diagramas desde el backend y renderiza
 * un DiagramaPallet por cada pallet que debe mostrarse.
 */

import { useState, useEffect } from 'react';
import { jsPDF } from 'jspdf';
import DiagramaPallet from './DiagramaPallet';
import ConfiguracionDiagramaView from './ConfiguracionDiagramaView';
import './DiagramasPalletView.css';

function DiagramasPalletView({ inspection, onClose }) {
  const [diagramData, setDiagramData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [generatingPDF, setGeneratingPDF] = useState(false);
  const [requiresConfiguration, setRequiresConfiguration] = useState(false);

  useEffect(() => {
    fetchDiagramData();
  }, [inspection.id]);

  const fetchDiagramData = async () => {
    try {
      setLoading(true);
      setError(null);

      const token = localStorage.getItem('access_token');
      const response = await fetch(
        `http://localhost:8000/api/muestreo/diagrama-pallets/${inspection.id}/`,
        {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      );

      const data = await response.json();

      // Verificar primero si requiere configuración (antes de verificar response.ok)
      if (data.requires_configuration) {
        console.info('ℹ️ Configuración de pallets requerida - Mostrando modal de configuración');
        setRequiresConfiguration(true);
        setLoading(false);
        return;
      }

      if (!response.ok) {
        throw new Error(data.message || 'Error al obtener datos de diagrama');
      }

      if (!data.success) {
        throw new Error(data.message);
      }

      setDiagramData(data.data);
      setRequiresConfiguration(false);
    } catch (err) {
      console.error('Error fetching diagram data:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleConfigurationCompleted = () => {
    // Después de configurar, volver a cargar los datos del diagrama
    setRequiresConfiguration(false);
    fetchDiagramData();
  };

  const generatePDF = async () => {
    if (!diagramData) return;

    setGeneratingPDF(true);

    try {
      const doc = new jsPDF();
      const pageWidth = doc.internal.pageSize.width;
      const pageHeight = doc.internal.pageSize.height;
      
      const { inspection: inspData, pallets } = diagramData;

      // Procesar pallets de 2 en 2
      for (let i = 0; i < pallets.length; i += 2) {
        // Nueva página (excepto para los primeros 2 pallets)
        if (i > 0) {
          doc.addPage();
        }

        // Dibujar primer pallet (arriba)
        const palletTop = pallets[i];
        drawPalletOnPDF(doc, palletTop, inspData, pageWidth, 10, pageHeight / 2 - 20, true);

        // Dibujar segundo pallet (abajo) si existe
        if (i + 1 < pallets.length) {
          const palletBottom = pallets[i + 1];
          drawPalletOnPDF(doc, palletBottom, inspData, pageWidth, pageHeight / 2 + 5, pageHeight / 2 - 20, false);
        }
      }

      // Guardar PDF
      doc.save(`Diagramas_Pallets_${inspData.numero_lote}.pdf`);
    } catch (error) {
      console.error('Error generating PDF:', error);
      alert('Error al generar PDF: ' + error.message);
    } finally {
      setGeneratingPDF(false);
    }
  };

  const drawPalletOnPDF = (doc, pallet, inspData, pageWidth, startY, maxHeight, isFirst) => {
    const { base, altura, cantidad_cajas } = pallet;

    // Encabezado del pallet
    doc.setFontSize(12);
    doc.setFont('helvetica', 'bold');
    doc.text(`Pallet ${pallet.numero_pallet}`, pageWidth / 2, startY + 5, { align: 'center' });

    // Información compacta
    doc.setFontSize(8);
    doc.setFont('helvetica', 'normal');
    let yPos = startY + 12;
    
    if (isFirst) {
      doc.text(`Lote: ${inspData.numero_lote} | Especie: ${inspData.especie}`, 15, yPos);
      yPos += 5;
    }
    
    doc.text(`Cajas: ${pallet.inicio_caja} - ${pallet.fin_caja} | Muestra: ${pallet.total_cajas_muestra}`, 15, yPos);
    yPos += 8;

    // Calcular tamaño de celda para que quepa en el espacio disponible
    const availableHeight = maxHeight - (yPos - startY) - 20;
    const cellSize = Math.min(
      (pageWidth - 30) / base,
      availableHeight / altura,
      8  // Máximo 8mm por celda
    );

    const gridWidth = base * cellSize;
    const gridHeight = altura * cellSize;
    const startX = (pageWidth - gridWidth) / 2;

    // Dibujar cada caja (invertido: caja 1 abajo)
    pallet.cajas.forEach((caja) => {
      const rowFromTop = Math.ceil(caja.numero_local / base);
      const rowFromBottom = altura - rowFromTop + 1;
      const col = ((caja.numero_local - 1) % base);
      
      const x = startX + (col * cellSize);
      const y = yPos + (rowFromBottom - 1) * cellSize;

      // Color según si es muestra o no
      if (caja.seleccionada) {
        doc.setFillColor(59, 130, 246); // Azul para muestra
        doc.setTextColor(255, 255, 255); // Texto blanco
      } else {
        doc.setFillColor(255, 255, 255); // Blanco para normal
        doc.setTextColor(55, 65, 81); // Texto gris oscuro
      }

      // Dibujar celda
      doc.setDrawColor(209, 213, 219);
      doc.setLineWidth(0.3);
      doc.rect(x, y, cellSize, cellSize, 'FD');

      // Número de caja
      const fontSize = Math.min(cellSize * 0.5, 7);
      doc.setFontSize(fontSize);
      doc.setFont('helvetica', 'bold');
      doc.text(
        caja.numero.toString(),
        x + cellSize / 2,
        y + cellSize / 2 + fontSize / 3,
        { align: 'center' }
      );
    });

    // Leyenda compacta
    const legendY = yPos + gridHeight + 5;
    doc.setTextColor(0, 0, 0);
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(7);

    // Normal
    doc.setFillColor(255, 255, 255);
    doc.setDrawColor(209, 213, 219);
    doc.rect(15, legendY, 5, 5, 'FD');
    doc.text('Normal', 22, legendY + 4);

    // Muestra
    doc.setFillColor(59, 130, 246);
    doc.rect(45, legendY, 5, 5, 'FD');
    doc.text('Muestra', 52, legendY + 4);

    // Info adicional
    doc.setFontSize(6);
    doc.setTextColor(107, 114, 128);
    doc.text(
      `Base: ${base} | Capas: ${altura} | Total: ${cantidad_cajas}`,
      pageWidth / 2,
      legendY + 4,
      { align: 'center' }
    );
  };

  if (loading) {
    return (
      <div className="diagramas-overlay">
        <div className="diagramas-modal loading-modal">
          <div className="spinner-large"></div>
          <p>Cargando diagramas de pallets...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="diagramas-overlay">
        <div className="diagramas-modal error-modal">
          <div className="error-icon">⚠</div>
          <h2>Error al cargar diagramas</h2>
          <p>{error}</p>
          <button className="btn btn-secondary" onClick={onClose}>
            Cerrar
          </button>
        </div>
      </div>
    );
  }

  // Si requiere configuración, mostrar modal de configuración
  if (requiresConfiguration) {
    return (
      <ConfiguracionDiagramaView
        inspection={inspection}
        onClose={onClose}
        onConfigured={handleConfigurationCompleted}
      />
    );
  }

  if (!diagramData) return null;

  return (
    <div className="diagramas-overlay">
      <div className="diagramas-modal">
        {/* Header */}
        <div className="diagramas-header">
          <div>
            <h2>Diagramas de Pallets</h2>
            <p className="diagramas-subtitle">
              Lote: {diagramData.inspection.numero_lote} - {diagramData.inspection.especie}
            </p>
          </div>
          <button className="btn-close" onClick={onClose}>×</button>
        </div>

        {/* Info general */}
        <div className="diagramas-info">
          <div className="info-item">
            <span className="info-label">Pallets Mostrados:</span>
            <span className="info-value">{diagramData.total_pallets_mostrados}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Lote:</span>
            <span className="info-value">{diagramData.inspection.numero_lote}</span>
          </div>
          <div className="info-item">
            <span className="info-label">Especie:</span>
            <span className="info-value">{diagramData.inspection.especie}</span>
          </div>
        </div>

        {/* Botones de acción */}
        <div className="diagramas-actions">
          <button
            className="btn btn-success"
            onClick={generatePDF}
            disabled={generatingPDF}
          >
            {generatingPDF ? (
              <>
                <span className="spinner"></span>
                Generando PDF...
              </>
            ) : (
              <>
                📄 Descargar PDF
              </>
            )}
          </button>
        </div>

        {/* Lista de diagramas */}
        <div className="diagramas-content">
          {diagramData.pallets.map((pallet) => (
            <DiagramaPallet
              key={pallet.numero_pallet}
              palletData={pallet}
              basePallet={pallet.base}
              alturaPallet={pallet.altura}
            />
          ))}
        </div>

        {/* Footer */}
        <div className="diagramas-footer">
          <button className="btn btn-secondary" onClick={onClose}>
            Cerrar
          </button>
        </div>
      </div>
    </div>
  );
}

export default DiagramasPalletView;
