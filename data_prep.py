import json 
import random 
import os 

remove = [ # what not to consider in the prompt.
            "Catalog Number",
            "Allowable Torque (Nm)",
            "Weight",
            "Precision Grade",
            "Heat Treatment",
            "Tooth Hardness",
            "DXF path",
            "Module",
            "info"
        ]

def prepare_data(file_path, frac_remove = 0.2):
    with open(file_path, 'r') as file:
        data = json.load(file)

    ngears = len(data)
    data_organized = []

    for igear in range(ngears):

        new_gear = {}

        keys = data[igear].keys() - remove
        keys = remove_and_random_resort(keys, frac_remove) # filter and sort

        context = "Generate a DXF file for a gear which conforms to the following description: "
        final = " Ensure that the output can be directly fed to CAD software."
        prompt = context
        for ikey, key in enumerate(keys):
            if ikey == len(keys) - 1:
                prompt += key + ": " + data[igear][key] + "."
            else:
                prompt += key + ": " + data[igear][key] + ", "

        prompt += final 
        new_gear["prompt"] = prompt
        

        file_path_dxf = data[igear]["DXF path"] + ".dxf"
        try: 
            dxf_text = read_dxf_file(file_path_dxf)
            new_gear["dxf_content"] = dxf_text
            data_organized.append(new_gear)
        except Exception:
            print("No DXF file for catalog ", data[igear]["Catalog Number"])

    return data_organized



def remove_and_random_resort(arr, removal_fraction=0.2):
    
    num_to_remove = int(len(arr) * removal_fraction)
    elements_to_remove = random.sample(range(len(arr)), num_to_remove)
    filtered_arr = [item for i, item in enumerate(arr) if i not in elements_to_remove]
    random.shuffle(filtered_arr)

    return filtered_arr

def get_test_data(file_path):

    test_data = []

    with open(file_path, 'r') as file:
        data = json.load(file)

    ngear = len(data)

    for igear in range(ngear):
        dxf_path = data[igear]["DXF path"] + ".dxf"

        if not os.path.isfile(dxf_path):
            test_data.append(data[igear])
    
    return test_data



def read_dxf_file(file_path):
    with open(file_path, 'r') as file:
        dxf_content = file.read()
    return dxf_content


if __name__ == "__main__":
    file_path = "gears_data_final.json"

    data_organized = prepare_data(file_path, 0.0)

    train_data_path = "train_data.json"

    with open(train_data_path, 'w') as json_file:
        json.dump(data_organized, json_file, indent=4)
