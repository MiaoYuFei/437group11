# 437group11 - Stocknews

[![Node.js CI](https://github.com/MiaoYuFei/437group11/actions/workflows/node.js.yml/badge.svg)](https://github.com/MiaoYuFei/437group11/actions/workflows/node.js.yml)
[![Deploy to Amazon EC2](https://github.com/MiaoYuFei/437group11/actions/workflows/aws.yml/badge.svg)](https://github.com/MiaoYuFei/437group11/actions/workflows/aws.yml)

## URL

[https://cse437s.yufeim.com/](https://cse437s.yufeim.com/)

## Backend

Flask, Firebase, Python

Python: v3+ required, v3.10 recommended.

- `cd backend`

- Install dependency packages: `pip3 install -r requirements.txt`. Needs to be run only if package dependencies changed.

- Run backend server: `python3 app.py`

NOTICE: The local development server will monitor all changes to the project. You do not need to reload the server.

NOTICE: The entry point of backend is in file `/backend/app.py`. It includes all the implementation of apis.

## Database

This project uses MySQL 8.0 for database.

- database: stocknews

- username: stocknews

- password: Cse@437s

- tables:

  - ticker: all tickers information

  - news: all news information

  - news_tickers: relationship between news and tickers

### Database Installation

Refer to online resource. Be sure to use version 8.0+. Also install MySQL Workbench. MySQL Workbench is not required but may help you to go through the database.

Remember your root user password. You need to log in MySQL Workbench with root user not stocknews user.

### Database User

Run `database\user.sql` file to create the stocknews user. This user is used by the program not human.

### Database Data Import

Run `database\data.sql` to create tables and import data.

### Notice

If you created a new table, be sure to incldue introduction here.

To run an sql file:

In a terminal:

`mysql -u root -p < file.sql`

and then enter your root password (the password you set when installing the databse).

For MACOS user:

Your `mysql` command will be inside `/usr/local/mysql/bin/`. Use `/usr/local/mysql/bin/mysql` instead.

You need to start the MySQL manually after installation.

### How to access database in backend (python)

In `utilities.py` there is a function `get_sql_connection()`. It returns a mysql connection.

`sql_cnx = get_sql_connection()`

`sql_cursor = sql_cnx.cursor()`

`sql_query = "SELECT * FROM TABLE WHERE COLUMN1=%s AND COLUMN2=%s;"`

`sql_cursor.execute(sql_query, [value1, value2])`

`result_rows = sql_cursor.fetchall()`

\#result_rows is a list of values. If you want to get a dictionary with both column name and values:

`result_columns = [column[0] for column in sql_cursor.description]`

`result_dict = [dict(zip(result_columns, result_rows)) for result_row in result_rows]`

\#result_dict is the data fetched from the database.

`sql_cnx.commit()` \#Save your changes

`sql_cursor.close()` \#Close cursor

`sql_cnx.close()` \#Close connection

NOTICE: You must cleanup the resourses by calling close() on cursor and conenction. Otherwise you will run out of resources.

## Frontend

Vite, Vue 3, TypeScript

Node.js: v16 or v18. v18 recommended.

- `cd frontend`

- Install dependency packages: `npm install`. Needs to be run only if package dependencies changed.

- Run a development server: `npm run dev`

- Go to [http://localhost:8080/](http://localhost:8080/) on local development machine. 127.0.0.1 is not allowed because Google reCAPTCHA requires a domain rather than IP address.

NOTICE: The local development server will monitor all changes to the project. You do not need to reload the server. Usually your changes will take effect immediately after saving. If not, click refresh button on your browser.

NOTICE: Please run `npm run lint` prior to each commit and resolve all issues if exist.

## API

The backend provides following api to the frontend. All apis must be called using post method.

### `/api/user/signin`

Signs the user in with email and password.

Request:

- email: string

- password: string

Response:

- code: number, 200 if sign in successful, 403 if invalid credentials.

### `/api/user/register`

Registers a new user with email and password.

Request:

- email: string

- password: string

Response:

- code: number, 200 if register successful, 403 if restricted by security policies.

### `/api/user/status`

Gets the status of the user. Can be used to check if the session has signed in, get email address, check if the user has verified its email address, and get user id.

#### Request

None. The backend will check the session.

#### Response

- code: number, 200 if successful, 403 if not signed in.

- data: array

  - id: string

  - name: string

  - email: string

  - emailVerified: boolean

### `/api/user/verifyemail`

Sends verification email to the user.

#### Request

- requestType: "registration", sends verification email to the user to finish registration. "sign_in", sends email to user for signing in. "reset_password", sends email to user for resetting password.

#### Response

- code: number, 200 if email sent successfuly, 403 if email already verified or restricted by security policies.

### `/api/user/signout`

Signs the user out.

#### Request

None. The backend will check the session.

#### Response

- code: number, will always be 200 which indicates successful.

Note: If api fails, i.e. not 200 code, it will have following structure:

- code: number, error code.

- data: array

  - reason: string, reason for the error, needs to be presented to the user on the UI.

### `/api/user/updateaccountinfo`

Update the information associated with the account. Currently supported: name.

#### Request

- displayName: string, shows as 'name' on profile page.

#### Response

- code: number, 200 if update succeded, 403 if restricted by security policies.

### `/api/user/updatepreferences`

Update the user preferences, which are ten boolean values.

#### Request

- agriculture: boolean.

- mining: boolean.

- construction: boolean.

- manufacturing: boolean.

- transportation: boolean.

- wholesale: boolean.

- retail: boolean.

- finance: boolean.

- services: boolean.

- public_administration: boolean.

#### Response

- code: number, 200 if update succeded, 403 if restricted by security policies.

### `/api/user/getpreferences`

Get the user preferences, which are ten boolean values.

#### Request

- None

#### Response

- code: number, 200 if get operation successfuly, 403 if restricted by security policies.

- data:

  - agriculture: boolean.

  - mining: boolean.

  - construction: boolean.

  - manufacturing: boolean.

  - transportation: boolean.

  - wholesale: boolean.

  - retail: boolean.

  - finance: boolean.

  - services: boolean.

  - public_administration: boolean.

### `/api/user/updatepassword`

Update the password of the user.

#### Request

- currentPassword: string, current / old password.

- newPassword: string, new password.

#### Response

- code: number, 200 if update succeded, 403 if restricted by security policies.

### `/api/stock/getprice`

Get the stock price from polygon api.

#### Request

- ticker: the ticker requested

- start_date: start date. format: 2023-01-01

- end_date: end date. format: 2023-01-01

#### Response

- code: number, 200 if update succeded, 403 if restricted by security policies.

- data:

  - price: a list of price

    - open: float

    - close: float

    - low: float

    - hight: float

### `/api/stock/gettickerinfo`

Get details about a ticker.

#### Request

- ticker: the ticker requested

#### Response

- code: number, 200 if update succeded, 403 if restricted by security policies.

- data: Ticker format. Refer to utilities.ts ITicker for format.

### `/api/polygon/proxy`

The ticker image is from polygon api and requires our api key. For security reasons, polygon api key should not be sent to the user. Use this api to proxy resources.

NOTICE: This is a GET endpoint.

#### Request

- url: The requested url.

#### Response

The raw resource if successful.

### `/api/news/getnews`

Get news (latest, by ticker, by category, search, recommendation for user, and user's collection)

#### Request

- requestType: News source.

- page: number of page. Optional. Default 1.

#### Response

- code: number, 200 if update succeded, 403 if restricted by security policies.

- data:

  - newsList: list of news. Refer to utilities.ts INews for news format.

  - totalCount: total number of news. Only returned for first page.

### `/api/news/setnewsuseraction`

Set user's action for news: like/un-like, collect/un-collect

#### Request

- news_id: News id.

- liked: 1 if liked 0 otherwise.

- collected: 1 if liked 0 otherwise.

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

`(response) => {`

`if (parseInt(response.data.code) === 200) {`

`// Api successful, you can acess response.data.data.`

`} else {`

`// Api failed. Please show the error.message to user.`

`}`

`},`

`(error) => {`

`// Error connecting to the api. Please show the error.message to the user.`

`}`

`);`

Notice: Don't forget parseInt on code as the data from backend is all string. Don't forget response.data.data (two data).

## backend data update rules

1. when user like or dislike, use the user hash id, locate the user ticker pref dict in user_ticker_pref collection on firestore
 * now we have the user_ticker_pref_dict for that user, now we need to update it.
 * find what tickers are related to that new article: get industry_news_dict from recent_news collection
 * find news article by news_hash_id (doc_name) in the collection
 * then find tickers field in that news article
 * use ticker_hash collection (as ticker_hash_dict) to map ticker to ticker_hash_id
 * then use ticker_hash_id to update (+1 or -1) for that user's user ticker pref dict in user_ticker_pref collection on firestore.
 Note: we have [new_hash_id, user_hash_id], need to interact with [user_ticker_pref, recent_news, ticker_hash]

2. when user want news feed, locate user news ranking by:
 * go to preferences_scores_user_rank collection on firestore
 * locate doc by using user_hash_id as key
 * get all data in that doc
 * rank the dictionary with key=new_hash_id and value=score, rank from max score to min score.
 * get new artcile by news_hash_id from recent_news collection
 Note: we have [user_hash_id], need to interact with [preferences_scores_user_rank, recent_news]
