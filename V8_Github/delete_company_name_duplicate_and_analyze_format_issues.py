#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Delete company/name duplicate and analyze companyName format issues
1. Delete company/name (100% duplicate)
2. Detailed format analysis of companyName standardization needs
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def delete_company_name_duplicate_and_analyze_format(df):
    """company/name sütununu sil ve companyName format issues'larını analiz et"""
    
    print("🗑️ COMPANY/NAME DUPLICATE DELETION & COMPANYNAME FORMAT ANALYSIS")
    print("=" * 75)
    
    # 1. DUPLICATE DELETION OPERATION
    print("🗑️ 1. DUPLICATE COLUMN DELETION")
    print("-" * 35)
    
    if 'company/name' in df.columns:
        # Pre-deletion stats
        original_shape = df.shape
        original_memory = df.memory_usage(deep=True).sum() / 1024**2
        column_memory = df['company/name'].memory_usage(deep=True) / 1024**2
        
        print(f"📊 Pre-deletion stats:")
        print(f"   Dataset shape: {original_shape}")
        print(f"   Total memory: {original_memory:.2f} MB")
        print(f"   company/name memory: {column_memory:.2f} MB")
        
        # Verify it's really a duplicate before deletion
        if 'companyName' in df.columns:
            both_non_null = df[(df['companyName'].notna()) & (df['company/name'].notna())]
            if len(both_non_null) > 0:
                identical_count = (both_non_null['companyName'] == both_non_null['company/name']).sum()
                duplicate_rate = (identical_count / len(both_non_null)) * 100
                print(f"   🔍 Verification: {duplicate_rate:.1f}% identical content")
                
                if duplicate_rate > 99:
                    # Safe to delete
                    df = df.drop('company/name', axis=1)
                    
                    new_shape = df.shape
                    new_memory = df.memory_usage(deep=True).sum() / 1024**2
                    memory_saved = original_memory - new_memory
                    
                    print(f"   ✅ DELETION COMPLETED!")
                    print(f"   📊 New shape: {new_shape}")
                    print(f"   💾 Memory saved: {memory_saved:.2f} MB ({memory_saved/original_memory*100:.1f}%)")
                    print(f"   🎯 Column count: {original_shape[1]} → {new_shape[1]} (-1)")
                else:
                    print(f"   ❌ DELETION CANCELLED: Not identical enough ({duplicate_rate:.1f}%)")
                    return df
            else:
                print(f"   ⚠️ No comparable records found")
        else:
            print(f"   ❌ companyName column not found for verification")
    else:
        print(f"   ⚠️ company/name column not found - already deleted?")
    
    print()
    
    # 2. COMPANYNAME FORMAT ISSUES DETAILED ANALYSIS
    print("🔧 2. COMPANYNAME FORMAT ISSUES DETAILED ANALYSIS")
    print("-" * 50)
    
    if 'companyName' not in df.columns:
        print("❌ companyName column not found!")
        return df
    
    company_data = df['companyName'].dropna()
    total_companies = len(company_data)
    
    print(f"📊 Analysis scope: {total_companies:,} company names")
    print()
    
    # 2.1 CASE PATTERN ISSUES
    print("🔤 2.1 CASE PATTERN ISSUES")
    print("-" * 25)
    
    case_issues = {
        'all_upper': company_data.str.isupper(),
        'all_lower': company_data.str.islower(),
        'title_case': company_data.str.istitle(),
        'mixed_case': ~(company_data.str.isupper() | company_data.str.islower() | company_data.str.istitle())
    }
    
    case_counts = {k: v.sum() for k, v in case_issues.items()}
    
    print(f"📋 Case Distribution:")
    for case_type, count in case_counts.items():
        percentage = (count / total_companies) * 100
        print(f"   {case_type.replace('_', ' ').title()}: {count:,} ({percentage:.1f}%)")
    
    # Show examples of problematic cases
    if case_counts['all_upper'] > 0:
        print(f"\n🔍 ALL CAPS Examples (first 5):")
        all_caps_examples = company_data[case_issues['all_upper']].head(5)
        for example in all_caps_examples:
            suggested = example.title()
            print(f"   ❌ '{example}' → ✅ '{suggested}'")
    
    if case_counts['all_lower'] > 0:
        print(f"\n🔍 Lowercase Examples (first 5):")
        lowercase_examples = company_data[case_issues['all_lower']].head(5)
        for example in lowercase_examples:
            suggested = example.title()
            print(f"   ❌ '{example}' → ✅ '{suggested}'")
    
    print()
    
    # 2.2 SPECIAL CHARACTER ISSUES
    print("🔧 2.2 SPECIAL CHARACTER ISSUES")
    print("-" * 30)
    
    # Detect various special character patterns
    special_char_patterns = {
        'unusual_punctuation': company_data.str.contains(r'[^\w\s\-\&\.\,\(\)]', regex=True, na=False),
        'multiple_spaces': company_data.str.contains(r'\s{2,}', regex=True, na=False),
        'leading_trailing_spaces': company_data.str.len() != company_data.str.strip().str.len(),
        'special_quotes': company_data.str.contains(r'[""''`]', regex=True, na=False),
        'unusual_dashes': company_data.str.contains(r'[—–―]', regex=True, na=False),
        'turkish_chars': company_data.str.contains(r'[çğıöşüÇĞIÖŞÜ]', regex=True, na=False),
        'numbers_mixed': company_data.str.contains(r'\d', regex=True, na=False)
    }
    
    special_char_counts = {k: v.sum() for k, v in special_char_patterns.items()}
    
    print(f"📋 Special Character Issues:")
    for pattern_type, count in special_char_counts.items():
        if count > 0:
            percentage = (count / total_companies) * 100
            print(f"   {pattern_type.replace('_', ' ').title()}: {count:,} ({percentage:.1f}%)")
    
    # Show examples of special character issues
    if special_char_counts['unusual_punctuation'] > 0:
        print(f"\n🔍 Unusual Punctuation Examples (first 5):")
        unusual_punct_examples = company_data[special_char_patterns['unusual_punctuation']].head(5)
        for example in unusual_punct_examples:
            # Find the unusual characters
            unusual_chars = re.findall(r'[^\w\s\-\&\.\,\(\)]', example)
            print(f"   ❌ '{example}' → Contains: {set(unusual_chars)}")
    
    if special_char_counts['turkish_chars'] > 0:
        print(f"\n🔍 Turkish Characters Examples (first 5):")
        turkish_examples = company_data[special_char_patterns['turkish_chars']].head(5)
        for example in turkish_examples:
            # Show Turkish to English transliteration
            turkish_map = {'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
                          'Ç': 'C', 'Ğ': 'G', 'I': 'I', 'Ö': 'O', 'Ş': 'S', 'Ü': 'U'}
            transliterated = example
            for tr_char, en_char in turkish_map.items():
                transliterated = transliterated.replace(tr_char, en_char)
            print(f"   🔤 '{example}' → '{transliterated}'")
    
    if special_char_counts['multiple_spaces'] > 0:
        print(f"\n🔍 Multiple Spaces Examples (first 5):")
        multiple_spaces_examples = company_data[special_char_patterns['multiple_spaces']].head(5)
        for example in multiple_spaces_examples:
            cleaned = re.sub(r'\s+', ' ', example)
            print(f"   ❌ '{example}' → ✅ '{cleaned}'")
    
    print()
    
    # 2.3 LENGTH AND STRUCTURE ISSUES
    print("📏 2.3 LENGTH AND STRUCTURE ISSUES")
    print("-" * 35)
    
    lengths = company_data.str.len()
    
    length_stats = {
        'min': lengths.min(),
        'max': lengths.max(),
        'mean': lengths.mean(),
        'median': lengths.median(),
        'std': lengths.std()
    }
    
    print(f"📊 Length Statistics:")
    print(f"   Min: {length_stats['min']} characters")
    print(f"   Max: {length_stats['max']} characters")
    print(f"   Average: {length_stats['mean']:.1f} characters")
    print(f"   Median: {length_stats['median']:.1f} characters")
    print(f"   Std Dev: {length_stats['std']:.1f} characters")
    
    # Identify outliers
    very_short = company_data[lengths <= 3]
    very_long = company_data[lengths >= 50]
    
    if len(very_short) > 0:
        print(f"\n🔍 Very Short Names (≤3 chars): {len(very_short)} companies")
        for short_name in very_short.head(5):
            print(f"   ⚠️ '{short_name}' ({len(short_name)} chars)")
    
    if len(very_long) > 0:
        print(f"\n🔍 Very Long Names (≥50 chars): {len(very_long)} companies")
        for long_name in very_long.head(3):
            print(f"   ⚠️ '{long_name[:50]}...' ({len(long_name)} chars)")
    
    print()
    
    # 2.4 BUSINESS NAME PATTERNS
    print("🏢 2.4 BUSINESS NAME PATTERNS")
    print("-" * 30)
    
    business_patterns = {
        'has_ltd': company_data.str.contains(r'\bLTD\b|\bLtd\b|\bltd\b', regex=True, na=False),
        'has_inc': company_data.str.contains(r'\bINC\b|\bInc\b|\binc\b', regex=True, na=False),
        'has_corp': company_data.str.contains(r'\bCORP\b|\bCorp\b|\bcorp\b', regex=True, na=False),
        'has_llc': company_data.str.contains(r'\bLLC\b|\bLlc\b|\bllc\b', regex=True, na=False),
        'has_sti': company_data.str.contains(r'ŞTİ|STI|şti|sti', regex=True, na=False),
        'has_as': company_data.str.contains(r'\bA\.S\b|\bAS\b|\bas\b', regex=True, na=False),
        'has_gmbh': company_data.str.contains(r'GMBH|GmbH|gmbh', regex=True, na=False)
    }
    
    business_pattern_counts = {k: v.sum() for k, v in business_patterns.items()}
    
    print(f"📋 Business Entity Patterns:")
    for pattern_type, count in business_pattern_counts.items():
        if count > 0:
            percentage = (count / total_companies) * 100
            print(f"   {pattern_type.replace('_', ' ').title()}: {count:,} ({percentage:.1f}%)")
    
    print()
    
    # 3. STANDARDIZATION RECOMMENDATIONS
    print("💡 3. STANDARDIZATION RECOMMENDATIONS")
    print("-" * 40)
    
    total_issues = 0
    recommendations = []
    
    if case_counts['all_upper'] > 0:
        total_issues += case_counts['all_upper']
        recommendations.append(f"🔤 Convert {case_counts['all_upper']:,} ALL CAPS names to Title Case")
    
    if case_counts['all_lower'] > 0:
        total_issues += case_counts['all_lower']
        recommendations.append(f"🔤 Convert {case_counts['all_lower']:,} lowercase names to Title Case")
    
    if special_char_counts['leading_trailing_spaces'] > 0:
        total_issues += special_char_counts['leading_trailing_spaces']
        recommendations.append(f"🧹 Trim {special_char_counts['leading_trailing_spaces']:,} names with leading/trailing spaces")
    
    if special_char_counts['multiple_spaces'] > 0:
        total_issues += special_char_counts['multiple_spaces']
        recommendations.append(f"🔧 Fix {special_char_counts['multiple_spaces']:,} names with multiple spaces")
    
    if special_char_counts['turkish_chars'] > 0:
        total_issues += special_char_counts['turkish_chars']
        recommendations.append(f"🔤 Transliterate {special_char_counts['turkish_chars']:,} names with Turkish characters")
    
    if special_char_counts['unusual_punctuation'] > 0:
        total_issues += special_char_counts['unusual_punctuation']
        recommendations.append(f"🔧 Standardize {special_char_counts['unusual_punctuation']:,} names with unusual punctuation")
    
    print(f"📊 Total issues detected: {total_issues:,} entries need standardization")
    print(f"📈 Issue rate: {(total_issues/total_companies)*100:.1f}% of company names")
    print()
    
    print(f"🎯 Recommended Actions:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print()
    
    # 4. PROPOSED STANDARDIZATION PIPELINE
    print("🔄 4. PROPOSED STANDARDIZATION PIPELINE")
    print("-" * 40)
    
    print(f"📋 Standardization Steps (in order):")
    print(f"   1. 🧹 Strip leading/trailing whitespace")
    print(f"   2. 🔧 Normalize multiple spaces to single space")
    print(f"   3. 🔤 Convert Turkish characters to English equivalents")
    print(f"   4. 🔤 Standardize case to Title Case (with exceptions for acronyms)")
    print(f"   5. 🔧 Normalize punctuation and special characters")
    print(f"   6. ✅ Final validation and cleanup")
    
    print(f"\n📊 Expected Outcomes:")
    print(f"   📈 Improved data consistency: {(total_issues/total_companies)*100:.1f}% → 0%")
    print(f"   🔍 Better company matching and deduplication")
    print(f"   💾 Potential memory optimization through category conversion")
    print(f"   🎯 Enhanced search and filtering capability")
    
    print("\n" + "=" * 75)
    
    return df

def main():
    """Ana execution function"""
    
    print("🔍 Company Name Duplicate Deletion & Format Analysis")
    print("=" * 55)
    
    # Load dataset
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step5.csv')
        print(f"✅ Dataset loaded: {len(df):,} rows, {len(df.columns)} columns")
        print()
    except Exception as e:
        print(f"❌ ERROR: Could not load dataset - {e}")
        return
    
    # Perform deletion and analysis
    df_cleaned = delete_company_name_duplicate_and_analyze_format(df)
    
    # Save cleaned dataset
    if df_cleaned is not None:
        try:
            output_file = 'linkedin_jobs_dataset_optimized_step6.csv'
            df_cleaned.to_csv(output_file, index=False)
            print(f"✅ Cleaned dataset saved: {output_file}")
            print(f"📊 Final shape: {df_cleaned.shape}")
        except Exception as e:
            print(f"❌ ERROR: Could not save dataset - {e}")

if __name__ == "__main__":
    main() 