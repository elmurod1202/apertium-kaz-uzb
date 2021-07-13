# lexical_selection_check.py
# Checks the dix file for multiple translations for a single entry for both sides.
# Generates two files for each side with ambigious translations.
# Output file names: left_variants.txt, right_variants.txt

from argparse import ArgumentParser
from collections import defaultdict

# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET

def get_variants(side):
    found_pairs = list()
    for key in side.keys():
        variants = side[key]
        if(len(variants)>1):
            print("Found: ", key, ":  ", variants)
            for variant in variants:
                found_pairs.append(key + " " + variant)  
    return found_pairs

def write_variants(file_name,side_list):
    with open(file_name,'w') as out_file:
        previous_el = side_list[0].split(" ")[0]
        for el in side_list:
            tmp = el.split(" ")[0]
            if previous_el != tmp:
                out_file.write("\n")
                previous_el = tmp
            out_file.write(el)
            out_file.write("\n")
    out_file.close()

if __name__ == "__main__":
    # START
    print("------------------------------------------------------------------------------------------------------------------------------------")

    # Parsing arguments:
    arg_parser = ArgumentParser()
    
    arg_parser.add_argument("--input_file", help="Path to the dix file you want to analyse.", required=True)
    args = arg_parser.parse_args()

    # input_file = '../../apertium-kaz-uzb.kaz-uzb.dix'
    input_file = args.input_file
    print("Starting analysis with file:", input_file)

    # Passing the path of the xml document to enable the parsing process
    tree = ET.parse(input_file)

    # getting the parent tag of
    # the xml document
    root = tree.getroot()

    section = root[2]
    l_side = defaultdict(list)
    r_side = defaultdict(list)
    for element in section:
        # Checking regex, skipping if present:
        if len(element.findall("re"))>0:
            continue
        l = ET.tostring(element.find("p/l"), encoding='unicode').strip()
        r = ET.tostring(element.find("p/r"), encoding='unicode').strip()
        l_side[l].append(r)
        r_side[r].append(l)

    l_list = get_variants(l_side)
    r_list = get_variants(r_side)
    print("Writing results to a file:")
    write_variants("left_variants.txt",l_list)
    write_variants("right_variants.txt",r_list)
    print("Finished writing to files.")


