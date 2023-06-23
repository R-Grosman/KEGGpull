import asyncio
from argparser import init_parser
import sys
import xml.etree.ElementTree as ET
import argparse
from tqdm.asyncio import tqdm_asyncio
from datetime import datetime
import utilities as utils
from logger import logger

__author__ = "R-Grosman"
__copyright__ = "R-Grosman"
__license__ = "MIT"
__version__ = "0.2.0"

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
    paths = utils.get_organism_pathways(args.organism)
    paths = utils.parse_organism_pathways(paths)
    list_len = len(paths)

    logger.info(f"Path List RECEIVED for {args.organism}: {list_len} Pathways.")
    responses = await tqdm_asyncio.gather(*[utils.send_async_kgml_request(path) for path in paths])

    logger.debug(f"{responses=}")

    kgml_roots = [
        (path_code, ET.fromstring(response)) for path_code, response in responses
    ]
    result = [
        utils.build_path_from_kgml(path_code, kgml_root)
        for path_code, kgml_root in kgml_roots
    ]

    result = utils.sort_lists(result)
    result = utils.pad_list_items(result)
    result = utils.transpose_table(result)

    output_str = ["\t".join(line) + "\n" for line in result]
    with open(args.outputfile, "w") as fh:
        fh.writelines(output_str)
    logger.info(f"Table created: {args.outputfile}")

def run():
    """ main entry point for terminal execution"""
    parser = init_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args(sys.argv[1:])
    logger.debug(f"{args=}")
    asyncio.run(main(args))
    sys.exit(0)


# Initiate Script
if __name__ == "__main__":
    input_args = ["__main__", *input("Enter your arguments:").split()]
    parser = init_parser()
    if len(input_args) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args(input_args[1:])
    asyncio.run(main(args))
