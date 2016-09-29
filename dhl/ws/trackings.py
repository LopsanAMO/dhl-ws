from common import WSCommon
from ..helpers import tracking


class DHLTracking(WSCommon):

    def __init__(self, service_name, **kwargs):
        super(DHLTracking, self).__init__(service_name, **kwargs)

    def xml_request(self, **kwargs):
        awbnumber = kwargs.pop('awbnumber', None)
        if not awbnumber:
            return False
        return tracking(self.site_id, self.password, awbnumber)

    def request(self):
        response = self.requests.post(self.url, data=self.xml_request(**self.kwargs))  # NOQA
        res_dict = self.jxmlease.parse(response._content)
        return res_dict['req:TrackingResponse']['AWBInfo']['Status']
