import requests
from bs4 import BeautifulSoup

def get_ipo_data():
    url = "https://merolagani.com/IPO.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    ipo_list = []
    for row in soup.select("table tr")[1:]:  # Skip table header
        cols = row.find_all("td")
        if cols:
            name = cols[0].text.strip()
            open_date = cols[3].text.strip()
            close_date = cols[4].text.strip()
            ipo_list.append((name, open_date, close_date))

    return ipo_list
