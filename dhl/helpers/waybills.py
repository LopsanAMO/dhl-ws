from datetime import datetime

from .common import Element, build_request, element, etree


def build_pieces(items):
    root = Element('Pieces')
    for i, data in enumerate(items):
        piece = Element('Piece')
        root.append(piece)
        piece.append(element('PieceID', '%i' % (i + 1)))
        piece.append(element('Weight', data['weight']))
        piece.append(element('Width', data['width']))
        piece.append(element('Height', data['height']))
        piece.append(element('Depth', data['depth']))
    return root


def billing(account_number):
    root = Element('Billing')
    root.append(element('ShipperAccountNumber', account_number))
    root.append(element('ShippingPaymentType', 'T'))  # question to Sebastien
    root.append(element('BillingAccountNumber', account_number))
    # Solo aplica para envios internacionales
    # root.append(element('DutyPaymentType', 'R'))
    # Si los impuestos los paga el shipper, indicar el numero de cuenta al
    # cual se hara el cargo.
    # root.append(element('DutyAccountNumber', account_number))
    return root


def contact(data):
    root = Element('Contact')
    root.append(element('PersonName', data['personal_name']))
    root.append(element('PhoneNumber', data['phone_number']))
    # root.append(element('PhoneExtension', ' '))
    root.append(element('Email', data['email']))
    return root


def consignee(data):
    # Info del destinatario
    root = Element('Consignee')
    root.append(element('CompanyName', data['contact']['personal_name']))
    root.append(element('AddressLine', data['line_1']))
    root.append(element('AddressLine', data['line_2']))
    root.append(element('AddressLine', data['line_3']))
    root.append(element('City', data['city']))
    root.append(element('PostalCode', data['postal_code']))
    root.append(element('CountryCode', 'MX'))
    root.append(element('CountryName', 'MEXICO'))
    root.append(contact(data['contact']))
    return root


def shipment_details(data):
    root = Element('ShipmentDetails')
    root.append(element('NumberOfPieces', str(len(data['items']))))
    root.append(build_pieces(data['items']))
    # peso total de la suma de pesos de items
    root.append(element('Weight', data['total_weight']))
    root.append(element('WeightUnit', 'K'))
    root.append(element('GlobalProductCode', 'N'))
    root.append(element('LocalProductCode', 'N'))
    root.append(element('Date', datetime.now().strftime('%Y-%m-%d')))
    root.append(element('Contents', 'DOCUMENTO NACIONAL'))
    root.append(element('DoorTo', 'DD'))
    root.append(element('DimensionUnit', 'C'))
    # root.append(element('InsuredAmount', '1000'))  # Monto asegurado
    root.append(element('PackageType', 'EE'))
    root.append(element('IsDutiable', 'N'))
    root.append(element('CurrencyCode', 'MXN'))
    return root


def shipper(account_number, data):
    root = Element('Shipper')
    root.append(element('ShipperID', account_number))
    root.append(element('CompanyName', data['contact']['personal_name']))
    root.append(element('RegisteredAccount', account_number))
    root.append(element('AddressLine', data['line_1']))
    root.append(element('AddressLine', data['line_2']))
    root.append(element('AddressLine', data['line_3']))
    root.append(element('City', data['city']))
    root.append(element('PostalCode', data['postal_code']))
    root.append(element('CountryCode', 'MX'))
    root.append(element('CountryName', 'MEXICO'))
    root.append(contact(data['contact']))
    return root


def shipping_guide(data):
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    root = Element('req:ShipmentRequest',
                   {'xmlns:req': 'http://www.dhl.com',
                    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                    'xsi:schemaLocation': 'http://www.dhl.com ship-val-global-req.xsd'})  # NOQA
    root.append(build_request(data['site_id'], data['password']))
    root.append(element('RegionCode', 'AM'))
    root.append(element('RequestedPickupTime', 'N'))
    # root.append(element('NewShipper', 'N'))
    root.append(element('LanguageCode', 'en'))
    root.append(element('PiecesEnabled', 'Y'))
    root.append(billing(data['account_number']))
    root.append(consignee(data['consignee']))  # info destinatario
    root.append(shipment_details(data['shipment_details']))
    root.append(shipper(data['account_number'], data['shipper']))
    root.append(element('EProcShip', 'N'))
    root.append(element('LabelImageFormat', 'PDF'))
    prev = '%s%s' % (xml, etree.tostring(root).decode('utf-8'))
    return prev.replace('ship-val-global-req.xsd"', 'ship-val-global-req.xsd" schemaVersion="4.0"').replace('\\', '')   # NOQA
