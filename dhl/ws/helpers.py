# -*- coding: utf-8 -*-
import xml.etree.ElementTree as etree
from datetime import datetime
from xml.etree.ElementTree import Element

date = datetime.now()


def element(tag, text):
    ele = Element(tag)
    ele.text = text
    return ele


def build_request(site_id, password):
    root = Element('Request')
    service_header = Element('ServiceHeader')
    root.append(service_header)
    service_header.append(element('MessageTime', date.strftime('%Y-%m-%dT%H:%M:%S-05:00')))  # NOQA
    service_header.append(element('MessageReference', '1234567890123456789012345678901'))  # NOQA
    service_header.append(element('SiteID', site_id))
    service_header.append(element('Password', password))
    return root


def build_from_to(tag, zipcode, country='MX'):
    root = Element(tag)
    root.append(element('CountryCode', country))
    root.append(element('Postalcode', zipcode))
    return root


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


def build_pieces_rate(items):
    root = Element('Pieces')
    for i, data in enumerate(items):
        piece = Element('Piece')
        root.append(piece)
        piece.append(element('PieceID', '%i' % (i + 1)))
        piece.append(element('Height', data['height']))
        piece.append(element('Depth', data['depth']))
        piece.append(element('Width', data['width']))
        piece.append(element('Weight', data['weight']))
    return root


def build_bkg_details(account_number, items):
    """
    hace falta date
    """
    root = Element('BkgDetails')
    root.append(element('PaymentCountryCode', 'MX'))
    root.append(element('Date', date.strftime('%Y-%m-%d')))
    root.append(element('ReadyTime', 'PT10H30M'))
    root.append(element('ReadyTimeGMTOffset', '+01:00'))
    root.append(element('DimensionUnit', 'CM'))
    root.append(element('WeightUnit', 'KG'))
    root.append(build_pieces_rate(items))
    root.append(element('PaymentAccountNumber', account_number))
    root.append(element('IsDutiable', 'N'))
    root.append(element('NetworkTypeCode', 'AL'))
    qtdshp = Element('QtdShp')
    root.append(qtdshp)
    qtdshp.append(element('GlobalProductCode', 'N'))
    qtdshp.append(element('LocalProductCode', 'N'))
    qtdshpexchrg = Element('QtdShpExChrg')
    qtdshp.append(qtdshpexchrg)
    qtdshpexchrg.append(element('SpecialServiceType', 'N'))  # Antes AA
    return root


def build_dutiable():
    root = Element('Dutiable')
    root.append(element('DeclaredCurrency', 'MXN'))
    root.append(element('DeclaredValue', '0'))
    return root


def get_quote(site_id, password, account_number, from_zipcode, to_zipcode, items):  # NOQA
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    root = Element('p:DCTRequest',
                   {'xmlns:p': 'http://www.dhl.com',
                    'xmlns:p1': 'http://www.dhl.com/datatypes',
                    'xmlns:p2': 'http://www.dhl.com/DCTRequestdatatypes',
                    'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                    'xsi:schemaLocation': 'http://www.dhl.com DCT-req.xsd'})
    get_quote = Element('GetQuote')
    root.append(get_quote)
    get_quote.append(build_request(site_id, password))
    get_quote.append(build_from_to('From', from_zipcode))
    get_quote.append(build_bkg_details(account_number, items))
    get_quote.append(build_from_to('To', to_zipcode))
    get_quote.append(build_dutiable())
    return '%s%s' % (xml, etree.tostring(root).decode('utf-8'))


def tracking(site_id, password, awbnumber):
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    root = Element('req:KnownTrackingRequest', {'xmlns:req': 'http://www.dhl.com'})  # NOQA
    root.append(build_request(site_id, password))
    root.append(element('LanguageCode', 'en'))
    root.append(element('AWBNumber', awbnumber))
    root.append(element('LevelOfDetails', 'ALL_CHECK_POINTS'))
    return '%s%s' % (xml, etree.tostring(root).decode('utf-8'))


def billing(account_number):
    root = Element('Billing')
    root.append(element('ShipperAccountNumber', account_number))
    root.append(element('ShippingPaymentType', 'T'))  # question to Sebastien
    root.append(element('BillingAccountNumber', account_number))
    # Solo aplica para envíos internacionales
    # root.append(element('DutyPaymentType', 'R'))
    # Si los impuestos los paga el shipper, indicar el numero de cuenta al
    # cual se hará el cargo.
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
    root.append(element('Date', date.strftime('%Y-%m-%d')))
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
    root.append(element('CompanyName', ''))
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
                    'xsi:schemaLocation': 'http://www.dhl.com ship-val-global-req.xsd',  # NOQA
                    'schemaVersion': '4.0'})
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
    return '%s%s' % (xml, etree.tostring(root).decode('utf-8'))
