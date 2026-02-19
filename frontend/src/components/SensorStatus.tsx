// Sensor status component
import type { SensorStatus as SensorStatusType } from '../types';

interface SensorStatusProps {
  sensorStatuses: SensorStatusType[];
}

export const SensorStatus = ({ sensorStatuses }: SensorStatusProps) => {
  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleString();
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>📡 Sensor Status</h2>
      <div style={styles.sensorsContainer}>
        {sensorStatuses.length === 0 ? (
          <div style={styles.noSensors}>
            <p>No sensor data available</p>
          </div>
        ) : (
          sensorStatuses.map((sensor, index) => (
            <div key={index} style={styles.sensorCard}>
              <div style={styles.sensorHeader}>
                <span style={styles.sensorName}>{sensor.device_id}</span>
                <span style={{
                  ...styles.statusBadge,
                  backgroundColor: sensor.status === 'online' ? '#4CAF50' : '#ff4444',
                }}>
                  {sensor.status === 'online' ? '🟢 ONLINE' : '🔴 OFFLINE'}
                </span>
              </div>
              <div style={styles.sensorInfo}>
                <p style={styles.lastSeen}>
                  Last seen: {formatTimestamp(sensor.last_seen)}
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
    padding: 'clamp(10px, 3vw, 20px)',
    marginBottom: '20px',
  },
  title: {
    color: '#fff',
    marginBottom: '15px',
    fontSize: 'clamp(16px, 4vw, 20px)',
  },
  sensorsContainer: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
  },
  noSensors: {
    padding: '20px',
    textAlign: 'center' as const,
    color: '#888',
    fontSize: 'clamp(12px, 2.5vw, 14px)',
  },
  sensorCard: {
    backgroundColor: '#2d2d2d',
    borderRadius: '6px',
    padding: 'clamp(10px, 2vw, 15px)',
    border: '1px solid #444',
  },
  sensorHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '10px',
    flexWrap: 'wrap' as const,
    gap: '8px',
  },
  sensorName: {
    color: '#fff',
    fontWeight: 'bold' as const,
    fontSize: 'clamp(13px, 3vw, 16px)',
  },
  statusBadge: {
    padding: '4px 10px',
    borderRadius: '12px',
    fontSize: 'clamp(10px, 2vw, 12px)',
    fontWeight: 'bold' as const,
    color: '#fff',
    whiteSpace: 'nowrap' as const,
  },
  sensorInfo: {
    marginTop: '10px',
  },
  lastSeen: {
    color: '#888',
    fontSize: 'clamp(10px, 2vw, 12px)',
    margin: 0,
    wordBreak: 'break-word' as const,
  },
};
