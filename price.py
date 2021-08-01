import base64
import os
import json
import requests
import simple_cache
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ID = "thereisfoodathome-135ad6fde1cadbc57b2fab4f6810457b793130090357053020"
secret = "pAmx3UH5NPhi3VGNSLv45KRbcE0olhzveSJD7Qph"
redirect = "https://green-double-5000.codio.io/"

API_URL = 'https://api.kroger.com/v1'

#url = "https://api.kroger.com/v1/connect/oauth2/authorize?scope=product.compact&response_type=code&client_id=thereisfoodathome-135ad6fde1cadbc57b2fab4f6810457b793130090357053020&redirect_uri=https://green-double-5000.codio.io/"


# client_id = os.environ[ID]
# client_secret = os.environ[secret]
# redirect_uri = os.environ[redirect]

encoded_client_token = base64.b64encode(f"{ID}:{secret}".encode('ascii')).decode('ascii')

customer_username = 'dpbolat19@earlham.edu'
customer_password = 'iLoveCod10'

param_map = {
    'brand': 'filter.brand',
    'chain': 'filter.chain',
    'fulfillment': 'filter.fulfillment',
    'limit': 'filter.limit',
    'location_id': 'filter.locationId',
    'product_id': 'filter.product_id',
    'term': 'filter.term',
    'within_miles': 'filter.radiusInMiles',
    'zipcode': 'filter.zipCode.near',
}
def get_customer_authorization_code(customer_username, customer_password):
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    driver = Chrome(options=chrome_options)

    url = AUTH_URL.format(client_id=client_id, redirect_uri=redirect_uri)

    # Go to the authorization url, enter username and password and submit
    driver.get(url)
    username = driver.find_element_by_id('username')
    username.send_keys(customer_username)
    password = driver.find_element_by_id('password')
    password.send_keys(customer_password)
    driver.find_element_by_id('signin_button').click()
    
    # The first time you authorize, or change the scope of the authorization, there is a 2nd page 
    # where we need to click an "Authorize button".  
    try:
        auth_button = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.ID, "authorize")))
        if auth_button:
            auth_button.click()
    except:
        pass
    
    uri = driver.current_url

    # After submitting, the authorization page redirects to your apps `uri` with a query parameter
    # `code`, which is the customer authorization code used to authentication the customer client.
    return uri.split("code=")[1]

def get_customer_access_token():
    customer_auth_code = get_customer_authorization_code(customer_username, customer_password)
    url = API_URL + '/connect/oauth2/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': f'Basic {encoded_client_token}',
    }
    payload = {
        'grant_type':"authorization_code",
        'code': customer_auth_code,
        'redirect_uri': redirect_uri,
    }
    response = requests.post(url, headers=headers, data=payload)
    return json.loads(response.text).get('access_token')

token = get_customer_access_token()

def _make_get_request(self, endpoint, params=None):
        url = API_URL + endpoint
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}',
        }

        response = requests.get(url, headers=headers, params=params)
        return json.loads(response.text)

def get_mapped_params(params):
    """ Maps a dictionary of parameters (ignore self) to the api's expected key value """
    return { param_map[key] : value for key, value in params.items() if key != 'self'}

def search_products(self, term=None, location_id=None, product_id=None, brand=None, fulfillment='csp', limit=5):
    params = get_mapped_params(locals())
    endpoint = '/products'

    results = self._make_get_request(endpoint, params=params)
    data = results.get('data')
    return [Product.from_json(product) for product in data]


def get_locations(self, zipcode, within_miles=10, limit=5, chain='Kroger'):
    params = get_mapped_params(locals())
    endpoint = '/locations'

    results = self._make_get_request(endpoint, params=params)
    data = results.get('data')
    return [Location.from_json(location) for location in data]

location = get_locations(47374)