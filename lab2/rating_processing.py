""" This script processes the bulk download data from the Open Library project."""

import csv
import os

def process_ratings():
    input_path = os.path.join("data/unprocessed/", "ol_dump_ratings.txt")
    output_path = os.path.join("data/processed/", "ratings_processed.csv")
    
    with open(output_path, 'w', newline='', encoding='utf-8') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(['work_key', 'book_key', 'rating_value', 'rating_date'])
        
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) >= 4: 
                    work_key = parts[0] if parts[0] else None
                    book_key = parts[1] if len(parts) > 1 and parts[1] else None
                    rating_value = parts[2] if parts[2] else None
                    rating_date = parts[3] if parts[3] else None
                    
                    if rating_value and rating_value.isdigit() and 1 <= int(rating_value) <= 5:
                        writer.writerow([
                            work_key if work_key else '',  # OL123W
                            book_key if book_key else '',  # OL123M
                            rating_value,
                            rating_date.split('T')[0] if rating_date else ''
                        ])

if __name__ == "__main__":
    process_ratings()