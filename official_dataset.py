from datasets import Dataset, DatasetDict
import json
import os 

# Load your raw JSON file
with open("train_data_split_prompted.json", "r") as f:
    data = json.load(f)

# Prepare lists for each split
train_data = []
val_data = []
test_data = []

# Iterate through each gear type and its splits (train, val, test)
for gear_type, splits in data.items():
    for split, entries in splits.items():
        for entry in entries:
            # Flatten the structure and add a split key
            entry["gear_type"] = gear_type
            entry["split"] = split
            
            # Append the data to the correct split list
            if split == "train":
                train_data.append(entry)
            elif split == "val":
                val_data.append(entry)
            elif split == "test":
                test_data.append(entry)

# Create dataset info dictionary
dataset_info = {
    "citation": "",
    "description": "",
    "features": {
        "gear_type": {"dtype": "string", "_type": "Value"},
        "split": {"dtype": "string", "_type": "Value"},
        "prompt": {"dtype": "string", "_type": "Value"},
        # "prompt": {k: {"dtype": "string", "_type": "Value"} for k in train_data[0]["prompt"].keys()},
        "dxf_content": {"dtype": "string", "_type": "Value"}
    }
}

# Save dataset info
for split in ["train", "val", "test"]:
    split_dir = f"unprompted/{split}"
    os.makedirs(split_dir, exist_ok=True)
    
    with open(f"{split_dir}/dataset_info.json", "w") as f:
        json.dump(dataset_info, f, indent=2)

# Create and save datasets
dataset = DatasetDict({
    "train": Dataset.from_dict({
        "gear_type": [entry["gear_type"] for entry in train_data],
        "split": [entry["split"] for entry in train_data],
        "prompt": [entry["prompt"] for entry in train_data],
        "dxf_content": [entry["dxf_content"] for entry in train_data],
    }),
    "val": Dataset.from_dict({
        "gear_type": [entry["gear_type"] for entry in val_data],
        "split": [entry["split"] for entry in val_data],
        "prompt": [entry["prompt"] for entry in val_data],
        "dxf_content": [entry["dxf_content"] for entry in val_data],
    }),
    "test": Dataset.from_dict({
        "gear_type": [entry["gear_type"] for entry in test_data],
        "split": [entry["split"] for entry in test_data],
        "prompt": [entry["prompt"] for entry in test_data],
        "dxf_content": [entry["dxf_content"] for entry in test_data],
    }),
})


# Save the dataset to disk in JSON format
for split_name, split_dataset in dataset.items():
    split_dir = f"prompted/{split_name}"
    os.makedirs(split_dir, exist_ok=True)
    
    split_data = {
        "gear_type": split_dataset["gear_type"],
        "split": split_dataset["split"],
        "prompt": split_dataset["prompt"],
        "dxf_content": split_dataset["dxf_content"]
    }
    
    with open(f"{split_dir}/data.json", "w") as f:
        json.dump(split_data, f, indent=2)