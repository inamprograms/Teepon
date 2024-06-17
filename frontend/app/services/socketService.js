

import io from 'socket.io-client';

const SOCKET_SERVER_URL = 'http://localhost:5000'; // Replace with your server URL

let socket;

const connectSocket = () => {
  socket = io(SOCKET_SERVER_URL);

  socket.on('connect', () => {
    console.log('Connected to socket server');
  });

  socket.on('disconnect', () => {
    console.log('Disconnected from socket server');
  });

  return socket;
};

const disconnectSocket = () => {
  if (socket) socket.disconnect();
};

const sendMessage = (message) => {
  if (socket) {
    socket.emit('message', message);
  } else {
    console.error('Socket is not connected');
  }
};

const subscribeToMessages = (callback) => {
  if (socket) {
    socket.on('message', (message) => {
      callback(message);
    });
  } else {
    console.error('Socket is not connected');
  }
};

export { connectSocket, disconnectSocket, sendMessage, subscribeToMessages };
