import asyncio
import logging
import re
import sys
import xml.etree.ElementTree as ET
import argparse
import requests
from tqdm.asyncio import tqdm_asyncio
from datetime import datetime

# from keggpull import __version__

__author__ = "R-Grosman"
__copyright__ = "R-Grosman"
__license__ = "MIT"
__version__ = "0.0.1"
# from time import perf_counter


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.addHandler(logging.StreamHandler(sys.stdout))


def parse_args(args: list[str]) -> argparse.Namespace:
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(description="Tabulate and export all pathways and its metabolites for a given organism")
    parser.add_argument(
        "--version",
        action="version",
        version="KEGGpull {ver}".format(ver=__version__),
    )
    parser.add_argument(
        "-o",
        "--organism",
        dest="organism",
        help="three letter organism code e.g. hsa",
        type=str,
        metavar="ORG"
        )
    parser.add_argument(
        "-of",
        "--output-file",
        dest="outputfile",
        help="output file name",
        type=str,
        metavar="OUT",
        nargs="?"
        )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


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


async def main(args:argparse.Namespace):
    """Main async function"""
    # organism_code = args.organism
    if args.loglevel:
        logger.setLevel(args.loglevel)

    if not args.outputfile:
        args.outputfile = f"{args.organism}_{datetime.now():%Y%m%d%H%M%S}.tsv"

    if args.organism is None:
        logger.error(
            "please provide a three letter kegg organism code e.g 'hsa' for Homo Sapiens"
        )
    paths = get_organism_pathways(args.organism)
    paths = parse_organism_pathways(paths)
    list_len = len(paths)

    logger.info(f"Path List RECEIVED for {args.organism}: {list_len} Pathways.")
    # responses = await asyncio.gather(*[send_async_kgml_request(path) for path in paths])
    responses = await tqdm_asyncio.gather(*[send_async_kgml_request(path) for path in paths])
    # responses = [send_async_kgml_request(path) for path in paths]
    # for query in tqdm.asyncio.tqdm.as_completed(responses):
    #     await query

    logger.debug(f"{responses=}")

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

    output_str = ["\t".join(line) + "\n" for line in result]
    with open(args.outputfile, "w") as fh:
        fh.writelines(output_str)
    logger.info(f"Table created: {args.outputfile}")

def run():
    """ main entry point for terminal execution"""
    args = parse_args(sys.argv[1:])
    logger.debug(f"{args=}")
    asyncio.run(main(args))


# Initiate Script
if __name__ == "__main__":
    # start = perf_counter()
    # args = parse_args(["-o", "aga","-of","output_test.tsv"])
    args = parse_args(["-o", "aga"])
    asyncio.run(main(args))
    # print(f"Time = {perf_counter() - start}")
