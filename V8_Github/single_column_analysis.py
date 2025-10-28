#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Single Column Deep Analysis
company/followingState/preDashFollowingInfoUrn sütunun kapsamlı analizi
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def analyze_predash_following_info_urn(df):
    """company/followingState/preDashFollowingInfoUrn sütunun detaylı analizi"""
    
    column_name = 'company/followingState/preDashFollowingInfoUrn'
    
    print(f"🔍 KAPSAMLI SÜTUN ANALİZİ: {column_name}")
    print("=" * 80)
    
    if column_name not in df.columns:
        print(f"❌ HATA: '{column_name}' sütunu bulunamadı!")
        available_cols = [col for col in df.columns if 'following' in col.lower()]
        if available_cols:
            print("🔍 Mevcut following sütunları:")
            for col in available_cols:
                print(f"   📋 {col}")
        return None
    
    col_data = df[column_name]
    
    # 1. SÜTUN TEMSİLİ VE ANLAMI
    print("📋 1. SÜTUN TEMSİLİ VE ANLAMI")
    print("-" * 40)
    print("🔗 Bu sütun: LinkedIn Following State URN bilgisini temsil eder")
    print("   📝 İçerik: Company following durumu öncesi URN (Uniform Resource Name) identifiers")
    print("   🎯 Business Value: User-company relationship tracking, engagement analysis")
    print("   📊 Expected Type: Text/String (object) - URN format")
    print("   💼 Domain Context: LinkedIn API following state management")
    print("   🔧 Technical Purpose: Unique identifier for following relationships")
    print()
    
    # 2. TEMEL İSTATİSTİKLER
    print("📊 2. TEMEL İSTATİSTİKLER")
    print("-" * 30)
    total_rows = len(col_data)
    null_count = col_data.isnull().sum()
    non_null_count = total_rows - null_count
    null_percentage = (null_count / total_rows) * 100
    
    print(f"📋 Toplam kayıt: {total_rows:,}")
    print(f"❌ Null değer: {null_count:,} ({null_percentage:.1f}%)")
    print(f"✅ Dolu değer: {non_null_count:,} ({100-null_percentage:.1f}%)")
    print(f"🔧 Mevcut veri tipi: {col_data.dtype}")
    print()
    
    # 3. VERİ TİPİ UYGUNLUĞU KONTROLÜ
    print("⚙️ 3. VERİ TİPİ UYGUNLUĞU KONTROLÜ")
    print("-" * 35)
    
    non_null_data = col_data.dropna()
    if len(non_null_data) > 0:
        # URN format kontrolü
        urn_pattern = r'^urn:'
        valid_urn_format = non_null_data.str.match(urn_pattern, na=False).sum()
        urn_format_pct = (valid_urn_format / len(non_null_data)) * 100 if len(non_null_data) > 0 else 0
        
        # String format kontrolü
        all_strings = all(isinstance(val, str) for val in non_null_data)
        has_numbers = any(str(val).isdigit() for val in non_null_data)
        
        print(f"📝 Tüm değerler string: {'✅ Evet' if all_strings else '❌ Hayır'}")
        print(f"🔗 Valid URN format: {valid_urn_format:,} ({urn_format_pct:.1f}%)")
        print(f"🔢 Sadece sayı olan değerler: {'⚠️ Var' if has_numbers else '✅ Yok'}")
        
        # URN pattern analizi
        if len(non_null_data) > 0:
            sample_values = non_null_data.head(5).tolist()
            print(f"\n📋 Örnek değerler:")
            for i, val in enumerate(sample_values, 1):
                display_val = str(val)[:60] + "..." if len(str(val)) > 60 else str(val)
                print(f"   {i}. {display_val}")
        
        # Önerilen veri tipi
        if urn_format_pct > 90:
            print(f"\n💡 ÖNERİ: 'object' tipi uygun (URN format detected)")
        elif urn_format_pct > 50:
            print(f"\n💡 ÖNERİ: 'object' tipi uygun ama format cleaning gerekli")
        else:
            print(f"\n⚠️ ÖNERİ: Format inconsistency detected - data cleaning required")
    print()
    
    # 4. İÇERİK ANALİZİ VE TUTARLILIK
    print("🔍 4. İÇERİK ANALİZİ VE TUTARLILIK")
    print("-" * 35)
    
    if len(non_null_data) > 0:
        # Benzersiz değer analizi
        unique_values = non_null_data.unique()
        unique_count = len(unique_values)
        value_counts = non_null_data.value_counts()
        
        print(f"🎯 Benzersiz değer sayısı: {unique_count:,}")
        
        if unique_count > 0:
            print(f"📊 En sık değer: '{value_counts.index[0][:50]}...' ({value_counts.iloc[0]:,} kez)")
            
            # Variance level assessment
            if unique_count == 1:
                variance_level = "🔴 ZERO VARIANCE"
            elif unique_count < 10:
                variance_level = "🟡 LOW VARIANCE" 
            elif unique_count < 100:
                variance_level = "🟠 MODERATE VARIANCE"
            else:
                variance_level = "🟢 HIGH VARIANCE"
            
            print(f"📈 Variance Level: {variance_level}")
        
        # URN pattern deep analysis
        print(f"\n🔍 URN Pattern Analysis:")
        
        # URN prefix analysis
        if len(non_null_data) > 0:
            # Extract URN prefixes
            urn_prefixes = []
            for val in non_null_data:
                if str(val).startswith('urn:'):
                    parts = str(val).split(':')
                    if len(parts) >= 3:
                        prefix = ':'.join(parts[:3])  # urn:li:something
                        urn_prefixes.append(prefix)
            
            if urn_prefixes:
                prefix_counts = Counter(urn_prefixes)
                print(f"   🔗 URN prefixes found: {len(prefix_counts)}")
                for prefix, count in prefix_counts.most_common(5):
                    pct = (count / len(urn_prefixes)) * 100
                    print(f"      📊 {prefix}: {count:,} ({pct:.1f}%)")
        
        # Uzunluk analizi
        if col_data.dtype == 'object':
            lengths = non_null_data.astype(str).str.len()
            print(f"\n📏 Karakter uzunluğu analizi:")
            print(f"   Min: {lengths.min()} | Max: {lengths.max()}")
            print(f"   Ortalama: {lengths.mean():.1f} | Medyan: {lengths.median():.1f}")
            
            # Standart URN uzunluğu kontrolü
            std_length_range = (lengths >= 40) & (lengths <= 100)  # Typical URN range
            std_length_count = std_length_range.sum()
            std_length_pct = (std_length_count / len(lengths)) * 100
            
            print(f"   🎯 Standard URN length (40-100 char): {std_length_count:,} ({std_length_pct:.1f}%)")
            
            # Çok kısa veya çok uzun değerleri tespit et
            very_short = (lengths <= 10).sum()
            very_long = (lengths >= 150).sum()
            if very_short > 0:
                print(f"   ⚠️ Çok kısa değerler (≤10 karakter): {very_short}")
            if very_long > 0:
                print(f"   ⚠️ Çok uzun değerler (≥150 karakter): {very_long}")
    print()
    
    # 5. FORMAT TUTARSIZLIKLARI VE STANDARDIZATION
    print("🔧 5. FORMAT TUTARSIZLIKLARI VE STANDARDIZATION")
    print("-" * 45)
    
    if len(non_null_data) > 0:
        # URN format consistency
        valid_urn_pattern = r'^urn:li:[a-zA-Z]+:\d+$'
        valid_urns = non_null_data.str.match(valid_urn_pattern, na=False).sum()
        valid_urn_pct = (valid_urns / len(non_null_data)) * 100
        
        print(f"🔗 Valid LinkedIn URN format: {valid_urns:,} ({valid_urn_pct:.1f}%)")
        
        # Case sensitivity check
        case_variations = len(non_null_data.unique()) != len(non_null_data.str.lower().unique())
        print(f"🔤 Case variations detected: {'⚠️ Yes' if case_variations else '✅ No'}")
        
        # Special character analysis
        special_chars = non_null_data.str.contains(r'[^a-zA-Z0-9:\-_]', regex=True, na=False).sum()
        print(f"🔧 Special characters: {special_chars:,} values")
        
        # Format inconsistency detection
        inconsistent_formats = []
        for val in non_null_data.head(20):  # Sample check
            val_str = str(val)
            if not val_str.startswith('urn:'):
                inconsistent_formats.append(val_str)
        
        if inconsistent_formats:
            print(f"⚠️ Format inconsistencies detected: {len(inconsistent_formats)} samples")
            print("   📋 Inconsistent samples:")
            for sample in inconsistent_formats[:3]:
                print(f"      • {sample[:50]}...")
        else:
            print("✅ Format consistency: Good")
    print()
    
    # 6. DİĞER SÜTUNLARLA İLİŞKİ ANALİZİ
    print("🔗 6. DİĞER SÜTUNLARLA İLİŞKİ ANALİZİ")
    print("-" * 35)
    
    # followingState namespace analysis
    following_state_columns = [col for col in df.columns if 'followingState' in col]
    print(f"🔍 FollowingState namespace sütunları: {len(following_state_columns)}")
    
    for col in following_state_columns:
        if col != column_name:
            # Basic correlation analysis
            try:
                other_data = df[col].dropna()
                if len(other_data) > 0 and len(non_null_data) > 0:
                    # Check for shared null patterns
                    both_null = (df[column_name].isnull() & df[col].isnull()).sum()
                    both_not_null = (df[column_name].notnull() & df[col].notnull()).sum()
                    
                    print(f"   📊 {col}:")
                    print(f"      🔗 Both null: {both_null:,}")
                    print(f"      ✅ Both populated: {both_not_null:,}")
                    
                    # Data type and basic stats
                    print(f"      📈 Other column stats: {len(other_data):,} non-null, {df[col].dtype}")
            except:
                pass
    
    # Company namespace correlation
    company_columns = [col for col in df.columns if col.startswith('company/') and col != column_name]
    high_correlation_cols = []
    
    print(f"\n🏢 Company namespace analysis:")
    for col in company_columns[:5]:  # Check first 5 company columns
        try:
            # Check null pattern correlation
            null_correlation = (df[column_name].isnull() == df[col].isnull()).mean()
            if null_correlation > 0.8:
                high_correlation_cols.append((col, null_correlation))
        except:
            pass
    
    if high_correlation_cols:
        print("   🔗 High null pattern correlation:")
        for col, corr in high_correlation_cols:
            print(f"      📊 {col}: {corr:.1%}")
    else:
        print("   ✅ No significant null pattern correlations")
    print()
    
    # 7. NULL DOLDURMA STRATEJİLERİ
    print("💡 7. NULL DOLDURMA STRATEJİLERİ")
    print("-" * 30)
    
    if null_percentage > 0:
        print(f"📊 Null oranı: %{null_percentage:.1f}")
        
        # Strategy recommendations based on null percentage
        if null_percentage > 80:
            strategy = "🚨 YÜKSEK NULL - Sütun silinmeyi düşünün"
        elif null_percentage > 50:
            strategy = "⚠️ ORTA-YÜKSEK NULL - Özel strateji gerekli"
        elif null_percentage > 20:
            strategy = "🔧 ORTA NULL - Doldurma stratejisi uygulanabilir"
        else:
            strategy = "✅ DÜŞÜK NULL - Minimal intervention"
        
        print(f"📋 Strateji önerisi: {strategy}")
        
        # Specific recommendations for URN data
        print("\n🎯 URN-specific doldurma önerileri:")
        print("   1. 🔗 'UNKNOWN_URN' placeholder value")
        print("   2. 📊 Company/following relationship based imputation")
        print("   3. 🗑️ Row deletion if URN critical for analysis")
        print("   4. 🔄 API re-fetch if possible")
        
        # Business logic recommendations
        print("\n💼 Business logic recommendations:")
        print("   • URN null = User not following company")
        print("   • Could create 'NOT_FOLLOWING' category")
        print("   • Pattern analysis with other following columns")
    else:
        print("✅ No null values detected!")
    print()
    
    # 8. OPTIMIZATION ÖNERİLERİ
    print("🚀 8. OPTIMIZATION ÖNERİLERİ VE EYLEM PLANI")
    print("-" * 45)
    
    recommendations = []
    
    # Data type optimization
    if col_data.dtype == 'object' and len(non_null_data) > 0:
        memory_current = col_data.memory_usage(deep=True) / 1024**2
        recommendations.append(f"💾 Current memory usage: {memory_current:.2f} MB")
        
        # Category conversion possibility
        if unique_count < 1000:
            potential_savings = memory_current * 0.3  # Estimate 30% savings
            recommendations.append(f"🔧 Category conversion potential: -{potential_savings:.2f} MB")
    
    # Format standardization
    if len(non_null_data) > 0:
        if valid_urn_pct < 95:
            recommendations.append("🔧 URN format standardization needed")
        
        if case_variations:
            recommendations.append("🔤 Case normalization recommended")
    
    # Business value assessment
    if unique_count == 1:
        recommendations.append("🚨 CRITICAL: Zero variance - DELETE column")
    elif unique_count < 10:
        recommendations.append("⚠️ Low variance - Question business value")
    elif null_percentage > 80:
        recommendations.append("🚨 High null ratio - Consider deletion")
    else:
        recommendations.append("✅ Good analytical potential")
    
    # Final recommendations
    print("📋 Final Recommendations:")
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    
    # Action priority
    print(f"\n🎯 ACTION PRIORITY:")
    if unique_count == 1:
        priority = "🔴 HIGH - Delete immediately (zero variance)"
    elif null_percentage > 80:
        priority = "🟠 MEDIUM-HIGH - Evaluate deletion vs imputation"
    elif null_percentage > 50:
        priority = "🟡 MEDIUM - Implement imputation strategy"
    else:
        priority = "🟢 LOW - Monitor and optimize format"
    
    print(f"   {priority}")
    
    print("\n" + "=" * 80)
    
    return {
        'column_name': column_name,
        'total_rows': total_rows,
        'null_count': null_count,
        'null_percentage': null_percentage,
        'unique_count': unique_count if len(non_null_data) > 0 else 0,
        'data_type': str(col_data.dtype),
        'urn_format_valid': valid_urn_pct if len(non_null_data) > 0 else 0,
        'recommendations': recommendations
    }

def main():
    """Ana analiz fonksiyonu"""
    
    print("🔍 LinkedIn Jobs Dataset - preDashFollowingInfoUrn Analysis")
    print("=" * 65)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_cleaned_columns.csv')
        print(f"✅ Cleaned dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # Analiz gerçekleştir
    result = analyze_predash_following_info_urn(df)
    
    if result:
        print("🎯 ANALİZ TAMAMLANDI!")
        print(f"📊 Sonuç: {result['unique_count']:,} benzersiz değer, %{result['null_percentage']:.1f} null")
        
        # Critical findings
        if result['unique_count'] <= 1:
            print("🚨 KRİTİK: Zero/minimal variance detected!")
        elif result['null_percentage'] > 80:
            print("⚠️ UYARI: Very high null percentage!")
        elif result['urn_format_valid'] < 50:
            print("⚠️ UYARI: Poor URN format consistency!")
        else:
            print("✅ Sütun genel olarak analiz için uygun görünüyor")

if __name__ == "__main__":
    main() 