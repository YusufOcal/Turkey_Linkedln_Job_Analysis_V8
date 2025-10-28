#!/usr/bin/env python3
"""
STEP 1: formattedJobFunctions Consolidation - CORRECTED PIPELINE

6 job function sütununu tek sütuna birleştirir:
- formattedJobFunctions/0, /1, /2  
- jobFunctions/0, /1, /2

Output: linkedin_jobs_after_step1_job_functions.csv
"""

import pandas as pd
import numpy as np

def step1_job_functions_consolidation():
    """Step 1: Job Functions Consolidation"""
    
    print("🚀 STEP 1: formattedJobFunctions Consolidation")
    print("=" * 60)
    
    # BAŞLANGIÇ: Orijinal dataset
    input_file = 'linkedin_jobs_dataset_insights_completed.csv'
    output_file = 'linkedin_jobs_after_step1_job_functions.csv'
    
    try:
        print(f"📂 Loading original dataset: {input_file}")
        df = pd.read_csv(input_file)
        print(f"✅ Original dataset loaded: {len(df):,} records, {len(df.columns)} columns")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return False
    
    # Target columns for consolidation
    job_function_columns = [
        'formattedJobFunctions/0',
        'formattedJobFunctions/1', 
        'formattedJobFunctions/2',
        'jobFunctions/0',
        'jobFunctions/1',
        'jobFunctions/2'
    ]
    
    print(f"\n📊 PRE-CONSOLIDATION ANALYSIS:")
    existing_columns = [col for col in job_function_columns if col in df.columns]
    print(f"   • Target columns found: {len(existing_columns)}/{len(job_function_columns)}")
    
    for col in existing_columns:
        unique_count = df[col].nunique()
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        print(f"   • {col}: {unique_count} unique, {null_count:,} null (%{null_pct:.1f})")
    
    if not existing_columns:
        print("❌ No job function columns found!")
        return False
    
    # Consolidation logic
    print(f"\n🔄 CONSOLIDATION PROCESS:")
    
    def consolidate_job_functions(row):
        """Consolidate job function values into single pipe-delimited string"""
        values = []
        for col in existing_columns:
            if pd.notna(row[col]) and str(row[col]).strip():
                value = str(row[col]).strip()
                if value not in values:  # Avoid duplicates
                    values.append(value)
        return ' | '.join(values) if values else None
    
    # Create consolidated column
    df['job_functions_combined'] = df.apply(consolidate_job_functions, axis=1)
    
    # Analysis of consolidated result
    combined_count = df['job_functions_combined'].count()
    combined_unique = df['job_functions_combined'].nunique()
    combined_null = df['job_functions_combined'].isnull().sum()
    
    print(f"   ✅ Consolidated column created: job_functions_combined")
    print(f"   • Non-null records: {combined_count:,} ({(combined_count/len(df)*100):.1f}%)")
    print(f"   • Unique combinations: {combined_unique:,}")
    print(f"   • Null records: {combined_null:,} ({(combined_null/len(df)*100):.1f}%)")
    
    # Drop original columns
    print(f"\n🗑️  DROPPING ORIGINAL COLUMNS:")
    columns_before = len(df.columns)
    df_cleaned = df.drop(columns=existing_columns)
    columns_after = len(df_cleaned.columns)
    
    print(f"   • Columns before: {columns_before}")
    print(f"   • Columns after: {columns_after}")
    print(f"   • Columns eliminated: {len(existing_columns)}")
    print(f"   • Net reduction: {columns_before - columns_after} columns")
    
    # Sample analysis
    print(f"\n📋 CONSOLIDATION EXAMPLES:")
    sample_data = df_cleaned['job_functions_combined'].dropna().head(5)
    for i, value in enumerate(sample_data, 1):
        print(f"   {i}. {value}")
    
    # Save result
    df_cleaned.to_csv(output_file, index=False)
    
    print(f"\n💾 STEP 1 OUTPUT SAVED:")
    print(f"   • File: {output_file}")
    print(f"   • Records: {len(df_cleaned):,}")
    print(f"   • Columns: {len(df_cleaned.columns)}")
    
    # Memory analysis
    memory_before = df.memory_usage(deep=True).sum() / (1024*1024)
    memory_after = df_cleaned.memory_usage(deep=True).sum() / (1024*1024)
    memory_saved = memory_before - memory_after
    
    print(f"\n📊 STEP 1 PERFORMANCE METRICS:")
    print(f"   • Memory before: {memory_before:.2f} MB")
    print(f"   • Memory after: {memory_after:.2f} MB") 
    print(f"   • Memory saved: {memory_saved:.2f} MB")
    print(f"   • Consolidation efficiency: {len(existing_columns)}→1 column")
    
    print(f"\n✅ STEP 1 COMPLETED: Job Functions Consolidation")
    print(f"🎯 READY FOR STEP 2: Input file = {output_file}")
    
    return True

if __name__ == "__main__":
    success = step1_job_functions_consolidation()
    if success:
        print(f"\n🎉 Step 1 successful! Ready for Step 2.")
    else:
        print(f"\n❌ Step 1 failed!") 