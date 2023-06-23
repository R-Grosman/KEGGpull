import argparse
import logging

__author__ = "R-Grosman"
__copyright__ = "R-Grosman"
__license__ = "MIT"
__version__ = "0.2.0"


def init_parser() -> argparse.ArgumentParser:
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
    return parser
    
