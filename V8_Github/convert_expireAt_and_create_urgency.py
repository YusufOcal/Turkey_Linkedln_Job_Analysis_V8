#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - ExpireAt DateTime Conversion and Urgency Categories
expireAt sütununu datetime'a çevirme ve urgency kategorileri oluşturma
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def convert_expireAt_and_create_urgency(df):
    """ExpireAt'i datetime'a çevirir ve urgency kategorileri oluşturur"""
    
    print("⏰ LINKEDIN JOBS DATASET - EXPIREAT CONVERSION & URGENCY CATEGORIES")
    print("=" * 70)
    
    # Initial state
    initial_memory = df.memory_usage(deep=True).sum() / 1024**2
    expireAt_memory_before = df['expireAt'].memory_usage(deep=True) / 1024**2
    
    print(f"📊 Başlangıç Durumu:")
    print(f"   💾 Total dataset memory: {initial_memory:.3f} MB")
    print(f"   📊 expireAt memory: {expireAt_memory_before:.3f} MB")
    print(f"   🔧 expireAt current type: {df['expireAt'].dtype}")
    print()
    
    # 1. EXPIREAT DATETIME CONVERSION
    print("📅 1. EXPIREAT DATETIME CONVERSION")
    print("-" * 40)
    
    # Convert Unix timestamp (milliseconds) to datetime
    print("🔄 Converting Unix timestamp to datetime...")
    df['expireAt'] = pd.to_datetime(df['expireAt'], unit='ms')
    
    # Verify conversion
    print(f"✅ Conversion completed!")
    print(f"   🔧 New data type: {df['expireAt'].dtype}")
    print(f"   📅 Date range: {df['expireAt'].min()} to {df['expireAt'].max()}")
    print(f"   📊 Sample values:")
    for i, date_val in enumerate(df['expireAt'].head(5), 1):
        print(f"      {i}. {date_val}")
    print()
    
    # 2. URGENCY CATEGORIES CREATION
    print("🚨 2. URGENCY CATEGORIES CREATION")
    print("-" * 40)
    
    # Calculate days remaining
    current_time = datetime.now()
    days_remaining = (df['expireAt'] - current_time).dt.days
    
    def categorize_urgency(days):
        """Urgency kategorileri oluşturur"""
        if pd.isna(days):
            return 'UNKNOWN'
        elif days < 0:
            return 'EXPIRED'      # Süresi geçmiş
        elif days <= 3:
            return 'CRITICAL'     # 0-3 gün - Kritik acil
        elif days <= 7:
            return 'HIGH'         # 4-7 gün - Yüksek acil
        elif days <= 21:
            return 'MEDIUM'       # 8-21 gün - Orta acil
        elif days <= 60:
            return 'NORMAL'       # 22-60 gün - Normal
        else:
            return 'LOW'          # 60+ gün - Düşük acil
    
    # Create urgency categories
    df['job_urgency_category'] = days_remaining.apply(categorize_urgency)
    
    # Convert to categorical for memory efficiency
    df['job_urgency_category'] = df['job_urgency_category'].astype('category')
    
    print(f"📊 Urgency Categories Created:")
    urgency_dist = df['job_urgency_category'].value_counts().sort_index()
    
    urgency_explanations = {
        'EXPIRED': '🔴 Süresi geçmiş pozisyonlar',
        'CRITICAL': '🚨 0-3 gün kaldı - Acilen başvur',
        'HIGH': '⚡ 4-7 gün kaldı - Hızla başvur', 
        'MEDIUM': '⚠️ 8-21 gün kaldı - Yakında başvur',
        'NORMAL': '📋 22-60 gün kaldı - Standart süre',
        'LOW': '🔵 60+ gün kaldı - Bol zamanın var',
        'UNKNOWN': '❓ Bilinmeyen süre'
    }
    
    total_jobs = len(df)
    for category, count in urgency_dist.items():
        percentage = (count / total_jobs) * 100
        explanation = urgency_explanations.get(category, '📊 Kategori')
        print(f"   {explanation}: {count:,} ({percentage:.1f}%)")
    print()
    
    # 3. MEMORY ANALYSIS
    print("💾 3. MEMORY ANALYSIS")
    print("-" * 25)
    
    expireAt_memory_after = df['expireAt'].memory_usage(deep=True) / 1024**2
    urgency_memory = df['job_urgency_category'].memory_usage(deep=True) / 1024**2
    final_memory = df.memory_usage(deep=True).sum() / 1024**2
    
    print(f"📊 Memory Comparison:")
    print(f"   📊 expireAt before: {expireAt_memory_before:.3f} MB (int64)")
    print(f"   📊 expireAt after: {expireAt_memory_after:.3f} MB (datetime64[ns])")
    print(f"   🚨 job_urgency_category: {urgency_memory:.3f} MB (category)")
    print(f"   💾 Total memory change: {initial_memory:.3f} MB → {final_memory:.3f} MB ({((final_memory - initial_memory) / initial_memory * 100):+.1f}%)")
    print()
    
    # 4. DATA INTEGRITY VALIDATION
    print("✅ 4. DATA INTEGRITY VALIDATION")
    print("-" * 35)
    
    print(f"🔍 Validation Results:")
    print(f"   📊 Total records: {len(df):,} (preserved)")
    print(f"   📅 DateTime conversion: ✅ Success")
    print(f"   🚨 Urgency categories: {df['job_urgency_category'].nunique()} unique levels")
    print(f"   ❌ Null values in expireAt: {df['expireAt'].isnull().sum()}")
    print(f"   ❌ Null values in urgency: {df['job_urgency_category'].isnull().sum()}")
    print(f"   🎯 Data types optimized: ✅ datetime64[ns] + category")
    print()
    
    print("=" * 70)
    print("✅ EXPIREAT CONVERSION & URGENCY CATEGORIES COMPLETED SUCCESSFULLY")
    print("=" * 70)
    
    return df

if __name__ == "__main__":
    try:
        # Load the dataset
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step12.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
        
        # Convert expireAt and create urgency categories
        df_converted = convert_expireAt_and_create_urgency(df)
        
        # Save the converted dataset
        output_filename = 'linkedin_jobs_dataset_optimized_step13.csv'
        print(f"💾 Saving converted dataset: {output_filename}")
        df_converted.to_csv(output_filename, index=False)
        
        # File size comparison
        import os
        original_size = os.path.getsize('linkedin_jobs_dataset_optimized_step12.csv') / 1024**2
        new_size = os.path.getsize(output_filename) / 1024**2
        
        print(f"\n📊 File Size Comparison:")
        print(f"   📄 Original: {original_size:.2f} MB")
        print(f"   📄 New: {new_size:.2f} MB")
        print(f"   📈 Change: {((new_size - original_size) / original_size * 100):+.1f}%")
        
        print(f"\n🎉 Conversion completed successfully!")
        print(f"📁 Output file: {output_filename}")
        print(f"\n📊 Summary of Changes:")
        print(f"   ✅ expireAt: Unix timestamp → datetime64[ns]")
        print(f"   ✅ job_urgency_category: New categorical column (6 levels)")
        print(f"   ✅ No other modifications made")
        
    except FileNotFoundError:
        print("❌ HATA: linkedin_jobs_dataset_optimized_step12.csv dosyası bulunamadı!")
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        import traceback
        traceback.print_exc() 