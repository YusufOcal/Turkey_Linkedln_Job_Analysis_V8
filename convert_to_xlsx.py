#!/usr/bin/env python3
"""
LinkedIn Jobs Dataset - CSV to XLSX Converter

Son optimize edilmiş dataset'i Excel formatında çıkarır.
Kullanıcı kontrolü ve analizi için XLSX format sağlar.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def convert_csv_to_xlsx():
    """CSV dosyasını XLSX formatına dönüştür"""
    
    print("📊 LinkedIn Jobs Dataset - XLSX Format Conversion")
    print("=" * 60)
    
    # Input ve output dosya isimleri
    input_file = 'linkedin_jobs_cleaned_no_redundant_links.csv'
    output_file = 'linkedin_jobs_final_optimized.xlsx'
    
    try:
        # CSV dosyasını yükle
        print(f"📂 CSV dosyası yükleniyor: {input_file}")
        df = pd.read_csv(input_file)
        
        print(f"✅ Dataset başarıyla yüklendi:")
        print(f"   • Kayıt sayısı: {len(df):,}")
        print(f"   • Sütun sayısı: {len(df.columns)}")
        print(f"   • Bellek kullanımı: {df.memory_usage(deep=True).sum() / (1024*1024):.2f} MB")
        
        # Sütun bilgileri
        print(f"\n📋 SÜTUN BİLGİLERİ:")
        print(f"   • Null değer içeren sütunlar:")
        null_columns = df.isnull().sum()
        null_columns = null_columns[null_columns > 0].sort_values(ascending=False)
        
        if len(null_columns) > 0:
            for col, null_count in null_columns.head(10).items():
                null_pct = (null_count / len(df)) * 100
                print(f"     - {col}: {null_count:,} null (%{null_pct:.1f})")
        else:
            print(f"     ✅ Hiç null değer yok!")
        
        # Veri tipleri özeti
        print(f"\n🔧 VERİ TİPLERİ ÖZETİ:")
        dtype_summary = df.dtypes.value_counts()
        for dtype, count in dtype_summary.items():
            print(f"   • {dtype}: {count} sütun")
        
        # Excel dosyasına kaydet - birden fazla sheet ile
        print(f"\n💾 XLSX dosyasına kaydediliyor: {output_file}")
        
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            # Ana dataset
            df.to_excel(writer, sheet_name='LinkedIn_Jobs_Dataset', index=False)
            
            # Dataset özeti
            summary_data = {
                'Metrik': [
                    'Toplam Kayıt Sayısı',
                    'Toplam Sütun Sayısı', 
                    'Bellek Kullanımı (MB)',
                    'Null Değer İçeren Sütun',
                    'Tamamen Dolu Sütun',
                    'Son Güncelleme'
                ],
                'Değer': [
                    f"{len(df):,}",
                    f"{len(df.columns)}",
                    f"{df.memory_usage(deep=True).sum() / (1024*1024):.2f}",
                    f"{len(null_columns)}",
                    f"{len(df.columns) - len(null_columns)}",
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Dataset_Summary', index=False)
            
            # Sütun bilgileri detayı
            column_info = []
            for col in df.columns:
                col_info = {
                    'Sütun Adı': col,
                    'Veri Tipi': str(df[col].dtype),
                    'Null Sayısı': df[col].isnull().sum(),
                    'Null Oranı (%)': round((df[col].isnull().sum() / len(df)) * 100, 2),
                    'Benzersiz Değer': df[col].nunique(),
                    'Benzersizlik Oranı (%)': round((df[col].nunique() / len(df)) * 100, 2) if len(df) > 0 else 0
                }
                column_info.append(col_info)
            
            column_df = pd.DataFrame(column_info)
            column_df.to_excel(writer, sheet_name='Column_Analysis', index=False)
            
            # Eliminasyon geçmişi
            elimination_history = {
                'Eliminasyon Sırası': [1, 2, 3],
                'Proje Kodu': ['53_', '54_', '55_'],
                'Silinen Sütun': [
                    'jobApplicantInsights/entityUrn',
                    'workRemoteAllowed', 
                    'link'
                ],
                'Eliminasyon Nedeni': [
                    'Perfect redundancy with id column',
                    'Perfect redundancy with jobWorkplaceTypes/0/localizedName',
                    'Perfect derivation from id column'
                ],
                'Bellek Tasarrufu (MB)': [1.18, 0.02, 1.22],
                'Duplicate Temizleme': [8944, 'N/A (mapping)', 8944],
                'Fonksiyonel Kayıp': ['0%', '0%', '0%']
            }
            
            elimination_df = pd.DataFrame(elimination_history)
            elimination_df.to_excel(writer, sheet_name='Elimination_History', index=False)
        
        # Başarı raporu
        print(f"✅ XLSX dönüşümü başarıyla tamamlandı!")
        print(f"\n📁 OLUŞTURULAN DOSYA: {output_file}")
        print(f"📊 İÇERİK:")
        print(f"   • Sheet 1: LinkedIn_Jobs_Dataset (Ana veri)")
        print(f"   • Sheet 2: Dataset_Summary (Genel özet)")
        print(f"   • Sheet 3: Column_Analysis (Sütun analizi)")
        print(f"   • Sheet 4: Elimination_History (Eliminasyon geçmişi)")
        
        # Dosya boyutu bilgisi
        import os
        if os.path.exists(output_file):
            file_size = os.path.getsize(output_file) / (1024*1024)  # MB
            print(f"\n💾 DOSYA BİLGİLERİ:")
            print(f"   • Dosya boyutu: {file_size:.2f} MB")
            print(f"   • Format: Excel (.xlsx)")
            print(f"   • Sheet sayısı: 4")
        
        # Optimization özeti
        print(f"\n🏆 OPTİMİZASYON ÖZETİ:")
        print(f"   • Başlangıç: 90 sütun")
        print(f"   • Son durum: {len(df.columns)} sütun")
        print(f"   • Eliminasyon: {90 - len(df.columns)} sütun (-{((90 - len(df.columns))/90*100):.1f}%)")
        print(f"   • Toplam bellek tasarrufu: ~2.42 MB")
        print(f"   • Duplicate temizleme: 17,888 entries")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Hata: {input_file} dosyası bulunamadı!")
        print(f"Mevcut dosyalar kontrol ediliyor...")
        import os
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        if csv_files:
            print(f"Mevcut CSV dosyaları:")
            for f in csv_files:
                print(f"   • {f}")
        return False
        
    except Exception as e:
        print(f"❌ Dönüştürme hatası: {e}")
        return False

if __name__ == "__main__":
    success = convert_csv_to_xlsx()
    if success:
        print(f"\n🎉 Excel dosyası hazır!")
        print(f"📋 Kullanım: Excel'de açarak dataset'inizi kontrol edebilirsiniz")
        print(f"🔍 Özellikle 'Column_Analysis' sheet'ini incelemenizi öneririm")
    else:
        print(f"\n❌ Dönüştürme başarısız!") 