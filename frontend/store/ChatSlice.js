// src/store/chatSlice.js
import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  messages: [],
  currentRoom: '',
  socketId: '',
  user: null,
};

const chatSlice = createSlice({
  name: 'chat',
  initialState,
  reducers: {
    addMessage: (state, action) => {
      const { message, sender } = action.payload;
      state.messages.push({ message, sender });
    
    },
    setCurrentRoom: (state, action) => {
      state.currentRoom = action.payload;
    },
    setSocketId: (state, action) => {
      state.socketId = action.payload;
    },
    setUser: (state, action) => {
      state.user = action.payload;
      console.log('from redux,', action.payload)
    },
    clearUser: (state) => {
      state.user = null;
    },
  },
});

export const { addMessage, setCurrentRoom, setSocketId, setUser,clearUser } = chatSlice.actions;

export default chatSlice.reducer;
