// Alerts panel component
import type { Alert } from '../types';

interface AlertsPanelProps {
  alerts: Alert[];
}

export const AlertsPanel = ({ alerts }: AlertsPanelProps) => {
  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>🚨 Alerts</h2>
      <div style={styles.alertsContainer}>
        {alerts.length === 0 ? (
          <div style={styles.noAlerts}>
            <p>✅ No alerts - All systems normal</p>
          </div>
        ) : (
          alerts.map((alert, index) => (
            <div key={index} style={styles.alert}>
              <div style={styles.alertHeader}>
                <span style={styles.alertIcon}>⚠️</span>
                <span style={styles.alertDevice}>{alert.device_id}</span>
                <span style={styles.alertTime}>{formatTimestamp(alert.timestamp)}</span>
              </div>
              <div style={styles.alertBody}>
                <p style={styles.alertMessage}>{alert.message}</p>
                <p style={styles.alertDetails}>
                  {alert.type === 'temp' ? '🌡️ Temperature' : '📳 Vibration'}: 
                  <span style={styles.alertValue}> {alert.value}</span>
                  {alert.type === 'temp' ? '°C' : 'g'}
                  {' '}(Threshold: {alert.threshold}{alert.type === 'temp' ? '°C' : 'g'})
                </p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: '#1e1e1e',
    borderRadius: '8px',
    padding: '20px',
    marginBottom: '20px',
  },
  title: {
    color: '#fff',
    marginBottom: '15px',
    fontSize: '20px',
  },
  alertsContainer: {
    maxHeight: '300px',
    overflowY: 'auto' as const,
  },
  noAlerts: {
    padding: '20px',
    textAlign: 'center' as const,
    color: '#4CAF50',
  },
  alert: {
    backgroundColor: '#2d1a1a',
    border: '2px solid #ff4444',
    borderRadius: '6px',
    padding: '12px',
    marginBottom: '10px',
    animation: 'fadeIn 0.3s ease-in',
  },
  alertHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '8px',
  },
  alertIcon: {
    fontSize: '20px',
  },
  alertDevice: {
    color: '#fff',
    fontWeight: 'bold' as const,
    flex: 1,
    marginLeft: '10px',
  },
  alertTime: {
    color: '#888',
    fontSize: '12px',
  },
  alertBody: {
    marginLeft: '30px',
  },
  alertMessage: {
    color: '#ff6666',
    margin: '5px 0',
    fontWeight: 'bold' as const,
  },
  alertDetails: {
    color: '#ddd',
    fontSize: '14px',
    margin: '5px 0',
  },
  alertValue: {
    color: '#ff4444',
    fontWeight: 'bold' as const,
  },
};
