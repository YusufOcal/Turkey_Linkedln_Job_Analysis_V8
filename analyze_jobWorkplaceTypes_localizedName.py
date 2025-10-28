#!/usr/bin/env python3
"""
LinkedIn Jobs Dataset Analysis: jobWorkplaceTypes/0/localizedName Column

Bu script jobWorkplaceTypes/0/localizedName sütununu kapsamlı olarak analiz eder:
1. Temel sütun karakteristikleri
2. Veri kalitesi analizi  
3. Benzersiz değer dağılımı
4. Diğer sütunlarla benzerlik analizi
5. Redundancy ve cross-column korelasyon tespiti
"""

import pandas as pd
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

def load_dataset():
    """Dataset'i yükle"""
    try:
        df = pd.read_csv('linkedin_jobs_cleaned_no_redundant_urn.csv')
        print(f"✅ Dataset başarıyla yüklendi: {len(df):,} kayıt, {len(df.columns)} sütun")
        return df
    except Exception as e:
        print(f"❌ Dataset yükleme hatası: {e}")
        return None

def analyze_target_column(df, target_col):
    """Target sütunun temel analizi"""
    print("=" * 80)
    print(f"🎯 TARGET SÜTUN ANALİZİ: {target_col}")
    print("=" * 80)
    
    # Temel istatistikler
    total_rows = len(df)
    non_null_count = df[target_col].count()
    null_count = df[target_col].isnull().sum()
    unique_count = df[target_col].nunique()
    
    print(f"📊 TEMEL İSTATİSTİKLER:")
    print(f"   • Veri Tipi: {df[target_col].dtype}")
    print(f"   • Toplam Kayıt: {total_rows:,}")
    print(f"   • Null Olmayan Değer: {non_null_count:,}")
    print(f"   • Null Değer: {null_count:,}")
    print(f"   • Veri Tamlığı: {(non_null_count/total_rows*100):.2f}%")
    print(f"   • Benzersiz Değer Sayısı: {unique_count:,}")
    print(f"   • Benzersizlik Oranı: {(unique_count/non_null_count*100):.2f}%")
    
    return {
        'total_rows': total_rows,
        'non_null_count': non_null_count, 
        'null_count': null_count,
        'unique_count': unique_count,
        'data_type': str(df[target_col].dtype)
    }

def analyze_unique_values(df, target_col):
    """Benzersiz değer analizi"""
    print(f"\n📈 BENZERSİZ DEĞER ANALİZİ:")
    print("-" * 50)
    
    # Value counts
    value_counts = df[target_col].value_counts()
    print(f"Toplam benzersiz değer: {len(value_counts)}")
    
    print(f"\n🔢 DEĞER DAĞILIMI:")
    for i, (value, count) in enumerate(value_counts.items(), 1):
        percentage = (count / df[target_col].count()) * 100
        print(f"   {i:2d}. '{value}': {count:,} kayıt ({percentage:.2f}%)")
    
    # Null analizi
    if df[target_col].isnull().sum() > 0:
        print(f"\n❓ NULL DEĞER ANALİZİ:")
        print(f"   • Null kayıtlar: {df[target_col].isnull().sum():,}")
        print(f"   • Null oranı: {(df[target_col].isnull().sum()/len(df)*100):.2f}%")
    
    return value_counts

def find_similar_columns(df, target_col):
    """Benzer sütunları tespit et"""
    print(f"\n🔍 BENZER SÜTUN ARAMA:")
    print("-" * 50)
    
    target_unique_count = df[target_col].nunique()
    target_values = set(df[target_col].dropna().unique())
    
    similar_columns = []
    workplace_related_columns = []
    
    for col in df.columns:
        if col == target_col:
            continue
            
        # Workplace/work ile ilgili sütunları tespit et
        if any(keyword in col.lower() for keyword in ['work', 'workplace', 'office', 'remote', 'location', 'place']):
            workplace_related_columns.append(col)
        
        # Benzersiz değer sayısı benzerliği
        col_unique_count = df[col].nunique()
        if col_unique_count == target_unique_count and col_unique_count < 10:  # Düşük kardinalite
            col_values = set(df[col].dropna().unique())
            
            # Değer benzerliği kontrolü
            if len(col_values & target_values) > 0:  # Ortak değerler var mı?
                jaccard_similarity = len(col_values & target_values) / len(col_values | target_values)
                similar_columns.append({
                    'column': col,
                    'unique_count': col_unique_count,
                    'jaccard_similarity': jaccard_similarity,
                    'common_values': col_values & target_values,
                    'all_values': col_values
                })
    
    print(f"🏢 WORKPLACE İLE İLGİLİ SÜTUNLAR ({len(workplace_related_columns)} adet):")
    for col in workplace_related_columns:
        unique_count = df[col].nunique()
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        print(f"   • {col}: {unique_count:,} benzersiz değer, %{null_pct:.1f} null")
    
    print(f"\n🎯 AYNI BENZERSİZ DEĞER SAYISINA SAHİP SÜTUNLAR:")
    if similar_columns:
        for sim in similar_columns:
            print(f"   • {sim['column']}: {sim['unique_count']} benzersiz değer")
            print(f"     - Jaccard Benzerliği: {sim['jaccard_similarity']:.3f}")
            print(f"     - Ortak Değerler: {sim['common_values']}")
            print(f"     - Tüm Değerler: {sim['all_values']}")
            print()
    else:
        print("   ❌ Aynı benzersiz değer sayısına sahip sütun bulunamadı")
    
    return similar_columns, workplace_related_columns

