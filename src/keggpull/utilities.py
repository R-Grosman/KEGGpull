import asyncio
import re
import sys
import xml.etree.ElementTree as ET
import requests
from .logger import logger

__author__ = "R-Grosman"
__copyright__ = "R-Grosman"
__license__ = "MIT"
__version__ = "0.2.0"



def pathway_list_url(user_input: str) -> str:
    """Returns the URL for the generating list of pathways"""
    return f"https://rest.kegg.jp/list/pathway/{user_input}"


def pathway_kgml_url(user_input: str) -> str:
    """Returns the URL for pathway information in kgml format"""
    return f"https://rest.kegg.jp/get/{user_input}/kgml"


def pathway_text_url(user_input: str) -> str:
    """Returns the URL for pathway information in plain text"""
    return f"https://rest.kegg.jp/get/{user_input}"


def get_organism_pathways(organism_code: str) -> str:
    """Queries KEGG and returns a str of pathways"""
    get_url = pathway_list_url(organism_code)
    logger.info(f"Querying {organism_code} with {get_url}")
    response = requests.get(get_url)
    if response.status_code != 200:
        logger.error(f"Request failed with status code {response.status_code}")
        sys.exit()

    return response.text


def rest_response_validator(api_response: requests.Response) -> bool:
    """Checks the REST query response and returns a bool"""
    if api_response.status_code == 200:
        logger.info(f"Query: {api_response.url} is valid")
        return True
    if api_response.status_code in [400, 404]:
        logger.info(f"Query: {api_response.url} is invalid")
        return False
    logger.error(
        f"Server responded with status code:{api_response.status_code} to {api_response.url}"
    )
    return False


def parse_organism_pathways(kegg_organism_pathways: str) -> list[str]:
    """Parses the string return from KEGG into a list of pathways"""
    paths = kegg_organism_pathways.split("\n")
    paths = [path.split("\t")[0].removeprefix("path:") for path in paths if path]

    return paths


def get_pathway_kgml(pathway_code: str) -> tuple[str, str]:
    """Queries KEGG for a pathway and returns a tuple of path code and the pathway in KGML format"""
    url = pathway_kgml_url(pathway_code)
    response = requests.get(url)

    return pathway_code, response.text


async def send_async_kgml_request(pathway_code: str) -> tuple[str, str]:
    """Async wrapper for the KGML requester"""
    return await asyncio.to_thread(get_pathway_kgml, pathway_code)


def build_path_from_kgml(path_code: str, root: ET.Element) -> list[str]:
    """Parses the KGML root (ElementTree object) and extracts the Compounds with C[0-9]{5} format"""
    regex = re.compile("C[0-9]{5}")
    compound_list = [
        path_code,
    ]
    for entry in root.findall("entry"):
        if entry.attrib["type"] == "compound":
            compund_entry = entry.attrib["name"].removeprefix("cpd:")
            results = regex.findall(compund_entry)
            compound_list.extend(results)

    return compound_list


def pad_list_items(input_list: list[list]) -> list[list]:
    """Pads each list in a list of lists with "" upto list with most items"""
    max_len = max([len(sublist) for sublist in input_list])
    padded_list = []
    for sub_list in input_list:
        padding = [
            "",
        ] * (max_len - len(sub_list))
        padded_list.append(sub_list + padding)

    return padded_list


def sort_lists(input_list: list[list]) -> list[list]:
    "Sorts a list of lists based on the first element of each list"
    return sorted(input_list, key=lambda x: x[0])


def transpose_table(input_list: list[list]) -> list[tuple]:
    """Transposes a list of lists with equal lengths"""
    return list(zip(*input_list))


def build_xml_root(xml_str: str) -> ET.Element:
    """Build the XML root from a string"""
    return ET.fromstring(xml_str)