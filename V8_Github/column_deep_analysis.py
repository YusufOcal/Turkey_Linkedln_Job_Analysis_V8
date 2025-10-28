#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Column Deep Analysis
merged_companyDescription ve company/followingState/followingType sütunlarının detaylı analizi
"""

import pandas as pd
import numpy as np
from collections import Counter
import re
import warnings
warnings.filterwarnings('ignore')

def analyze_column_deep(df, column_name):
    """Belirli bir sütun için kapsamlı analiz yapar"""
    
    print(f"🔍 DETAYLI ANALIZ: {column_name}")
    print("=" * 80)
    
    if column_name not in df.columns:
        print(f"❌ HATA: '{column_name}' sütunu bulunamadı!")
        return None
    
    col_data = df[column_name]
    
    # 1. SÜTUN TEMSİLİ - Ne temsil ediyor?
    print("📋 1. SÜTUN TEMSİLİ VE ANLAMI")
    print("-" * 40)
    
    if 'companyDescription' in column_name:
        print("🏢 Bu sütun: Şirket açıklamalarını (descriptions) temsil eder")
        print("   📝 İçerik: Şirketlerin kendilerini tanıttığı metin bilgileri")
        print("   🎯 Business Value: Şirket profili analizi, sector classification")
        print("   📊 Expected Type: Text/String (object)")
    
    elif 'followingType' in column_name:
        print("👥 Bu sütun: LinkedIn'de takip türü kategorisini temsil eder")
        print("   📝 İçerik: Kullanıcıların şirketi nasıl takip ettiği (PERSON, COMPANY, vb.)")
        print("   🎯 Business Value: User engagement analysis, following behavior")
        print("   📊 Expected Type: Categorical (object veya category)")
    
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
    print("⚙️ 3. VERİ TİPİ UYGUNLUĞU")
    print("-" * 25)
    
    non_null_data = col_data.dropna()
    if len(non_null_data) > 0:
        # String kontrolü
        all_strings = all(isinstance(val, str) for val in non_null_data)
        has_numbers = any(str(val).isdigit() for val in non_null_data)
        has_mixed = any(bool(re.search(r'\d', str(val))) and bool(re.search(r'[a-zA-Z]', str(val))) 
                       for val in non_null_data)
        
        print(f"📝 Tüm değerler string: {'✅ Evet' if all_strings else '❌ Hayır'}")
        print(f"🔢 Sayı içeren değerler: {'⚠️ Var' if has_numbers else '✅ Yok'}")
        print(f"🔤 Karışık içerik: {'⚠️ Var' if has_mixed else '✅ Yok'}")
        
        # Önerilen veri tipi
        if 'followingType' in column_name:
            unique_count = len(non_null_data.unique())
            if unique_count < 20:
                print(f"💡 ÖNERİ: 'category' tipine çevrilebilir ({unique_count} benzersiz değer)")
            else:
                print(f"💡 ÖNERİ: 'object' tipi uygun ({unique_count} benzersiz değer)")
        else:
            print("💡 ÖNERİ: 'object' tipi uygun (text content)")
    print()
    
    # 4. İÇERİK ANALİZİ VE TUTARSIZLIK TESPİTİ
    print("🔍 4. İÇERİK ANALİZİ VE TUTARLILIK")
    print("-" * 35)
    
    if len(non_null_data) > 0:
        # Benzersiz değer analizi
        unique_values = non_null_data.unique()
        unique_count = len(unique_values)
        value_counts = non_null_data.value_counts()
        
        print(f"🎯 Benzersiz değer sayısı: {unique_count:,}")
        print(f"📊 En sık değer: '{value_counts.index[0]}' ({value_counts.iloc[0]:,} kez)")
        
        if unique_count <= 20:
            print("\n📋 Tüm benzersiz değerler:")
            for i, (value, count) in enumerate(value_counts.items(), 1):
                percentage = (count / len(non_null_data)) * 100
                print(f"   {i:2d}. '{value}' → {count:,} ({percentage:.1f}%)")
        else:
            print(f"\n📋 En sık 10 değer:")
            for i, (value, count) in enumerate(value_counts.head(10).items(), 1):
                percentage = (count / len(non_null_data)) * 100
                # Uzun metinleri kısalt
                display_value = value[:50] + "..." if len(str(value)) > 50 else value
                print(f"   {i:2d}. '{display_value}' → {count:,} ({percentage:.1f}%)")
        
        # Uzunluk analizi (text için)
        if col_data.dtype == 'object':
            lengths = non_null_data.astype(str).str.len()
            print(f"\n📏 Karakter uzunluğu analizi:")
            print(f"   Min: {lengths.min()} | Max: {lengths.max()}")
            print(f"   Ortalama: {lengths.mean():.1f} | Medyan: {lengths.median():.1f}")
            
            # Çok kısa veya çok uzun değerleri tespit et
            very_short = (lengths <= 2).sum()
            very_long = (lengths >= 1000).sum()
            if very_short > 0:
                print(f"   ⚠️ Çok kısa değerler (≤2 karakter): {very_short}")
            if very_long > 0:
                print(f"   ⚠️ Çok uzun değerler (≥1000 karakter): {very_long}")
    print()
    
    # 5. FORMAT TUTARSIZLIKLARI
    print("🔧 5. FORMAT TUTARSIZLIKLARI")
    print("-" * 25)
    
    if len(non_null_data) > 0:
        # Büyük/küçük harf farklılıkları
        case_issues = {}
        normalized_values = non_null_data.str.lower()
        original_unique = len(non_null_data.unique())
        normalized_unique = len(normalized_values.unique())
        
        if original_unique != normalized_unique:
            case_difference = original_unique - normalized_unique
            print(f"⚠️ Büyük/küçük harf farklılıkları: {case_difference} potansiyel duplike")
            
            # Case-insensitive duplicates bul
            case_groups = non_null_data.groupby(non_null_data.str.lower()).apply(list)
            duplicates = case_groups[case_groups.str.len() > 1]
            
            if len(duplicates) > 0:
                print("   📋 Tespit edilen farklılıklar:")
                for i, (normalized, variants) in enumerate(duplicates.head(5).items(), 1):
                    print(f"      {i}. '{normalized}' → {variants}")
        else:
            print("✅ Büyük/küçük harf tutarsızlığı bulunamadı")
        
        # Özel karakter kontrolü
        special_chars = non_null_data.str.contains(r'[^\w\s\-\.\,\(\)]', regex=True, na=False).sum()
        if special_chars > 0:
            print(f"⚠️ Özel karakter içeren değerler: {special_chars}")
        else:
            print("✅ Özel karakter sorunu bulunamadı")
        
        # Türkçe karakter kontrolü
        turkish_chars = non_null_data.str.contains(r'[çğıöşüÇĞIÖŞÜ]', regex=True, na=False).sum()
        english_equivalent = non_null_data.str.contains(r'[cgiosüCGIOSU]', regex=True, na=False).sum()
        
        if turkish_chars > 0 and english_equivalent > 0:
            print(f"⚠️ Türkçe/İngilizce karakter karışımı olabilir")
            print(f"   Türkçe karakter içeren: {turkish_chars}")
    print()
    
    # 6. DİĞER SÜTUNLARLA İLİŞKİ ANALİZİ
    print("🔗 6. DİĞER SÜTUNLARLA İLİŞKİ")
    print("-" * 30)
    
    # Benzer isimli sütunları bul
    similar_columns = []
    col_base = column_name.lower().replace('/', '_').split('_')
    
    for other_col in df.columns:
        if other_col != column_name:
            other_base = other_col.lower().replace('/', '_').split('_')
            # Ortak kelime sayısı
            common_words = set(col_base) & set(other_base)
            if len(common_words) > 0:
                similarity_score = len(common_words) / max(len(col_base), len(other_base))
                if similarity_score > 0.3:
                    similar_columns.append((other_col, similarity_score))
    
    if similar_columns:
        print("🔍 Benzer isimli sütunlar bulundu:")
        for similar_col, score in sorted(similar_columns, key=lambda x: x[1], reverse=True)[:5]:
            print(f"   📊 {similar_col} (benzerlik: {score:.2f})")
            
            # İçerik benzerliği kontrolü
            if similar_col in df.columns:
                try:
                    other_data = df[similar_col].dropna()
                    if len(other_data) > 0 and len(non_null_data) > 0:
                        # Ortak değer analizi
                        common_values = set(non_null_data.astype(str)) & set(other_data.astype(str))
                        if len(common_values) > 0:
                            overlap_pct = len(common_values) / max(len(set(non_null_data.astype(str))), len(set(other_data.astype(str)))) * 100
                            print(f"      🔗 İçerik örtüşmesi: {overlap_pct:.1f}% ({len(common_values)} ortak değer)")
                except:
                    pass
    else:
        print("✅ Benzer isimli sütun bulunamadı")
    print()
    
    # 7. ÖNERİLER VE EYLEMLERİ
    print("💡 7. ÖNERİLER VE EYLEM PLANI")
    print("-" * 30)
    
    recommendations = []
    
    # Null değer önerileri
    if null_percentage > 50:
        recommendations.append(f"🚨 ÇOK YÜKSEK NULL (%{null_percentage:.1f}) - Sütun silinmeyi düşünülebilir")
    elif null_percentage > 20:
        recommendations.append(f"⚠️ Yüksek null (%{null_percentage:.1f}) - Doldurma stratejisi gerekli")
        
        if 'companyDescription' in column_name:
            recommendations.append("   → 'Açıklama mevcut değil' veya benzer şirketlerden tahmin")
        elif 'followingType' in column_name:
            recommendations.append("   → Dominant kategori ile doldur veya 'Unknown' kategorisi")
    
    # Veri tipi önerileri
    if 'followingType' in column_name and len(non_null_data.unique()) < 10:
        recommendations.append("🔧 'category' veri tipine çevir (memory optimization)")
    
    # Format standardizasyonu
    if original_unique != normalized_unique:
        recommendations.append("🔤 Büyük/küçük harf standardizasyonu yap")
    
    # Tutarsızlık çözümleri
    if turkish_chars > 0 and english_equivalent > 0:
        recommendations.append("🌐 Türkçe karakter standardizasyonu (ı→i, ş→s, vb.)")
    
    # Benzerlik önerileri
    if similar_columns:
        for similar_col, score in similar_columns:
            if score > 0.8:
                recommendations.append(f"🔄 '{similar_col}' ile birleştirmeyi değerlendir (benzerlik: {score:.2f})")
    
    print("📋 Önerilen Eylemler:")
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print("   ✅ Sütun genel olarak iyi durumda, major action gerekmiyor")
    
    print("\n" + "=" * 80)
    return {
        'column_name': column_name,
        'total_rows': total_rows,
        'null_count': null_count,
        'null_percentage': null_percentage,
        'unique_count': unique_count if len(non_null_data) > 0 else 0,
        'data_type': str(col_data.dtype),
        'recommendations': recommendations
    }

def main():
    """Ana analiz fonksiyonu"""
    
    print("🔍 LinkedIn Jobs Dataset - Column Deep Analysis")
    print("=" * 60)
    
    # Dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_insights_completed.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
    except Exception as e:
        print(f"❌ HATA: Dataset yüklenemedi - {e}")
        return
    
    # Analiz edilecek sütunlar
    target_columns = [
        'merged_companyDescription',
        'company/followingState/followingType'
    ]
    
    results = {}
    
    for column in target_columns:
        result = analyze_column_deep(df, column)
        if result:
            results[column] = result
        print()
    
    # GENEL ÖZETİ VE SON ÖNERİLER
    print("🎯 GENEL ÖZET VE STRATEJİK ÖNERİLER")
    print("=" * 50)
    
    for col_name, result in results.items():
        null_pct = result['null_percentage']
        unique_cnt = result['unique_count']
        
        print(f"\n📊 {col_name}:")
        print(f"   Null: %{null_pct:.1f} | Benzersiz: {unique_cnt:,}")
        
        if result['recommendations']:
            print("   🎯 Öncelik eylemleri:")
            for rec in result['recommendations'][:3]:  # İlk 3 öneri
                print(f"      • {rec}")
    
    print("\n🚀 SONRAKI ADIM: Hangi sütundan başlamak istiyorsunuz?")

if __name__ == "__main__":
    main() 