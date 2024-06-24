const express = require('express');
const { Server } = require('socket.io');
const { createServer } = require('http');
const cors = require('cors');


const app = express();
const server = createServer(app);

const io = new Server(server, {
  cors: {
    origin: "*",
    methods: ["GET", "POST"],
    credentials: true,
  },
});


app.get("/", (req, res) => {
  res.send("Hello World!");
});

io.on('connection', (socket) => {
  console.log('A user connected', socket.id);

  socket.on('join-room', (room) => {
    socket.join(room);
    console.log('user joind successfully', room)
    socket.to(room).emit('message', `User ${socket.id} has joined the room`);
  });

  socket.on('message', (data) => {
    const { message, room, sender } = data;
    console.log(data)
    io.to(room).emit('receive-message', {message,sender});
    
  });

  socket.on('disconnect', () => {
    console.log('A user disconnected', socket.id);
  });
});

server.listen(5000, () => {
  console.log('Listening on port 5000');
});
