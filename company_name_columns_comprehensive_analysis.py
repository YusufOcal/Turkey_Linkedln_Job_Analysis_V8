#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Company Name Columns Comprehensive Analysis
companyName vs company/name ve diğer company identity sütunlarının detaylı analizi
CRITICAL: Duplicate detection and standardization strategy
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def analyze_company_name_columns_comprehensive(df):
    """Company name sütunları için kapsamlı analiz ve duplicate detection"""
    
    print("🏢 LINKEDIN JOBS DATASET - COMPANY NAME COLUMNS ANALYSIS")
    print("=" * 70)
    
    # Primary company identity columns
    company_identity_columns = [
        'companyName',           # Main target column
        'company/name',          # Potential duplicate
        'company/universalName', # URL-friendly name
        'companyLinkedinUrl',    # Company LinkedIn profile
        'companyId'              # Company identifier
    ]
    
    # Check column existence
    existing_columns = [col for col in company_identity_columns if col in df.columns]
    missing_columns = [col for col in company_identity_columns if col not in df.columns]
    
    print("🔍 COLUMN EXISTENCE VERIFICATION:")
    print("-" * 35)
    for col in existing_columns:
        print(f"   ✅ {col}")
    for col in missing_columns:
        print(f"   ❌ {col} - Missing")
    print()
    
    if len(existing_columns) < 2:
        print("⚠️ Insufficient columns for comprehensive comparison analysis!")
        return None
    
    # 1. SÜTUN TEMSİLLERİ VE ANLAMI
    print("📋 1. SÜTUN TEMSİLLERİ VE ANLAMI")
    print("-" * 40)
    
    column_purposes = {
        'companyName': {
            'purpose': 'Company Display Name',
            'content_type': 'Human-readable company name',
            'business_value': 'User interface display, company identification',
            'expected_format': 'Formatted company title (mixed case, special chars)',
            'source': 'LinkedIn Company API - Display name field',
            'data_usage': 'Frontend display, search, branding'
        },
        'company/name': {
            'purpose': 'Company Official Name',
            'content_type': 'Official company name (structured)',
            'business_value': 'Company identification, matching, deduplication',
            'expected_format': 'Official business name format',
            'source': 'LinkedIn Company API - Official name field',
            'data_usage': 'Data processing, company matching, analytics'
        },
        'company/universalName': {
            'purpose': 'Company URL Slug',
            'content_type': 'URL-friendly company identifier',
            'business_value': 'LinkedIn profile identification, URL generation',
            'expected_format': 'lowercase, hyphens, no spaces (URL-safe)',
            'source': 'LinkedIn Company API - Universal name field',
            'data_usage': 'URL generation, company profile linking'
        },
        'companyLinkedinUrl': {
            'purpose': 'Company LinkedIn Profile URL',
            'content_type': 'Full LinkedIn company profile URL',
            'business_value': 'Direct profile access, external linking',
            'expected_format': 'https://linkedin.com/company/{universalName}',
            'source': 'LinkedIn Company API - Profile URL',
            'data_usage': 'External linking, profile access'
        },
        'companyId': {
            'purpose': 'Company Unique Identifier',
            'content_type': 'Numeric or alphanumeric company ID',
            'business_value': 'Unique identification, data joins, relationships',
            'expected_format': 'Numeric ID or alphanumeric string',
            'source': 'LinkedIn Company API - Company ID',
            'data_usage': 'Primary key, data relationships, joins'
        }
    }
    
    for col in existing_columns:
        if col in column_purposes:
            info = column_purposes[col]
            print(f"🏢 {col}:")
            print(f"   📝 Purpose: {info['purpose']}")
            print(f"   💼 Content: {info['content_type']}")
            print(f"   🎯 Business Value: {info['business_value']}")
            print(f"   📊 Expected Format: {info['expected_format']}")
            print(f"   🔗 Source: {info['source']}")
            print(f"   🎨 Usage: {info['data_usage']}")
            print()
    
    # 2. TEMEL İSTATİSTİKLER VE VERİ TİPİ UYUMLULUĞU
    print("📊 2. TEMEL İSTATİSTİKLER VE VERİ TİPİ UYUMLULUĞU")
    print("-" * 55)
    
    stats_comparison = {}
    
    for col in existing_columns:
        col_data = df[col]
        
        # Basic statistics
        total_count = len(col_data)
        null_count = col_data.isnull().sum()
        non_null_count = total_count - null_count
        null_percentage = (null_count / total_count) * 100
        unique_count = col_data.nunique()
        
        # Data type analysis
        current_dtype = col_data.dtype
        
        # Memory usage
        memory_usage_mb = col_data.memory_usage(deep=True) / 1024**2
        
        stats_comparison[col] = {
            'total_count': total_count,
            'non_null_count': non_null_count,
            'null_count': null_count,
            'null_percentage': null_percentage,
            'unique_count': unique_count,
            'current_dtype': current_dtype,
            'memory_usage_mb': memory_usage_mb
        }
        
        print(f"📋 {col}:")
        print(f"   📊 Records: {total_count:,} total, {non_null_count:,} non-null ({100-null_percentage:.1f}%)")
        print(f"   🔢 Unique values: {unique_count:,}")
        print(f"   🏷️ Data type: {current_dtype}")
        print(f"   💾 Memory: {memory_usage_mb:.2f} MB")
        
        # Data type compatibility check
        if col == 'companyId':
            if current_dtype == 'object':
                print(f"   ⚠️ DATA TYPE ISSUE: ID should be numeric, currently {current_dtype}")
        elif col in ['companyName', 'company/name']:
            if current_dtype != 'object':
                print(f"   ⚠️ DATA TYPE ISSUE: Name should be object, currently {current_dtype}")
        elif col == 'company/universalName':
            if current_dtype != 'object':
                print(f"   ⚠️ DATA TYPE ISSUE: Universal name should be object, currently {current_dtype}")
        elif col == 'companyLinkedinUrl':
            if current_dtype != 'object':
                print(f"   ⚠️ DATA TYPE ISSUE: URL should be object, currently {current_dtype}")
        else:
            print(f"   ✅ Data type appropriate for content")
        print()
    
    # 3. CRITICAL DUPLICATE DETECTION ANALYSIS
    print("🚨 3. CRITICAL DUPLICATE DETECTION ANALYSIS")
    print("-" * 45)
    
    duplicate_analysis = {}
    critical_findings = []
    
    # Focus on companyName vs company/name comparison
    if 'companyName' in existing_columns and 'company/name' in existing_columns:
        
        print("🔍 MAIN DUPLICATE ANALYSIS: companyName vs company/name")
        print("-" * 55)
        
        col1, col2 = 'companyName', 'company/name'
        
        # Extract non-null data for both columns
        both_non_null = df[(df[col1].notna()) & (df[col2].notna())]
        
        if len(both_non_null) > 0:
            # Perfect matches
            perfect_matches = (both_non_null[col1] == both_non_null[col2]).sum()
            perfect_match_rate = (perfect_matches / len(both_non_null)) * 100
            
            # Case-insensitive matches
            case_insensitive_matches = (both_non_null[col1].str.lower() == both_non_null[col2].str.lower()).sum()
            case_insensitive_rate = (case_insensitive_matches / len(both_non_null)) * 100
            
            # Normalized matches (remove special chars, spaces)
            def normalize_company_name(name):
                if pd.isna(name):
                    return name
                return re.sub(r'[^\w\s]', '', str(name).lower().strip())
            
            normalized_col1 = both_non_null[col1].apply(normalize_company_name)
            normalized_col2 = both_non_null[col2].apply(normalize_company_name)
            normalized_matches = (normalized_col1 == normalized_col2).sum()
            normalized_match_rate = (normalized_matches / len(both_non_null)) * 100
            
            duplicate_analysis[f'{col1}_vs_{col2}'] = {
                'total_comparable': len(both_non_null),
                'perfect_matches': perfect_matches,
                'perfect_match_rate': perfect_match_rate,
                'case_insensitive_matches': case_insensitive_matches,
                'case_insensitive_rate': case_insensitive_rate,
                'normalized_matches': normalized_matches,
                'normalized_match_rate': normalized_match_rate
            }
            
            print(f"📊 Comparison Results:")
            print(f"   🔢 Comparable records: {len(both_non_null):,}")
            print(f"   ✅ Perfect matches: {perfect_matches:,} ({perfect_match_rate:.1f}%)")
            print(f"   🔤 Case-insensitive matches: {case_insensitive_matches:,} ({case_insensitive_rate:.1f}%)")
            print(f"   🧹 Normalized matches: {normalized_matches:,} ({normalized_match_rate:.1f}%)")
            
            # Critical assessment
            if perfect_match_rate > 95:
                critical_findings.append(f"🚨 CRITICAL DUPLICATE: {col1} and {col2} are {perfect_match_rate:.1f}% identical!")
                print(f"   🚨 ASSESSMENT: CRITICAL DUPLICATE DETECTED!")
            elif case_insensitive_rate > 95:
                critical_findings.append(f"⚠️ HIGH SIMILARITY: {col1} and {col2} with case differences")
                print(f"   ⚠️ ASSESSMENT: High similarity with case variations")
            elif normalized_match_rate > 90:
                critical_findings.append(f"⚠️ MODERATE SIMILARITY: {col1} and {col2} with format differences")
                print(f"   ⚠️ ASSESSMENT: Moderate similarity with format differences")
            else:
                print(f"   ✅ ASSESSMENT: Columns contain different information")
            
            # Sample differences for analysis
            if perfect_match_rate < 100:
                differences = both_non_null[both_non_null[col1] != both_non_null[col2]]
                if len(differences) > 0:
                    print(f"\n📋 Sample Differences (first 5):")
                    for idx, row in differences.head(5).iterrows():
                        print(f"   {col1}: '{row[col1]}'")
                        print(f"   {col2}: '{row[col2]}'")
                        print(f"   ---")
        print()
    
    # 4. DATA CONSISTENCY VALIDATION
    print("🔍 4. DATA CONSISTENCY VALIDATION")
    print("-" * 35)
    
    consistency_issues = []
    
    for col in existing_columns:
        if col in df.columns:
            col_data = df[col].dropna()
            
            if len(col_data) > 0:
                # Check for empty strings
                empty_strings = (col_data == '').sum()
                
                # Check for whitespace-only entries
                if col_data.dtype == 'object':
                    whitespace_only = col_data.str.strip().eq('').sum()
                    
                    # Check for unusual characters
                    unusual_chars = col_data.str.contains(r'[^\w\s\-\&\.\,\(\)]', regex=True, na=False).sum()
                    
                    # Check length distribution
                    lengths = col_data.astype(str).str.len()
                    
                    print(f"🔍 {col} Consistency Analysis:")
                    print(f"   📝 Empty strings: {empty_strings}")
                    print(f"   🔘 Whitespace-only: {whitespace_only}")
                    print(f"   🔧 Unusual characters: {unusual_chars}")
                    print(f"   📏 Length range: {lengths.min()}-{lengths.max()} (avg: {lengths.mean():.1f})")
                    
                    if empty_strings > 0:
                        consistency_issues.append(f"{col}: {empty_strings} empty strings")
                    if whitespace_only > 0:
                        consistency_issues.append(f"{col}: {whitespace_only} whitespace-only entries")
                    if unusual_chars > 0:
                        consistency_issues.append(f"{col}: {unusual_chars} entries with unusual characters")
                    
                    # Specific validation for different column types
                    if col == 'companyLinkedinUrl':
                        # URL validation
                        url_pattern = col_data.str.contains(r'^https?://', regex=True, na=False)
                        valid_urls = url_pattern.sum()
                        invalid_urls = len(col_data) - valid_urls
                        
                        linkedin_pattern = col_data.str.contains(r'linkedin\.com', regex=True, na=False)
                        linkedin_urls = linkedin_pattern.sum()
                        
                        print(f"   🌐 Valid URL format: {valid_urls}/{len(col_data)}")
                        print(f"   🔗 LinkedIn URLs: {linkedin_urls}/{len(col_data)}")
                        
                        if invalid_urls > 0:
                            consistency_issues.append(f"{col}: {invalid_urls} invalid URL formats")
                    
                    elif col == 'company/universalName':
                        # Universal name should be URL-friendly
                        url_friendly = col_data.str.match(r'^[a-z0-9\-]+$', na=False)
                        url_friendly_count = url_friendly.sum()
                        non_url_friendly = len(col_data) - url_friendly_count
                        
                        print(f"   🔗 URL-friendly format: {url_friendly_count}/{len(col_data)}")
                        
                        if non_url_friendly > 0:
                            consistency_issues.append(f"{col}: {non_url_friendly} non-URL-friendly formats")
                    
                    print()
    
    # 5. NULL DENSITY ANALYSIS VE DOLDURMA ÖNERİLERİ
    print("📈 5. NULL DENSITY ANALYSIS VE DOLDURMA ÖNERİLERİ")
    print("-" * 50)
    
    null_analysis = {}
    
    for col in existing_columns:
        null_pct = stats_comparison[col]['null_percentage']
        non_null_count = stats_comparison[col]['non_null_count']
        
        null_analysis[col] = {
            'null_percentage': null_pct,
            'severity': 'HIGH' if null_pct > 50 else 'MEDIUM' if null_pct > 20 else 'LOW'
        }
        
        print(f"📊 {col}:")
        print(f"   🔢 Null rate: {null_pct:.1f}%")
        print(f"   🎯 Severity: {null_analysis[col]['severity']}")
        
        # Filling suggestions
        if null_pct > 50:
            print(f"   🚨 HIGH NULL RATE - Consider column deletion or major data enrichment")
        elif null_pct > 20:
            print(f"   ⚠️ MODERATE NULL RATE - Data enrichment recommended")
        elif null_pct > 10:
            print(f"   📝 MINOR NULL RATE - Default/placeholder values feasible")
        else:
            print(f"   ✅ ACCEPTABLE NULL RATE - No immediate action needed")
        
        # Specific filling strategies
        if col == 'companyName' or col == 'company/name':
            if null_pct > 0:
                print(f"   💡 Filling Strategy: Use other company name column if available")
        elif col == 'company/universalName':
            if null_pct > 0:
                print(f"   💡 Filling Strategy: Generate from company name (normalize + slugify)")
        elif col == 'companyLinkedinUrl':
            if null_pct > 0:
                print(f"   💡 Filling Strategy: Generate from universalName: 'https://linkedin.com/company/{{universalName}}'")
        elif col == 'companyId':
            if null_pct > 0:
                print(f"   💡 Filling Strategy: Extract from LinkedIn URL or assign sequential IDs")
        
        print()
    
    # 6. FORMAT STANDARDIZATION ÖNERILERİ
    print("🔧 6. FORMAT STANDARDIZATION ÖNERILERİ")
    print("-" * 40)
    
    standardization_recommendations = []
    
    for col in existing_columns:
        if col in df.columns:
            col_data = df[col].dropna()
            
            if len(col_data) > 0 and col_data.dtype == 'object':
                print(f"🔧 {col} Standardization Analysis:")
                
                # Case consistency analysis
                if col in ['companyName', 'company/name']:
                    # Check case patterns
                    all_upper = col_data.str.isupper().sum()
                    all_lower = col_data.str.islower().sum()
                    title_case = col_data.str.istitle().sum()
                    mixed_case = len(col_data) - all_upper - all_lower - title_case
                    
                    print(f"   🔤 Case Distribution:")
                    print(f"      UPPER: {all_upper} ({all_upper/len(col_data)*100:.1f}%)")
                    print(f"      lower: {all_lower} ({all_lower/len(col_data)*100:.1f}%)")
                    print(f"      Title: {title_case} ({title_case/len(col_data)*100:.1f}%)")
                    print(f"      Mixed: {mixed_case} ({mixed_case/len(col_data)*100:.1f}%)")
                    
                    if all_upper > len(col_data) * 0.1:
                        standardization_recommendations.append(f"{col}: Convert ALL CAPS to Title Case")
                    if all_lower > len(col_data) * 0.1:
                        standardization_recommendations.append(f"{col}: Convert lowercase to Title Case")
                
                # Special character analysis
                special_chars_count = col_data.str.contains(r'[^\w\s\-\&\.\,\(\)]', regex=True, na=False).sum()
                if special_chars_count > 0:
                    print(f"   🔧 Special characters: {special_chars_count} entries")
                    standardization_recommendations.append(f"{col}: Standardize special characters")
                
                # Whitespace analysis
                leading_trailing_space = col_data.str.len() != col_data.str.strip().str.len()
                leading_trailing_count = leading_trailing_space.sum()
                if leading_trailing_count > 0:
                    print(f"   🔘 Leading/trailing spaces: {leading_trailing_count} entries")
                    standardization_recommendations.append(f"{col}: Trim whitespace")
                
                print()
    
    # 7. COLUMN SIMILARITY MATRIX VE CONSOLIDATION ÖNERİLERİ
    print("🔄 7. COLUMN SIMILARITY MATRIX VE CONSOLIDATION ÖNERİLERİ")
    print("-" * 60)
    
    consolidation_recommendations = []
    
    # Create similarity matrix
    similarity_matrix = {}
    
    for i, col1 in enumerate(existing_columns):
        for j, col2 in enumerate(existing_columns):
            if i < j:  # Avoid duplicate comparisons
                # Calculate similarity
                both_non_null = df[(df[col1].notna()) & (df[col2].notna())]
                
                if len(both_non_null) > 0:
                    # Perfect match similarity
                    perfect_matches = (both_non_null[col1] == both_non_null[col2]).sum()
                    similarity_pct = (perfect_matches / len(both_non_null)) * 100
                    
                    similarity_matrix[f"{col1}_vs_{col2}"] = similarity_pct
                    
                    print(f"📊 {col1} ↔ {col2}:")
                    print(f"   🔢 Comparable records: {len(both_non_null):,}")
                    print(f"   🎯 Similarity: {similarity_pct:.1f}%")
                    
                    # Consolidation recommendations
                    if similarity_pct > 95:
                        print(f"   🚨 CRITICAL DUPLICATE - DELETE ONE COLUMN!")
                        consolidation_recommendations.append(f"DELETE {col2} (duplicate of {col1})")
                    elif similarity_pct > 80:
                        print(f"   ⚠️ HIGH SIMILARITY - CONSOLIDATION CANDIDATE")
                        consolidation_recommendations.append(f"CONSOLIDATE {col1} and {col2}")
                    elif similarity_pct > 50:
                        print(f"   📝 MODERATE SIMILARITY - REVIEW RELATIONSHIP")
                    else:
                        print(f"   ✅ DIFFERENT CONTENT - KEEP SEPARATE")
                    print()
    
    # 8. FINAL OPTIMIZATION RECOMMENDATIONS
    print("💡 8. FINAL OPTIMIZATION RECOMMENDATIONS")
    print("-" * 45)
    
    print("📋 CRITICAL FINDINGS:")
    for finding in critical_findings:
        print(f"   {finding}")
    
    print(f"\n🔧 STANDARDIZATION NEEDS:")
    for rec in standardization_recommendations:
        print(f"   📝 {rec}")
    
    print(f"\n🔄 CONSOLIDATION RECOMMENDATIONS:")
    for rec in consolidation_recommendations:
        print(f"   📋 {rec}")
    
    print(f"\n🗑️ DELETION CANDIDATES:")
    deletion_candidates = []
    for col in existing_columns:
        null_pct = stats_comparison[col]['null_percentage']
        if null_pct > 80:
            deletion_candidates.append(f"{col} ({null_pct:.1f}% null)")
    
    if deletion_candidates:
        for candidate in deletion_candidates:
            print(f"   🗑️ {candidate}")
    else:
        print(f"   ✅ No deletion candidates based on null density")
    
    # 9. MEMORY OPTIMIZATION POTENTIAL
    print(f"\n💾 MEMORY OPTIMIZATION POTENTIAL:")
    total_memory = sum(stats['memory_usage_mb'] for stats in stats_comparison.values())
    print(f"   📊 Total memory usage: {total_memory:.2f} MB")
    
    # Category conversion potential
    for col in existing_columns:
        unique_count = stats_comparison[col]['unique_count']
        current_memory = stats_comparison[col]['memory_usage_mb']
        
        if unique_count < 1000 and col_data.dtype == 'object':
            potential_savings = current_memory * 0.6  # Estimated 60% savings
            print(f"   🔧 {col}: Convert to category (save ~{potential_savings:.2f} MB)")
    
    print("\n" + "=" * 70)
    
    return {
        'stats_comparison': stats_comparison,
        'duplicate_analysis': duplicate_analysis,
        'consistency_issues': consistency_issues,
        'critical_findings': critical_findings,
        'consolidation_recommendations': consolidation_recommendations,
        'standardization_recommendations': standardization_recommendations,
        'similarity_matrix': similarity_matrix
    }

def main():
    """Ana analiz fonksiyonu"""
    
    print("🔍 LinkedIn Jobs Dataset - Company Name Columns Analysis")
    print("=" * 65)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step5.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # Comprehensive analysis gerçekleştir
    result = analyze_company_name_columns_comprehensive(df)
    
    if result:
        print("🎯 COMPANY NAME COLUMNS ANALYSIS COMPLETED!")
        
        # Summary of critical findings
        if result['critical_findings']:
            print("\n🚨 CRITICAL ACTIONS REQUIRED:")
            for finding in result['critical_findings']:
                print(f"   {finding}")
        
        if result['consolidation_recommendations']:
            print("\n🔄 CONSOLIDATION ACTIONS:")
            for rec in result['consolidation_recommendations']:
                print(f"   {rec}")

if __name__ == "__main__":
    main() 