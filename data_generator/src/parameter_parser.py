import argparse
from datetime import datetime

def parse_arguments():
    """Parses command-line arguments for data generator."""
    parser = argparse.ArgumentParser(description="Data Generator Parameters")
    
    # Feed type
    parser.add_argument(
        "--feed",
        type=str,
        required=True,
        choices=["customer", "product", "store", "inventory", "promo", "transactions", "iot"],
        help="Type of feed to generate (e.g., customer, product)."
    )
    
    # Number of records
    parser.add_argument(
        "--records",
        type=int,
        required=True,
        help="Number of records to generate."
    )
    
    # Start date
    parser.add_argument(
        "--start_date",
        type=str,
        default=datetime.now().strftime("%Y-%m-%d"),
        help="Start date for the feed generation (default: today)."
    )
    
    # End date
    parser.add_argument(
        "--end_date",
        type=str,
        default="9999-12-31",
        help="End date for the feed generation (default: 9999-12-31)."
    )
    
    args = parser.parse_args()
    return args
