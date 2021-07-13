# lexical_selection_generate.py
# Reads manually revieved dix elements
# Creates lexical selection rules for them in a new file.

from argparse import ArgumentParser
from collections import defaultdict

# importing element tree
# under the alias of ET
import xml.etree.ElementTree as ET


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
    
    arg_parser.add_argument("--input_file", help="Path to the dix-like formatted file you want rules tobe generated from.", required=True)
    args = arg_parser.parse_args()

    file_in = args.input_file
    print("Starting analysis with file:", file_in)

    # file_in = "tmp.txt"
    file_out = file_in + "_result.txt"

    output_file = open(file_out,"w")

    # Reading file line by line:
    with open(file_in, "r") as input_file:
        for line in input_file.readlines():
            line = line.strip()
            
            # Skipping blank line:
            if len(line) == 0:
                continue
            
            # Converting line into a proper xml format:
            line = "<e>" + line + "</e>"
            
            # Reading line as an XML Tree:
            tree = ET.fromstring(line)
            l = tree.find("l")
            l_word = l.text
            l_tag = l.find("s").get("n")
            r = tree.find("r")
            r_word = r.text
            r_tag = r.find("s").get("n")
            # print(l_word, l_tag,r_word, r_tag)

            # Making LRX format:

            # Multiline option:
            #   <rule weight ="1">  <!-- default translation -->
            #     <match lemma="ақырын" tags="adj">
            #       <select lemma="sekin" tags="adj"/>
            #     </match>
            #   </rule>

            # or, a better alternative: 
            # <rule weight ="1"> <match lemma="ақырын" tags="adj"> <select lemma="sekin" tags="adj"/> </match> </rule>

            output_file.write("<!-- default translation for the word \"{}\"-->\n".format(l_word))
            rule1 = "<match lemma=\"{}\" tags=\"{}\"><select lemma=\"{}\" tags=\"{}\"/></match></rule>\n".format(l_word,l_tag,r_word,r_tag)
            rule2 = "<match lemma=\"{}\" tags=\"{}.*\"><select lemma=\"{}\" tags=\"{}.*\"/></match></rule>\n".format(l_word,l_tag,r_word,r_tag)
            print("Rule: ", rule2)
            output_file.write(rule1)
            output_file.write(rule2)
            output_file.write("\n")

            # print(ET.tostring(r, encoding="unicode"))

    input_file.close()
    output_file.close()
    print("Finished. Resulting rules saved in a file: ", file_out)