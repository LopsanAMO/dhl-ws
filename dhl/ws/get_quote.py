# import xml.etree.ElementTree as ET
# from xml import etree
import logging

import jxmlease

from .common import WSCommon
from .helpers import get_quote

FROM = '22604'
TO = '04310'


class DHLGetQuote(WSCommon):

    url = 'http://xmlpi-ea.dhl.com/XMLShippingServlet'

    def __init__(self, site_id, password, account_number, service_name, **kwargs):  # NOQA
        super(DHLGetQuote, self).__init__(site_id, password, account_number, service_name, **kwargs)  # NOQA
        self.kwargs = kwargs

    def xml_request(self, **kwargs):
        from_zipcode = kwargs.pop('from_zipcode', None)
        to_zipcode = kwargs.pop('to_zipcode', None)
        items = kwargs.pop('items', None)
        if not from_zipcode or not to_zipcode or not items:
            logging.warning('No se recibieron los parametros necesarios')
            return False
        return get_quote(self.site_id, self.password, self.account_number,
                         from_zipcode, to_zipcode, items)

    def request(self):
        response = self.requests.post(self.url, data=self.xml_request(**self.kwargs))  # NOQA
        res_dict = jxmlease.parse(response._content)
        if 'res:ErrorResponse' in res_dict:
            # Response > ServiceHeader > Status > Condition > ConditionData
            logging.error(
                '''Error in parsing request XML: The markup in the document
                 preceding the root element must be well-formed.''')
            return False
        elif 'res:DCTResponse' in res_dict:
            """
            The markup xml is ok
            """
            if 'Note' in res_dict['res:DCTResponse']['GetQuoteResponse']:
                # res:DCTResponse > GetQuoteResponse > Response > Note
                # > Condition > ConditionData
                print(res_dict['res:DCTResponse']['GetQuoteResponse'][
                      'Note']['Condition']['ConditionData'])
                return False
            print(res_dict['res:DCTResponse']['GetQuoteResponse']
                  ['BkgDetails']['QtdShp']['ShippingCharge'])
            return True

        # Print as xml
        # root = ET.fromstring(response._content)
        # print(etree.ElementTree.tostring(root).decode('utf-8'))
