#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - company/logo Single Column Deep Analysis
Kapsamlı tek sütun analizi: format, içerik, optimize edilebilirlik
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import urllib.parse
from urllib.parse import urlparse
import warnings
warnings.filterwarnings('ignore')

def analyze_company_logo_column(df):
    """company/logo sütunu için kapsamlı analiz"""
    
    print("🏢 LINKEDIN JOBS DATASET - COMPANY/LOGO COLUMN ANALYSIS")
    print("=" * 65)
    
    column_name = 'company/logo'
    
    # Check if column exists
    if column_name not in df.columns:
        print(f"❌ HATA: {column_name} sütunu bulunamadı!")
        return None
    
    col_data = df[column_name]
    
    # 1. SÜTUN TEMSİLİ VE ANLAMI
    print("📋 1. SÜTUN TEMSİLİ VE ANLAMI")
    print("-" * 35)
    
    column_info = {
        'name': column_name,
        'purpose': 'Company Logo URL/Path Storage',
        'content_type': 'URL/URI pointing to company logo image',
        'business_value': 'Visual branding, company identification, UI/UX enhancement',
        'expected_format': 'HTTP/HTTPS URLs or relative paths to image files',
        'source': 'LinkedIn Company API - Logo image reference',
        'data_usage': 'Frontend display, company branding, visual analytics',
        'expected_file_types': 'JPG, PNG, SVG, WebP image formats'
    }
    
    print(f"🏢 {column_info['name']}:")
    print(f"   📝 Purpose: {column_info['purpose']}")
    print(f"   💼 Content Type: {column_info['content_type']}")
    print(f"   🎯 Business Value: {column_info['business_value']}")
    print(f"   📊 Expected Format: {column_info['expected_format']}")
    print(f"   🔗 Source: {column_info['source']}")
    print(f"   🎨 Usage: {column_info['data_usage']}")
    print(f"   📸 Expected Types: {column_info['expected_file_types']}")
    print()
    
    # 2. TEMEL İSTATİSTİKLER
    print("📊 2. TEMEL İSTATİSTİKLER")
    print("-" * 25)
    
    total_rows = len(col_data)
    null_count = col_data.isnull().sum()
    non_null_count = total_rows - null_count
    null_percentage = (null_count / total_rows) * 100
    unique_count = len(col_data.dropna().unique()) if non_null_count > 0 else 0
    memory_usage = col_data.memory_usage(deep=True) / 1024**2
    
    basic_stats = {
        'total_rows': total_rows,
        'null_count': null_count,
        'non_null_count': non_null_count,
        'null_percentage': null_percentage,
        'unique_count': unique_count,
        'memory_mb': memory_usage,
        'data_type': str(col_data.dtype)
    }
    
    print(f"📊 Temel İstatistikler:")
    print(f"   📈 Toplam kayıt: {total_rows:,}")
    print(f"   ❌ Null: {null_count:,} ({null_percentage:.1f}%)")
    print(f"   ✅ Dolu: {non_null_count:,} ({100-null_percentage:.1f}%)")
    print(f"   🎯 Benzersiz: {unique_count:,}")
    print(f"   💾 Memory: {memory_usage:.2f} MB")
    print(f"   🔧 Tip: {col_data.dtype}")
    print()
    
    if non_null_count == 0:
        print("❌ HATA: Hiç veri yok, analiz durduruluyor!")
        return None
    
    # 3. İÇERİK TUTARLILİK ANALİZİ
    print("🔍 3. İÇERİK TUTARLILİK ANALİZİ")
    print("-" * 35)
    
    non_null_data = col_data.dropna()
    
    # URL format detection
    url_patterns = {
        'http_urls': len(non_null_data[non_null_data.str.startswith('http://', na=False)]),
        'https_urls': len(non_null_data[non_null_data.str.startswith('https://', na=False)]),
        'relative_paths': len(non_null_data[non_null_data.str.startswith('/', na=False)]),
        'data_urls': len(non_null_data[non_null_data.str.startswith('data:', na=False)]),
        'other_protocols': len(non_null_data[~non_null_data.str.startswith(('http://', 'https://', '/', 'data:'), na=False)])
    }
    
    print(f"🔗 URL Format Dağılımı:")
    for format_type, count in url_patterns.items():
        pct = (count / non_null_count) * 100 if non_null_count > 0 else 0
        print(f"   {format_type}: {count:,} ({pct:.1f}%)")
    
    # Domain analysis for URLs
    domains = []
    invalid_urls = 0
    
    for url in non_null_data:
        try:
            if str(url).startswith(('http://', 'https://')):
                parsed = urlparse(str(url))
                if parsed.netloc:
                    domains.append(parsed.netloc.lower())
                else:
                    invalid_urls += 1
            else:
                # Non-URL entries
                pass
        except:
            invalid_urls += 1
    
    if domains:
        domain_counts = Counter(domains)
        print(f"\n🌐 Top Domains (URLs only):")
        for domain, count in domain_counts.most_common(5):
            pct = (count / len(domains)) * 100
            print(f"   {domain}: {count:,} ({pct:.1f}%)")
    
    if invalid_urls > 0:
        print(f"\n⚠️ Invalid URL formats: {invalid_urls:,}")
    
    # File extension analysis
    extensions = []
    for url in non_null_data:
        url_str = str(url).lower()
        # Extract extension from URL path
        path = urlparse(url_str).path if url_str.startswith(('http://', 'https://')) else url_str
        if '.' in path:
            ext = path.split('.')[-1].split('?')[0].split('#')[0]  # Remove query params
            if len(ext) <= 5:  # Reasonable extension length
                extensions.append(ext)
    
    if extensions:
        ext_counts = Counter(extensions)
        print(f"\n📸 File Extensions:")
        for ext, count in ext_counts.most_common(8):
            pct = (count / len(extensions)) * 100
            print(f"   .{ext}: {count:,} ({pct:.1f}%)")
    
    # 4. VERİ TİPİ UYUMLULUĞU
    print(f"\n🔧 4. VERİ TİPİ UYUMLULUĞU")
    print("-" * 25)
    
    current_type = col_data.dtype
    print(f"📊 Mevcut veri tipi: {current_type}")
    
    # Check if all non-null values are strings
    string_compatible = True
    non_string_count = 0
    
    for val in non_null_data:
        if not isinstance(val, (str, type(np.nan))):
            string_compatible = False
            non_string_count += 1
    
    print(f"🔤 String uyumluluğu: {'✅ Uyumlu' if string_compatible else f'❌ {non_string_count} uyumsuz'}")
    
    # URL length analysis
    lengths = non_null_data.astype(str).str.len()
    length_stats = {
        'min': lengths.min(),
        'max': lengths.max(),
        'mean': lengths.mean(),
        'median': lengths.median(),
        'std': lengths.std()
    }
    
    print(f"📏 URL Length İstatistikleri:")
    print(f"   Min: {length_stats['min']} karakter")
    print(f"   Max: {length_stats['max']} karakter") 
    print(f"   Ortalama: {length_stats['mean']:.1f} karakter")
    print(f"   Medyan: {length_stats['median']:.1f} karakter")
    print(f"   Std: {length_stats['std']:.1f}")
    
    # Unusual length detection
    unusual_short = len(lengths[lengths < 10])
    unusual_long = len(lengths[lengths > 200])
    
    if unusual_short > 0:
        print(f"   ⚠️ Çok kısa URL'ler (<10 char): {unusual_short:,}")
    if unusual_long > 0:
        print(f"   ⚠️ Çok uzun URL'ler (>200 char): {unusual_long:,}")
    
    # 5. BOŞ ALAN YOĞUNLUKİ VE DOLDURMA ÖNERİLERİ
    print(f"\n📈 5. BOŞ ALAN YOĞUNLUĞİ VE DOLDURMA ÖNERİLERİ")
    print("-" * 50)
    
    print(f"📊 Null Analizi:")
    print(f"   Null oran: {null_percentage:.1f}%")
    
    if null_percentage > 0:
        # Analyze null pattern by company
        if 'company/name' in df.columns:
            company_logo_stats = df.groupby('company/name').agg({
                column_name: ['count', lambda x: x.isnull().sum()]
            }).round(2)
            
            companies_with_logos = len(df[df['company/name'].notna() & df[column_name].notna()]['company/name'].unique())
            total_companies = len(df[df['company/name'].notna()]['company/name'].unique())
            
            print(f"   🏢 Logo'lu şirket sayısı: {companies_with_logos:,}/{total_companies:,}")
            print(f"   📈 Şirket logo coverage: {(companies_with_logos/total_companies)*100:.1f}%")
    
    print(f"\n💡 Doldurma Önerileri:")
    if null_percentage > 50:
        print(f"   🚨 Yüksek null oran ({null_percentage:.1f}%) - DELETE candidate")
    elif null_percentage > 20:
        print(f"   ⚠️ Orta seviye null - Default placeholder önerisi")
        print(f"   💡 Default: 'https://static.licdn.com/company/default-logo.png'")
    else:
        print(f"   ✅ Kabul edilebilir null oran ({null_percentage:.1f}%)")
    
    # 6. FORMAT STANDARDİZASYONU
    print(f"\n🔧 6. FORMAT STANDARDİZASYONU")
    print("-" * 30)
    
    format_issues = {
        'mixed_protocols': 0,
        'inconsistent_domains': 0,
        'malformed_urls': 0,
        'case_variations': 0
    }
    
    # Protocol analysis
    http_count = url_patterns['http_urls']
    https_count = url_patterns['https_urls']
    
    if http_count > 0 and https_count > 0:
        format_issues['mixed_protocols'] = http_count + https_count
        print(f"⚠️ Mixed protocols detected: {http_count} HTTP, {https_count} HTTPS")
        print(f"   💡 Öneri: Tüm HTTP → HTTPS conversion")
    
    # Case sensitivity check
    if domains:
        original_domains = set(domains)
        normalized_domains = set(d.lower() for d in domains)
        if len(original_domains) != len(normalized_domains):
            format_issues['case_variations'] = len(original_domains) - len(normalized_domains)
            print(f"⚠️ Case variations detected in domains")
    
    # Malformed URL detection
    malformed_count = 0
    for url in non_null_data.head(100):  # Sample check
        url_str = str(url)
        if url_str.startswith(('http://', 'https://')):
            try:
                parsed = urlparse(url_str)
                if not parsed.netloc or not parsed.scheme:
                    malformed_count += 1
            except:
                malformed_count += 1
    
    if malformed_count > 0:
        estimated_malformed = (malformed_count / 100) * non_null_count
        print(f"⚠️ Estimated malformed URLs: ~{estimated_malformed:.0f}")
        format_issues['malformed_urls'] = estimated_malformed
    
    # Standardization recommendations
    print(f"\n💡 Standardization Önerileri:")
    if format_issues['mixed_protocols'] > 0:
        print(f"   1. HTTP → HTTPS conversion ({http_count:,} URLs)")
    if format_issues['case_variations'] > 0:
        print(f"   2. Domain case normalization")
    if format_issues['malformed_urls'] > 0:
        print(f"   3. URL validation ve cleanup (~{format_issues['malformed_urls']:.0f} URLs)")
    
    # 7. DİĞER SÜTUNLARLA BENZERLIK ANALİZİ
    print(f"\n🔗 7. DİĞER SÜTUNLARLA BENZERLIK ANALİZİ")
    print("-" * 40)
    
    # Look for similar columns
    potential_similar_columns = []
    for col in df.columns:
        if col != column_name:
            if any(keyword in col.lower() for keyword in ['logo', 'image', 'picture', 'avatar', 'icon', 'media']):
                potential_similar_columns.append(col)
    
    print(f"🔍 Potential similar columns:")
    if potential_similar_columns:
        for sim_col in potential_similar_columns:
            sim_null_pct = (df[sim_col].isnull().sum() / len(df)) * 100
            sim_unique = df[sim_col].nunique()
            print(f"   📋 {sim_col}: {sim_unique:,} unique, {sim_null_pct:.1f}% null")
    else:
        print(f"   ✅ No similar columns detected")
    
    # Company name correlation analysis
    if 'company/name' in df.columns:
        # Check if company logos are unique per company
        company_logo_pairs = df[['company/name', column_name]].dropna()
        if len(company_logo_pairs) > 0:
            unique_companies = company_logo_pairs['company/name'].nunique()
            unique_logos = company_logo_pairs[column_name].nunique()
            
            print(f"\n🏢 Company-Logo Relationship:")
            print(f"   Companies with logos: {unique_companies:,}")
            print(f"   Unique logos: {unique_logos:,}")
            print(f"   Logo/Company ratio: {unique_logos/unique_companies:.2f}")
            
            if unique_logos > unique_companies:
                print(f"   ⚠️ More logos than companies - possible duplicates or variations")
            elif unique_logos < unique_companies * 0.8:
                print(f"   ⚠️ Many companies share logos - possible generic/default logos")
    
    # 8. OPTİMİZASYON ÖNERİLERİ
    print(f"\n💡 8. OPTİMİZASYON ÖNERİLERİ")
    print("-" * 30)
    
    optimization_recommendations = []
    
    # Memory optimization
    if unique_count < 1000:
        potential_savings = memory_usage * 0.7
        optimization_recommendations.append(f"🔧 Category type conversion (save ~{potential_savings:.2f} MB)")
    
    # URL optimization
    if url_patterns['http_urls'] > 0:
        optimization_recommendations.append(f"🔒 HTTP → HTTPS migration ({url_patterns['http_urls']:,} URLs)")
    
    # Default value suggestion
    if null_percentage > 10:
        optimization_recommendations.append(f"🎨 Default logo implementation for {null_count:,} records")
    
    # Compression possibilities
    if domains and len(set(domains)) < len(domains) * 0.5:
        optimization_recommendations.append(f"📦 URL compression (many shared domains)")
    
    print(f"📋 Öneriler:")
    for i, rec in enumerate(optimization_recommendations, 1):
        print(f"   {i}. {rec}")
    
    # 9. KRİTİK BULGULAR VE KARARLAR
    print(f"\n🎯 9. KRİTİK BULGULAR VE KARARLAR")
    print("-" * 35)
    
    critical_findings = []
    
    # High null percentage
    if null_percentage > 50:
        critical_findings.append(f"🚨 HIGH NULL RATIO ({null_percentage:.1f}%) - DELETE CANDIDATE")
    elif null_percentage > 30:
        critical_findings.append(f"⚠️ MODERATE NULL RATIO ({null_percentage:.1f}%) - NEEDS ATTENTION")
    
    # URL format consistency
    if format_issues['mixed_protocols'] > 100:
        critical_findings.append(f"⚠️ MIXED PROTOCOLS - STANDARDIZATION REQUIRED")
    
    # Business value assessment
    if unique_count < total_rows * 0.1:
        critical_findings.append(f"⚠️ LOW VARIETY - Many duplicate/default logos")
    
    print(f"🔍 Critical Findings:")
    if critical_findings:
        for finding in critical_findings:
            print(f"   • {finding}")
    else:
        print(f"   ✅ No critical issues detected")
    
    # Final recommendation
    print(f"\n🎯 FINAL RECOMMENDATION:")
    if null_percentage > 60:
        print(f"   🗑️ RECOMMENDATION: DELETE COLUMN (low business value)")
        action = "DELETE"
    elif null_percentage > 30:
        print(f"   🔧 RECOMMENDATION: OPTIMIZE with default values")
        action = "OPTIMIZE"
    else:
        print(f"   ✅ RECOMMENDATION: KEEP and standardize formats")
        action = "KEEP"
    
    print("\n" + "=" * 65)
    
    return {
        'column_name': column_name,
        'basic_stats': basic_stats,
        'url_patterns': url_patterns,
        'format_issues': format_issues,
        'length_stats': length_stats,
        'optimization_recommendations': optimization_recommendations,
        'critical_findings': critical_findings,
        'final_action': action
    }

def main():
    """Ana analiz fonksiyonu"""
    
    print("🔍 LinkedIn Jobs Dataset - company/logo Column Analysis")
    print("=" * 60)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step3.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # company/logo analizi gerçekleştir
    result = analyze_company_logo_column(df)
    
    if result:
        print("🎯 COMPANY/LOGO ANALİZİ TAMAMLANDI!")
        print(f"📊 Final Action: {result['final_action']}")
        
        if result['final_action'] == 'DELETE':
            print("🚨 COLUMN DELETION RECOMMENDED!")
        elif result['final_action'] == 'OPTIMIZE':
            print("🔧 OPTIMIZATION REQUIRED!")
        else:
            print("✅ COLUMN STRUCTURE ACCEPTABLE!")

if __name__ == "__main__":
    main() 