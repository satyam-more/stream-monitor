// TypeScript types for the application

export interface TelemetryData {
  device_id: string;
  timestamp: string;
  type: 'temp' | 'vibration';
  value: number;
}

export interface Alert {
  device_id: string;
  timestamp: string;
  type: 'temp' | 'vibration';
  value: number;
  threshold: number;
  message: string;
}

export interface Sensor {
  device_id: string;
  last_seen: string;
}

export interface SensorStatus {
  device_id: string;
  status: 'online' | 'offline';
  last_seen: string;
}

export interface Stats {
  device_id: string;
  type: string;
  min: number;
  max: number;
  avg: number;
  count: number;
}

export interface WebSocketMessage {
  event: 'new_data' | 'alert' | 'stream_stopped' | 'status_update';
  data: any;
}
