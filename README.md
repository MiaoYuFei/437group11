# 437group11 - Stocknews

## URL

[https://cse437s.yufeim.com/](https://cse437s.yufeim.com/)

## Backend

Flask, Firebase, Python

Python: v3+ required, v3.10 recommended.

- `cd backend`

- Install dependency packages: `pip3 install -r requirements.txt`. Needs to be run only if package dependencies changed.

- Run backend server: `python3 app.py`

## Frontend

Vite, Vue 3, TypeScript

Node.js: v16 or v18. v18 recommended.

- `cd frontend`

- Install dependency packages: `npm install`. Needs to be run only if package dependencies changed.

- Run a development server: `npm run dev`

- Go to [http://localhost:8080/](http://localhost:8080/) on local development machine. 127.0.0.1 is not allowed because Google reCAPTCHA requires a domain rather than IP address.

NOTICE: Please run `npm run lint` prior to each commit and resolve all issues if exist.

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

    - id: string

    - name: string

    - email: string

    - emailVerified: boolean

### `/api/user/verifyemail`:

Sends verification email to the user.

#### Request:

- requestType: "registration", sends verification email to the user to finish registration. "sign_in", sends email to user for signing in. "reset_password", sends email to user for resetting password.

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

### `/api/user/update_account_info`

Update the information associated with the account. Currently supported: name.

#### Request:

- displayName: string, shows as 'name' on profile page.

#### Response:

- code: number, 200 if update succeded, 403 if restricted by security policies.

### `/api/user/updatepreferences`

Update the user preferences, which are ten boolean values.

#### Request:

- algriculture: boolean.

- mining: boolean.

- construction: boolean.

- manufacuring: boolean.

- transportation: boolean.

- wholesale: boolean.

- retail: boolean.

- finance: boolean.

- services: boolean.

- public_administration: boolean.

#### Response:

- code: number, 200 if update succeded, 403 if restricted by security policies.

### `/api/user/getpreferences`

Get the user preferences, which are ten boolean values.

#### Request:

- None

#### Response:

- code: number, 200 if get operation successfuly, 403 if restricted by security policies.

- data:

  - algriculture: boolean.

  - mining: boolean.

  - construction: boolean.

  - manufacuring: boolean.

  - transportation: boolean.

  - wholesale: boolean.

  - retail: boolean.

  - finance: boolean.

  - services: boolean.

  - public_administration: boolean.

### `/api/user/updatepassword`

Update the password of the user.

#### Request:

- currentPassword: string, current / old password.

- newPassword: string, new password.

#### Response:

- code: number, 200 if update succeded, 403 if restricted by security policies.

## Calling API

`import { handleApi } from "@/utilities";`

`handleApi` is the function used to call api.

Input:

- method: string, "get" or "post"

- action: string, api url

- data: any | undefined, api data

### Case 1: Submit form data to api

i.e. sign in or register, which will submit email and password.

You need a `<form>` element in the html.

`import { getFormData } from "@/utilities";`

`getFormData` will retrieve the data specified from the form.

`const apiData = getFormData(this.$refs.form, ["email", "password"]);`

You need to apply `name="email"` and `name="password"` on the corresponding `<input>` element inside the `<form>` for `getFormData` to work.

`handleApi("post", "/api/user/signin", apiData)`

`this.$refs.form` refers to the form holds the data. Use `ref="form"` on the `<form>` element. Each form should have unique name.

### Case 2: Submit form data and additional data to api

i.e. when registering, also add recaptcha response to the data.

You need a `<form>` element in the html.

`const apiData = getFormData(this.$refs.form, ["email", "password"]);`

After you got the data from the form, also apply your additional data to apiData:

apiData["recaptch"] = "response";

then call the `handleApi` as normal.

`handleApi("post", "/api/user/register", apiData)`

### Case 3: No need to submit form data to api

i.e. sign out the user, refresh the user status.

You don't need a `<form>` element in the html.

Just call the `handleApi` with `{}`

`handleApi("post", "/api/user/status", {})`

### Get the response data

`handleApi` will return a `Promise`.

Please call `then` function on it.

`handleApi("method", "action", apiData).then(`

`  (response) => {`

`    if (parseInt(response.data.code) === 200) {`

`      // Api successful, you can acess response.data.data.`

`    } else {`

`      // Api failed. Please show the error.message to user.`

`    }`

`  },`

`  (error) => {`

`    // Error connecting to the api. Please show the error.message to the user.`

`  }`

`);`

Notice: Don't forget parseInt on code as the data from backend is all string. Don't forget response.data.data (two data).
