// get the client
const mysql = require("mysql2/promise");

// Create the connection pool. The pool-specific settings are the defaults
const pool = mysql.createPool({
  host: "YOUR_HOST",
  user: "YOUR_USER",
  password: "YOUR_PASSWORD",
  database: "YOUR_DATABASE",
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0,
});

module.exports = pool;
