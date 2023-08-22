.. These are examples of badges you might want to add to your README:
   please update the URLs accordingly

    .. image:: https://api.cirrus-ci.com/github/<USER>/KEGGpull.svg?branch=main
        :alt: Built Status
        :target: https://cirrus-ci.com/github/<USER>/KEGGpull
    .. image:: https://readthedocs.org/projects/KEGGpull/badge/?version=latest
        :alt: ReadTheDocs
        :target: https://KEGGpull.readthedocs.io/en/stable/
    .. image:: https://img.shields.io/coveralls/github/<USER>/KEGGpull/main.svg
        :alt: Coveralls
        :target: https://coveralls.io/r/<USER>/KEGGpull
    .. image:: https://img.shields.io/pypi/v/KEGGpull.svg
        :alt: PyPI-Server
        :target: https://pypi.org/project/KEGGpull/

.. image:: https://img.shields.io/badge/-PyScaffold-005CA0?logo=pyscaffold
    :alt: Project generated with PyScaffold
    :target: https://pyscaffold.org/
.. .. image:: https://pepy.tech/badge/KEGGpull/month
..     :alt: Monthly Downloads
..     :target: https://pepy.tech/project/KEGGpull

|

========
KEGGpull
========


    An async utility for creating metabolite tables from KEGG database.


To perform pathway enrichment analysis one of the inputs required is a table of metabolites per pathway.
KEGG[1-3] is a great database for this purpose.
KEGGpull streamlines this process by using async requests and formats the results and finally exports as a tab separated file.

[1]Kanehisa, M. and Goto, S.; KEGG: Kyoto Encyclopedia of Genes and Genomes. Nucleic Acids Res. 28, 27-30 (2000). `doi <https://doi.org/10.1093/nar/28.1.27>`
[2]Kanehisa, M; Toward understanding the origin and evolution of cellular organisms. Protein Sci. 28, 1947-1951 (2019). `doi <https://doi.org/10.1002/pro.3715>`
[3]Kanehisa, M., Furumichi, M., Sato, Y., Kawashima, M. and Ishiguro-Watanabe, M.; KEGG for taxonomy-based analysis of pathways and genomes. Nucleic Acids Res. 51, D587-D592 (2023). `doi <https://doi.org/10.1093/nar/gkac963>`


.. _pyscaffold-notes:

Note
====

This project has been set up using PyScaffold 4.3.1. For details and usage
information on PyScaffold see https://pyscaffold.org/.

If you use this tool please cite this repo.
