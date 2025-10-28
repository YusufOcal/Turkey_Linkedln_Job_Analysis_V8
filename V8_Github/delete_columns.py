#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Column Deletion Script
merged_companyDescription ve company/followingState/followingType sütunlarını siler
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def delete_problematic_columns():
    """Problematik sütunları siler ve sonuçları raporlar"""
    
    print("🗑️ LinkedIn Jobs Dataset - Column Deletion Operation")
    print("=" * 60)
    
    try:
        # Dataset'i yükle
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_insights_completed.csv')
        
        # İlk durum
        initial_rows = len(df)
        initial_cols = len(df.columns)
        initial_memory = df.memory_usage(deep=True).sum() / 1024**2
        
        print(f"✅ Dataset yüklendi!")
        print(f"📊 İlk durum: {initial_rows:,} satır × {initial_cols} sütun")
        print(f"💾 İlk memory: {initial_memory:.2f} MB")
        print()
        
        # Silinecek sütunlar
        columns_to_delete = [
            'merged_companyDescription',
            'company/followingState/followingType'
        ]
        
        print("🎯 DELETION ANALYSIS")
        print("-" * 25)
        
        total_memory_saved = 0
        deletion_report = []
        
        for col in columns_to_delete:
            if col in df.columns:
                # Bu sütunun memory kullanımı
                col_memory = df[col].memory_usage(deep=True) / 1024**2
                null_count = df[col].isnull().sum()
                null_pct = (null_count / len(df)) * 100
                unique_count = len(df[col].dropna().unique()) if df[col].notna().sum() > 0 else 0
                
                print(f"🔍 {col}:")
                print(f"   📊 Null: {null_count:,} ({null_pct:.1f}%)")
                print(f"   🎯 Benzersiz değer: {unique_count:,}")
                print(f"   💾 Memory: {col_memory:.2f} MB")
                print(f"   ✅ SİLİNECEK!")
                
                deletion_report.append({
                    'column': col,
                    'memory_mb': col_memory,
                    'null_count': null_count,
                    'null_percentage': null_pct,
                    'unique_values': unique_count
                })
                
                total_memory_saved += col_memory
                print()
            else:
                print(f"⚠️ {col}: Sütun bulunamadı!")
                print()
        
        # Sütunları sil
        print("🗑️ DELETION PROCESS")
        print("-" * 20)
        
        existing_columns = [col for col in columns_to_delete if col in df.columns]
        
        if existing_columns:
            df_cleaned = df.drop(columns=existing_columns)
            
            # Son durum
            final_rows = len(df_cleaned)
            final_cols = len(df_cleaned.columns)
            final_memory = df_cleaned.memory_usage(deep=True).sum() / 1024**2
            
            # İstatistikler
            cols_deleted = len(existing_columns)
            memory_saved = initial_memory - final_memory
            memory_saved_pct = (memory_saved / initial_memory) * 100
            
            print(f"✅ {cols_deleted} sütun başarıyla silindi!")
            print(f"📊 Son durum: {final_rows:,} satır × {final_cols} sütun")
            print(f"💾 Son memory: {final_memory:.2f} MB")
            print()
            
            print("📈 OPTIMIZATION RESULTS")
            print("-" * 25)
            print(f"🔻 Sütun azalması: {initial_cols} → {final_cols} (-{cols_deleted})")
            print(f"💾 Memory tasarrufu: {memory_saved:.2f} MB ({memory_saved_pct:.1f}%)")
            print(f"📊 Satır korunma: {final_rows:,} / {initial_rows:,} (100.0%)")
            print()
            
            # Silinen sütunların detay raporu
            print("📋 DELETION SUMMARY")
            print("-" * 20)
            for i, report in enumerate(deletion_report, 1):
                print(f"{i}. {report['column']}:")
                print(f"   📊 Null oranı: %{report['null_percentage']:.1f}")
                print(f"   🎯 Benzersiz değer: {report['unique_values']:,}")
                print(f"   💾 Memory kurtarılan: {report['memory_mb']:.2f} MB")
                
                # Silme gerekçesi
                if report['null_percentage'] > 50:
                    reason = "🚨 Çok yüksek null oranı"
                elif report['unique_values'] <= 1:
                    reason = "🔴 Zero/minimal variance"
                else:
                    reason = "⚠️ Low business value"
                print(f"   💡 Gerekçe: {reason}")
                print()
            
            # Yeni dosyayı kaydet
            print("💾 SAVING CLEANED DATASET")
            print("-" * 25)
            
            output_filename = 'linkedin_jobs_dataset_cleaned_columns.csv'
            df_cleaned.to_csv(output_filename, index=False)
            
            # Dosya boyutu kontrolü
            file_size = Path(output_filename).stat().st_size / 1024**2
            original_size = Path('linkedin_jobs_dataset_insights_completed.csv').stat().st_size / 1024**2
            size_reduction = original_size - file_size
            size_reduction_pct = (size_reduction / original_size) * 100
            
            print(f"✅ Temizlenmiş dataset kaydedildi: {output_filename}")
            print(f"📄 Dosya boyutu: {file_size:.1f} MB (önceki: {original_size:.1f} MB)")
            print(f"💾 Dosya boyutu tasarrufu: {size_reduction:.1f} MB ({size_reduction_pct:.1f}%)")
            print()
            
            # Kalite kontrolü
            print("🔍 QUALITY CHECK")
            print("-" * 15)
            
            # Null oranları karşılaştırması
            original_null_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            cleaned_null_pct = (df_cleaned.isnull().sum().sum() / (len(df_cleaned) * len(df_cleaned.columns))) * 100
            
            print(f"📊 Null oranı: %{original_null_pct:.1f} → %{cleaned_null_pct:.1f}")
            print(f"🎯 Data quality improvement: {'✅ İyileşti' if cleaned_null_pct < original_null_pct else '➖ Aynı'}")
            
            # Veri tipi optimizasyonu kontrolü
            numeric_cols = len(df_cleaned.select_dtypes(include=[np.number]).columns)
            bool_cols = len(df_cleaned.select_dtypes(include=['bool', 'boolean']).columns)
            optimized_cols = numeric_cols + bool_cols
            optimization_pct = (optimized_cols / len(df_cleaned.columns)) * 100
            
            print(f"⚙️ Optimized columns: {optimized_cols}/{len(df_cleaned.columns)} ({optimization_pct:.1f}%)")
            print()
            
            # Sonuç özeti
            print("🏆 OPERATION SUMMARY")
            print("-" * 20)
            print("✅ İşlemler başarıyla tamamlandı!")
            print(f"🗑️ Silinen sütunlar: {', '.join(existing_columns)}")
            print(f"📊 Dataset optimizasyonu: {cols_deleted} sütun, {memory_saved:.1f} MB tasarruf")
            print(f"💾 Yeni dosya: {output_filename}")
            print()
            print("🚀 NEXT STEPS:")
            print("   1. Yeni dataset'i inceleyin")
            print("   2. Diğer problematik sütunları tespit edin") 
            print("   3. Veri kalitesi optimizasyonuna devam edin")
            
            return df_cleaned, deletion_report
            
        else:
            print("❌ Silinecek sütun bulunamadı!")
            return df, []
            
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        return None, []

if __name__ == "__main__":
    cleaned_df, report = delete_problematic_columns()
    
    if cleaned_df is not None:
        print(f"\n🎯 İşlem tamamlandı! Yeni dataset: {len(cleaned_df)} satır × {len(cleaned_df.columns)} sütun")
    else:
        print("\n❌ İşlem başarısız!") 