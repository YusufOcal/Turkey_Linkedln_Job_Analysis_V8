#!/usr/bin/env python3
"""
LinkedIn Jobs Dataset - workRemoteAllowed Sütun Eliminasyonu

Bu script perfect redundancy tespit edilen workRemoteAllowed sütununu siler.
jobWorkplaceTypes/0/localizedName sütunu daha zengin bilgi sağladığı için korunur.
"""

import pandas as pd
import numpy as np

def delete_workRemoteAllowed_column():
    """workRemoteAllowed sütununu sil"""
    
    print("🚀 workRemoteAllowed Sütun Eliminasyonu")
    print("=" * 60)
    
    # Dataset yükle
    try:
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step10.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} kayıt, {len(df.columns)} sütun")
    except Exception as e:
        print(f"❌ Dataset yükleme hatası: {e}")
        return False
    
    # Mevcut durum kontrolü
    target_column = 'workRemoteAllowed'
    replacement_column = 'jobWorkplaceTypes/0/localizedName'
    
    print(f"\n📊 MEVCUT DURUM:")
    print(f"   • Target sütun: {target_column}")
    print(f"   • Replacement sütun: {replacement_column}")
    print(f"   • {target_column} var mı: {target_column in df.columns}")
    print(f"   • {replacement_column} var mı: {replacement_column in df.columns}")
    
    if target_column not in df.columns:
        print(f"❌ {target_column} sütunu bulunamadı!")
        return False
    
    if replacement_column not in df.columns:
        print(f"❌ {replacement_column} sütunu bulunamadı!")
        return False
    
    # Pre-deletion metrics
    memory_before = df.memory_usage(deep=True).sum()
    target_memory = df[target_column].memory_usage(deep=True)
    
    print(f"\n📏 PRE-DELETION METRİKLER:")
    print(f"   • Toplam bellek kullanımı: {memory_before / (1024*1024):.2f} MB")
    print(f"   • {target_column} bellek kullanımı: {target_memory / (1024*1024):.2f} MB")
    print(f"   • Mevcut sütun sayısı: {len(df.columns)}")
    
    # Son validasyon - Perfect redundancy kontrolü
    print(f"\n🔍 SON VALİDASYON:")
    crosstab = pd.crosstab(df[replacement_column], df[target_column], margins=True)
    print("Cross-tabulation:")
    print(crosstab)
    
    # Perfect mapping kontrolü
    remote_mapping = all(df[df[replacement_column] == 'Remote'][target_column] == True)
    non_remote_mapping = all(df[df[replacement_column].isin(['On-site', 'Hybrid'])][target_column] == False)
    
    print(f"\n✅ Perfect mapping doğrulandı:")
    print(f"   • Remote -> True: {remote_mapping}")
    print(f"   • Non-Remote -> False: {non_remote_mapping}")
    
    if not (remote_mapping and non_remote_mapping):
        print("❌ Perfect redundancy doğrulanamadı! İşlem iptal edildi.")
        return False
    
    # Silme işlemi
    print(f"\n🗑️  SİLME İŞLEMİ:")
    df_cleaned = df.drop(columns=[target_column])
    
    # Post-deletion metrics
    memory_after = df_cleaned.memory_usage(deep=True).sum()
    memory_saved = memory_before - memory_after
    
    print(f"   ✅ {target_column} sütunu silindi")
    print(f"   📊 Sonuç:")
    print(f"      • Yeni sütun sayısı: {len(df_cleaned.columns)} (önceki: {len(df.columns)})")
    print(f"      • Kayıt sayısı: {len(df_cleaned):,} (değişmedi)")
    print(f"      • Bellek tasarrufu: {memory_saved / (1024*1024):.2f} MB")
    print(f"      • Bellek kullanımı: {memory_after / (1024*1024):.2f} MB")
    
    # Yeni dosya kaydet
    output_file = 'linkedin_jobs_dataset_optimized_step11.csv'
    df_cleaned.to_csv(output_file, index=False)
    
    print(f"\n💾 DOSYA KAYDI:")
    print(f"   ✅ Yeni dataset: {output_file}")
    print(f"   📁 Dosya boyutu: {len(df_cleaned):,} kayıt x {len(df_cleaned.columns)} sütun")
    
    # Özet rapor
    print(f"\n📋 ÖZET RAPOR:")
    print(f"   🎯 Silinen sütun: {target_column}")
    print(f"   ✅ Korunan sütun: {replacement_column}")
    print(f"   📈 Optimizasyon: {len(df.columns)} → {len(df_cleaned.columns)} sütun")
    print(f"   💾 Bellek tasarrufu: {memory_saved / (1024*1024):.2f} MB")
    print(f"   🏆 Fonksiyonel kayıp: 0% (perfect redundancy)")
    
    # Replacement sütun özeti
    print(f"\n🏢 {replacement_column} SÜTUN ÖZETİ:")
    value_counts = df_cleaned[replacement_column].value_counts()
    for value, count in value_counts.items():
        percentage = (count / len(df_cleaned)) * 100
        print(f"   • {value}: {count:,} (%{percentage:.1f})")
    
    print(f"\n✅ workRemoteAllowed sütun eliminasyonu başarıyla tamamlandı!")
    
    return True

if __name__ == "__main__":
    success = delete_workRemoteAllowed_column()
    if success:
        print("\n🎉 İşlem başarılı!")
    else:
        print("\n❌ İşlem başarısız!") 