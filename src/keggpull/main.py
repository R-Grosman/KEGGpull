import re
import sys
import xml.etree.ElementTree as ET
from time import perf_counter

import requests


def getAPI(APIin, retType):
    # Make API requests and return the APi object
    # Take three letter organism code and a request type:
    # list: returns all the available pathways of the organism
    # pathKGML: returns the KGML file of the pathway
    # path: returns the text information of the pathway
    if retType == "list":
        APIreq = "http://rest.kegg.jp/list/pathway/" + APIin
    elif retType == "pathKGML":
        APIreq = "http://rest.kegg.jp/get/" + APIin + "/kgml"
    elif retType == "path":
        APIreq = "http://rest.kegg.jp/get/" + APIin
    else:
        sys.exit("Invalid request type")
    APIresp = requests.get(APIreq)
    return APIresp


def checkAPI(APIresp):
    # Takes an API response and checks if the request was succesfull.
    # Returns a message on success/fail
    if APIresp.status_code == 200:
        print("API Request Successful!")
    else:
        sys.exit("Request Failed!")


def buildPathKGML(root):
    # Builds a list of unique (no repeats) metabolites for a given parsed (via Elementree XML parser) KGML pathway file
    # Returns a list
    tmpPath = []
    tmpPathRet = []
    for entry in root.findall("entry"):
        if entry.attrib["type"] == "compound":
            tmpCpd = entry.attrib["name"]
            tmpPath.extend(tmpCpd.split(" "))
            tmpPath = [i for i in tmpPath if "cpd:" in i]
            if tmpPath:
                tmpPath = [re.sub("cpd:", "", i) for i in tmpPath]
                tmpPathRet.extend(list(set(tmpPath)))
            else:
                return []
    return tmpPathRet


def combinePaths(MasterList, counter, Total):
    # Sends API requests for KGML files per pathway, turns the compounds into a list and writes it in to a file,
    # Takes MasterListm counter and Total all are created in main()
    with open(sys.argv[2], "w") as fh:
        for PathCode in MasterList:
            print("Compiling:", PathCode)
            APIres = getAPI(PathCode, "pathKGML")
            checkAPI(APIres)
            root = ET.fromstring(APIres.content)
            tmpPath = buildPathKGML(root)
            if tmpPath:
                print(PathCode + "\t" + "\t".join(tmpPath), file=fh)
            else:
                print(PathCode, file=fh)
            counter += 1
            print(counter, "of", Total, "completed.")
    print("Pathway table creted in:", sys.argv[2])


def main():
    # 1st block uses the first terminal input to create an API request for list of pathways
    # 2nd block creates the master list to be used in table
    # 3rd block sets the counters for the script and combines the pathways into a table
    print("Retrieveing Pathway list for", sys.argv[1])
    APIres = getAPI(sys.argv[1], "list")
    checkAPI(APIres)
    APIres = APIres.text.split("\n")[0:-1]

    print("Creating master list for building table")
    MasterList = []
    for path in APIres:
        tmpcode = path.split("\t")[0]
        tmpcode = re.sub("path:", "", tmpcode)
        MasterList.append(tmpcode)
    print("Completed!\n")

    counter = 0
    Total = len(MasterList)
    combinePaths(MasterList, counter, Total)


# Initiate Script
if __name__ == "__main__":
    sys.argv = ["qwe", "hsa", "old_OUT.tsv"]
    start = perf_counter()
    main()
    print(f"Time: {perf_counter() - start}")
