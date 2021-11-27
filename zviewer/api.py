import re
import requests

class ZendeskServiceError(Exception):
    pass

class ZendeskService():
    """
    Class that handles interfacing with the Zendesk API (version 2).
    """
    def __init__(self, subdomain: str, username: str, password: str) -> None:
        self._connect(subdomain, username, password)

    def _subdomain(self, subdomain: str) -> None:
        # Full form url, e.g. 'https://zcctakemeasintern.zendesk.com/'
        if re.match(
            r'https?:\/\/[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}/?',
            subdomain
        ):
            self.subdomain = subdomain.rstrip('/')
        # Just the subdomain, e.g. 'zcctakemasintern'
        elif re.match(
            r'[-a-zA-Z0-9%_]{1,256}',
            subdomain
        ):
            self.subdomain = f'https://{subdomain}.zendesk.com'
        else:
            raise ZendeskServiceError('Subdomain provided does not fit the format required.')

    def _connect(self, subdomain: str, username: str, password: str) -> None:
        self._subdomain(subdomain)
        self.creds = (username, password)
        r = self._get('/users.json')
        if r.status_code != 200:
            raise ZendeskServiceError('Unknown error when testing credentials on endpoint.')
    
    def _get(self, endpoint: str):
        if endpoint.startswith("http://") or \
           endpoint.startswith("https://"):
            url = endpoint
        else:
            url = self._endpoint(endpoint)

        r = requests.get(url, auth=self.creds)
        if r.status_code == 200:
            return r
        elif r.status_code == 401:
            raise ZendeskServiceError('Authorization error, credentials may be invalid or unauthorized.')
        else:
            return r

    def _endpoint(self, endpoint: str) -> str:
        url = self.subdomain+'/api/v2/'+endpoint.lstrip('/')
        return url
    
    """
    List every single ticket in Zendesk workspace
    """
    def list_tickets(self) -> list:
        tickets = []
        endpoint = '/tickets'
        while endpoint:
            r = self._get(endpoint)
            if r.status_code != 200:
                raise ZendeskServiceError('Unhandled error when trying to list tickets.')
            data = r.json()
            tickets += data['tickets']
            endpoint = data['next_page']
        return tickets
    
    """
    Get ticket data for individual ticket
    """
    def get_ticket(self, id: int):
        r = self._get(f'/tickets/{id}.json')
        if r.status_code == 200:
            pass
        elif r.status_code == 404:
            return None
        else:
            raise ZendeskServiceError(f'Unhandled error when trying to get ticket #{id}')
        
        data = r.json()
        ticket_data = data['ticket']
        return ticket_data

    """
    Get ticket data for multiple tickets
    """
    def get_tickets(self, ticket_ids: list[int]):
        l = ','.join([str(i) for i in ticket_ids])
        r = self._get(f'/tickets/show_many.json?ids={l}')
        if r.status_code != 200:
            raise ZendeskServiceError('Unhandled error when trying to get multiple tickets')
        data = r.json()
        tickets_data = data['tickets']
        return tickets_data

    """
    Get url for Zendesk workspace in use.
    """
    def get_url(self) -> str:
        return self.subdomain