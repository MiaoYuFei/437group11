import path from "path";
import { fileURLToPath } from "url";
import express from "express";

const application_path = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)) + "/../dist"
);
const app = express();

app.use(express.static(application_path));
app.post("/api/*", (req, res) => {
  res.sendStatus(404);
});
app.use((req, res) => {
  res.sendFile(application_path + "/index.html");
});

app.listen(8080, (error) => {
  if (error) {
    console.log(error);
  }
});
