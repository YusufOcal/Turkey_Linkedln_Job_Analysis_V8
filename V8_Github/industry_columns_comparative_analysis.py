#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Industry Columns Comparative Analysis
company/industry/0 vs formattedIndustries/0,1,2 karşılaştırmalı analiz
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def analyze_industry_columns_comparative(df):
    """Industry sütunları arasında kapsamlı karşılaştırmalı analiz"""
    
    print("🏭 LINKEDIN JOBS DATASET - INDUSTRY COLUMNS COMPARATIVE ANALYSIS")
    print("=" * 80)
    
    # Target columns
    industry_columns = [
        'company/industry/0',
        'formattedIndustries/0', 
        'formattedIndustries/1',
        'formattedIndustries/2'
    ]
    
    # Verify columns exist
    existing_columns = [col for col in industry_columns if col in df.columns]
    missing_columns = [col for col in industry_columns if col not in df.columns]
    
    print(f"🔍 COLUMN EXISTENCE CHECK")
    print("-" * 30)
    print(f"✅ Mevcut sütunlar: {len(existing_columns)}")
    for col in existing_columns:
        print(f"   📋 {col}")
    
    if missing_columns:
        print(f"❌ Eksik sütunlar: {len(missing_columns)}")
        for col in missing_columns:
            print(f"   ⚠️ {col}")
    print()
    
    if len(existing_columns) < 2:
        print("❌ HATA: Karşılaştırma için en az 2 sütun gerekli!")
        return None
    
    # 1. SÜTUN TEMSİLLERİ VE ANLAMI
    print("📋 1. SÜTUN TEMSİLLERİ VE ANLAMI")
    print("-" * 40)
    
    column_purposes = {
        'company/industry/0': {
            'purpose': 'Primary Company Industry Classification',
            'content': 'Ana şirket sektör kategorisi (LinkedIn company profile)',
            'business_value': 'Company sector analysis, market segmentation',
            'expected_type': 'Categorical (object/category)',
            'source': 'LinkedIn Company API - Primary industry field'
        },
        'formattedIndustries/0': {
            'purpose': 'Primary Formatted Industry (Job-level)',
            'content': 'İş ilanı seviyesinde formatlanmış birincil sektör',
            'business_value': 'Job industry classification, role categorization',
            'expected_type': 'Categorical (object/category)', 
            'source': 'LinkedIn Jobs API - Job posting industry'
        },
        'formattedIndustries/1': {
            'purpose': 'Secondary Formatted Industry (Job-level)',
            'content': 'İş ilanı seviyesinde formatlanmış ikincil sektör',
            'business_value': 'Multi-sector companies, cross-industry roles',
            'expected_type': 'Categorical (object/category)',
            'source': 'LinkedIn Jobs API - Secondary industry tag'
        },
        'formattedIndustries/2': {
            'purpose': 'Tertiary Formatted Industry (Job-level)',
            'content': 'İş ilanı seviyesinde formatlanmış üçüncül sektör',
            'business_value': 'Complex industry categorization',
            'expected_type': 'Categorical (object/category)',
            'source': 'LinkedIn Jobs API - Tertiary industry tag'
        }
    }
    
    for col in existing_columns:
        if col in column_purposes:
            info = column_purposes[col]
            print(f"🏭 {col}:")
            print(f"   📝 Purpose: {info['purpose']}")
            print(f"   💼 Content: {info['content']}")
            print(f"   🎯 Business Value: {info['business_value']}")
            print(f"   📊 Expected Type: {info['expected_type']}")
            print(f"   🔗 Source: {info['source']}")
            print()
    
    # 2. TEMEL İSTATİSTİKLER KARŞILAŞTIRMASI
    print("📊 2. TEMEL İSTATİSTİKLER KARŞILAŞTIRMASI")
    print("-" * 45)
    
    stats_comparison = {}
    
    for col in existing_columns:
        col_data = df[col]
        total_rows = len(col_data)
        null_count = col_data.isnull().sum()
        non_null_count = total_rows - null_count
        null_percentage = (null_count / total_rows) * 100
        unique_count = len(col_data.dropna().unique()) if non_null_count > 0 else 0
        
        stats_comparison[col] = {
            'total_rows': total_rows,
            'null_count': null_count,
            'non_null_count': non_null_count,
            'null_percentage': null_percentage,
            'unique_count': unique_count,
            'data_type': str(col_data.dtype)
        }
        
        print(f"📋 {col}:")
        print(f"   📊 Null: {null_count:,} ({null_percentage:.1f}%)")
        print(f"   ✅ Dolu: {non_null_count:,} ({100-null_percentage:.1f}%)")
        print(f"   🎯 Benzersiz: {unique_count:,}")
        print(f"   🔧 Tip: {col_data.dtype}")
        print()
    
    # 3. İÇERİK OVERLAP ANALİZİ (KRİTİK!)
    print("🔍 3. İÇERİK OVERLAP ANALİZİ (DUPLICATE DETECTION)")
    print("-" * 55)
    
    # Her sütun için unique values topla
    unique_values_by_column = {}
    all_values_combined = set()
    
    for col in existing_columns:
        non_null_data = df[col].dropna()
        unique_vals = set(non_null_data.astype(str).str.strip().str.lower())
        unique_values_by_column[col] = unique_vals
        all_values_combined.update(unique_vals)
        
        print(f"📊 {col}:")
        print(f"   🎯 Benzersiz değer sayısı: {len(unique_vals)}")
        if len(unique_vals) > 0:
            # Top 5 values
            value_counts = non_null_data.value_counts()
            print(f"   📈 En sık 3 değer:")
            for i, (val, count) in enumerate(value_counts.head(3).items(), 1):
                pct = (count / len(non_null_data)) * 100
                print(f"      {i}. '{val}' ({count:,}, {pct:.1f}%)")
        print()
    
    # Cross-column overlap analysis
    print("🔗 CROSS-COLUMN OVERLAP ANALYSIS:")
    print("-" * 35)
    
    overlap_matrix = {}
    for i, col1 in enumerate(existing_columns):
        for j, col2 in enumerate(existing_columns):
            if i < j:  # Avoid duplicate comparisons
                set1 = unique_values_by_column[col1]
                set2 = unique_values_by_column[col2]
                
                if len(set1) > 0 and len(set2) > 0:
                    overlap = set1 & set2
                    overlap_count = len(overlap)
                    overlap_pct1 = (overlap_count / len(set1)) * 100
                    overlap_pct2 = (overlap_count / len(set2)) * 100
                    
                    overlap_matrix[f"{col1}_vs_{col2}"] = {
                        'overlap_count': overlap_count,
                        'overlap_pct_col1': overlap_pct1,
                        'overlap_pct_col2': overlap_pct2,
                        'common_values': list(overlap)[:5]  # First 5 for display
                    }
                    
                    print(f"📊 {col1.split('/')[-1]} vs {col2.split('/')[-1]}:")
                    print(f"   🔗 Ortak değer: {overlap_count}")
                    print(f"   📈 Overlap: {overlap_pct1:.1f}% vs {overlap_pct2:.1f}%")
                    
                    if overlap_count > 0:
                        print(f"   📋 Örnek ortak değerler: {', '.join(list(overlap)[:3])}")
                    
                    # Critical overlap assessment
                    if overlap_pct1 > 80 or overlap_pct2 > 80:
                        print(f"   🚨 KRİTİK: Yüksek overlap detected! DUPLICATE CANDIDATE")
                    elif overlap_pct1 > 50 or overlap_pct2 > 50:
                        print(f"   ⚠️ UYARI: Orta seviye overlap - consolidation consider")
                    print()
    
    # 4. ACTUAL DATA COMPARISON (RECORD LEVEL)
    print("🎯 4. RECORD-LEVEL DATA COMPARISON")
    print("-" * 35)
    
    # Sample records comparison
    sample_size = min(100, len(df))
    sample_df = df[existing_columns].head(sample_size)
    
    identical_records = 0
    partial_matches = 0
    
    for idx, row in sample_df.iterrows():
        non_null_values = [str(val).strip().lower() for val in row.dropna()]
        unique_non_null = set(non_null_values)
        
        if len(non_null_values) > 1:
            if len(unique_non_null) == 1:
                identical_records += 1
            elif len(unique_non_null) < len(non_null_values):
                partial_matches += 1
    
    print(f"📊 Sample analysis ({sample_size} records):")
    print(f"   🔄 Completely identical records: {identical_records}")
    print(f"   ⚡ Partial match records: {partial_matches}")
    print(f"   📈 Complete duplication rate: {(identical_records/sample_size)*100:.1f}%")
    print(f"   📈 Partial duplication rate: {(partial_matches/sample_size)*100:.1f}%")
    print()
    
    # 5. FORMAT TUTARSIZLIKLARI
    print("🔧 5. FORMAT TUTARSIZLIKLARI VE STANDARDIZATION")
    print("-" * 50)
    
    format_issues = {}
    
    for col in existing_columns:
        non_null_data = df[col].dropna()
        if len(non_null_data) > 0:
            # Case variations
            original_unique = len(non_null_data.unique())
            normalized_unique = len(non_null_data.str.lower().unique())
            case_variations = original_unique - normalized_unique
            
            # Special characters
            special_chars = non_null_data.str.contains(r'[^\w\s\-\&\.]', regex=True, na=False).sum()
            
            # Length variations (potential formatting issues)
            lengths = non_null_data.astype(str).str.len()
            length_stats = {
                'min': lengths.min(),
                'max': lengths.max(),
                'mean': lengths.mean(),
                'std': lengths.std()
            }
            
            format_issues[col] = {
                'case_variations': case_variations,
                'special_chars': special_chars,
                'length_stats': length_stats
            }
            
            print(f"🔧 {col}:")
            print(f"   🔤 Case variations: {case_variations}")
            print(f"   🔧 Special characters: {special_chars}")
            print(f"   📏 Length: {length_stats['min']}-{length_stats['max']} (avg: {length_stats['mean']:.1f})")
            
            if case_variations > 0:
                print(f"   ⚠️ Case standardization needed")
            if length_stats['std'] > 10:
                print(f"   ⚠️ High length variation - format inconsistency")
            print()
    
    # 6. CONSOLIDATION ÖNERILER
    print("💡 6. CONSOLIDATION VE OPTIMIZATION ÖNERİLERİ")
    print("-" * 50)
    
    recommendations = []
    
    # Analyze hierarchy pattern (0,1,2 sequence)
    formatted_industries = [col for col in existing_columns if 'formattedIndustries' in col]
    if len(formatted_industries) > 1:
        print("🔍 FormattedIndustries Hierarchy Analysis:")
        
        for i, col in enumerate(formatted_industries):
            non_null_count = stats_comparison[col]['non_null_count']
            null_pct = stats_comparison[col]['null_percentage']
            print(f"   📊 {col}: {non_null_count:,} ({100-null_pct:.1f}% dolu)")
        
        # Check hierarchical pattern
        if len(formatted_industries) == 3:
            col0_count = stats_comparison['formattedIndustries/0']['non_null_count']
            col1_count = stats_comparison['formattedIndustries/1']['non_null_count']
            col2_count = stats_comparison['formattedIndustries/2']['non_null_count']
            
            if col0_count > col1_count > col2_count:
                print("   ✅ Expected hierarchy pattern detected (0>1>2)")
                recommendations.append("🔗 Consolidate formattedIndustries into single column")
            else:
                print("   ⚠️ Unexpected hierarchy pattern")
        print()
    
    # Company vs Job level comparison
    if 'company/industry/0' in existing_columns and 'formattedIndustries/0' in existing_columns:
        company_industry = unique_values_by_column['company/industry/0']
        job_industry = unique_values_by_column['formattedIndustries/0']
        
        overlap = company_industry & job_industry
        overlap_pct = (len(overlap) / max(len(company_industry), len(job_industry))) * 100
        
        print("🏢 Company vs Job Industry Comparison:")
        print(f"   📊 Company unique: {len(company_industry)}")
        print(f"   📊 Job unique: {len(job_industry)}")
        print(f"   🔗 Overlap: {len(overlap)} ({overlap_pct:.1f}%)")
        
        if overlap_pct > 80:
            recommendations.append("🚨 HIGH REDUNDANCY: Consider deleting one industry source")
        elif overlap_pct > 50:
            recommendations.append("⚠️ MODERATE REDUNDANCY: Evaluate consolidation")
        print()
    
    # Memory optimization potential
    total_memory = sum(df[col].memory_usage(deep=True) for col in existing_columns) / 1024**2
    print(f"💾 Total memory usage: {total_memory:.2f} MB")
    
    # Category conversion potential
    for col in existing_columns:
        unique_count = stats_comparison[col]['unique_count']
        if unique_count < 100:
            potential_savings = df[col].memory_usage(deep=True) * 0.7 / 1024**2
            recommendations.append(f"🔧 Convert {col} to category (save ~{potential_savings:.2f} MB)")
    
    print("📋 FINAL RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    # 7. ACTION PRIORITY ASSESSMENT
    print(f"\n🎯 ACTION PRIORITY ASSESSMENT:")
    print("-" * 30)
    
    # Calculate redundancy score
    high_overlap_pairs = [k for k, v in overlap_matrix.items() 
                         if v['overlap_pct_col1'] > 80 or v['overlap_pct_col2'] > 80]
    
    if len(high_overlap_pairs) > 0:
        priority = "🔴 HIGH - Immediate consolidation required"
        action = "DELETE or MERGE redundant columns"
    elif len([k for k, v in overlap_matrix.items() 
             if v['overlap_pct_col1'] > 50 or v['overlap_pct_col2'] > 50]) > 0:
        priority = "🟠 MEDIUM - Evaluate consolidation benefits"
        action = "ANALYZE business value difference"
    else:
        priority = "🟢 LOW - Optimize data types only"
        action = "CONVERT to category type for memory efficiency"
    
    print(f"   {priority}")
    print(f"   💡 Recommended action: {action}")
    
    print("\n" + "=" * 80)
    
    return {
        'existing_columns': existing_columns,
        'stats_comparison': stats_comparison,
        'overlap_matrix': overlap_matrix,
        'format_issues': format_issues,
        'recommendations': recommendations,
        'total_memory_mb': total_memory
    }

def main():
    """Ana analiz fonksiyonu"""
    
    print("🔍 LinkedIn Jobs Dataset - Industry Columns Comparative Analysis")
    print("=" * 70)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step2.csv')
        print(f"✅ Optimized dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # Karşılaştırmalı analiz gerçekleştir
    result = analyze_industry_columns_comparative(df)
    
    if result:
        print("🎯 KARŞILAŞTIRMALI ANALİZ TAMAMLANDI!")
        print(f"📊 Analiz edilen sütun sayısı: {len(result['existing_columns'])}")
        print(f"💾 Toplam memory kullanımı: {result['total_memory_mb']:.2f} MB")
        
        # Critical findings
        high_overlap = any(v['overlap_pct_col1'] > 80 or v['overlap_pct_col2'] > 80 
                          for v in result['overlap_matrix'].values())
        
        if high_overlap:
            print("🚨 KRİTİK: High overlap detected - CONSOLIDATION REQUIRED!")
        else:
            print("✅ Overlap seviyeleri kabul edilebilir")

if __name__ == "__main__":
    main() 