import requests


class WSCommon(object):

    data = None
    message = None
    requests = requests

    def __init__(self, site_id, password, account_number, service_name, **kwargs):  # NOQA
        self.site_id = site_id
        self.password = password
        self.account_number = account_number
        self.service_name = service_name
