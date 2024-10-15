# clustr

A command line tool that identifies communities of articles based on semantic similarity.

## Requirements

- [Python (version >=3.11)](https://www.python.org/)
- [Poetry (version >=1.5.0)](https://python-poetry.org/)
- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Optional)
  - For creating virtual environments. Any other solution will work.
- Graphics Processing Unit (GPU) (Optional)

## Usage

Create a conda environment, here named `clustr`:

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

## Run clustering

There is a command-line script `cli.py` to run against a json file:

```bash
$ python ./clustr/cli.py /data/2024-08-01_2024-10-15-alzheimer.json
```

- Arguments
  - positional: path to json file
  - `--threshold`: cosine similarity minimum threshold (default: 0.96)
  - `--outpath`: path to output file (default: `data/cluster.json`)

## Testing

There is a convenience script that can be launched:

```bash
$ ./test.sh
```

This will run the tests in `./tests`, lint with [flake8](https://flake8.pycqa.org/en/latest/) and type check with [mypy](http://mypy-lang.org/).


