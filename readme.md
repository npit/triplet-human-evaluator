# Simple human evaluation tool for triplet preference submissions.

Requires:
- Path to json data, in the format `{'id1': 'Text for doc 1', 'id2': 'Text for doc 2'}`
- Path to triplet evaluations to be executed, in the format `{'id1': ['id2', 'id3', 'id4'], 'id5': ['id2', 'id3, 'id7']}`. This will generate all possible tuple combinations to compare against the reference document -- i.e., the id combinations for `id1` would be `[(2,3), (2,4), (3,4)]` and each will be presented for evaluation compared with id1.

Generates:
A `results.json` is created / updated after each evaluation. Program re-runs read the file to skip already completed results.

Arguments:
See the help page and/or code for argument values and defaults.