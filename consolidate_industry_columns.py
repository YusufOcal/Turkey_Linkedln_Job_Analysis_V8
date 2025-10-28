#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Industry Columns Consolidation
Eksiksiz birleştirme: formattedIndustries/0,1,2 → industries (consolidated)
Silme: company/industry/0 (redundant)
"""

import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def consolidate_industry_columns(df):
    """Industry sütunlarını eksiksiz birleştir ve optimize et"""
    
    print("🔧 LINKEDIN JOBS DATASET - INDUSTRY CONSOLIDATION")
    print("=" * 60)
    
    # Target columns
    formatted_cols = ['formattedIndustries/0', 'formattedIndustries/1', 'formattedIndustries/2']
    company_col = 'company/industry/0'
    
    # Verify columns exist
    missing_cols = [col for col in formatted_cols + [company_col] if col not in df.columns]
    if missing_cols:
        print(f"❌ HATA: Eksik sütunlar: {missing_cols}")
        return None
    
    print("📋 BAŞLANGIÇ DURUMU:")
    print("-" * 25)
    
    initial_stats = {}
    total_initial_memory = 0
    
    for col in formatted_cols + [company_col]:
        null_count = df[col].isnull().sum()
        non_null_count = len(df) - null_count
        null_pct = (null_count / len(df)) * 100
        memory_mb = df[col].memory_usage(deep=True) / 1024**2
        total_initial_memory += memory_mb
        
        initial_stats[col] = {
            'null_count': null_count,
            'non_null_count': non_null_count,
            'null_pct': null_pct,
            'memory_mb': memory_mb
        }
        
        print(f"📊 {col.split('/')[-1]}: {non_null_count:,} dolu ({100-null_pct:.1f}%)")
    
    print(f"💾 Toplam memory: {total_initial_memory:.2f} MB")
    print()
    
    # 1. EKSIKSIZ CONSOLIDATION STRATEGY
    print("🔗 1. EKSIKSIZ CONSOLIDATION STRATEGY")
    print("-" * 40)
    
    # Create consolidated column
    df_consolidated = df.copy()
    
    def consolidate_industries_row(row):
        """Her satır için industry bilgilerini eksiksiz birleştir"""
        values = []
        
        # formattedIndustries/0,1,2 sırasıyla kontrol et
        for col in formatted_cols:
            val = row[col]
            if pd.notna(val) and str(val).strip():
                val_clean = str(val).strip()
                if val_clean not in values:  # Duplicate check
                    values.append(val_clean)
        
        if values:
            return ' | '.join(values)  # Multi-value separator
        else:
            return np.nan
    
    print("🔧 Consolidation işlemi başlatılıyor...")
    
    # Apply consolidation
    df_consolidated['industries_consolidated'] = df_consolidated[formatted_cols].apply(
        consolidate_industries_row, axis=1
    )
    
    # 2. CONSOLIDATION VERIFICATION
    print("✅ 2. CONSOLIDATION VERIFICATION")
    print("-" * 35)
    
    # Check data preservation
    original_non_null_total = sum(df[col].notna().sum() for col in formatted_cols)
    consolidated_non_null = df_consolidated['industries_consolidated'].notna().sum()
    
    # Detailed verification
    verification_stats = {}
    
    for i, col in enumerate(formatted_cols):
        # Count how many values from this column made it to consolidated
        preserved_count = 0
        for idx, row in df.iterrows():
            if pd.notna(row[col]):
                consolidated_val = df_consolidated.loc[idx, 'industries_consolidated']
                if pd.notna(consolidated_val) and str(row[col]).strip() in str(consolidated_val):
                    preserved_count += 1
        
        original_count = df[col].notna().sum()
        preservation_rate = (preserved_count / original_count * 100) if original_count > 0 else 0
        
        verification_stats[col] = {
            'original_count': original_count,
            'preserved_count': preserved_count,
            'preservation_rate': preservation_rate
        }
        
        print(f"📊 {col}:")
        print(f"   📈 Original: {original_count:,}")
        print(f"   ✅ Preserved: {preserved_count:,}")
        print(f"   📈 Rate: {preservation_rate:.1f}%")
    
    print(f"\n💯 OVERALL VERIFICATION:")
    print(f"   📊 Consolidated records: {consolidated_non_null:,}")
    print(f"   📈 Expected minimum: {max(initial_stats[col]['non_null_count'] for col in formatted_cols):,}")
    
    # Check if we preserved at least the maximum single column data
    max_single_column = max(initial_stats[col]['non_null_count'] for col in formatted_cols)
    if consolidated_non_null >= max_single_column:
        print(f"   ✅ SUCCESS: Data preservation verified!")
    else:
        print(f"   ❌ ERROR: Data loss detected!")
        return None
    
    # 3. REMOVE REDUNDANT COLUMNS
    print(f"\n🗑️ 3. REDUNDANT COLUMNS REMOVAL")
    print("-" * 35)
    
    columns_to_remove = formatted_cols + [company_col]
    
    print(f"📋 Silinecek sütunlar:")
    for col in columns_to_remove:
        memory_saved = initial_stats[col]['memory_mb']
        print(f"   🗑️ {col} (saves {memory_saved:.2f} MB)")
    
    # Remove columns
    df_final = df_consolidated.drop(columns=columns_to_remove)
    
    # 4. FINAL OPTIMIZATION
    print(f"\n🔧 4. FINAL OPTIMIZATION")
    print("-" * 25)
    
    # Convert to category for memory efficiency
    unique_count = df_final['industries_consolidated'].nunique()
    if unique_count < 1000:  # Good candidate for category
        original_memory = df_final['industries_consolidated'].memory_usage(deep=True) / 1024**2
        df_final['industries_consolidated'] = df_final['industries_consolidated'].astype('category')
        new_memory = df_final['industries_consolidated'].memory_usage(deep=True) / 1024**2
        memory_saved_cat = original_memory - new_memory
        
        print(f"📊 Category conversion:")
        print(f"   🎯 Unique values: {unique_count:,}")
        print(f"   💾 Memory saved: {memory_saved_cat:.2f} MB")
    
    # 5. FINAL STATISTICS
    print(f"\n📊 5. FINAL STATISTICS")
    print("-" * 25)
    
    final_null_count = df_final['industries_consolidated'].isnull().sum()
    final_non_null = len(df_final) - final_null_count
    final_null_pct = (final_null_count / len(df_final)) * 100
    final_memory = df_final['industries_consolidated'].memory_usage(deep=True) / 1024**2
    
    print(f"📋 industries_consolidated (NEW):")
    print(f"   📊 Null: {final_null_count:,} ({final_null_pct:.1f}%)")
    print(f"   ✅ Dolu: {final_non_null:,} ({100-final_null_pct:.1f}%)")
    print(f"   🎯 Benzersiz: {unique_count:,}")
    print(f"   💾 Memory: {final_memory:.2f} MB")
    
    # Calculate total savings
    total_memory_saved = total_initial_memory - final_memory
    columns_removed = len(columns_to_remove)
    
    print(f"\n🎯 CONSOLIDATION SUMMARY:")
    print("-" * 30)
    print(f"   📊 Columns: {len(df.columns)} → {len(df_final.columns)} (-{columns_removed})")
    print(f"   💾 Memory: {total_initial_memory:.2f} → {final_memory:.2f} MB (-{total_memory_saved:.2f} MB)")
    print(f"   📈 Memory reduction: {(total_memory_saved/total_initial_memory)*100:.1f}%")
    print(f"   🎯 Data integrity: PRESERVED (eksiksiz birleştirme)")
    
    # Sample of consolidated data
    print(f"\n📋 SAMPLE CONSOLIDATED DATA:")
    print("-" * 30)
    sample_data = df_final['industries_consolidated'].dropna().head(5)
    for i, val in enumerate(sample_data, 1):
        # Show only first 60 chars to avoid long output
        display_val = str(val)[:60] + "..." if len(str(val)) > 60 else str(val)
        print(f"   {i}. {display_val}")
    
    print(f"\n✅ CONSOLIDATION COMPLETED SUCCESSFULLY!")
    
    return df_final

def main():
    """Ana consolidation fonksiyonu"""
    
    print("🔧 LinkedIn Jobs Dataset - Industry Consolidation")
    print("=" * 55)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step2.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # Consolidation işlemini gerçekleştir
    df_consolidated = consolidate_industry_columns(df)
    
    if df_consolidated is not None:
        # Save the consolidated dataset
        output_filename = 'linkedin_jobs_dataset_optimized_step3.csv'
        df_consolidated.to_csv(output_filename, index=False)
        
        print(f"\n💾 DATASET SAVED:")
        print(f"   📁 File: {output_filename}")
        print(f"   📊 Rows: {len(df_consolidated):,}")
        print(f"   📊 Columns: {len(df_consolidated.columns)}")
        
        # File size comparison
        import os
        original_size = os.path.getsize('linkedin_jobs_dataset_optimized_step2.csv') / 1024**2
        new_size = os.path.getsize(output_filename) / 1024**2
        size_reduction = original_size - new_size
        
        print(f"   💾 Size: {original_size:.1f} → {new_size:.1f} MB (-{size_reduction:.1f} MB)")
        print(f"   📈 Size reduction: {(size_reduction/original_size)*100:.1f}%")

if __name__ == "__main__":
    main() 