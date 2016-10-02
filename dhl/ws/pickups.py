from .common import WSCommon
from ..helpers import pickup


class DHLPickup(WSCommon):

    def __init__(self, service_name, **kwargs):
        super(DHLPickup, self).__init__(service_name, **kwargs)

    def xml_request(self, data):
        data['site_id'] = self.site_id
        data['password'] = self.password
        data['account_number'] = self.account_number
        return pickup(data)

    def request(self):
        xml_request = self.xml_request(self.kwargs)
        res = self.requests.post(self.url, data=xml_request)
        res_dict = self.jxmlease.parse(res._content)
        return xml_request, res_dict
