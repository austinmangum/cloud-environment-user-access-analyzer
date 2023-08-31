#!/usr/bin/env python3

import argparse
from src import aws_analyzer, gcp_analyzer

def parse_args():
    parser = argparse.ArgumentParser(description='Cloud Environment User Access Analyzer (CEUAA)')
    parser.add_argument('provider', type=str, choices=['aws', 'gcp'], 
                        help='Cloud provider to analyze. Choices are "aws" or "gcp".')
    
    # If you need more command line arguments, you can add them here.
    
    return parser.parse_args()

def main():
    args = parse_args()

    if args.provider == "aws":
        aws_analyzer.run_analysis()
    elif args.provider == "gcp":
        gcp_analyzer.run_analysis()
    else:
        print("Unsupported cloud provider!")
        sys.exit(1)

if __name__ == "__main__":
    main()
