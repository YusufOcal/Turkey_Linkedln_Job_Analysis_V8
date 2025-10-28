import pandas as pd
import os

def process_column_deletions():
    """
    Read fixed_all_company_colums.csv, delete specified columns, 
    and save in 3 formats with same names
    """
    
    # Read the CSV file
    input_file = "fixed_all_company_colums.csv"
    
    print(f"Reading {input_file}...")
    df = pd.read_csv(input_file)
    
    print(f"Initial dataset: {len(df)} records, {len(df.columns)} columns")
    
    # Columns to delete
    columns_to_delete = [
        'companyLinkedinUrl',
        'jobState', 
        'salaryInsights/salaryExplorerUrl',
        'company/universalName'
    ]
    
    # Check which columns exist before deletion
    existing_columns = []
    missing_columns = []
    
    for col in columns_to_delete:
        if col in df.columns:
            existing_columns.append(col)
        else:
            missing_columns.append(col)
    
    print(f"\nColumns to delete: {len(columns_to_delete)}")
    print(f"Found columns: {len(existing_columns)} - {existing_columns}")
    
    if missing_columns:
        print(f"Missing columns: {len(missing_columns)} - {missing_columns}")
    
    # Delete existing columns
    if existing_columns:
        df = df.drop(columns=existing_columns)
        print(f"\nDeleted {len(existing_columns)} columns successfully")
    
    print(f"Final dataset: {len(df)} records, {len(df.columns)} columns")
    
    # Save in all 3 formats with same names
    print(f"\nSaving files...")
    
    # CSV
    csv_file = "fixed_all_company_colums.csv"
    df.to_csv(csv_file, index=False)
    csv_size = os.path.getsize(csv_file) / (1024*1024)
    print(f"✅ {csv_file} - {csv_size:.2f} MB")
    
    # JSON
    json_file = "fixed_all_company_colums.json"
    df.to_json(json_file, orient='records', indent=2)
    json_size = os.path.getsize(json_file) / (1024*1024)
    print(f"✅ {json_file} - {json_size:.2f} MB")
    
    # Excel
    xlsx_file = "fixed_all_company_colums.xlsx"
    df.to_excel(xlsx_file, index=False, engine='openpyxl')
    xlsx_size = os.path.getsize(xlsx_file) / (1024*1024)
    print(f"✅ {xlsx_file} - {xlsx_size:.2f} MB")
    
    print(f"\n🎯 Column deletion and file generation completed successfully!")
    print(f"📊 Data integrity: {len(df)} records maintained across all formats")

if __name__ == "__main__":
    process_column_deletions() 