def cross_column_analysis(df, target_col, workplace_columns):
    """Cross-column detaylı analiz"""
    print(f"\n🔄 CROSS-COLUMN DETAYLI ANALİZ:")
    print("-" * 50)
    
    # jobWorkplaceTypes ile ilgili diğer sütunları bul
    workplace_type_columns = [col for col in df.columns if 'jobWorkplaceTypes' in col]
    
    print(f"📋 JOBWORKPLACETYPES SÜTUN GRU BU ({len(workplace_type_columns)} adet):")
    for col in workplace_type_columns:
        unique_count = df[col].nunique()
        null_count = df[col].isnull().sum()
        null_pct = (null_count / len(df)) * 100
        print(f"   • {col}")
        print(f"     - Benzersiz değer: {unique_count:,}")
        print(f"     - Null: {null_count:,} (%{null_pct:.1f})")
        
        # Eğer benzersiz değer sayısı düşükse, değerleri göster
        if unique_count <= 10:
            values = df[col].value_counts()
            print(f"     - Değerler: {dict(values)}")
        print()
    
    return workplace_type_columns

def redundancy_assessment(df, target_col, similar_columns, workplace_columns):
    """Redundancy değerlendirmesi"""
    print(f"\n⚠️  REDUNDANCY DEĞERLENDİRMESİ:")
    print("-" * 50)
    
    target_unique_count = df[target_col].nunique()
    target_null_pct = (df[target_col].isnull().sum() / len(df)) * 100
    
    print(f"🎯 TARGET SÜTUN: {target_col}")
    print(f"   • Benzersiz değer: {target_unique_count}")
    print(f"   • Null oranı: %{target_null_pct:.1f}")
    
    # Potansiyel redundant sütunları tespit et
    redundant_candidates = []
    
    for col in workplace_columns:
        if col == target_col:
            continue
            
        col_unique = df[col].nunique()
        col_null_pct = (df[col].isnull().sum() / len(df)) * 100
        
        # Aynı benzersiz değer sayısı ve düşük kardinalite
        if col_unique == target_unique_count and col_unique <= 5:
            # Değer benzerliği kontrolü
            target_values = set(df[target_col].dropna().unique())
            col_values = set(df[col].dropna().unique())
            
            if len(target_values & col_values) > 0:
                jaccard = len(target_values & col_values) / len(target_values | col_values)
                redundant_candidates.append({
                    'column': col,
                    'unique_count': col_unique,
                    'null_pct': col_null_pct,
                    'jaccard_similarity': jaccard,
                    'common_values': target_values & col_values
                })
    
    if redundant_candidates:
        print(f"\n🚨 POTANSIYEL REDUNDANT SÜTUNLAR:")
        for candidate in redundant_candidates:
            print(f"   • {candidate['column']}")
            print(f"     - Benzersiz değer: {candidate['unique_count']}")
            print(f"     - Null oranı: %{candidate['null_pct']:.1f}")
            print(f"     - Jaccard benzerliği: {candidate['jaccard_similarity']:.3f}")
            print(f"     - Ortak değerler: {candidate['common_values']}")
            print()
    else:
        print("   ✅ Redundant sütun tespit edilmedi")
    
    return redundant_candidates

