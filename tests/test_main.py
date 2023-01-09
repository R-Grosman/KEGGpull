import re
import xml.etree.ElementTree as ET

import pytest
import requests

from keggpull.main import (
    build_xml_root,
    main,
    pad_list_items,
    parse_organism_pathways,
    pathway_kgml_url,
    pathway_list_url,
    pathway_text_url,
    rest_response_validator,
    sort_lists,
    transpose_table,
)

__author__ = "RGmetab"
__copyright__ = "RGmetab"
__license__ = "MIT"


def test_sort_lists():
    unsorted_list = [
        ["hsa00059", "C00032", "", ""],
        ["hsa00010", "", "", ""],
        ["hsa00030", "C02032", "", "C11111"],
    ]
    sorted_list = [
        ["hsa00010", "", "", ""],
        ["hsa00030", "C02032", "", "C11111"],
        ["hsa00059", "C00032", "", ""],
    ]
    assert sort_lists(unsorted_list) == sorted_list


def test_transpose_table():
    normal_list = [
        ["hsa00001", "C00011", "C00012", "C00013"],
        ["hsa00002", "C00021", "C00022", "C00023"],
        ["hsa00003", "C00031", "C00032", "C00033"],
    ]
    transposed_list = [
        ("hsa00001", "hsa00002", "hsa00003"),
        ("C00011", "C00021", "C00031"),
        ("C00012", "C00022", "C00032"),
        ("C00013", "C00023", "C00033"),
    ]
    assert transpose_table(normal_list) == transposed_list


def test_pad_list_items():
    input_list = [
        ["hsa00059", "C00032"],
        [
            "hsa00010",
        ],
        ["hsa00030", "C02032", "C00032", "C11111"],
    ]
    output_list = [
        ["hsa00059", "C00032", "", ""],
        ["hsa00010", "", "", ""],
        ["hsa00030", "C02032", "C00032", "C11111"],
    ]
    assert pad_list_items(input_list) == output_list


def test_rest_response_validator():
    mock_response_object = requests.Response()
    test_cases = {200: True, 400: False, 404: False, 300: False, 100: False, 500: False}

    for test_code, response in test_cases.items():
        mock_response_object.status_code = test_code
        assert rest_response_validator(mock_response_object) == response


def test_pathway_kgml_url():
    keys = ["hsa00010", "aga01124"]
    vals = [f"https://rest.kegg.jp/get/{value}/kgml" for value in keys]
    for argument, response in zip(keys, vals):
        assert pathway_kgml_url(argument) == response


def test_pathway_list_url():
    keys = ["hsa", "aga"]
    vals = [f"https://rest.kegg.jp/list/pathway/{value}" for value in keys]
    for argument, response in zip(keys, vals):
        assert pathway_list_url(argument) == response


def test_pathway_text_url():
    keys = ["hsa00010", "aga01124"]
    vals = [f"https://rest.kegg.jp/get/{value}" for value in keys]
    for argument, response in zip(keys, vals):
        assert pathway_text_url(argument) == response


def test_parse_organism_pathways():
    total_items = 352
    with open("tests/data/hsa_pathway_list.tsv", "r") as fh:
        hsa_input_data = fh.read()

    data_parsed = parse_organism_pathways(hsa_input_data)
    kegg_code_re = re.compile("^hsa[0-9]{5}$")
    mathching = [kegg_code_re.match(pathway) for pathway in data_parsed]

    assert len(data_parsed) == total_items
    assert len(mathching) == total_items


def test_build_xml_root():
    with open("tests/data/hsa00010.kgml", "r") as fh:
        input_data = fh.read()
    assert isinstance(build_xml_root(input_data), ET.Element)


# def test_main():
#     with pytest.raises(Exception) as e_info:
#         main(organism_code=None)
