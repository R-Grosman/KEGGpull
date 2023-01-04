import asyncio
import re
import sys
import xml.etree.ElementTree as ET
from time import perf_counter

import requests

# import aiohttp


def pathway_list_url(user_input: str) -> str:
    return f"https://rest.kegg.jp/list/pathway/{user_input}"


def pathway_kgml_url(user_input: str) -> str:
    return f"https://rest.kegg.jp/get/{user_input}/kgml"


def pathway_text_url(user_input: str) -> str:
    return f"https://rest.kegg.jp/get/{user_input}"


async def get_organism_pathways(organism_code: str) -> list[str]:
    url = pathway_list_url(organism_code)
    response = requests.get(url)

    if response.status_code != 200:
        sys.exit(f"Request failed with status code {response.status_code}")

    paths = response.text.split("\n")
    paths = [path.split("\t")[0].removeprefix("path:") for path in paths if path]

    return paths


def get_pathway_kgml(pathway_code: str) -> str:
    url = pathway_kgml_url(pathway_code)
    response = requests.get(url)

    return pathway_code, response.text


async def send_async_kgml_request(pathway_code: str) -> str:
    # print(f"FIRED:{pathway_code}")
    return await asyncio.to_thread(get_pathway_kgml, pathway_code)


def build_path_from_kgml(path_code, root):
    # Builds a list of unique (no repeats) metabolites for a given parsed (via Elementree XML parser) KGML pathway file
    # Returns a list
    # print(f"{root.attrib['name'].removeprefix("path:")}")
    regex = re.compile("C[0-9]{5}")
    compound_list = [
        path_code,
    ]
    for entry in root.findall("entry"):
        if entry.attrib["type"] == "compound":
            compund_entry = entry.attrib["name"].removeprefix("cpd:")
            results = regex.findall(compund_entry)
            compound_list.extend(results)

    # for entry in root.findall("entry"):
    #     if entry.attrib["type"] == "compound":
    #         tmpCpd = entry.attrib["name"]
    #         tmpPath.extend(tmpCpd.split(" "))
    #         tmpPath = [i for i in tmpPath if "cpd:" in i]
    #         if tmpPath:
    #             tmpPath = [re.sub("cpd:", "", i) for i in tmpPath]
    #             tmpPathRet.extend(list(set(tmpPath)))
    #         else:
    #             return []
    return compound_list


def pad_list_items(input_list):
    max_len = max([len(sublist) for sublist in input_list])
    padded_list = []
    for sub_list in input_list:
        padding = [
            "",
        ] * (max_len - len(sub_list))
        padded_list.append(sub_list + padding)

    return padded_list


def sort_lists(input_list):
    return sorted(input_list, key=lambda x: x[0])


def transpose_table(input_list):
    return list(zip(*input_list))


async def main():
    paths = await get_organism_pathways("hsa")
    list_len = len(paths)

    print(f"PATH LIST RECEIVED: {list_len} ITEMS.")
    responses = await asyncio.gather(*[send_async_kgml_request(path) for path in paths])

    # result = "\n".join([a_.split("\n")[4].strip() for a_ in ans])
    kgml_roots = [
        (path_code, ET.fromstring(response)) for path_code, response in responses
    ]
    result = [
        build_path_from_kgml(path_code, kgml_root)
        for path_code, kgml_root in kgml_roots
    ]

    result = sort_lists(result)
    result = pad_list_items(result)
    result = transpose_table(result)

    # print(result)

    # for prog_counter, path in enumerate(paths, 1):
    #     # ans = requests.get(pathway_kgml_url(path)).text.split("\n")[4].strip()
    #     ans = await send_async_kgml_request(path)
    #     ans = ans.split("\n")[4].strip()
    #     print(f"{ans}\t{prog_counter}/{list_len}")

    output_str = ["\t".join(line) + "\n" for line in result]
    with open("OUTPUT.tsv", "w") as fh:
        fh.writelines(output_str)


# Initiate Script
if __name__ == "__main__":
    start = perf_counter()
    asyncio.run(main())
    print(f"Time = {perf_counter() - start}")


# def getAPI(APIin, retType):
#     # Make API requests and return the APi object
#     # Take three letter organism code and a request type:
#     # list: returns all the available pathways of the organism
#     # pathKGML: returns the KGML file of the pathway
#     # path: returns the text information of the pathway
#     if retType == "list":
#         APIreq = "http://rest.kegg.jp/list/pathway/" + APIin
#     elif retType == "pathKGML":
#         APIreq = "http://rest.kegg.jp/get/" + APIin + "/kgml"
#     elif retType == "path":
#         APIreq = "http://rest.kegg.jp/get/" + APIin
#     else:
#         sys.exit("Invalid request type")
#     APIresp = requests.get(APIreq)
#     return APIresp


# def checkAPI(APIresp):
#     # Takes an API response and checks if the request was succesfull.
#     # Returns a message on success/fail
#     if APIresp.status_code != 200:
#         sys.exit("Request Failed!")
#     print("API Request Successful!")


# def buildPathKGML(root):
#     # Builds a list of unique (no repeats) metabolites for a given parsed (via Elementree XML parser) KGML pathway file
#     # Returns a list
#     tmpPath = []
#     tmpPathRet = []
#     for entry in root.findall("entry"):
#         if entry.attrib["type"] == "compound":
#             tmpCpd = entry.attrib["name"]
#             tmpPath.extend(tmpCpd.split(" "))
#             tmpPath = [i for i in tmpPath if "cpd:" in i]
#             if tmpPath:
#                 tmpPath = [re.sub("cpd:", "", i) for i in tmpPath]
#                 tmpPathRet.extend(list(set(tmpPath)))
#             else:
#                 return []
#     return tmpPathRet

# async def build_path_kgml_async():
#     asyncio.to_thread()

# def combinePaths(MasterList, counter, Total):
#     # Sends API requests for KGML files per pathway, turns the compounds into a list and writes it in to a file,
#     # Takes MasterListm counter and Total all are created in main()
#     with open(sys.argv[2], "w") as fh:
#         for PathCode in MasterList:
#             print("Compiling:", PathCode)
#             APIres = getAPI(PathCode, "pathKGML")
#             checkAPI(APIres)
#             root = ET.fromstring(APIres.content)
#             tmpPath = buildPathKGML(root)
#             if tmpPath:
#                 print(PathCode + "\t" + "\t".join(tmpPath), file=fh)
#             else:
#                 print(PathCode, file=fh)
#             counter += 1
#             print(counter, "of", Total, "completed.")
#     print("Pathway table creted in:", sys.argv[2])


# def main():
#     # 1st block uses the first terminal input to create an API request for list of pathways
#     # 2nd block creates the master list to be used in table
#     # 3rd block sets the counters for the script and combines the pathways into a table
#     print("Retrieveing Pathway list for", sys.argv[1])
#     APIres = getAPI(sys.argv[1], "list")
#     checkAPI(APIres)
#     APIres = APIres.text.split("\n")[0:-1]

#     print("Creating master list for building table")
#     MasterList = []
#     for path in APIres:
#         tmpcode = path.split("\t")[0]
#         tmpcode = re.sub("path:", "", tmpcode)
#         MasterList.append(tmpcode)
#     print("Completed!\n")

#     counter = 0
#     Total = len(MasterList)
#     combinePaths(MasterList, counter, Total)
