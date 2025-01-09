from parameter_parser import parse_arguments

if __name__ == "__main__":
    args = parse_arguments()
    print(f"Feed: {args.feed}")
    print(f"Records: {args.records}")
    print(f"Start Date: {args.start_date}")
    print(f"End Date: {args.end_date}")
