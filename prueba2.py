import requests
from requests_oauthlib import OAuth2Session

# Configuration
client_id = 'gencat.vass.cat'
client_secret = 'bc41139f-1546-4076-ba4b-00b0ef509ea1'
authorization_base_url = 'https://identitats-pre.aoc.cat/o/oauth2/auth'
token_url = 'https://identitats-pre.aoc.cat/o/oauth2/token'
user_info_url = 'https://identitats-pre.aoc.cat/serveis-rest/getUserInfo'
redirect_uri = 'https://identitats-pre.aoc.cat/users/auth/idcat_mobil/callback'  # Update to your redirect URI

# Step 1: Redirect user to the authorization URL
oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
authorization_url, state = oauth.authorization_url(authorization_base_url)

print(f'Please go to {authorization_url} and authorize access.')

# Step 2: After user authorization, get the authorization response
authorization_response = input('Enter the full callback URL: ')

# Step 3: Fetch the access token using the authorization response URL
token = oauth.fetch_token(
    token_url=token_url,
    authorization_response=authorization_response,
    client_id=client_id,
    client_secret=client_secret
)

# Step 4: Access user information
response = oauth.get(user_info_url)
user_info = response.json()

print("User information:")
print(user_info)
