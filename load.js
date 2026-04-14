import http from 'k6/http';

export let options = {
  stages: [
    { duration: '20s', target: 150 }, // normal
    { duration: '10s', target: 300 },
    { duration: '20s', target: 50 },
    { duration: '15s', target: 1000 }, // ramp up fast
    { duration: '15s', target: 1000 }, // 🔥 HOLD PEAK
    { duration: '20s', target: 200 },   // recovery
  ],
};

export default function () {
  http.get('http://localhost:4000/products');
}