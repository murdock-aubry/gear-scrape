from scrape import get_dxf_file
import json
import os 
import shutil 

dir_path = "/Users/murdockaubry/Library/Mobile Documents/com~apple~CloudDocs/Research/Personal Research/gear-gen/gear_dxf"

file_path = "gears_data.json"

with open(file_path, 'r') as file:
    data = json.load(file) 

ngears = len(data)

catalog_numbers = []
catalogs = {
    "Spur Gears": 2,
    "Helical Gears": 4,
    "Worm Gears": 5,
    "Bevel Gears": 6,
    "Internal Gear": 7,
    "Screw Gears": 8
}

catalog_url = []


# Get all Catalog numbers
for igear in range(ngears):
    try:
        cat_num = data[igear]["Catalog Number"]
    except Exception as e:
        # print(f"An error occurred: {e}")
        gear_type = 'Not Found'

    if not cat_num:
        cat_num = data[igear]["CatalogNumber"]

    
    url = "catalog" + str(catalogs[data[igear]["Type"]])


    if not os.path.isfile("gear_dxf/" + cat_num + ".dxf"):
        catalog_url.append(url)
        catalog_numbers.append(cat_num)


print(len(catalog_numbers))
quit()

get_dxf_file(catalog_numbers, catalog_url)



