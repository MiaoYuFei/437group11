import fs from "fs";
import http from "http";
import path from "path";
import process from "process";
import { fileURLToPath } from "url";
import express from "express";

const application_path = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)) + "/../dist"
);
const app = express();

app.post("/api/*", (req, res) => {
  res.sendStatus(404);
});
app.use(express.static(application_path));
app.use((req, res) => {
  res.sendFile(application_path + "/index.html");
});

let listen_address;
if (process.env.SOCK != undefined) {
  listen_address = process.env.SOCK;
  if (fs.existsSync(listen_address)) {
    fs.unlinkSync(listen_address);
  }
} else {
  listen_address = process.env.PORT || 8080;
}

const server = http.createServer(app);

process.on("SIGINT", () => {
  server.close();
  if (fs.existsSync(listen_address)) {
    fs.unlinkSync(listen_address);
  }
  process.exit(0);
});

server.listen(listen_address, (error) => {
  if (error) {
    console.log(error);
  } else {
    console.log("Listening on " + listen_address);
  }
});
