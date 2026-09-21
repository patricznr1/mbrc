# MBRC — Memory Benchmark Reporting Checklist

MBRC is a reporting checklist for benchmark results of long-term memory systems: ten rules, one verdict per criterion, and one machine-readable result record per measurement.

The canonical version of the checklist is the page at https://patric-zeller.de/MBRC. This repository does not duplicate the page text as a second source; it holds the result schema, the validator, a fictional example record, an archived copy of the page text per published version (`text/`), and the issue tracker for corrections and comments.

## Validate a record

    python tools/mbrc-validate.py record.json schema/1.0/mbrc.schema.json

Exit status 0 means that every field required by the branches the record declares is present and non-empty. The validator needs Python 3 and no third-party packages. It checks completeness, not truth.

## Licences

- `LICENSE-CC-BY-4.0.md` (CC BY 4.0) covers the text of the checklist and the documentation: `text/`, `README.md`, `CHANGELOG.md`, `CITATION.cff`, the issue templates.
- `LICENSE-CC0-1.0.md` (CC0 1.0) covers the schema, the validator and the example record: `schema/`, `tools/`, `examples/`.

## Corrections and comments

If a rule, a cited figure or its stated conditions is wrong, open an issue here or write to info@patric-zeller.de. It gets fixed, the change is recorded with its date, and the person who found it is named.

## Competing interest

The maintainer also builds a long-term memory system (NEXUS), and no figure of that system appears in MBRC.

## Cite

DOI of this version: https://doi.org/10.5281/zenodo.22878931 · DOI of all versions: https://doi.org/10.5281/zenodo.22878930

```bibtex
@misc{zeller2026mbrc,
  author       = {Zeller, Patric},
  title        = {Memory Benchmark Reporting Checklist ({MBRC}) 1.0},
  year         = {2026},
  month        = {9},
  howpublished = {\url{https://patric-zeller.de/MBRC}},
  doi          = {10.5281/zenodo.22878931},
  note         = {Version 1.0, published 15 September 2026. Licence CC BY 4.0.}
}
```
