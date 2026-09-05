import axios from 'axios';

const API = axios.create({ baseURL: 'http://localhost:8000/api' });

export const detectSpill = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return API.post('/detect', formData).then(res => res.data);
};

export const hindcast = (lat, lon, steps) => {
  return API.post('/drift', { lat, lon, steps }).then(res => res.data);
};

export const rankVessels = (incidentId, lat, lon, timeStart, timeEnd) => {
  return API.post('/rank', { incident_id: incidentId, origin_lat: lat, origin_lon: lon, time_start: timeStart, time_end: timeEnd }).then(res => res.data);
};

export const generateReport = (incidentId) => {
  return API.post('/report', { incident_id: incidentId }).then(res => res.data);
};