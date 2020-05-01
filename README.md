# TACRED Revisited: A Thorough Evaluation of the TACRED Relation Extraction Task [[Paper](https://arxiv.org/abs/2004.14855)]

## Table of Contents

* [Overview](#-overview)
* [Requirements](#-requirements)
* [Installation](#-installation)
* [Patch TACRED](#-patch-the-original-tacred)
* [Experiments](#-experiments)
* [Citation](#-citation)
* [License](#-license)


## 🔭&nbsp; Overview

| Path     	               | Description                         	|
|------------------------- |------------------------------	|
| [dataset/](dataset/)     | The experiment notebooks expect the patched TACRED dataset splits to be stored here. |
| [notebooks/](notebooks/) | This directory contains the notebooks that we used to produce the results in the paper.|
| [patch/](patch/) | This directory contains the patches for dev and test split of the original TACRED.|
| [results/](results/)     | This directory contains the predictions of all models on dev ([dev_results/](results/dev_results/)) and test split ([test_results/](results/test_results/)).|
| [scripts/](scripts/)     | This directory contains scripts, e.g., to apply the patch to TACRED dev or test split.|


## ✅&nbsp; Requirements

The code is tested with:

- Python 3.7
- Mysql Config 5.7 (required by Errudite) 
  ```
  # Minimal dependency install (Ubuntu)
  sudo apt install default-libmysqlclient-dev
  ```


## 🚀&nbsp; Installation

### From source
```bash
git clone https://github.com/DFKI-NLP/tacrev
cd tacrev
pip install -r requirements.txt  # only necessary for notebooks
```

## 💡&nbsp; Patch the original TACRED

### Dev Split

```bash
python scripts/apply_tacred_patch.py \
  --dataset-file <TACRED DIR>/dev.json \
  --patch-file ./patch/dev_patch.json \
  --output-file ./dataset/dev_rev.json
```

md5 checksum of patched dev split: `ce23ba10ca15bde94a3f733679bf1b05`

### Test Split

```bash
python scripts/apply_tacred_patch.py \
  --dataset-file <TACRED DIR>/test.json \
  --patch-file ./patch/test_patch.json \
  --output-file ./dataset/test_rev.json
```

md5 checksum of patched test split: `dbcce82f5ab67fbfd1062db6cc6b66cd`


## 🔬&nbsp; Experiments

- [notebooks/tables.ipynb](notebooks/tables.ipynb) produces the tables presented in the paper.
- [notebooks/error_groups.ipynb](notebooks/error_groups.ipynb) produces the error group bar chart from the paper.


## 📚&nbsp; Citation

If you find the code or dataset patch helpful, please cite the following paper:
```
@inproceedings{alt-etal-2020-tacrev,
    title={TACRED Revisited: A Thorough Evaluation of the TACRED Relation Extraction Task},
    author={Christoph Alt and Aleksandra Gabryszak and Leonhard Hennig},
    year={2020},
    booktitle={Proceedings of ACL},
    url={https://arxiv.org/abs/2004.14855}
}
```

## 📘&nbsp; License
The code is released under the under terms of the [MIT License](LICENSE).
