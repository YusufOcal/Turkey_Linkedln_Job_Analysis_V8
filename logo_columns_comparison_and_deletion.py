#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Logo Columns Comparison and Deletion
company/logo vs companyLogo comparison + deletion of less complete column
"""

import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def compare_and_delete_logo_columns(df):
    """Logo sütunlarını karşılaştır ve daha az complete olanı sil"""
    
    print("🏢 LINKEDIN JOBS DATASET - LOGO COLUMNS COMPARISON")
    print("=" * 60)
    
    logo_columns = ['company/logo', 'companyLogo']
    
    # Check if columns exist
    existing_columns = [col for col in logo_columns if col in df.columns]
    missing_columns = [col for col in logo_columns if col not in df.columns]
    
    print("🔍 COLUMN EXISTENCE CHECK:")
    for col in existing_columns:
        print(f"   ✅ {col}")
    for col in missing_columns:
        print(f"   ❌ {col} - Missing")
    print()
    
    if len(existing_columns) < 2:
        print("⚠️ Less than 2 logo columns found. Skipping comparison.")
        return df
    
    # 1. COMPARATIVE STATISTICS
    print("📊 1. COMPARATIVE STATISTICS")
    print("-" * 30)
    
    comparison_stats = {}
    
    for col in existing_columns:
        col_data = df[col]
        null_count = col_data.isnull().sum()
        non_null_count = len(col_data) - null_count
        null_pct = (null_count / len(col_data)) * 100
        unique_count = col_data.nunique()
        memory_mb = col_data.memory_usage(deep=True) / 1024**2
        
        comparison_stats[col] = {
            'null_count': null_count,
            'non_null_count': non_null_count,
            'null_pct': null_pct,
            'unique_count': unique_count,
            'memory_mb': memory_mb,
            'completeness_score': 100 - null_pct
        }
        
        print(f"📋 {col}:")
        print(f"   📊 Null: {null_count:,} ({null_pct:.1f}%)")
        print(f"   ✅ Dolu: {non_null_count:,} ({100-null_pct:.1f}%)")
        print(f"   🎯 Benzersiz: {unique_count:,}")
        print(f"   💾 Memory: {memory_mb:.2f} MB")
        print(f"   📈 Completeness Score: {100-null_pct:.1f}%")
        print()
    
    # 2. CONTENT OVERLAP ANALYSIS
    print("🔍 2. CONTENT OVERLAP ANALYSIS")
    print("-" * 30)
    
    # Get non-null data from both columns
    col1_data = df[existing_columns[0]].dropna()
    col2_data = df[existing_columns[1]].dropna()
    
    # Find common values
    col1_values = set(col1_data.astype(str).str.lower())
    col2_values = set(col2_data.astype(str).str.lower())
    
    overlap = col1_values & col2_values
    overlap_count = len(overlap)
    
    if len(col1_values) > 0 and len(col2_values) > 0:
        overlap_pct1 = (overlap_count / len(col1_values)) * 100
        overlap_pct2 = (overlap_count / len(col2_values)) * 100
        
        print(f"🔗 Content Overlap:")
        print(f"   Common values: {overlap_count:,}")
        print(f"   Overlap vs {existing_columns[0]}: {overlap_pct1:.1f}%")
        print(f"   Overlap vs {existing_columns[1]}: {overlap_pct2:.1f}%")
        
        if overlap_pct1 > 80 or overlap_pct2 > 80:
            print(f"   🚨 HIGH OVERLAP - Strong candidate for consolidation")
        elif overlap_pct1 > 50 or overlap_pct2 > 50:
            print(f"   ⚠️ MODERATE OVERLAP - Consider consolidation")
        else:
            print(f"   ✅ LOW OVERLAP - Columns serve different purposes")
    
    # 3. DECISION MATRIX
    print(f"\n🎯 3. DECISION MATRIX")
    print("-" * 20)
    
    decision_criteria = {}
    
    for col in existing_columns:
        stats = comparison_stats[col]
        
        # Calculate composite score
        completeness_weight = 0.4
        uniqueness_weight = 0.3
        memory_efficiency_weight = 0.3
        
        # Normalize metrics (higher is better)
        completeness_score = stats['completeness_score']
        uniqueness_score = min(100, (stats['unique_count'] / len(df)) * 100 * 10)  # Scale up
        memory_efficiency_score = max(0, 100 - (stats['memory_mb'] * 10))  # Lower memory = higher score
        
        composite_score = (
            completeness_score * completeness_weight +
            uniqueness_score * uniqueness_weight +
            memory_efficiency_score * memory_efficiency_weight
        )
        
        decision_criteria[col] = {
            'completeness': completeness_score,
            'uniqueness': uniqueness_score, 
            'memory_efficiency': memory_efficiency_score,
            'composite_score': composite_score
        }
        
        print(f"📊 {col} Scores:")
        print(f"   📈 Completeness: {completeness_score:.1f}/100")
        print(f"   🎯 Uniqueness: {uniqueness_score:.1f}/100")
        print(f"   💾 Memory Efficiency: {memory_efficiency_score:.1f}/100")
        print(f"   ⭐ Composite Score: {composite_score:.1f}/100")
        print()
    
    # 4. FINAL DECISION
    print("🎯 4. FINAL DECISION")
    print("-" * 18)
    
    # Find the column with highest completeness (primary criterion)
    best_column = max(existing_columns, key=lambda x: comparison_stats[x]['completeness_score'])
    worst_column = min(existing_columns, key=lambda x: comparison_stats[x]['completeness_score'])
    
    print(f"🏆 WINNER: {best_column}")
    print(f"   📈 Completeness: {comparison_stats[best_column]['completeness_score']:.1f}%")
    print(f"   🎯 Records: {comparison_stats[best_column]['non_null_count']:,}")
    
    print(f"\n🗑️ TO DELETE: {worst_column}")
    print(f"   📈 Completeness: {comparison_stats[worst_column]['completeness_score']:.1f}%")
    print(f"   🎯 Records: {comparison_stats[worst_column]['non_null_count']:,}")
    
    completeness_diff = comparison_stats[best_column]['completeness_score'] - comparison_stats[worst_column]['completeness_score']
    record_diff = comparison_stats[best_column]['non_null_count'] - comparison_stats[worst_column]['non_null_count']
    
    print(f"\n📊 IMPROVEMENT BY KEEPING {best_column}:")
    print(f"   ⬆️ Completeness gain: +{completeness_diff:.1f}%")
    print(f"   ⬆️ Additional records: +{record_diff:,}")
    
    # 5. EXECUTE DELETION
    print(f"\n🗑️ 5. EXECUTING DELETION")
    print("-" * 25)
    
    if worst_column in df.columns:
        memory_freed = df[worst_column].memory_usage(deep=True) / 1024**2
        df_optimized = df.drop(columns=[worst_column])
        
        print(f"✅ Deleted column: {worst_column}")
        print(f"💾 Memory freed: {memory_freed:.2f} MB")
        print(f"📊 Columns: {len(df.columns)} → {len(df_optimized.columns)} (-1)")
        
        # Rename the remaining column to standardized name if needed
        if best_column == 'companyLogo':
            df_optimized = df_optimized.rename(columns={'companyLogo': 'company_logo_url'})
            final_column_name = 'company_logo_url'
            print(f"🔄 Renamed {best_column} → {final_column_name}")
        else:
            final_column_name = best_column
        
        # 6. FINAL STATISTICS
        print(f"\n📊 6. FINAL OPTIMIZED COLUMN STATISTICS")
        print("-" * 40)
        
        final_col_data = df_optimized[final_column_name]
        final_null_count = final_col_data.isnull().sum()
        final_non_null = len(final_col_data) - final_null_count
        final_null_pct = (final_null_count / len(final_col_data)) * 100
        final_unique = final_col_data.nunique()
        final_memory = final_col_data.memory_usage(deep=True) / 1024**2
        
        print(f"📋 {final_column_name} (OPTIMIZED):")
        print(f"   📊 Total: {len(final_col_data):,}")
        print(f"   ✅ Dolu: {final_non_null:,} ({100-final_null_pct:.1f}%)")
        print(f"   ❌ Null: {final_null_count:,} ({final_null_pct:.1f}%)")
        print(f"   🎯 Benzersiz: {final_unique:,}")
        print(f"   💾 Memory: {final_memory:.2f} MB")
        
        print(f"\n✅ LOGO COLUMN OPTIMIZATION COMPLETED!")
        
        return df_optimized, final_column_name
    
    else:
        print(f"❌ Error: {worst_column} not found for deletion!")
        return df, best_column

def analyze_business_insights(df, logo_column):
    """Logo sütunu ile business insights analizi"""
    
    print(f"\n🎯 BUSINESS INSIGHTS ANALYSIS - {logo_column}")
    print("=" * 55)
    
    if logo_column not in df.columns:
        print(f"❌ Column {logo_column} not found!")
        return
    
    logo_data = df[logo_column]
    
    # 1. COMPANY BRANDING COVERAGE
    print("🏢 1. COMPANY BRANDING COVERAGE")
    print("-" * 32)
    
    total_companies = df['company/name'].nunique() if 'company/name' in df.columns else len(df)
    companies_with_logos = len(df[df[logo_column].notna() & df['company/name'].notna()]['company/name'].unique()) if 'company/name' in df.columns else logo_data.notna().sum()
    
    branding_coverage = (companies_with_logos / total_companies) * 100 if total_companies > 0 else 0
    
    print(f"📊 Company Branding Statistics:")
    print(f"   🏢 Total companies: {total_companies:,}")
    print(f"   🎨 Companies with logos: {companies_with_logos:,}")
    print(f"   📈 Branding coverage: {branding_coverage:.1f}%")
    
    if branding_coverage > 95:
        print(f"   ✅ EXCELLENT: Near-complete visual branding")
    elif branding_coverage > 80:
        print(f"   ✅ GOOD: Strong visual branding presence")
    elif branding_coverage > 60:
        print(f"   ⚠️ MODERATE: Room for improvement in branding")
    else:
        print(f"   ❌ POOR: Significant branding gaps")
    
    # 2. LOGO URL PATTERN ANALYSIS
    print(f"\n🌐 2. LOGO URL PATTERN ANALYSIS")
    print("-" * 32)
    
    non_null_logos = logo_data.dropna()
    
    if len(non_null_logos) > 0:
        # Domain analysis
        domains = []
        for url in non_null_logos:
            try:
                from urllib.parse import urlparse
                parsed = urlparse(str(url))
                if parsed.netloc:
                    domains.append(parsed.netloc.lower())
            except:
                pass
        
        if domains:
            domain_counts = Counter(domains)
            print(f"🌐 Domain Distribution:")
            for domain, count in domain_counts.most_common(5):
                pct = (count / len(domains)) * 100
                print(f"   {domain}: {count:,} ({pct:.1f}%)")
            
            # Domain concentration analysis
            top_domain_pct = (domain_counts.most_common(1)[0][1] / len(domains)) * 100
            
            if top_domain_pct > 95:
                print(f"\n   🎯 INSIGHT: Highly standardized logo hosting ({top_domain_pct:.1f}%)")
                print(f"   💡 OPPORTUNITY: CDN optimization, caching strategies")
            elif top_domain_pct > 80:
                print(f"\n   🎯 INSIGHT: Good standardization with some diversity")
            else:
                print(f"\n   🎯 INSIGHT: Diverse logo hosting sources")
                print(f"   ⚠️ CONSIDERATION: Potential performance inconsistencies")
    
    # 3. BUSINESS VALUE INSIGHTS
    print(f"\n💰 3. BUSINESS VALUE INSIGHTS")
    print("-" * 30)
    
    insights = []
    
    # Logo availability by industry
    if 'industries_consolidated' in df.columns:
        industry_logo_stats = df.groupby('industries_consolidated').agg({
            logo_column: lambda x: x.notna().sum(),
            'company/name': 'nunique'
        }).round(2)
        
        if not industry_logo_stats.empty:
            industry_logo_stats['logo_coverage'] = (industry_logo_stats[logo_column] / industry_logo_stats['company/name'] * 100).round(1)
            top_coverage_industries = industry_logo_stats.nlargest(3, 'logo_coverage')
            
            print(f"🏭 Logo Coverage by Industry (Top 3):")
            for industry, stats in top_coverage_industries.iterrows():
                coverage = stats['logo_coverage']
                companies = stats['company/name']
                print(f"   {industry[:50]}...: {coverage:.1f}% ({companies:.0f} companies)")
            
            insights.append("Industry-specific branding patterns identified")
    
    # Logo availability vs company size (job count proxy)
    if 'company/name' in df.columns:
        company_job_counts = df['company/name'].value_counts()
        company_logo_presence = df[df[logo_column].notna()]['company/name'].value_counts()
        
        # Analyze large companies (>10 jobs)
        large_companies = company_job_counts[company_job_counts >= 10]
        large_companies_with_logos = large_companies.index.intersection(company_logo_presence.index)
        
        large_company_logo_rate = len(large_companies_with_logos) / len(large_companies) * 100 if len(large_companies) > 0 else 0
        
        print(f"\n🏢 Large Company Logo Analysis:")
        print(f"   Companies with 10+ jobs: {len(large_companies):,}")
        print(f"   Large companies with logos: {len(large_companies_with_logos):,}")
        print(f"   Large company logo rate: {large_company_logo_rate:.1f}%")
        
        if large_company_logo_rate > 90:
            insights.append("Excellent branding among major employers")
        else:
            insights.append("Branding opportunity with large companies")
    
    # 4. TECHNICAL INSIGHTS
    print(f"\n🔧 4. TECHNICAL INSIGHTS")
    print("-" * 25)
    
    if len(non_null_logos) > 0:
        # URL length analysis for performance
        url_lengths = non_null_logos.astype(str).str.len()
        avg_length = url_lengths.mean()
        
        print(f"🌐 URL Performance Metrics:")
        print(f"   Average URL length: {avg_length:.0f} characters")
        
        if avg_length > 200:
            print(f"   ⚠️ CONSIDERATION: Long URLs may impact load times")
            insights.append("URL length optimization opportunity")
        else:
            print(f"   ✅ Good URL length for performance")
        
        # Unique logo count vs company count
        unique_logos = logo_data.nunique()
        total_companies = df['company/name'].nunique() if 'company/name' in df.columns else len(df)
        
        logo_diversity = (unique_logos / total_companies) * 100 if total_companies > 0 else 0
        
        print(f"\n🎨 Logo Diversity:")
        print(f"   Unique logos: {unique_logos:,}")
        print(f"   Logo diversity: {logo_diversity:.1f}%")
        
        if logo_diversity > 80:
            insights.append("High logo diversity - strong brand differentiation")
        elif logo_diversity < 50:
            insights.append("Moderate logo sharing - potential generic/default logos")
    
    # 5. ACTIONABLE RECOMMENDATIONS
    print(f"\n💡 5. ACTIONABLE RECOMMENDATIONS")
    print("-" * 35)
    
    recommendations = []
    
    if branding_coverage < 90:
        missing_logos = total_companies - companies_with_logos
        recommendations.append(f"🎨 Implement default logos for {missing_logos:,} companies")
    
    if domains and len(set(domains)) == 1:
        recommendations.append(f"🚀 Implement CDN caching strategy (single domain)")
    
    if 'industries_consolidated' in df.columns:
        recommendations.append(f"📊 Create industry-specific branding analytics dashboard")
    
    recommendations.append(f"🔍 Monitor logo load performance and user engagement")
    recommendations.append(f"🎯 Use logo presence as company profile completeness metric")
    
    print(f"📋 Business Recommendations:")
    for i, rec in enumerate(recommendations, 1):
        print(f"   {i}. {rec}")
    
    print(f"\n🎯 KEY INSIGHTS SUMMARY:")
    for i, insight in enumerate(insights, 1):
        print(f"   {i}. {insight}")
    
    return {
        'branding_coverage': branding_coverage,
        'domain_concentration': top_domain_pct if 'top_domain_pct' in locals() else 0,
        'insights': insights,
        'recommendations': recommendations
    }

def main():
    """Ana analiz ve optimizasyon fonksiyonu"""
    
    print("🏢 LinkedIn Jobs Dataset - Logo Columns Optimization")
    print("=" * 55)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step3.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # Logo columns comparison ve deletion
    df_optimized, final_logo_column = compare_and_delete_logo_columns(df)
    
    # Business insights analysis
    insights_result = analyze_business_insights(df_optimized, final_logo_column)
    
    # Save optimized dataset
    output_filename = 'linkedin_jobs_dataset_optimized_step4.csv'
    df_optimized.to_csv(output_filename, index=False)
    
    print(f"\n💾 OPTIMIZED DATASET SAVED:")
    print(f"   📁 File: {output_filename}")
    print(f"   📊 Rows: {len(df_optimized):,}")
    print(f"   📊 Columns: {len(df_optimized.columns)}")
    
    # File size comparison
    import os
    if os.path.exists('linkedin_jobs_dataset_optimized_step3.csv'):
        original_size = os.path.getsize('linkedin_jobs_dataset_optimized_step3.csv') / 1024**2
        new_size = os.path.getsize(output_filename) / 1024**2
        size_reduction = original_size - new_size
        
        print(f"   💾 Size: {original_size:.1f} → {new_size:.1f} MB (-{size_reduction:.1f} MB)")
        
    print(f"\n🎯 OPTIMIZATION COMPLETED!")
    print(f"📊 Final logo column: {final_logo_column}")
    print(f"🎨 Branding coverage: {insights_result['branding_coverage']:.1f}%")

if __name__ == "__main__":
    main() 