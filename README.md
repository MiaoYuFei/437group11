# 437group11 - Stocknews

## URL

[https://cse437s.yufeim.com/](https://cse437s.yufeim.com/)

## Backend

Flask, Firebase, Python

Python: v3+ required, v3.10 recommended, v3.11 not supported

- `cd backend`

- Install dependency packages: `pip install -r requirements.txt`. Needs to be run only if package dependencies changed.

- Run backend server: `python main.py`

## Frontend

Vite, Vue 3, TypeScript

Node.js: v16 and v18 work so far, v19 not supported

- `cd frontend/stocknews`

- Install dependency packages: `npm install`. Needs to be run only if package dependencies changed.

- Run a development server: `npm run dev`

- Run a production server: `npm run build`

- Go to [http://localhost:8080/](http://localhost:8080/) on local development machine. 127.0.0.1 is not allowed because Google reCAPTCHA requires a domain rather than IP address.
