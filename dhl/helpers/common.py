import xml.etree.ElementTree as etree  # NOQA
from datetime import datetime
from xml.etree.ElementTree import Element


def build_request(site_id, password):
    root = Element('Request')
    service_header = Element('ServiceHeader')
    root.append(service_header)
    service_header.append(element('MessageTime', datetime.now().strftime('%Y-%m-%dT%H:%M:%S-05:00')))  # NOQA
    service_header.append(element('MessageReference', '1234567890123456789012345678901'))  # NOQA
    service_header.append(element('SiteID', site_id))
    service_header.append(element('Password', password))
    return root


def element(tag, text):
    ele = Element(tag)
    ele.text = text
    return ele
