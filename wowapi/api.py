from datetime import datetime, timedelta
import requests
from .gamedata import GameData

class WowApi(GameData):    
    __base_url = '{0}.api.blizzard.com'

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

        self._session = requests.Session()
        self._access_tokens = {}

    def _utcnow(self):
        return datetime.utcnow()

    def _get_client_credentials(self, region):
        path = f'/oauth/token?grant_type=client_credentials&client_id={self.client_id}&client_secret={self.client_secret}'
        url = f'https://{region}.battle.net' + path
        if region == 'cn':
            url = 'https://www.battlenet.com.cn' + path
        
        now = self._utcnow()
        try:
            response = self._session.get(url)
        except:
            print(f'Could not reach {url}')

        if not response.ok:
            print(f'Response not okay: {response.status_code} for {url}')

        try:
            json = response.json()
        except:
            print(f'Invalid Json in OAuth response: {response.content} for {url}')

        token = json['access_token']
        expiration = now + timedelta(seconds=json['expires_in'])

        self._access_tokens[region] = {
            'token': token,
            'expiration': expiration
        }

    def _handle_request(self, url, **kwargs):
        try:
            response = self._session.get(url, **kwargs)
        except:
            print('Cannot handle request')

        if not response.ok:
            print(f'Invalid response - {response.status_code}')

        try:
            return response.json()
        except:
            print(f'Invalid Json: {response.content} for {url}')
    
    def get_resource(self, resource, region, *args, **filters):
        resource = resource.format(*args)

        # fetch access token for new region
        if region not in self._access_tokens:
            self._get_client_credentials(region)
        else:
            now = self._utcnow()
            # renew access token if expiring in 30 seconds or less
            if now >= self._access_tokens[region]['expiration'] - timedelta(seconds=30):
                self._get_client_credentials(region)
        
        filters['access_token'] = self._access_tokens[region]['token']
        url = self._format_base_url(resource, region)
        
        return self._handle_request(url, params=filters)