// Stream Monitor Dashboard
import { useWebSocket } from './hooks/useWebSocket';
import { ConnectionStatus } from './components/ConnectionStatus';
import { LiveTable } from './components/LiveTable';
import { AlertsPanel } from './components/AlertsPanel';
import { SensorStatus } from './components/SensorStatus';
import './App.css';

function App() {
  const { isConnected, latestData, alerts, sensorStatuses, streamStopped } = useWebSocket();

  return (
    <div style={styles.app}>
      <header style={styles.header}>
        <h1 style={styles.title}>🚀 Stream Monitor Dashboard</h1>
        <p style={styles.subtitle}>Real-time IoT Telemetry Monitoring System</p>
      </header>

      <ConnectionStatus isConnected={isConnected} streamStopped={streamStopped} />

      <div style={styles.grid}>
        <div style={styles.leftColumn}>
          <LiveTable latestData={latestData} />
        </div>
        
        <div style={styles.rightColumn}>
          <AlertsPanel alerts={alerts} />
          <SensorStatus sensorStatuses={sensorStatuses} />
        </div>
      </div>

      <footer style={styles.footer}>
        <p>Backend: http://localhost:8000 | Frontend: http://localhost:5173</p>
      </footer>
    </div>
  );
}

const styles = {
  app: {
    minHeight: '100vh',
    backgroundColor: '#121212',
    padding: '20px',
  },
  header: {
    textAlign: 'center' as const,
    marginBottom: '30px',
    paddingBottom: '20px',
    borderBottom: '2px solid #333',
  },
  title: {
    color: '#4CAF50',
    fontSize: '36px',
    margin: '0 0 10px 0',
  },
  subtitle: {
    color: '#888',
    fontSize: '16px',
    margin: 0,
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr',
    gap: '20px',
    marginBottom: '20px',
  },
  leftColumn: {
    minWidth: 0,
  },
  rightColumn: {
    minWidth: 0,
  },
  footer: {
    textAlign: 'center' as const,
    color: '#666',
    fontSize: '12px',
    marginTop: '30px',
    paddingTop: '20px',
    borderTop: '1px solid #333',
  },
};

export default App;
