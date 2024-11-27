#!/bin/bash

# Generate raw dirty data
python generate_dirty_data.py

# Remove comment lines, empty lines, replace double commas with single commas, extract important columns, output to CSV
grep -v '^#' ms_data_dirty.csv | grep -v '^$' | sed 's/,,*/,/g' | cut -d ',' -f1,2,3,4,5,6,7 > ms_data.csv

# Create insurance type file
echo 'insurance_type
Basic
Premium
Platinum' > insurance.lst

# Display summary in terminal
echo "Number of rows in cleaned data:"s
wc -l ms_data.csv

echo "Preview of cleaned data:"
head -n 8 ms_data.csv