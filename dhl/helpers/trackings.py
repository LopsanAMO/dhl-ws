from .common import Element, build_request, date, element, etree


def tracking(site_id, password, awbnumber):
    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    root = Element('req:KnownTrackingRequest', {'xmlns:req': 'http://www.dhl.com'})  # NOQA
    root.append(build_request(site_id, password))
    root.append(element('LanguageCode', 'en'))
    root.append(element('AWBNumber', awbnumber))
    root.append(element('LevelOfDetails', 'ALL_CHECK_POINTS'))
    return '%s%s' % (xml, etree.tostring(root).decode('utf-8'))
