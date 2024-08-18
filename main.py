import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
import tkinter as tk
from tkinter import ttk # for table view

@dataclass
class GasStation:
    name: str
    price: float
    addr: str  
    
def get_gas_prices(): # i want this to do the sams club price too, but have not got there yet
    headers = { # so we dont get flagged
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }  
    gasBudURL = "https://www.gasbuddy.com/home?search=78729&fuel=1&method=all&maxAge=0"
    # samsURl = "https://www.samsclub.com/local/fuel-center/austin-tx-sams-club/6188"

    gasBudResponse = requests.get(gasBudURL, headers=headers)
    # samResponse = requests.get(samsURl, headers=headers)

    if gasBudResponse.status_code == 200: # if we get anything from them
        stations = [] # list of gas station objects and what we are returning
        budSoup = BeautifulSoup(gasBudResponse.content, 'lxml')
        # all div elements with the specified class, each one is a station and its price
        panels = budSoup.find_all('div', class_='panel__panel___3Q2zW panel__white___19KTz colors__bgWhite___1stjL panel__bordered___1Xe-S panel__rounded___2etNE GenericStationListItem-module__station___1O4vF')
        
        for panel in panels:
            # get the station names, they are nested
            station_name_tag = panel.find('h3').find('a')
            station_name = station_name_tag.text.strip() if station_name_tag else "no name station"
            
            # get the address and replace <br> with ", "
            station_addr_tag = panel.find('div', class_='StationDisplay-module__address___2_c7v')
            if station_addr_tag:
                # get raw html, with the br
                station_addr_html = station_addr_tag.decode_contents()
                station_addr = station_addr_html.replace('<br/>', '').replace('Austin, TX', '').strip() # replace it cuz its ugly
            else:
                station_addr = "idk where its at"
            
            # get the price
            price_span = panel.find('span', class_='text__xl___2MXGo text__left___1iOw3 StationDisplayPrice-module__price___3rARL')
            
            if price_span:
                price_text = price_span.text.strip()
                
                if price_text != "- - -":  # these are stations without their prices listed
                    price = float(price_text.replace('$', ''))  # removing $ sign so we can convert to float
                    stations.append(GasStation(name=station_name, price=price, addr=station_addr)) # adds a new GasStation obejct to the list

    else:
        print(f"failed. code: {gasBudResponse.status_code}")
    return stations

lst = get_gas_prices()

root = tk.Tk()
root.title("Gas Prices")

tree = ttk.Treeview(root, columns=("Name", "Price", "Address"), show='headings')

tree.heading("Name", text="Name")
tree.heading("Price", text="Price")
tree.heading("Address", text="Address")
tree.column("Name", width=150)
tree.column("Price", width=100)
tree.column("Address", width=250)

tree.pack(expand=True, fill='both')

for i in lst:
    tree.insert("", tk.END, values=(i.name, i.price, i.addr)) # add them to the table

label = tk.Label(root)

root.mainloop()