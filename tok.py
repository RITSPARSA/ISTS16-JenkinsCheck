import requests
from config import Config
import logging

def getToken():
    """
    Gets an auth token for our white team account from the auth api
    :returns token: the auth token for white team account
    """
    data = dict()
    data['username'] = Config.API_USERNAME
    data['password'] = Config.API_PASSWORD
    url = Config.API_AUTH_URL
    endpoint = 'login'
    resp = apiRequest(url, endpoint, data=data)
    if 'token' not in resp:
        raise Exception('No token in AUTH_API response')
    
    Config.API_TOK = resp['token']
    logging.debug("Got API token")

def apiRequest(url, endpoint, data=None, method='POST'):
    """
    Makes a request to our api and returns the response
    :param endpoint: the api endpoint to hit
    :param data: the data to send in dictionary format
    :returns resp: the api response
    """
    url += "/" + endpoint
    cookies = {'token': Config.API_TOK}
    if method == 'POST':
        resp = requests.post(url, json=data, cookies=cookies)
    else:
        resp = requests.get(url, cookies=cookies)
    
    if resp.status_code == 400:
        msg = "Bad request sent to API"
        raise Exception(msg)
    if resp.status_code == 403:
        msg = resp.json()['error']
        raise Exception(msg)
    elif resp.status_code != 200:
        msg = "API returned {} for /{}".format(resp.status_code, endpoint)
        raise Exception(msg)
    resp_data = resp.json()
    return resp_data

