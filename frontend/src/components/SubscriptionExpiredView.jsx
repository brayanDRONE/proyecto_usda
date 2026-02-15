/**
 * SubscriptionExpiredView - Vista de suscripción expirada/inactiva
 */

import './SubscriptionExpiredView.css';

function SubscriptionExpiredView() {
  return (
    <div className="subscription-expired-container">
      <div className="card expired-card">
        <div className="expired-icon">
          <svg width="64" height="64" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </div>

        <h2 className="expired-title">Suscripción Vencida</h2>
        
        <p className="expired-message">
          El establecimiento seleccionado no tiene una suscripción activa.
        </p>

        <div className="expired-info">
          <p>Para continuar usando el sistema, es necesario renovar la suscripción mensual.</p>
        </div>

        <div className="contact-section">
          <h3>¿Cómo renovar?</h3>
          <ul>
            <li>Contacte al administrador del sistema</li>
            <li>Solicite la renovación de su licencia</li>
            <li>Una vez activada, podrá utilizar todas las funcionalidades</li>
          </ul>
        </div>

        <div className="support-info">
          <p className="support-label">¿Necesita ayuda?</p>
          <p className="support-text">
            Contacte al administrador para obtener más información sobre la renovación de su suscripción.
          </p>
        </div>
      </div>
    </div>
  );
}

export default SubscriptionExpiredView;
