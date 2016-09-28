from .common import WSCommon
from .helpers import shipping_guide


class DHLShipmentValidation(WSCommon):

    def __init__(self, service_name, **kwargs):
        super(DHLShipmentValidation, self).__init__(service_name, **kwargs)

    def xml_request(self, **kwargs):
        kwargs['site_id'] = self.site_id
        kwargs['password'] = self.password
        kwargs['account_number'] = self.account_number
        # Needless validate 'kwargs'
        return shipping_guide(kwargs)

    def request(self):
        response = self.requests.post(self.url,
                                      data=self.xml_request(**self.kwargs))
        res_dict = self.jxmlease.parse(response._content)
        return res_dict
