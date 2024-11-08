import unittest
from unittest.mock import patch, MagicMock
from idcat_movil import IdCatMobilOAuth

class TestIdCatMobilOAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client_id = "CLIENT_ID"
        cls.client_secret = "CLIENT_SECRET"
        cls.site = "https://identitats-pre.aoc.cat"
        cls.redirect_uri = "https://test.participa.gencat.cat/users/auth/idcat_mobil/callback"
        cls.idcat = IdCatMobilOAuth(cls.client_id, cls.client_secret, cls.site, cls.redirect_uri)

    def test_authorization_url(self):
        auth_url, state = self.idcat.get_authorization_url()
        self.assertIn("autenticacio_usuari", auth_url)
        self.assertIn("response_type=code", auth_url)

    @patch("idcat_movil.OAuth2Session.fetch_token")
    def test_fetch_token(self, mock_fetch_token):
        mock_fetch_token.return_value = {"access_token": "mock_token"}
        token = self.idcat.fetch_token("mock_authorization_response")
        self.assertEqual(token["access_token"], "mock_token")

    @patch("idcat_movil.OAuth2Session.get")
    def test_get_user_info(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "identifier": "123456789",
            "email": "email@example.net",
            "name": "Oriol",
            "prefix": "972",
            "phone": "505152",
            "surname1": "Junquerol",
            "surname2": "Balaguer",
            "surnames": "Junquerol Balaguer",
            "countryCode": "CAT",
            "identifierType": "1",
            "method": "idcatmobil",
            "assuranceLevel": "low",
            "status": "ok"
        }
        mock_get.return_value = mock_response

        user_info = self.idcat.get_user_info()
        self.assertEqual(user_info["identifier"], "123456789")
        self.assertEqual(user_info["email"], "email@example.net")

    @patch("idcat_movil.OAuth2Session.get")
    def test_logout(self, mock_get):
        mock_response = MagicMock()
        mock_get.return_value = mock_response
        token = "mock_token"
        self.idcat.logout(token)
        mock_get.assert_called_with(f"https://identitats-pre.aoc.cat/o/oauth2/logout?token={token}")

if __name__ == "__main__":
    unittest.main()
