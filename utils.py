import os

def average_lines_in_dxf(directory):
    total_lines = 0
    dxf_file_count = 0
    
    # Loop through the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".dxf"):
            dxf_file_count += 1
            file_path = os.path.join(directory, filename)
            
            # Open and count lines in the file
            with open(file_path, 'r') as file:
                line_count = sum(1 for _ in file)
                total_lines += line_count

    # Calculate the average
    average_lines = total_lines / dxf_file_count
    return average_lines


def line_reduction_rate(original_directory, clean_directory):
    original_average = average_lines_in_dxf(original_directory)
    clean_average = average_lines_in_dxf(clean_directory)
    print("Average lines (original) = ", original_average)
    print("Average lines (clean = ", clean_average)
    print("clean/orig ration = ", clean_average / original_average)
    print("Percentage of data remove = ", (1 - clean_average / original_average) * 100)


if __name__ == "__main__":

    original_directory = "./gear_dxf"
    clean_directory = "./gear_dxf_clean"

    line_reduction_rate(original_directory, clean_directory)