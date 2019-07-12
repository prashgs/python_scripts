from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_html(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    print(content_type)
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def main():
    headers = []
    countries_html = get_html("https://www.geonames.org/countries/")
    html = bs(countries_html, 'html.parser')
    countries_table = html.find("table", {"id": "countries"})

    # Get Column header names, starting with Country(4th column)
    data = {header.text: [] for header in countries_table.findAll("th")[4:]}
    print("-------Headers-------")
    print(headers)
    # Get each row(tr), get all tds for each row
    for row in countries_table.findAll("tr")[1:]:
        for key, a in zip(data.keys(), row.find_all("td")[4:]):
            data[key].append(a.text)

    print("-------Extract-------")
    print(data)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("countries_data")
    print(df.head())

if __name__ == "__main__":
    main()
