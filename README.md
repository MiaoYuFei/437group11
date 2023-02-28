# 437group11 - Stocknews

## URL

[https://cse437s.yufeim.com/](https://cse437s.yufeim.com/)

## Backend

Flask, Firebase, Python

Python: v3+ required, v3.9 recommended, v3.10 and v3.11 are not supported.

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

## API

The backend provides following api to the frontend. All apis must be called using post method. 

### `/api/user/signin`:

Signs the user in with email and password.

Request:

- email: string

- password: string

Response:

- code: number, 200 if sign in successful, 403 if invalid credentials.

### `/api/user/register`:

Registers a new user with email and password.

Request:

- email: string

- password: string

Response:

- code: number, 200 if register successful, 403 if restricted by security policies.

### `/api/user/status`:

Gets the status of the user. Can be used to check if the session has signed in, get email address, check if the user has verified its email address, and get user id.

#### Request:

None. The backend will check the session.

#### Response:

- code: number, 200 if successful, 403 if not signed in.

- data: array

    - userid: string

    - email: string

    - emailVerified: boolean

### `/api/user/verifyemail`:

Sends verification email to the user.

#### Request:

None. The backend will check the session.

#### Response:

- code: number, 200 if email sent successfuly, 403 if email already verified or restricted by security policies.

### `/api/user/signout`:

Signs the user out.

#### Request:

None. The backend will check the session.

#### Response:

- code: number, will always be 200 which indicates successful.

Note: If api fails, i.e. not 200 code, it will have following structure:

- code: number, error code.

- data: array

    - reason: string, reason for the error, needs to be presented to the user on the UI.
