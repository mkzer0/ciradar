import argparse
import sys

# Append the correct path to sys.path to recognize the src folder and its sub-packages
sys.path.append('./src')

# Importing from the ciradar package
from ciradar import load, plot

def main():
    parser = argparse.ArgumentParser(description='CI Radar Tool')
    parser.add_argument('mode', choices=['load', 'plot'], help='Choose mode to either load data or plot data.')
    parser.add_argument('--token', help='GitHub API token, required for loading data.')
    parser.add_argument('--repo', help='GitHub repository in the format "owner/repo", required for loading data.')
    parser.add_argument('--batch_size', type=int, default=500, help='Number of PRs to process per batch (default: 500)')

    args = parser.parse_args()

    # Call the appropriate function from the ciradar package
    if args.mode == 'load':
        if not args.token or not args.repo:
            print("Error: Token and repository name are required for loading data.")
            return
        load.execute(args.token, args.repo, 'pr_data2.csv', args.batch_size)
    elif args.mode == 'plot':
        plot.execute('pr_data2.csv')  # Assuming plot function doesn't need batch size

if __name__ == '__main__':
    main()
