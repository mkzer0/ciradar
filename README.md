
# CI Radar Tool

This tool allows you to either load data from a GitHub repository or plot the data to visualize various statistics related to pull requests.

## Prerequisites

- Python 3.x
- Required Python packages (install using `requirements.txt` if provided)

## Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Loading Data

To load data from a GitHub repository, use the `load` mode. You need to provide your GitHub API token and the repository in the format `owner/repo`.

```sh
python main.py load --token <your_github_token> --repo <owner/repo> [--batch_size <batch_size>]
```

**Arguments:**
- `--token` (required): GitHub API token.
- `--repo` (required): GitHub repository in the format `owner/repo`.
- `--batch_size` (optional): Number of pull requests to process per batch (default is 500).

Example:
```sh
python main.py load --token ghp_exampleToken12345 --repo octocat/Hello-World --batch_size 100
```

### Plotting Data

To plot the data that was loaded, use the `plot` mode. This will generate various plots to visualize the statistics of the pull requests.

```sh
python main.py plot
```

The plot mode does not require additional arguments.

Example:
```sh
python main.py plot
```

## Directory Structure

- `main.py`: The main script to run the CI Radar tool.
- `src/ciradar/`: Contains the `load` and `plot` modules.

## Script Details

### `main.py`

This script provides a command-line interface to either load data from a GitHub repository or plot the data. It uses the `argparse` library to handle command-line arguments.

- The `load` mode calls the `load.execute` function from the `ciradar` package, which requires a GitHub token and repository name.
- The `plot` mode calls the `plot.execute` function from the `ciradar` package, which generates plots from the loaded data.

## Example

Load data from a GitHub repository:
```sh
python main.py load --token your_github_token --repo owner/repo --batch_size 500
```

Plot the loaded data:
```sh
python main.py plot
```

Ensure that you have the necessary permissions and quota on your GitHub account to access the repository data through the GitHub API.
