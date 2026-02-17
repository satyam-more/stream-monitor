// Connection status indicator
interface ConnectionStatusProps {
  isConnected: boolean;
  streamStopped: boolean;
}

export const ConnectionStatus = ({ isConnected, streamStopped }: ConnectionStatusProps) => {
  return (
    <div style={styles.container}>
      <div style={styles.statusBar}>
        <div style={styles.statusItem}>
          <span style={{
            ...styles.indicator,
            backgroundColor: isConnected ? '#4CAF50' : '#ff4444',
          }} />
          <span style={styles.label}>
            WebSocket: {isConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
        
        {isConnected && (
          <div style={styles.statusItem}>
            <span style={{
              ...styles.indicator,
              backgroundColor: streamStopped ? '#ff9800' : '#4CAF50',
            }} />
            <span style={styles.label}>
              Stream: {streamStopped ? 'Stopped' : 'Active'}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};

const styles = {
  container: {
    backgroundColor: '#1e1e1e',
    borderRadius: '8px',
    padding: '15px',
    marginBottom: '20px',
  },
  statusBar: {
    display: 'flex',
    gap: '30px',
    alignItems: 'center',
  },
  statusItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '10px',
  },
  indicator: {
    width: '12px',
    height: '12px',
    borderRadius: '50%',
    animation: 'pulse 2s infinite',
  },
  label: {
    color: '#ddd',
    fontSize: '14px',
  },
};
