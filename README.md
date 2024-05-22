# submit_variants_INCA
:warning: **Shiredata and INCA table are live database so be careful when you run the script**
## What does this script do?
`submit_variant.py` is a python script to submit the variants from csv file (output of variant workbook parser) to Shiredata (INCA table)

## What are typical use cases for this script?

This script may be executed as a standalone. It should be incorporated into variant workbook parser in the future.

## What data are required for this script to run?
**Packages**
pandas==2.2.0
pyodbc==5.1.0
numpy==1.26.4

**File inputs (required)**:
- `--input` / `--i`: input csv file name
- `-uid`: user ID to connect to the Server 
- `--password` / `-pw` : password to connect to the Server

## Command line to run
`python .\submit_variant.py -i <file> -uid <UserID> -pw <password>`

example: `python .\submit_variant.py -i "H:\SNV_all_variants.csv" -uid ABC -pw xyz`
