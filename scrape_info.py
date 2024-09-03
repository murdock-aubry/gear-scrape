import json
import os
from scrape import scrape_gears, get_dxf_file, scrape_gears2


while True:
        n1 = 0
        n2 = 100

        catalogs = {
        "Spur Gears": 2,
        "Helical Gears": 4,
        "Worm Gears": 5,
        "Bevel Gears": 6,
        "Internal Gear": 7,
        "Screw Gears": 8
        }



        file_path = "gears_data.json"
        with open(file_path, 'r') as file:
                data = json.load(file) 


        catalog_url = []
        catalog_nums = []
        ngears = len(data)


        original_catalog = [data[igear]["Catalog Number"] for igear in range(ngears)]

        file_path_new = "gears_data_extended.json"
        with open(file_path_new, 'r') as file:
                data_existing = json.load(file)

        nexisting = len(data_existing)


        existing_catalog =[data_existing[igear]["Catalog Number"] for igear in range(nexisting)]
        new_catalog = list(set(original_catalog) - set(existing_catalog))

        for igear in range(len(new_catalog)):
                cat_num = new_catalog[igear]
                catalog_nums.append(cat_num)

                for i in range(ngears):
                        if data[i]["Catalog Number"] == cat_num:
                                iurl = catalogs[data[i]["Type"]]

                url = "https://khkgears2.net/" + "catalog" + str(iurl) + "/" + cat_num
                catalog_url.append(url)
                

        new_data = scrape_gears2(catalog_url[n1:n2])

        data_existing += new_data


        with open(file_path_new, 'w') as json_file:
                json.dump(data_existing, json_file, indent=4)
