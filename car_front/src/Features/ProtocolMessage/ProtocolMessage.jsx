import React, { useEffect, useState } from 'react';

function Toast({ message, onClose }) {
  useEffect(() => {
    const timer = setTimeout(() => onClose(), 5000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <div style={{
      position: 'fixed',
      bottom: 20,
      right: 20,
      backgroundColor: '#333',
      color: '#fff',
      padding: '10px 20px',
      borderRadius: 5,
      boxShadow: '0 0 10px rgba(0,0,0,0.5)'
    }}>
      {message}
    </div>
  );
}

function ReportNotifications() {
  const [toasts, setToasts] = useState([]);

  useEffect(() => {
    const ws = new WebSocket('ws://127.0.0.1:8000/ws/somepath/');

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setToasts((prev) => [...prev, data.message]);
    };

    ws.onclose = () => {
      console.log('WebSocket закрыт');
    };

    return () => ws.close();
  }, []);

  return (
    <>
      {toasts.map((msg, idx) => (
        <Toast
          key={idx}
          message={msg}
          onClose={() => setToasts((prev) => prev.filter((_, i) => i !== idx))}
        />
      ))}
    </>
  );
}
export default ReportNotifications
