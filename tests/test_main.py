import pytest

from keggpull.main import (
    pad_list_items,
    parse_organism_pathways,
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


def test_parse_organism_pathways():
    input = """path:hsa00010	Glycolysis / Gluconeogenesis - Homo sapiens (human)
path:hsa00020	Citrate cycle (TCA cycle) - Homo sapiens (human)
path:hsa00030	Pentose phosphate pathway - Homo sapiens (human)
path:hsa00040	Pentose and glucuronate interconversions - Homo sapiens (human)
path:hsa00051	Fructose and mannose metabolism - Homo sapiens (human)
path:hsa00230	Purine metabolism - Homo sapiens (human)"""

    output = [
        "hsa00010",
        "hsa00020",
        "hsa00030",
        "hsa00040",
        "hsa00051",
        "hsa00230",
    ]
    assert parse_organism_pathways(input) == output
