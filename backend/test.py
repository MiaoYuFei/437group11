#!/usr/bin/env python3

import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyB8eOEHSXykFluDLDDeBe7wkyR55stIAAM",
  "authDomain": "stocknews-aa6b7.firebaseapp.com",
  "databaseURL": "https://stocknews-aa6b7.firebaseio.com",
  "projectId": "stocknews-aa6b7",
  "storageBucket": "stocknews-aa6b7.appspot.com",
  "messagingSenderId": "425418971970",
  "appId": "1:425418971970:web:565abf186779c1edf306db",
  "measurementId": "G-SYMFM414XJ"
}

fb = pyrebase.initialize_app(firebaseConfig)
auth = fb.auth()


email = "yufeim@yufeim.com"
password = "mypassword"
# user = auth.create_user_with_email_and_password(email, password)
# result = auth.send_email_verification(user["idToken"])
# print("---------------------------------------------------------------------------")
# print(user["idToken"])
# print(result)

user = auth.get_account_info("eyJhbGciOiJSUzI1NiIsImtpZCI6IjE1YzJiNDBhYTJmMzIyNzk4NjY2YTZiMzMyYWFhMDNhNjc3MzAxOWIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vc3RvY2tuZXdzLWFhNmI3IiwiYXVkIjoic3RvY2tuZXdzLWFhNmI3IiwiYXV0aF90aW1lIjoxNjc3NTY4MTI4LCJ1c2VyX2lkIjoiUnc4bm40Szc0MWVzTHFoYnBwUGc5T0kwWnI3MyIsInN1YiI6IlJ3OG5uNEs3NDFlc0xxaGJwcFBnOU9JMFpyNzMiLCJpYXQiOjE2Nzc1NjgxMjgsImV4cCI6MTY3NzU3MTcyOCwiZW1haWwiOiJ5dWZlaW1AeXVmZWltLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJlbWFpbCI6WyJ5dWZlaW1AeXVmZWltLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6InBhc3N3b3JkIn19.W0nWdAjdT883D6EqGPV5rWucOPhYK8VI2LpTE-ZqAB4OpsRctiXNgpM8FGyzBBHPfn_Bpp-X0LQcTyglp-AzB850ECaEubf3tjXFxJvRfwX2lB4mI0OBl_PSCvlw-me-27Crd3XuwIDgSbFKURrmtfVdAoe2kG9ci2HFc3SRub7Wdcaxs_Or_nGftb-mF3-H4-txoXB2ViitOIDOCyj9zyw1L_7HuX5wl1oOv1q6eAvqDDQMMo3CAMN2tVQXMSfzxHd6scTOEb4R2kcraQz1qeM97vrfuqezZa3mMfjoNgPWP3FntlTpLl02qlii4JNpHr-ygf0Q2wflSab6WJVJOw")
print(user)
