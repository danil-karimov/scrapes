import xml.etree.ElementTree as ET
import os
from xml.dom import minidom

directory_path = '/Users/danil/Downloads/data-10102023-structure-10062023'
file_count = 0
master_root = ET.Element('master_root')



for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)

    if os.path.isfile(file_path) and filename.endswith('.xml'):
        if 'VO_RRMSPSV' in filename:

            # with open(file_path, 'r') as f:
            #     content = f.read()
            #     print(f"Extract {filename}")
            #     all_content += content + "/n"
            tree = ET.parse(file_path)
            root = tree.getroot()
            master_root.append(root)

            file_count +=1
            print(f"Processing file {filename}, completed step {file_count}")
            if file_count >= 2000:
                print("Too much")
                break

master_tree = ET.ElementTree(master_root)

# Convert the ElementTree to a string
rough_string = ET.tostring(master_root, 'utf-8')

# Re-parse the string to a minidom object
reparsed = minidom.parseString(rough_string)

# Pretty-print the minidom object to a string
pretty_string = reparsed.toprettyxml(indent="\t")

# Write the pretty-printed string to a file
with open("xml_fns_data/master_file.xml", 'w', encoding='utf-8') as f:
    f.write(pretty_string)

# with open('xml_fns_data/master_file.xml', 'wb') as f:
#     master_tree.write(f, encoding='utf-8', xml_declaration=True)

print(f"Processed {file_count} XML files and saved the combined content to 'master_file.xml'.")