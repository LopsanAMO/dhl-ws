import ws


class DHL:
    """
    Provee y centraliza la carga de los servicios DHL
    """
    services = ['GetQuote', 'GetCapability', 'Tracking', 'ShipmentValidation',
                'Pickup']

    def service(self, service_name, **kwargs):
        if service_name in self.services:
            class_name = 'DHL' + service_name
            service = getattr(ws, class_name)(service_name, **kwargs)
            return service.request()
        raise DHLError("The service {} does not exist".format(service_name))


class DHLError(Exception):

    def __init__(self, result):
        Exception.__init__(self, result)


# ITEMS = [{'id': '40', 'height': '1000', 'depth': '41', 'width': '31', 'weight': '1.0'},  # NOQA
#          {'id': '50', 'height': '1', 'depth': '41', 'width': '31', 'weight': '1.0'}]  # NOQA
# kwargs = {'from_zipcode': '22604', 'to_zipcode': '04310', 'items': ITEMS}
# result = DHL().service('GetQuote', **kwargs)
# print(result)
