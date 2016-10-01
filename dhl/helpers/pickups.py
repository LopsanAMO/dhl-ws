from .common import Element, build_request, element, etree


def pieces(data):
    root = Element('Pieces')
    root.append(element('Weight', data['weight']))
    root.append(element('Width', data['width']))
    root.append(element('Height', data['height']))
    root.append(element('Depth', data['depth']))
    return root


def shipment_details(data):
    root = Element('ShipmentDetails')
    root.append(element('AccountType', 'D'))
    root.append(element('AccountNumber', data['account_number']))
    root.append(element('BillToAccountNumber', data['account_number']))
    root.append(element('NumberOfPieces', data['pieces']['number']))
    root.append(element('Weight', data['pieces']['weight']))
    root.append(element('WeightUnit', 'K'))
    root.append(element('DoorTo', 'DD'))
    root.append(element('DimensionUnit', 'C'))
    root.append(pieces(data['pieces']))
    return root


def contact(data):
    root = Element('PickupContact')
    root.append(element('PersonName', data['person_name']))
    root.append(element('Phone', data['phone']))
    return root


def pickup_info(data):
    root = Element('Pickup')
    root.append(element('PickupDate', data['pickup_date']))
    root.append(element('PickupByTime', data['pickup_time']))
    root.append(element('CloseTime', data['pickup_close']))
    root.append(element('Pieces', data['pieces']))
    weight = Element('weight')
    weight.append(element('Weight', data['weight_total']))
    weight.append(element('WeightUnit', 'K'))
    root.append(weight)
    return root


def place(data):
    root = Element('Place')
    root.append(element('LocationType', 'R'))
    root.append(element('Address1', data['line_1']))
    root.append(element('Address2', data['line_2']))
    root.append(element('PackageLocation', data['pkg_location_info']))
    root.append(element('City', data['city']))
    root.append(element('DivisionName', data['division_name']))
    root.append(element('CountryCode', 'MX'))
    root.append(element('PostalCode', data['postal_code']))
    return root


def requestor(account_number):
    root = Element('Requestor')
    root.append(element('AccountType', 'D'))
    root.append(element('AccountNumber', account_number))
    return root


def pickup(data):
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    root = Element('req:BookPickupRequest',
                   {'xmlns:req': 'http://www.dhl.com',
                    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                    'xsi:schemaLocation': 'http://www.dhl.com book-pickup-req.xsd'})  # NOQA
    root.append(build_request(data['site_id'], data['password']))
    root.append(requestor(data['account_number']))
    root.append(place(data['place']))
    root.append(pickup_info(data['pickup_info']))
    root.append(contact(data['contact']))
    root.append(shipment_details(data['details']))
    return '%s%s' % (xml, etree.tostring(root).decode('utf-8'))