def business_value_assessment(df, target_col, value_counts):
    """İş değeri değerlendirmesi"""
    print(f"\n💼 İŞ DEĞERİ DEĞERLENDİRMESİ:")
    print("-" * 50)
    
    unique_count = len(value_counts)
    
    print(f"📊 WORKPLACE TYPES ANALİZİ:")
    print(f"   • Toplam workplace türü: {unique_count}")
    
    if unique_count <= 10:
        print(f"   • Düşük kardinalite: Kategorik veri uygun")
        
        # İş değeri analizi
        print(f"\n🏢 WORKPLACE TÜRÜ DAĞILIMI:")
        total_non_null = df[target_col].count()
        
        for i, (workplace_type, count) in enumerate(value_counts.items(), 1):
            percentage = (count / total_non_null) * 100
            print(f"   {i}. {workplace_type}")
            print(f"      - Kayıt sayısı: {count:,}")
            print(f"      - Oran: %{percentage:.2f}")
            
            # İş insights
            if 'remote' in str(workplace_type).lower():
                print(f"      - 🏠 Uzaktan çalışma fırsatı")
            elif 'office' in str(workplace_type).lower():
                print(f"      - 🏢 Ofis bazlı çalışma")
            elif 'hybrid' in str(workplace_type).lower():
                print(f"      - 🔄 Hibrit çalışma modeli")
            print()
    
    # Business value score
    completeness_score = (df[target_col].count() / len(df)) * 100
    diversity_score = min(unique_count / 5 * 100, 100)  # 5 ideal kategorik çeşitlilik
    distribution_score = 100 - (value_counts.iloc[0] / df[target_col].count() * 100)  # Dağılım dengesi
    
    business_score = (completeness_score * 0.4 + diversity_score * 0.3 + distribution_score * 0.3)
    
    print(f"📈 İŞ DEĞERİ SKORU:")
    print(f"   • Veri Tamlığı: %{completeness_score:.1f}")
    print(f"   • Kategori Çeşitliliği: %{diversity_score:.1f}")
    print(f"   • Dağılım Dengesi: %{distribution_score:.1f}")
    print(f"   • TOPLAM İŞ DEĞERİ: %{business_score:.1f}")
    
    return business_score

def generate_recommendations(df, target_col, redundant_candidates, business_score):
    """Öneriler oluştur"""
    print(f"\n💡 STRATEJİK ÖNERİLER:")
    print("=" * 50)
    
    # Veri kalitesi önerileri
    null_pct = (df[target_col].isnull().sum() / len(df)) * 100
    unique_count = df[target_col].nunique()
    
    print(f"🎯 SÜTUN: {target_col}")
    print(f"   • İş Değeri Skoru: %{business_score:.1f}")
    
    if business_score >= 80:
        print(f"   ✅ YÜKSEKDeğer - Korunması önerilir")
    elif business_score >= 60:
        print(f"   ⚠️  ORTA Değer - Optimizasyon değerlendirilebilir")
    else:
        print(f"   ❌ DÜŞÜK Değer - Eliminasyon değerlendirilebilir")
    
    print(f"\n📋 DETAYLI ÖNERİLER:")
    
    # Null handling
    if null_pct > 5:
        print(f"   • Null Değer Optimizasyonu: %{null_pct:.1f} null var")
        print(f"     - Veri kaynağı kalitesini gözden geçirin")
        print(f"     - Default değer atama stratejisi değerlendirin")
    
    # Redundancy handling
    if redundant_candidates:
        print(f"   • Redundancy Yönetimi:")
        for candidate in redundant_candidates:
            print(f"     - {candidate['column']} ile %{candidate['jaccard_similarity']*100:.1f} benzerlik")
            print(f"     - Consolidation değerlendirin")
    
    # Business insights
    if unique_count <= 5:
        print(f"   • Kategorik Analiz Fırsatı:")
        print(f"     - Workplace types segmentasyonu için idealn")
        print(f"     - HR analytics için değerli insight")
        print(f"     - Trend analizi yapılabilir")
    
    print(f"\n📊 SONUÇ:")
    if business_score >= 70 and len(redundant_candidates) == 0:
        print(f"   ✅ KORUMA: Sütun optimize edilmiş durumda")
    elif len(redundant_candidates) > 0:
        print(f"   🔄 OPTİMİZASYON: Redundancy eliminasyonu önerilir")
    else:
        print(f"   ⚠️  İNCELEME: Detaylı business value analizi yapın")

def main():
    """Ana analiz fonksiyonu"""
    print("🚀 LinkedIn Jobs Dataset - jobWorkplaceTypes/0/localizedName Sütun Analizi")
    print("=" * 80)
    
    # Dataset yükle
    df = load_dataset()
    if df is None:
        return
    
    target_col = 'jobWorkplaceTypes/0/localizedName'
    
    # Sütun varlığını kontrol et
    if target_col not in df.columns:
        print(f"❌ Hata: '{target_col}' sütunu bulunamadı!")
        print(f"Mevcut sütunlar: {[col for col in df.columns if 'workplace' in col.lower()]}")
        return
    
    # Analizleri gerçekleştir
    basic_stats = analyze_target_column(df, target_col)
    value_counts = analyze_unique_values(df, target_col)
    similar_columns, workplace_columns = find_similar_columns(df, target_col)
    workplace_type_columns = cross_column_analysis(df, target_col, workplace_columns)
    redundant_candidates = redundancy_assessment(df, target_col, similar_columns, workplace_columns)
    business_score = business_value_assessment(df, target_col, value_counts)
    generate_recommendations(df, target_col, redundant_candidates, business_score)
    
    print(f"\n✅ Analiz tamamlandı!")
    print(f"📁 Sonuç dosyası: workplace_types_analysis_results.txt olarak kaydedilebilir")

if __name__ == "__main__":
    main() 