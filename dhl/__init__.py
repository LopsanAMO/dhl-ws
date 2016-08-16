import ws


class DHL:
    """
    Provee y centraliza la carga de los servicios DHL
    """
    services = ['GetQuote', 'GetCapability']

    def __init__(self, site_id, password, account_number):
        self.site_id = site_id
        self.password = password
        self.account_number = account_number

    def service(self, service_name, **kwargs):
        if service_name in self.services:
            class_name = 'DHL' + service_name
            service = getattr(ws, class_name)(self.site_id,
                                              self.password,
                                              self.account_number,
                                              service_name,
                                              **kwargs)
            return service.request()
        raise DHLError("The service {} does not exist".format(service_name))


class DHLError(Exception):

    def __init__(self, result):
        Exception.__init__(self, result)


ITEMS = [{'height': '1', 'depth': '41', 'width': '31', 'weight': '5.0'}]
dhl = DHL('DHLMexico', 'hUv5E3nMjQz6', '980055450')
data = {'from_zipcode': '22604', 'to_zipcode': '04310', 'items': ITEMS}
result = dhl.service('GetQuote', **data)
print(result)
