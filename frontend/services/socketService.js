// src/services/socketService.js
import { io } from 'socket.io-client';
import store from '../store/store';
import { addMessage, setSocketId } from '../store/ChatSlice';

let socket;

export const connectSocket = () => {
  socket = io('http://localhost:5000');

  socket.on('connect', () => {
  
    store.dispatch(setSocketId(socket.id)); // Set socket ID in Redux
  });

  socket.on('receive-message', (data) => {
    store.dispatch(addMessage(data)); // Add received message to Redux
   
});

  return socket;
};

export const disconnectSocket = () => {
  if (socket) {
    socket.disconnect();
    console.log('Disconnected');
  }
};

export const joinRoom = (roomName) => {
  if (socket) {
    socket.emit('join-room', roomName);
    console.log('join',roomName)
  }
};

export const sendMessage = (message, room, sender) => {
  if (socket) {
    socket.emit('message', { message, room, sender });
    
  }
};
