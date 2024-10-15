# clustr

A command line tool that identifies communities of articles based on semantic similarity.

## Requirements

- [Python (version >=3.9)](https://www.python.org/)
- [Poetry (version >=1.5.0)](https://python-poetry.org/)
<!-- - [Docker (version 20.10.14) and Docker Compose (version 2.5.1)](https://www.docker.com/)
  - We use Docker to create a [RethinkDB (v2.3.6)](https://rethinkdb.com/) instance for loading data. -->
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Optional)
  - For creating virtual environments. Any other solution will work.
- Graphics Processing Unit (GPU) (Optional)
  - The pipeline classifier can be sped up an order of magnitude by running on a system with a GPU. We have been using a system running Ubuntu 18.04.5 LTS, Intel(R) Xeon(R) CPU E5-2687W, 24 Core with an NVIDIA GP102 [TITAN Xp] GPU.

## Usage

Create a conda environment, here named `pipeline`:

```bash
$ conda create --name clustr python=3.11 --yes
$ conda activate clustr
```

Download the remote:

```bash
$ git clone https://github.com/jvwong/clustr
$ cd clustr
```

Install the dependencies:

For Intel Mac [14.6.1 (23G93); 3.6 GHz 8-Core Intel Core i9]:

```bash
$ conda install -c conda-forge sentence-transformers --yes
```

```bash
$ poetry install
```

## Testing

There is a convenience script that can be launched:

```bash
$ ./test.sh
```

This will run the tests in `./tests`, lint with [flake8](https://flake8.pycqa.org/en/latest/) and type check with [mypy](http://mypy-lang.org/).


