import xml.etree.ElementTree as etree
from xml.etree.ElementTree import Element, ElementTree


def element(tag, text):
    ele = Element(tag)
    ele.text = text
    return ele


def build_request(date=None, site_id=None, password=None):
    root = Element('Request')
    service_header = Element('ServiceHeader')
    root.append(service_header)
    service_header.append(element('MessageTime', '2002-08-20T11:28:56.000-08:00'))  # NOQA
    service_header.append(element('MessageReference', '1234567890123456789012345678901'))  # NOQA
    service_header.append(element('SiteID', 'DHLMexico'))
    service_header.append(element('Password', 'hUv5E3nMjQz6'))
    return root


def build_from_to(tag, zipcode, country='MX'):
    root = Element(tag)
    root.append(element('CountryCode', country))
    root.append(element('Postalcode', zipcode))
    return root


def build_pieces(pieces):
    root = Element('Pieces')
    for i, data in enumerate(pieces):
        piece = Element('Piece')
        root.append(piece)
        piece.append(element('PieceID', '%i' % (i + 1)))
        piece.append(element('Height', data['height']))
        piece.append(element('Depth', data['depth']))
        piece.append(element('Width', data['width']))
        piece.append(element('Weight', data['weight']))
    return root


def build_bkg_details():
    """
    hace falta date
    """
    root = Element('BkgDetails')
    root.append(element('PaymentCountryCode', 'MX'))
    root.append(element('Date', '2016-08-12'))
    root.append(element('ReadyTime', 'PT10H21M'))
    root.append(element('ReadyTimeGMTOffset', '+01:00'))
    root.append(element('DimensionUnit', 'CM'))
    root.append(element('WeightUnit', 'KG'))
    root.append(build_pieces([{'height': '1', 'depth': '1', 'width': '1', 'weight': '5.0'}, {'height': '1', 'depth': '1', 'width': '1', 'weight': '6.0'}]))  # NOQA
    root.append(element('PaymentAccountNumber', '980055450'))
    root.append(element('IsDutiable', 'N'))
    root.append(element('NetworkTypeCode', 'AL'))
    qtdshp = Element('QtdShp')
    root.append(qtdshp)
    qtdshp.append(element('GlobalProductCode', 'N'))
    qtdshp.append(element('LocalProductCode', 'N'))
    qtdshpexchrg = Element('QtdShpExChrg')
    qtdshp.append(qtdshpexchrg)
    qtdshpexchrg.append(element('SpecialServiceType', 'AA'))
    return root


def build_dutiable():
    root = Element('Dutiable')
    root.append(element('DeclaredCurrency', 'MXN'))
    root.append(element('DeclaredValue', '0'))
    return root


def get_quote():
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    root = Element('p:DCTRequest',
               {'xmlns:p': 'http://www.dhl.com',
                'xmlns:p1': 'http://www.dhl.com/datatypes',
                'xmlns:p2': 'http://www.dhl.com/DCTRequestdatatypes',
                'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                'xsi:schemaLocation': 'http://www.dhl.com DCT-req.xsd'})
    get_quote = Element('GetQuote')
    root.append(get_quote)
    get_quote.append(build_request())
    get_quote.append(build_from_to('From', '22604'))
    get_quote.append(build_bkg_details())
    get_quote.append(build_from_to('To', '04310'))
    get_quote.append(build_dutiable())
    return '%s%s' % (xml, etree.tostring(root))
