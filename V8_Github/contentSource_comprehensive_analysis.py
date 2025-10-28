#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - contentSource Column Comprehensive Analysis
ContentSource sütununun derinlemesine analizi: format, tutarlılık, veri tipi uyumluluğu, diğer sütunlarla benzerlik
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def analyze_contentSource_comprehensive(df):
    """contentSource sütunu için kapsamlı analiz"""
    
    print("🔍 LINKEDIN JOBS DATASET - CONTENTSOURCE COLUMN COMPREHENSIVE ANALYSIS")
    print("=" * 75)
    
    column_name = 'contentSource'
    
    # Check if column exists
    if column_name not in df.columns:
        print(f"❌ HATA: {column_name} sütunu bulunamadı!")
        print(f"📋 Mevcut sütunlar: {list(df.columns)}")
        return None
    
    col_data = df[column_name]
    
    # 1. SÜTUN TEMSİLİ VE ANLAMI
    print("🏗️ 1. SÜTUN TEMSİLİ VE ANLAMI")
    print("-" * 35)
    
    column_info = {
        'name': column_name,
        'purpose': 'Job Content Source Classification',
        'content_type': 'LinkedIn Job Source Type Identifier',
        'business_value': 'Job posting source analysis, premium vs organic classification',
        'expected_format': 'Categorical string values (JOBS_PREMIUM, JOBS_PREMIUM_OFFLINE, JOBS_CREATE)',
        'source': 'LinkedIn Jobs API - Content source metadata',
        'data_usage': 'Job quality analysis, premium content identification, source filtering',
        'api_context': 'LinkedIn backend job processing pipeline identifier'
    }
    
    print(f"📊 {column_info['name']}:")
    print(f"   📝 Purpose: {column_info['purpose']}")
    print(f"   💼 Content Type: {column_info['content_type']}")
    print(f"   🎯 Business Value: {column_info['business_value']}")
    print(f"   📋 Expected Format: {column_info['expected_format']}")
    print(f"   🔗 Source: {column_info['source']}")
    print(f"   🎨 Usage: {column_info['data_usage']}")
    print(f"   🔧 API Context: {column_info['api_context']}")
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
    
    print(f"📈 Temel İstatistikler:")
    print(f"   📊 Toplam kayıt: {total_rows:,}")
    print(f"   ❌ Null: {null_count:,} ({null_percentage:.1f}%)")
    print(f"   ✅ Dolu: {non_null_count:,} ({100-null_percentage:.1f}%)")
    print(f"   🎯 Benzersiz değer: {unique_count:,}")
    print(f"   💾 Memory kullanımı: {memory_usage:.3f} MB")
    print(f"   🔧 Mevcut veri tipi: {col_data.dtype}")
    print()
    
    if non_null_count == 0:
        print("❌ HATA: Hiç veri yok, analiz durduruluyor!")
        return None
    
    # 3. VERİ TİPİ UYUMLULUĞU KONTROLÜ
    print("⚙️ 3. VERİ TİPİ UYUMLULUĞU KONTROLÜ")
    print("-" * 35)
    
    non_null_data = col_data.dropna()
    current_dtype = str(col_data.dtype)
    
    # Check if all values are strings
    all_strings = all(isinstance(val, str) for val in non_null_data)
    has_numbers = any(str(val).isdigit() for val in non_null_data)
    has_mixed = any(bool(re.search(r'\d', str(val))) and bool(re.search(r'[a-zA-Z]', str(val))) 
                   for val in non_null_data)
    
    print(f"📝 Mevcut veri tipi: {current_dtype}")
    print(f"🔤 Tüm değerler string: {'✅ Evet' if all_strings else '❌ Hayır'}")
    print(f"🔢 Sayı içeren değerler: {'⚠️ Var' if has_numbers else '✅ Yok'}")
    print(f"🔤 Karışık içerik: {'⚠️ Var' if has_mixed else '✅ Yok'}")
    
    # Recommended data type
    if unique_count <= 20:
        print(f"💡 ÖNERİ: 'category' tipine çevrilebilir!")
        print(f"   🎯 Sebep: Sadece {unique_count} benzersiz değer var")
        print(f"   💾 Memory Kazancı: %50-90 memory tasarrufu bekleniyor")
        recommended_type = 'category'
    else:
        print(f"💡 ÖNERİ: 'object' tipi uygun")
        print(f"   🎯 Sebep: {unique_count} benzersiz değer, category için fazla")
        recommended_type = 'object'
    
    print(f"🎯 Recommended Type: {recommended_type}")
    print()
    
    # 4. İÇERİK TUTARLILİK ANALİZİ
    print("🔍 4. İÇERİK TUTARLILİK ANALİZİ")
    print("-" * 30)
    
    # Value distribution analysis
    value_counts = non_null_data.value_counts()
    value_distribution = (non_null_data.value_counts(normalize=True) * 100).round(2)
    
    print(f"📋 Değer Dağılımı ({unique_count} benzersiz değer):")
    for value, count in value_counts.head(10).items():
        percentage = value_distribution[value]
        print(f"   📊 '{value}': {count:,} kayıt ({percentage:.1f}%)")
    
    if len(value_counts) > 10:
        print(f"   📝 ... ve {len(value_counts)-10} değer daha")
    print()
    
    # 5. VARIANCE ANALİZİ (ÖNEMLİ!)
    print("🎯 5. VARIANCE ANALİZİ (KRİTİK!)")
    print("-" * 30)
    
    if unique_count == 1:
        print("🚨 KRİTİK: ZERO VARIANCE DETECTED!")
        print(f"   📊 Tek değer: '{value_counts.index[0]}'")
        print(f"   ❌ Analitik değer: NONE")
        print(f"   💡 ÖNERİ: DELETE column (zero variance)")
        variance_issue = "ZERO_VARIANCE"
    elif unique_count <= 3:
        print("⚠️ DİKKAT: Very Low Variance!")
        print(f"   📊 Sadece {unique_count} değer var")
        print(f"   🎯 Category conversion HIGHLY recommended")
        variance_issue = "LOW_VARIANCE"
    else:
        print("✅ İyi: Normal variance seviyesi")
        variance_issue = "NORMAL"
    print()
    
    # 6. FORMAT STANDARDİZASYON ANALİZİ
    print("📝 6. FORMAT STANDARDİZASYON ANALİZİ")
    print("-" * 35)
    
    format_issues = []
    
    # Case analysis
    has_lowercase = any(val.islower() for val in non_null_data if isinstance(val, str))
    has_uppercase = any(val.isupper() for val in non_null_data if isinstance(val, str))
    has_mixed_case = any(val != val.upper() and val != val.lower() for val in non_null_data if isinstance(val, str))
    
    print(f"📋 Case Analizi:")
    print(f"   🔤 Lowercase var: {'⚠️ Evet' if has_lowercase else '✅ Hayır'}")
    print(f"   🔠 Uppercase var: {'✅ Evet' if has_uppercase else '⚠️ Hayır'}")
    print(f"   🔤 Mixed case var: {'⚠️ Evet' if has_mixed_case else '✅ Hayır'}")
    
    # Special characters analysis
    special_chars = set()
    for val in non_null_data:
        if isinstance(val, str):
            special_chars.update(char for char in val if not char.isalnum())
    
    print(f"📋 Özel Karakter Analizi:")
    print(f"   🔧 Bulunan özel karakterler: {sorted(special_chars) if special_chars else 'YOK'}")
    
    # Whitespace analysis
    has_leading_spaces = any(str(val).startswith(' ') for val in non_null_data)
    has_trailing_spaces = any(str(val).endswith(' ') for val in non_null_data)
    has_multiple_spaces = any('  ' in str(val) for val in non_null_data)
    
    print(f"📋 Whitespace Analizi:")
    print(f"   ⬅️ Leading spaces: {'⚠️ Var' if has_leading_spaces else '✅ Yok'}")
    print(f"   ➡️ Trailing spaces: {'⚠️ Var' if has_trailing_spaces else '✅ Yok'}")
    print(f"   🔄 Multiple spaces: {'⚠️ Var' if has_multiple_spaces else '✅ Yok'}")
    
    if has_lowercase or has_mixed_case or special_chars or has_leading_spaces or has_trailing_spaces or has_multiple_spaces:
        print(f"\n💡 FORMAT STANDARDİZASYON ÖNERİSİ:")
        if has_lowercase or has_mixed_case:
            print(f"   🔠 Case standardization: UPPERCASE öneriliyor")
        if has_leading_spaces or has_trailing_spaces:
            print(f"   ✂️ Whitespace cleanup: strip() işlemi")
        if has_multiple_spaces:
            print(f"   🔄 Multiple space normalization gerekli")
    else:
        print(f"\n✅ Format: Standardizasyon gerekmez")
    print()
    
    # 7. BOŞ ALAN YoĞUNLUĞU VE DOLDURMA ÖNERİLERİ
    print("🕳️ 7. BOŞ ALAN YOĞUNLUĞU VE DOLDURMA ÖNERİLERİ")
    print("-" * 45)
    
    if null_count > 0:
        print(f"📊 Null oranı: {null_percentage:.1f}% ({null_count:,} kayıt)")
        
        if null_percentage < 5:
            print("✅ Düşük null oranı - problematik değil")
            fill_recommendation = "NOT_REQUIRED"
        elif null_percentage < 15:
            print("⚠️ Orta seviye null oranı")
            fill_recommendation = "OPTIONAL"
        else:
            print("🚨 Yüksek null oranı - dikkate alınmalı")
            fill_recommendation = "RECOMMENDED"
        
        print(f"\n💡 NULL DOLDURMA ÖNERİLERİ:")
        print(f"   🎯 İş Logic: En yaygın değer ile doldur")
        if len(value_counts) > 0:
            most_common = value_counts.index[0]
            most_common_pct = value_distribution.iloc[0]
            print(f"   📊 En yaygın: '{most_common}' ({most_common_pct:.1f}%)")
        print(f"   🔧 Alternative: 'UNKNOWN' ya da 'NOT_SPECIFIED' değeri")
        print(f"   ⚠️ Risk: Business logic'i değiştirebilir")
    else:
        print("✅ Null değer yok - mükemmel!")
        fill_recommendation = "NOT_NEEDED"
    print()
    
    # 8. DİĞER SÜTUNLARLA BENZERLİK KONTROLÜ
    print("🔍 8. DİĞER SÜTUNLARLA BENZERLİK KONTROLÜ")
    print("-" * 40)
    
    similar_columns = []
    potential_source_columns = []
    
    # Check for similar column names or content patterns
    for other_col in df.columns:
        if other_col != column_name:
            # Name similarity check
            if ('source' in other_col.lower() or 
                'content' in other_col.lower() or 
                'type' in other_col.lower() or
                'category' in other_col.lower() or
                'premium' in other_col.lower() or
                'jobs' in other_col.lower()):
                
                potential_source_columns.append(other_col)
    
    print(f"🔍 Potansiyel benzer sütunlar:")
    if potential_source_columns:
        for col in potential_source_columns[:10]:  # Show first 10
            print(f"   📝 {col}")
        if len(potential_source_columns) > 10:
            print(f"   📝 ... ve {len(potential_source_columns)-10} sütun daha")
        
        print(f"\n💡 BENZERLİK ANALİZİ ÖNERİSİ:")
        print(f"   🔍 Bu sütunların içeriğini detaylı karşılaştır")
        print(f"   📊 Value overlap oranlarını hesapla")
        print(f"   🎯 Eğer >80% overlap varsa, duplicate possibility")
    else:
        print("   ✅ Benzer sütun bulunamadı")
    print()
    
    # 9. SÜTUN ÇOĞULLAŞMASı KONTROLÜ  
    print("🔄 9. SÜTUN ÇOĞULLAŞMASI KONTROLÜ")
    print("-" * 35)
    
    # Check for numbered variations or namespace patterns
    related_columns = []
    base_name = column_name.split('/')[0] if '/' in column_name else column_name
    
    for col in df.columns:
        if (base_name in col and col != column_name) or \
           (column_name in col and col != column_name):
            related_columns.append(col)
    
    if related_columns:
        print(f"🔍 İlgili sütunlar bulundu:")
        for col in related_columns:
            print(f"   📝 {col}")
        
        print(f"\n💡 ÇOĞULLAŞMA ANALİZİ ÖNERİSİ:")
        print(f"   🔍 Array/list pattern check et")
        print(f"   📊 Content distribution analiz et")
        print(f"   🎯 Consolidation opportunity'leri araştır")
    else:
        print("✅ Çoğullaşmış sütun bulunamadı")
    print()
    
    # 10. STRATEJİK DEĞERLENDİRME VE ÖNERİLER
    print("🎯 10. STRATEJİK DEĞERLENDİRME VE ÖNERİLER")
    print("-" * 45)
    
    recommendations = []
    
    # Data type optimization
    if recommended_type == 'category':
        recommendations.append("🔧 DATA TYPE: 'category' tipine çevir (memory optimization)")
    
    # Variance issue handling
    if variance_issue == "ZERO_VARIANCE":
        recommendations.append("🚨 DELETE: Zero variance - analitik değer yok")
    elif variance_issue == "LOW_VARIANCE":
        recommendations.append("⚠️ CONSIDER: Low variance - consolidation opportunity")
    
    # Null handling
    if fill_recommendation in ["RECOMMENDED", "OPTIONAL"]:
        recommendations.append(f"🕳️ NULL FILL: {fill_recommendation} - business logic ile doldur")
    
    # Format standardization
    if format_issues:
        recommendations.append("📝 FORMAT: Standardization gerekli")
    
    print(f"📋 Öncelikli Öneriler:")
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   ✅ Sütun optimize edilmiş durumda")
    
    print(f"\n🎯 OVERALL ASSESSMENT:")
    
    # Calculate overall quality score
    quality_score = 0
    if null_percentage < 5: quality_score += 25
    elif null_percentage < 15: quality_score += 15
    elif null_percentage < 25: quality_score += 5
    
    if variance_issue == "NORMAL": quality_score += 25
    elif variance_issue == "LOW_VARIANCE": quality_score += 15
    elif variance_issue == "ZERO_VARIANCE": quality_score += 0
    
    if unique_count <= 20: quality_score += 20  # Good for category
    elif unique_count <= 100: quality_score += 15
    else: quality_score += 10
    
    if len(format_issues) == 0: quality_score += 15
    else: quality_score += max(0, 15 - len(format_issues) * 3)
    
    if recommended_type == 'category': quality_score += 15
    else: quality_score += 10
    
    print(f"   📊 Quality Score: {quality_score}/100")
    
    if quality_score >= 80:
        overall_status = "EXCELLENT"
        action = "OPTIMIZE for category type"
    elif quality_score >= 60:
        overall_status = "GOOD" 
        action = "MINOR optimizations needed"
    elif quality_score >= 40:
        overall_status = "PROBLEMATIC"
        action = "SIGNIFICANT improvements required"
    else:
        overall_status = "CRITICAL"
        action = "CONSIDER DELETION or major restructuring"
    
    print(f"   🎯 Status: {overall_status}")
    print(f"   💡 Action: {action}")
    print()
    
    return {
        'column_name': column_name,
        'total_rows': total_rows,
        'null_count': null_count,
        'null_percentage': null_percentage,
        'unique_count': unique_count,
        'memory_mb': memory_usage,
        'data_type': current_dtype,
        'recommended_type': recommended_type,
        'variance_issue': variance_issue,
        'quality_score': quality_score,
        'overall_status': overall_status,
        'action_required': action,
        'recommendations': recommendations,
        'format_issues': format_issues,
        'similar_columns': potential_source_columns,
        'related_columns': related_columns
    }

if __name__ == "__main__":
    # Load the dataset
    try:
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_insights_completed.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} kayıt, {len(df.columns)} sütun")
        print()
        
        # Run analysis
        result = analyze_contentSource_comprehensive(df)
        
        if result:
            print("✅ Analiz tamamlandı!")
        else:
            print("❌ Analiz başarısız!")
            
    except FileNotFoundError:
        print("❌ HATA: Dataset dosyası bulunamadı!")
        print("📂 Lütfen 'linkedin_jobs_dataset_insights_completed.csv' dosyasının var olduğundan emin olun")
    except Exception as e:
        print(f"❌ HATA: {str(e)}") 