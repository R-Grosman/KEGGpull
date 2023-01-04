import logging
import re
import xml.etree.ElementTree as ET

with open("TEST_KGML.xml", "r") as fh:
    data = fh.read()

root = ET.fromstring(data)
path_code = root.attrib["name"].removeprefix("path:")

compound_list = [
    path_code,
]
regex = re.compile("C[0-9]{5}")
for entry in root.findall("entry"):
    if entry.attrib["type"] == "compound" and "cpd:" in entry.attrib["name"]:
        compund_entry = entry.attrib["name"].removeprefix("cpd:")
        results = regex.findall(compund_entry)

        compound_list.extend(results)

#         if tmpPath:
#             tmpPath = [re.sub("cpd:", "", i) for i in tmpPath]
#             tmpPathRet.extend(list(set(tmpPath)))

print(compound_list)
