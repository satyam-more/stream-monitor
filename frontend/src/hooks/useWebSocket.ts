// Custom hook for WebSocket connection
import { useEffect, useState, useRef } from 'react';
import type { TelemetryData, Alert, SensorStatus } from '../types';

// WebSocket URL - use environment variable or default to localhost
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [latestData, setLatestData] = useState<TelemetryData | null>(null);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [sensorStatuses, setSensorStatuses] = useState<SensorStatus[]>([]);
  const [streamStopped, setStreamStopped] = useState(false);
  
  const ws = useRef<WebSocket | null>(null);
  const reconnectTimeout = useRef<number | undefined>(undefined);

  const connect = () => {
    try {
      console.log('Connecting to WebSocket...');
      ws.current = new WebSocket(WS_URL);

      ws.current.onopen = () => {
        console.log('✅ WebSocket connected');
        setIsConnected(true);
        setStreamStopped(false);
      };

      ws.current.onmessage = (event) => {
        try {
          const message = JSON.parse(event.data);
          console.log('📨 Received:', message);

          // Handle different event types
          if (message.event === 'new_data') {
            setLatestData(message.data);
            setStreamStopped(false);
          } else if (message.event === 'alert') {
            // Add alert and keep last 10
            setAlerts(prev => [message.data, ...prev].slice(0, 10));
          } else if (message.event === 'status_update') {
            setSensorStatuses(message.data);
          } else if (message.event === 'stream_stopped') {
            setStreamStopped(true);
          }
        } catch (error) {
          console.error('Error parsing message:', error);
        }
      };

      ws.current.onerror = (error) => {
        console.error('❌ WebSocket error:', error);
      };

      ws.current.onclose = () => {
        console.log('🔌 WebSocket disconnected');
        setIsConnected(false);
        
        // Auto-reconnect after 3 seconds
        reconnectTimeout.current = setTimeout(() => {
          console.log('🔄 Reconnecting...');
          connect();
        }, 3000);
      };
    } catch (error) {
      console.error('Error connecting to WebSocket:', error);
    }
  };

  useEffect(() => {
    connect();

    // Cleanup on unmount
    return () => {
      if (reconnectTimeout.current) {
        clearTimeout(reconnectTimeout.current);
      }
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return {
    isConnected,
    latestData,
    alerts,
    sensorStatuses,
    streamStopped,
  };
};
