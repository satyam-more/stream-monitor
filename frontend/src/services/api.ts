// API service for backend communication
import axios from 'axios';
import type { TelemetryData, Sensor, SensorStatus, Stats } from '../types';

// Base URL for API - use environment variable or default to localhost
const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

// Get all telemetry data
export const getData = async (params?: {
  start?: string;
  end?: string;
  device_id?: string;
  limit?: number;
}): Promise<TelemetryData[]> => {
  try {
    const response = await api.get('/api/data', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    return [];
  }
};

// Get data for specific sensor
export const getSensorData = async (deviceId: string): Promise<TelemetryData[]> => {
  try {
    const response = await api.get(`/api/sensor/${deviceId}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching sensor data:', error);
    return [];
  }
};

// Get list of all sensors
export const getSensors = async (): Promise<Sensor[]> => {
  try {
    const response = await api.get('/api/sensors');
    return response.data;
  } catch (error) {
    console.error('Error fetching sensors:', error);
    return [];
  }
};

// Get sensor status (online/offline)
export const getSensorStatus = async (): Promise<SensorStatus[]> => {
  try {
    const response = await api.get('/api/sensors/status');
    return response.data;
  } catch (error) {
    console.error('Error fetching sensor status:', error);
    return [];
  }
};

// Get statistics
export const getStats = async (params?: {
  device_id?: string;
  start?: string;
  end?: string;
  type?: string;
}): Promise<Stats | null> => {
  try {
    const response = await api.get('/api/data/stats', { params });
    return response.data;
  } catch (error) {
    console.error('Error fetching stats:', error);
    return null;
  }
};

export default api;
