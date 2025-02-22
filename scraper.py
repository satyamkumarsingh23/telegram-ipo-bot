import requests
from bs4 import BeautifulSoup

def get_offering_data():
    url = "https://merolagani.com/IPO.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    offering_list = []
    
    for row in soup.select("table tr")[1:]:  # Skip table header
        cols = row.find_all("td")
        if len(cols) >= 5:  # Ensure the row has enough columns
            name = cols[0].text.strip()
            open_date = cols[3].text.strip()
            close_date = cols[4].text.strip()

            # Determine if it's an IPO or FPO based on the name
            offering_type = "FPO" if "FPO" in name.upper() else "IPO"

            offering_list.append((name, offering_type, open_date, close_date))

    return offering_list  # List of (Company Name, Offering Type, Open Date, Close Date)

# Test the function
if __name__ == "__main__":
    print(get_offering_data())  # Run this to verify IPOs & FPOs are detected correctly
