#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Logo URL to Boolean Conversion
company_logo_url → has_company_logo (boolean) + URL column deletion
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def convert_logo_to_boolean(df):
    """Logo URL sütununu boolean flag'e çevir ve URL sütununu sil"""
    
    print("🎯 LINKEDIN JOBS DATASET - LOGO URL TO BOOLEAN CONVERSION")
    print("=" * 65)
    
    logo_url_column = 'company_logo_url'
    new_boolean_column = 'has_company_logo'
    
    # Check if logo URL column exists
    if logo_url_column not in df.columns:
        print(f"❌ HATA: {logo_url_column} sütunu bulunamadı!")
        return None
    
    # 1. MEVCUT SÜTUN ANALİZİ
    print("📊 1. MEVCUT SÜTUN ANALİZİ")
    print("-" * 28)
    
    logo_data = df[logo_url_column]
    
    # Current statistics
    total_rows = len(logo_data)
    null_count = logo_data.isnull().sum()
    non_null_count = total_rows - null_count
    null_percentage = (null_count / total_rows) * 100
    unique_count = logo_data.nunique()
    current_memory = logo_data.memory_usage(deep=True) / 1024**2
    
    # URL length analysis
    if non_null_count > 0:
        url_lengths = logo_data.dropna().astype(str).str.len()
        avg_url_length = url_lengths.mean()
        total_characters = url_lengths.sum()
    else:
        avg_url_length = 0
        total_characters = 0
    
    print(f"📋 {logo_url_column} (CURRENT):")
    print(f"   📊 Total rows: {total_rows:,}")
    print(f"   ✅ Non-null (has logo): {non_null_count:,} ({100-null_percentage:.1f}%)")
    print(f"   ❌ Null (no logo): {null_count:,} ({null_percentage:.1f}%)")
    print(f"   🎯 Unique URLs: {unique_count:,}")
    print(f"   💾 Current memory: {current_memory:.2f} MB")
    print(f"   📏 Avg URL length: {avg_url_length:.0f} characters")
    print(f"   📝 Total characters stored: {total_characters:,}")
    print()
    
    # 2. BOOLEAN CONVERSION LOGIC
    print("🔄 2. BOOLEAN CONVERSION LOGIC")
    print("-" * 30)
    
    print("📋 Conversion Rules:")
    print("   ✅ Non-null URL → True (company has logo)")
    print("   ❌ Null URL → False (company has no logo)")
    print("   🎯 Data Type: boolean (True/False)")
    print()
    
    # Create boolean column
    df_converted = df.copy()
    df_converted[new_boolean_column] = df_converted[logo_url_column].notna()
    
    # 3. BOOLEAN COLUMN VERIFICATION
    print("✅ 3. BOOLEAN COLUMN VERIFICATION")
    print("-" * 35)
    
    new_boolean_data = df_converted[new_boolean_column]
    
    # Verify conversion
    true_count = (new_boolean_data == True).sum()
    false_count = (new_boolean_data == False).sum()
    
    print(f"📊 Boolean Conversion Results:")
    print(f"   ✅ True (has logo): {true_count:,}")
    print(f"   ❌ False (no logo): {false_count:,}")
    print(f"   📈 True percentage: {(true_count/total_rows)*100:.1f}%")
    print(f"   📈 False percentage: {(false_count/total_rows)*100:.1f}%")
    
    # Verification check
    if true_count == non_null_count and false_count == null_count:
        print(f"   ✅ VERIFICATION PASSED: Perfect conversion!")
    else:
        print(f"   ❌ VERIFICATION FAILED: Conversion error!")
        return None
    
    # 4. MEMORY OPTIMIZATION ANALYSIS
    print(f"\n💾 4. MEMORY OPTIMIZATION ANALYSIS")
    print("-" * 35)
    
    # Boolean column memory
    boolean_memory = new_boolean_data.memory_usage(deep=True) / 1024**2
    memory_savings = current_memory - boolean_memory
    memory_reduction_pct = (memory_savings / current_memory) * 100
    
    print(f"📊 Memory Comparison:")
    print(f"   📋 Original URL column: {current_memory:.2f} MB")
    print(f"   📋 New boolean column: {boolean_memory:.2f} MB")
    print(f"   💰 Memory savings: {memory_savings:.2f} MB")
    print(f"   📈 Memory reduction: {memory_reduction_pct:.1f}%")
    
    # Storage efficiency analysis
    original_bytes_per_record = current_memory * 1024**2 / total_rows
    boolean_bytes_per_record = boolean_memory * 1024**2 / total_rows
    
    print(f"\n📏 Storage Efficiency:")
    print(f"   📋 Original: {original_bytes_per_record:.1f} bytes/record")
    print(f"   📋 Boolean: {boolean_bytes_per_record:.1f} bytes/record")
    print(f"   ⚡ Efficiency gain: {original_bytes_per_record/boolean_bytes_per_record:.1f}x")
    
    # 5. DELETE ORIGINAL URL COLUMN
    print(f"\n🗑️ 5. DELETE ORIGINAL URL COLUMN")
    print("-" * 32)
    
    print(f"🗑️ Deleting {logo_url_column}...")
    df_final = df_converted.drop(columns=[logo_url_column])
    
    print(f"✅ Column deleted successfully!")
    print(f"📊 Schema change: {len(df.columns)} → {len(df_final.columns)} columns (-1)")
    print(f"💾 Memory freed: {current_memory:.2f} MB")
    
    # 6. FINAL OPTIMIZATION STATISTICS
    print(f"\n📊 6. FINAL OPTIMIZATION STATISTICS")
    print("-" * 38)
    
    final_boolean_data = df_final[new_boolean_column]
    final_memory = final_boolean_data.memory_usage(deep=True) / 1024**2
    
    print(f"📋 {new_boolean_column} (FINAL):")
    print(f"   📊 Total records: {len(final_boolean_data):,}")
    print(f"   ✅ True values: {(final_boolean_data == True).sum():,}")
    print(f"   ❌ False values: {(final_boolean_data == False).sum():,}")
    print(f"   🔧 Data type: {final_boolean_data.dtype}")
    print(f"   💾 Memory usage: {final_memory:.2f} MB")
    print(f"   📈 Coverage: {(final_boolean_data.sum()/len(final_boolean_data))*100:.1f}%")
    
    # 7. BUSINESS IMPACT ANALYSIS
    print(f"\n💰 7. BUSINESS IMPACT ANALYSIS")
    print("-" * 30)
    
    business_insights = []
    
    # Information preservation
    print(f"🎯 Information Preservation:")
    print(f"   ✅ Logo availability status: 100% preserved")
    print(f"   ✅ Business logic: Fully maintained")
    print(f"   ✅ Analytics capability: Enhanced (boolean operations)")
    
    business_insights.append("Complete information preservation with improved efficiency")
    
    # Analytics advantages
    print(f"\n📊 Analytics Advantages:")
    print(f"   ⚡ Faster boolean queries (has_logo = True)")
    print(f"   📈 Easier aggregations (SUM, COUNT operations)")
    print(f"   🔍 Simpler filtering and grouping")
    print(f"   📊 Direct percentage calculations")
    
    business_insights.append("Enhanced analytics performance with boolean operations")
    
    # Storage benefits
    print(f"\n💾 Storage Benefits:")
    print(f"   📦 {memory_reduction_pct:.1f}% memory reduction")
    print(f"   ⚡ {original_bytes_per_record/boolean_bytes_per_record:.1f}x storage efficiency")
    print(f"   🚀 Faster column operations")
    print(f"   💰 Reduced storage costs")
    
    business_insights.append("Massive storage optimization with maintained functionality")
    
    # 8. BUSINESS RECOMMENDATIONS
    print(f"\n💡 8. BUSINESS RECOMMENDATIONS")
    print("-" * 35)
    
    recommendations = [
        "🎯 Use has_company_logo for company profile completeness scoring",
        "📊 Create branding analytics dashboards with boolean aggregations", 
        "⚡ Implement fast logo availability filters in applications",
        "📈 Track branding coverage trends with time-series analysis",
        "🔍 Use for A/B testing: logo presence vs user engagement",
        "💰 Apply cost-benefit analysis: logo ROI measurement"
    ]
    
    print(f"📋 Actionable Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # 9. QUERY EXAMPLES
    print(f"\n🔍 9. OPTIMIZED QUERY EXAMPLES")
    print("-" * 32)
    
    print(f"📊 Boolean Query Examples:")
    print(f"   • Companies with logos: df[df.has_company_logo == True]")
    print(f"   • Logo coverage rate: df.has_company_logo.mean()")
    print(f"   • Companies without logos: df[~df.has_company_logo]")
    print(f"   • Industry logo stats: df.groupby('industry').has_company_logo.mean()")
    print(f"   • Logo count: df.has_company_logo.sum()")
    
    print(f"\n✅ LOGO URL TO BOOLEAN CONVERSION COMPLETED!")
    
    return df_final, {
        'original_memory': current_memory,
        'new_memory': final_memory,
        'memory_savings': memory_savings,
        'memory_reduction_pct': memory_reduction_pct,
        'true_count': true_count,
        'false_count': false_count,
        'business_insights': business_insights,
        'recommendations': recommendations
    }

def main():
    """Ana conversion fonksiyonu"""
    
    print("🎯 LinkedIn Jobs Dataset - Logo URL to Boolean Optimization")
    print("=" * 65)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step4.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # Logo URL to boolean conversion
    result = convert_logo_to_boolean(df)
    
    if result is not None:
        df_optimized, stats = result
        
        # Save optimized dataset
        output_filename = 'linkedin_jobs_dataset_optimized_step5.csv'
        df_optimized.to_csv(output_filename, index=False)
        
        print(f"\n💾 OPTIMIZED DATASET SAVED:")
        print(f"   📁 File: {output_filename}")
        print(f"   📊 Rows: {len(df_optimized):,}")
        print(f"   📊 Columns: {len(df_optimized.columns)}")
        
        # File size comparison
        import os
        if os.path.exists('linkedin_jobs_dataset_optimized_step4.csv'):
            original_size = os.path.getsize('linkedin_jobs_dataset_optimized_step4.csv') / 1024**2
            new_size = os.path.getsize(output_filename) / 1024**2
            size_reduction = original_size - new_size
            
            print(f"   💾 File size: {original_size:.1f} → {new_size:.1f} MB (-{size_reduction:.1f} MB)")
            print(f"   📈 File reduction: {(size_reduction/original_size)*100:.1f}%")
        
        print(f"\n🎯 CONVERSION SUMMARY:")
        print(f"   💾 Memory optimization: {stats['memory_reduction_pct']:.1f}% reduction")
        print(f"   ✅ Companies with logos: {stats['true_count']:,}")
        print(f"   ❌ Companies without logos: {stats['false_count']:,}")
        print(f"   📊 Logo coverage: {(stats['true_count']/(stats['true_count']+stats['false_count']))*100:.1f}%")
        
        print(f"\n🚀 BOOLEAN OPTIMIZATION COMPLETED!")

if __name__ == "__main__":
    main() 