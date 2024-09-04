# This file contains functions used to strip the DXF files for their raw material.

import dxfgrabber
import ezdxf
import sys
import os


def clean_up_dxf(file_name):

    path = "/Users/murdockaubry/Library/Mobile Documents/com~apple~CloudDocs/Research/Personal Research/gear-gen/gear_dxf/" + file_name

    doc0 = ezdxf.readfile(path)

    color_to_remove = 5  # Turqoise
    doc1 = remove_entities_of_color(doc0, color_to_remove)

    color_to_remove = 7  # white
    doc2 = remove_entities_of_color(doc1, color_to_remove)

    doc3 = remove_all_text(doc2)


    doc4 = remove_dashdot_arcs(doc3)
    output_path = "/Users/murdockaubry/Library/Mobile Documents/com~apple~CloudDocs/Research/Personal Research/gear-gen/gear_dxf_clean/" + file_name
    
    doc4.saveas(output_path)

    get_last_section(output_path, output_path)



def remove_entities_of_color(doc, color_to_remove):
    # Access the modelspace where entities are typically stored
    msp = doc.modelspace()
    
    # List to store entities to be removed
    entities_to_remove = []
    
    # Iterate through all entities in the modelspace
    for entity in msp:
        if (entity.dxftype() in ['LINE', 'POLYLINE'] and 
            entity.dxf.color == color_to_remove):
            entities_to_remove.append(entity)

    # Remove the entities
    for entity in entities_to_remove:
        msp.delete_entity(entity)
    
    return doc


def remove_all_text(doc):
    # Access the modelspace where entities are typically stored
    msp = doc.modelspace()
    
    # List to store entities to be removed
    entities_to_remove = []
    
    # Iterate through all entities in the modelspace
    for entity in msp:
        if entity.dxftype() in ['TEXT', 'MTEXT']:
            entities_to_remove.append(entity)
    
    # Remove the entities
    for entity in entities_to_remove:
        msp.delete_entity(entity)
    
    # Return the modified document
    return doc


def remove_dashdot_arcs(doc):
    msp = doc.modelspace()
    
    for arc in msp.query('ARC'):
        if arc.dxf.layer == 'DASHDOT':  # This might need adjustment based on actual DXF structure
            msp.delete_entity(arc)
    return doc


def get_last_section(file_path, path_out):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    last_section_start = -1
    for i, line in enumerate(lines):
        if "SECTION" in line:
            last_section_start = i
    
    with open(path_out, 'w') as file:
        file.writelines(lines[last_section_start - 1:]) # Must include 0 beforehand
    
    return path_out


# # Example usage
# path = "/Users/murdockaubry/Library/Mobile Documents/com~apple~CloudDocs/Research/Personal Research/gear-gen/gear_dxf/AG0.5-20R1.dxf"
# temp_path = "/Users/murdockaubry/Library/Mobile Documents/com~apple~CloudDocs/Research/Personal Research/gear-gen/dxf_experiments/temp_file.dxf"


# output_path = get_last_section(path, temp_path)

dxf_file_path = "/Users/murdockaubry/Library/Mobile Documents/com~apple~CloudDocs/Research/Personal Research/gear-gen/gear_dxf/"

dxf_files = os.listdir(dxf_file_path)

for file in dxf_files:
    clean_up_dxf(file)



