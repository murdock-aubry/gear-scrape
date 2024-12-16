import json
import random
import os

# Load the original json file
with open('train_data_unprompted.json', 'r') as f:
    data = json.load(f)

gear_types = data.keys()

for gear_type in gear_types:

    data_gear = data[gear_type]

    random.seed(42)  
    random.shuffle(data_gear)

    total_size = len(data_gear)
    test_size = int(0.1 * total_size)
    val_size = int(0.1 * total_size)
    train_size = total_size - test_size - val_size

    # Split the data
    test_data = data_gear[:test_size]
    val_data = data_gear[test_size:test_size + val_size] 
    train_data = data_gear[test_size + val_size:]

    # Replace original data with splits
    data[gear_type] = {
        'train': train_data,
        'val': val_data, 
        'test': test_data
    }

# Save entire split dataset
with open('train_data_split_unprompted.json', 'w') as f:
    json.dump(data, f, indent=4)

print("Data split complete and saved to data_split.json")
print("Split sizes for each gear type:")
for gear_type in gear_types:
    print(f"\n{gear_type}:")
    print(f"Training samples: {len(data[gear_type]['train'])}")
    print(f"Validation samples: {len(data[gear_type]['val'])}")
    print(f"Test samples: {len(data[gear_type]['test'])}")
