#!/usr/bin/env python3
"""
Redundancy Analysis: jobWorkplaceTypes/0/localizedName vs workRemoteAllowed
"""

import pandas as pd
import numpy as np

def analyze_workplace_redundancy():
    """İki sütun arasındaki redundancy analizi"""
    
    # Dataset yükle
    df = pd.read_csv('linkedin_jobs_cleaned_no_redundant_urn.csv')
    
    print("=" * 80)
    print("🔍 WORKPLACE REDUNDANCY ANALİZİ")
    print("=" * 80)
    
    col1 = 'jobWorkplaceTypes/0/localizedName'
    col2 = 'workRemoteAllowed'
    
    print(f"🎯 Target Sütunlar:")
    print(f"   • Sütun 1: {col1}")
    print(f"   • Sütun 2: {col2}")
    
    # Temel istatistikler
    print(f"\n📊 TEMEL İSTATİSTİKLER:")
    print(f"   • {col1}:")
    print(f"     - Benzersiz değer: {df[col1].nunique()}")
    print(f"     - Null: {df[col1].isnull().sum()}")
    print(f"     - Değerler: {list(df[col1].value_counts().index)}")
    
    print(f"   • {col2}:")
    print(f"     - Benzersiz değer: {df[col2].nunique()}")
    print(f"     - Null: {df[col2].isnull().sum()}")
    print(f"     - Değerler: {list(df[col2].value_counts().index)}")
    
    # Değer dağılımları
    print(f"\n📈 DEĞER DAĞILIMLARI:")
    print(f"\n{col1}:")
    vc1 = df[col1].value_counts()
    for value, count in vc1.items():
        print(f"   • {value}: {count:,} ({count/len(df)*100:.1f}%)")
    
    print(f"\n{col2}:")
    vc2 = df[col2].value_counts()
    for value, count in vc2.items():
        print(f"   • {value}: {count:,} ({count/len(df)*100:.1f}%)")
    
    # Crosstab analizi
    print(f"\n🔄 CROSSTAB ANALİZİ:")
    crosstab = pd.crosstab(df[col1], df[col2], margins=True)
    print(crosstab)
    
    # Perfect mapping kontrolü
    print(f"\n🎯 PERFECT MAPPING KONTROLÜ:")
    
    # Remote -> True mapping
    remote_true_perfect = all(df[df[col1] == 'Remote'][col2] == True)
    print(f"   • Remote -> True: {'✅ Perfect' if remote_true_perfect else '❌ Imperfect'}")
    
    # Non-remote -> False mapping  
    non_remote_false_perfect = all(df[df[col1].isin(['On-site', 'Hybrid'])][col2] == False)
    print(f"   • Non-Remote -> False: {'✅ Perfect' if non_remote_false_perfect else '❌ Imperfect'}")
    
    # Genel tutarlılık
    # Remote = True ve Non-Remote = False olmalı
    consistent_mapping = (
        ((df[col1] == 'Remote') & (df[col2] == True)) |
        ((df[col1].isin(['On-site', 'Hybrid'])) & (df[col2] == False))
    )
    
    total_consistent = consistent_mapping.sum()
    total_records = len(df[df[col1].notna() & df[col2].notna()])
    consistency_rate = (total_consistent / total_records) * 100
    
    print(f"\n📊 TUTARLILIK ANALİZİ:")
    print(f"   • Tutarlı kayıtlar: {total_consistent:,}")
    print(f"   • Toplam kayıt: {total_records:,}")
    print(f"   • Tutarlılık oranı: %{consistency_rate:.2f}")
    
    # Redundancy assessment
    print(f"\n🚨 REDUNDANCY DEĞERLENDİRMESİ:")
    
    if consistency_rate >= 99.9:
        print(f"   ✅ PERFECT REDUNDANCY: %{consistency_rate:.2f} tutarlılık")
        print(f"   📋 Mapping Kuralları:")
        print(f"      • Remote ↔ True")
        print(f"      • On-site ↔ False") 
        print(f"      • Hybrid ↔ False")
        
        # Bilgi kaybı analizi
        print(f"\n💼 İŞ DEĞERİ KARŞILAŞTIRMASI:")
        print(f"   • {col1}: 3 kategori (Remote, On-site, Hybrid)")
        print(f"   • {col2}: 2 kategori (True, False)")
        print(f"   • Bilgi kaybı: Hybrid ve On-site ayrımı kaybolur")
        
        # Eliminasyon önerisi
        print(f"\n💡 ELİMİNASYON ÖNERİSİ:")
        
        # workRemoteAllowed'ı eliminate etmek
        print(f"   🎯 SEÇENEK 1: {col2} eliminasyonu")
        print(f"      ✅ Avantajlar:")
        print(f"         - {col1} daha detaylı bilgi sağlar")
        print(f"         - Hybrid vs On-site ayrımı korunur")
        print(f"         - İş analizi için daha değerli")
        print(f"      ❌ Dezavantajlar:")
        print(f"         - Boolean kolay filtreleme kaybolur")
        
        # jobWorkplaceTypes'ı eliminate etmek
        print(f"\n   🎯 SEÇENEK 2: {col1} eliminasyonu")
        print(f"      ✅ Avantajlar:")
        print(f"         - Daha basit boolean veri tipi")
        print(f"         - Hızlı remote/non-remote filtreleme")
        print(f"      ❌ Dezavantajlar:")
        print(f"         - Hybrid vs On-site ayrımı kaybolur")
        print(f"         - İş insights azalır")
        
        print(f"\n🏆 ÖNERİLEN STRATEJİ:")
        print(f"   {col2} sütununu eliminate edin")
        print(f"   {col1} sütununu koruyun (daha zengin bilgi)")
        
    else:
        print(f"   ⚠️  PARTIAL REDUNDANCY: %{consistency_rate:.2f} tutarlılık")
        print(f"   🔍 Daha detaylı araştırma gerekli")
    
    return consistency_rate >= 99.9

if __name__ == "__main__":
    result = analyze_workplace_redundancy() 