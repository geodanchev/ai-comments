import xml.etree.ElementTree as ET


def parse_element(element):
    result = {}
    for child in element:
        # Store the tag name and its content when the child tag has no other children
        if len(child) == 0:
            result[child.tag] = child.text
        # Recursively parse the child element
        else:
            result[child.tag] = parse_element(child)
    return result

def xml_to_object(xmlString):
    xml_object = ET.fromstring(xmlString)
    result = []

    for xml_elem in xml_object:
        json_data = {"id": xml_elem.attrib["id"]}
        json_data.update(parse_element(xml_elem))
        result.append(json_data)
    
    return result;    
    