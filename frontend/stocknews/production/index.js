import path from "path";
import process from "node:process";
import express from "express";
import { fileURLToPath } from "url";

const application_path = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)) + "/../dist"
);
const application_port = process.env.PORT || 8080;
const app = express();

app.post("/api/*", (req, res) => {
  res.sendStatus(404);
});
app.use(express.static(application_path));
app.use((req, res) => {
  res.sendFile(application_path + "/index.html");
});

app.listen(application_port, (error) => {
  if (error) {
    console.log(error);
  }
});
