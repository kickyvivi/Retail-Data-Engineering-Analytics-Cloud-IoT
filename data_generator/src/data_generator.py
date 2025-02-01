import os
import dependencies
from parameter_parser import parse_arguments

# Parse arguments and generate feed file
args = parse_arguments()

if args.feed == "customer":
    # Import the customer feed module and calls the function to generate the data
    from customer_feed import generate_customer_feed
    generate_customer_feed()
else:
    print(f"Feed type: {args.feed} not implemented in this data generator. List of supported feeds: customer, product, store, inventory, promo, transactions, iot")