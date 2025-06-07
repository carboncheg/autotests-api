import httpx

login_payload = {
    "email": "user@example.com",
    "password": "string"
}

login_response = httpx.post("http://localhost:8000/api/v1/authentication/login", json=login_payload)
login_response_data = login_response.json()

get_user_me_headers = {
    "Authorization": f"Bearer {login_response_data["token"]["accessToken"]}"
}

get_user_me_response = httpx.get("http://localhost:8000/api/v1/users/me", headers=get_user_me_headers)
get_user_me_response_data = get_user_me_response.json()

print("Status Code:", get_user_me_response.status_code)
print("User Response:", get_user_me_response_data)
