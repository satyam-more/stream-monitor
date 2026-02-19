// Live telemetry data table
import { useEffect, useState } from 'react';
import type { TelemetryData } from '../types';

interface LiveTableProps {
  latestData: TelemetryData | null;
}

export const LiveTable = ({ latestData }: LiveTableProps) => {
  const [dataList, setDataList] = useState<TelemetryData[]>([]);

  useEffect(() => {
    if (latestData) {
      // Add new data and keep last 50 entries
      setDataList(prev => [latestData, ...prev].slice(0, 50));
    }
  }, [latestData]);

  const formatTimestamp = (timestamp: string) => {
    return new Date(timestamp).toLocaleTimeString();
  };

  const getValueColor = (type: string, value: number) => {
    if (type === 'temp' && value > 50) return '#ff4444';
    if (type === 'vibration' && value > 0.08) return '#ff4444';
    return '#4CAF50';
  };

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>📊 Live Telemetry Data</h2>
      <div style={styles.tableContainer}>
        <table style={styles.table}>
          <thead>
            <tr style={styles.headerRow}>
              <th style={styles.th}>Device ID</th>
              <th style={styles.th}>Type</th>
              <th style={styles.th}>Value</th>
              <th style={styles.th}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {dataList.length === 0 ? (
              <tr>
                <td colSpan={4} style={styles.noData}>
                  Waiting for data...
                </td>
              </tr>
            ) : (
              dataList.map((data, index) => (
                <tr key={index} style={styles.row}>
                  <td style={styles.td}>{data.device_id}</td>
                  <td style={styles.td}>
                    {data.type === 'temp' ? '🌡️ Temperature' : '📳 Vibration'}
                  </td>
                  <td style={{
                    ...styles.td,
                    color: getValueColor(data.type, data.value),
                    fontWeight: 'bold'
                  }}>
                    {data.value} {data.type === 'temp' ? '°C' : 'g'}
                  </td>
                  <td style={styles.td}>{formatTimestamp(data.timestamp)}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
      <p style={styles.info}>Showing last {dataList.length} entries (max 50)</p>
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
  tableContainer: {
    overflowY: 'auto' as const,
    overflowX: 'auto' as const,
    maxHeight: '400px',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse' as const,
    minWidth: '500px',
  },
  headerRow: {
    backgroundColor: '#2d2d2d',
    position: 'sticky' as const,
    top: 0,
  },
  th: {
    padding: 'clamp(8px, 2vw, 12px)',
    textAlign: 'left' as const,
    color: '#4CAF50',
    borderBottom: '2px solid #4CAF50',
    fontSize: 'clamp(11px, 2vw, 14px)',
  },
  row: {
    borderBottom: '1px solid #333',
  },
  td: {
    padding: 'clamp(8px, 2vw, 12px)',
    color: '#ddd',
    fontSize: 'clamp(11px, 2vw, 14px)',
  },
  noData: {
    padding: '20px',
    textAlign: 'center' as const,
    color: '#888',
    fontSize: 'clamp(12px, 2.5vw, 14px)',
  },
  info: {
    color: '#888',
    fontSize: 'clamp(10px, 2vw, 12px)',
    marginTop: '10px',
  },
};
