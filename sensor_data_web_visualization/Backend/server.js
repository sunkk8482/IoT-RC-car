const express = require("express");
const app = express();
const port = 3000;
const cors = require("cors");
const pool = require("./db");

const http = require("http");
const server = http.createServer(app);
const { Server } = require("socket.io");

const io = new Server(server, {
  cors: {
    origin: true,
  },
  pingInterval: 100, //100 ms
  pingTimeout: 1,
});

app.use(
  cors({
    origin: true,
  })
);

io.on("connection", async (socket) => {
  const ret = await pool.query("select num1, num2, num3 from sensor limit 1");
  socket.emit("sensing data", ret[0][0]);
});

server.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
