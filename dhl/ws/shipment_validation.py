from .common import WSCommon
from .helpers import shipping_guide


class DHLShipmentValidation(WSCommon):

    def __init__(self, service_name, **kwargs):
        super(DHLShipmentValidation, self).__init__(service_name, **kwargs)

    def xml_request(self, data):
        data['site_id'] = self.site_id
        data['password'] = self.password
        data['account_number'] = self.account_number
        # Needless validate 'kwargs'
        return shipping_guide(data)

    def request(self):
        response = self.requests.post(self.url,
                                      data=self.xml_request(self.kwargs))
        res_dict = self.jxmlease.parse(response._content)
        return res_dict
