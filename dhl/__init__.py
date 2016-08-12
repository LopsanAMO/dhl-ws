import requests
from .helpers import get_quote


def rate_request(from_zipcode, to_zipcode, items):
    """
    Para una cotizacion, necesitamos
    from_zipcode => seller
    to_zipcode ===> buyer
    [{height, depth, width, weight},]
    """
    xml_request = get_quote(from_zipcode, to_zipcode, items)
    url = 'http://xmlpi-ea.dhl.com/XMLShippingServlet'
    response = requests.post(url, data=xml_request)
    print response._content
