from datetime import datetime

from .common import Element, build_request, element, etree


def build_from_to(tag, zipcode, country='MX'):
    root = Element(tag)
    root.append(element('CountryCode', country))
    root.append(element('Postalcode', zipcode))
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
    root.append(element('Date', datetime.now().strftime('%Y-%m-%d')))
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
