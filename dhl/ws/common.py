import os
import xml.etree.ElementTree as ET
from xml import etree

import jxmlease
import requests


class WSCommon(object):

    ET = ET
    etree = etree
    jxmlease = jxmlease
    requests = requests
    url = 'http://xmlpi-ea.dhl.com/XMLShippingServlet'

    def __init__(self, service_name, **kwargs):  # NOQA
        self.account_number = os.getenv('DHL_ACCOUNT_NUMBER')
        self.kwargs = self.kwargs
        self.password = os.getenv('DHL_PASSWORD')
        self.service_name = service_name
        self.site_id = os.getenv('DHL_SITE_ID')
