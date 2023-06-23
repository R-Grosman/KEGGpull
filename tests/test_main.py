import pytest

from keggpull.main import main

__author__ = "RGmetab"
__copyright__ = "RGmetab"
__license__ = "MIT"

def test_main():
    with pytest.raises(Exception) as e_info:
        main(organism_code=None)
