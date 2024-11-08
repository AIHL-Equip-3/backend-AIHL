import logging
import requests
from requests_oauthlib import OAuth2Session
from urllib.parse import urljoin

class IdCatMobilOAuth:
    def __init__(self, client_id, client_secret, site, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.site = site
        self.redirect_uri = redirect_uri
        self.authorization_base_url = urljoin(site, "/o/oauth2/auth")
        self.token_url = urljoin(site, "/o/oauth2/token")
        self.user_info_path = "/serveis-rest/getUserInfo"
        self.oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
        self.logger = logging.getLogger("idcat_mobil")
        logging.basicConfig(level=logging.DEBUG)

    def get_authorization_url(self):
        auth_url, state = self.oauth.authorization_url(
            self.authorization_base_url,
            scope="autenticacio_usuari",
            response_type="code",
            approval_prompt="auto",
            access_type="online"
        )
        self.logger.debug("Authorization URL: %s", auth_url)
        return auth_url, state

    def fetch_token(self, authorization_response):
        token = self.oauth.fetch_token(
            self.token_url,
            authorization_response=authorization_response,
            client_secret=self.client_secret
        )
        self.logger.debug("Access token obtained: %s", token)
        return token

    def get_user_info(self):
        user_info_url = urljoin(self.site, self.user_info_path)
        response = self.oauth.get(user_info_url)
        response.raise_for_status()
        raw_info = response.json()
        self.logger.debug("User info: %s", raw_info)
        return raw_info

    def logout(self, token):
        logout_url = urljoin(self.site, f"/o/oauth2/logout?token={token}")
        response = self.oauth.get(logout_url)
        response.raise_for_status()
        self.logger.debug("Logged out successfully from IdCat Mòbil")

# Sample usage
if __name__ == "__main__":
    client_id = "YOUR_CLIENT_ID"
    client_secret = "YOUR_CLIENT_SECRET"
    site = "https://identitats-pre.aoc.cat"
    redirect_uri = "https://your-redirect-uri.com/callback"

    idcat = IdCatMobilOAuth(client_id, client_secret, site, redirect_uri)
    auth_url, state = idcat.get_authorization_url()
    print("Visit this URL to authorize:", auth_url)

    # After visiting the URL and getting the authorization response
    authorization_response = input("Enter the full callback URL: ")
    token = idcat.fetch_token(authorization_response)
    user_info = idcat.get_user_info()
    print("User Info:", user_info)

    idcat.logout(token["access_token"])
