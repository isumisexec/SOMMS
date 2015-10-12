__author__ = 'John'
import urllib.request
import urllib.parse
import re


def get_raw_html(net_id):
    """
    Retrieves the HTML for the given net id from the Iowa State directory

    :param net_id: the net id whose information is to be retrieved
    :return: the raw HTML from the search request
    """
    general_url = 'http://info.iastate.edu/individuals/search/'
    general_url += net_id+"@iastate.edu"
    req = urllib.request.Request(general_url)
    resp = urllib.request.urlopen(req)
    data = resp.read()
    return data


def parse_student_data(raw_html):
    """
    Takes raw HTML from the Iowa State info database request and parses out the
    classification, name and major using regular expressions.

    NOTE TO Developer:
    This function is <<EXTREMELY>> dependant on the current way that the Info.Iastate directory
    serves up data. If the HTML formatting changes there could be problems. Make sure to include this problem
    in the documentation.

    Returns the data in a dictionary object.
    :param raw_html: The raw markup retrieved from the HTTP request
    :return: A dictionary object with keys 'name', 'major', 'classification''
    """
    name = re.findall(r'<h1>.*?</h1>', str(raw_html))
    name = ''.join(name)
    name = name.replace('<h1>', '')
    name = name.replace('</h1>', '')
    name = name.strip()

    major = re.findall(r'Major:</span>.*?</div>', str(raw_html))
    major = ''.join(major)
    major = major.replace('Major:</span>', '')
    major = major.replace('</div>', '')
    major = major.strip()

    classification = re.findall(r'Classification:</span>.*?</div>', str(raw_html))
    classification = ''.join(classification)
    classification = classification.replace('Classification:</span>', '')
    classification = classification.replace('</div>', '')
    classification = classification.strip()

    if name and major and classification:
        return {'name': name,
                'classification': classification,
                'major': major}
    else:
        return None
