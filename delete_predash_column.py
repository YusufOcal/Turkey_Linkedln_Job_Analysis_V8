#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - preDashFollowingInfoUrn Column Deletion
company/followingState/preDashFollowingInfoUrn sütununu siler ve sonuçları raporlar
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def delete_predash_following_info_urn():
    """preDashFollowingInfoUrn sütununu siler ve sonuçları raporlar"""
    
    print("🗑️ LinkedIn Jobs Dataset - preDashFollowingInfoUrn Deletion Operation")
    print("=" * 70)
    
    try:
        # Dataset'i yükle
        print("📂 Cleaned dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_cleaned_columns.csv')
        
        # İlk durum
        initial_rows = len(df)
        initial_cols = len(df.columns)
        initial_memory = df.memory_usage(deep=True).sum() / 1024**2
        
        print(f"✅ Dataset yüklendi!")
        print(f"📊 İlk durum: {initial_rows:,} satır × {initial_cols} sütun")
        print(f"💾 İlk memory: {initial_memory:.2f} MB")
        print()
        
        # Silinecek sütun
        column_to_delete = 'company/followingState/preDashFollowingInfoUrn'
        
        print("🎯 DELETION ANALYSIS")
        print("-" * 25)
        
        if column_to_delete in df.columns:
            # Bu sütunun detay analizi
            col_data = df[column_to_delete]
            col_memory = col_data.memory_usage(deep=True) / 1024**2
            null_count = col_data.isnull().sum()
            null_pct = (null_count / len(df)) * 100
            unique_count = len(col_data.dropna().unique()) if col_data.notna().sum() > 0 else 0
            
            print(f"🔍 {column_to_delete}:")
            print(f"   📊 Null: {null_count:,} ({null_pct:.1f}%)")
            print(f"   🎯 Benzersiz değer: {unique_count:,}")
            print(f"   💾 Memory: {col_memory:.2f} MB")
            print(f"   🔗 URN format: LinkedIn internal identifier")
            print(f"   ✅ SİLİNECEK!")
            print()
            
            # Silme gerekçesi analizi
            print("💡 DELETION RATIONALE")
            print("-" * 20)
            print("📋 Silme gerekçeleri:")
            print("   1. 🔗 Internal URN identifier - limited business value")
            print("   2. 📊 Following relationship already tracked by other columns")
            print("   3. 💾 Memory optimization opportunity")
            print("   4. 🔧 Complex format requires preprocessing")
            print("   5. 📈 Alternative: company/followingState/following (boolean) more useful")
            print()
            
            # FollowingState namespace temizliği
            following_state_cols = [col for col in df.columns if 'followingState' in col]
            print("🔍 FollowingState Namespace Analysis:")
            print(f"   📊 Namespace'de kalan sütunlar: {len(following_state_cols)-1}")
            for col in following_state_cols:
                if col != column_to_delete:
                    non_null = df[col].notna().sum()
                    print(f"      ✅ {col}: {non_null:,} non-null ({df[col].dtype})")
            print()
        
        # Sütunu sil
        print("🗑️ DELETION PROCESS")
        print("-" * 20)
        
        if column_to_delete in df.columns:
            df_cleaned = df.drop(columns=[column_to_delete])
            
            # Son durum
            final_rows = len(df_cleaned)
            final_cols = len(df_cleaned.columns)
            final_memory = df_cleaned.memory_usage(deep=True).sum() / 1024**2
            
            # İstatistikler
            memory_saved = initial_memory - final_memory
            memory_saved_pct = (memory_saved / initial_memory) * 100
            
            print(f"✅ 1 sütun başarıyla silindi!")
            print(f"📊 Son durum: {final_rows:,} satır × {final_cols} sütun")
            print(f"💾 Son memory: {final_memory:.2f} MB")
            print()
            
            print("📈 OPTIMIZATION RESULTS")
            print("-" * 25)
            print(f"🔻 Sütun azalması: {initial_cols} → {final_cols} (-1)")
            print(f"💾 Memory tasarrufu: {memory_saved:.2f} MB ({memory_saved_pct:.1f}%)")
            print(f"📊 Satır korunma: {final_rows:,} / {initial_rows:,} (100.0%)")
            print()
            
            # Namespace temizlik sonucu
            remaining_following_cols = [col for col in df_cleaned.columns if 'followingState' in col]
            print("🔍 NAMESPACE CLEANUP RESULT")
            print("-" * 30)
            print(f"📊 FollowingState kalan sütunlar: {len(remaining_following_cols)}")
            for col in remaining_following_cols:
                col_type = df_cleaned[col].dtype
                non_null = df_cleaned[col].notna().sum()
                print(f"   ✅ {col}: {non_null:,} non-null ({col_type})")
            print()
            
            # Yeni dosyayı kaydet
            print("💾 SAVING OPTIMIZED DATASET")
            print("-" * 25)
            
            output_filename = 'linkedin_jobs_dataset_optimized_step2.csv'
            df_cleaned.to_csv(output_filename, index=False)
            
            # Dosya boyutu kontrolü
            file_size = Path(output_filename).stat().st_size / 1024**2
            original_size = Path('linkedin_jobs_dataset_cleaned_columns.csv').stat().st_size / 1024**2
            size_reduction = original_size - file_size
            size_reduction_pct = (size_reduction / original_size) * 100
            
            print(f"✅ Optimized dataset kaydedildi: {output_filename}")
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
            print(f"🎯 Data quality: {'✅ İyileşti' if cleaned_null_pct < original_null_pct else '➖ Aynı'}")
            
            # Veri tipi optimizasyonu kontrolü
            numeric_cols = len(df_cleaned.select_dtypes(include=[np.number]).columns)
            bool_cols = len(df_cleaned.select_dtypes(include=['bool', 'boolean']).columns)
            optimized_cols = numeric_cols + bool_cols
            optimization_pct = (optimized_cols / len(df_cleaned.columns)) * 100
            
            print(f"⚙️ Optimized columns: {optimized_cols}/{len(df_cleaned.columns)} ({optimization_pct:.1f}%)")
            print()
            
            # Cumulative optimization summary
            print("📊 CUMULATIVE OPTIMIZATION SUMMARY")
            print("-" * 35)
            original_dataset_size = 94  # Başlangıç sütun sayısı
            total_deleted = original_dataset_size - final_cols
            
            print(f"🔻 Toplam silinen sütun: {total_deleted}")
            print(f"📈 Dataset optimization: {original_dataset_size} → {final_cols}")
            print(f"🎯 Optimization ratio: {(total_deleted/original_dataset_size)*100:.1f}%")
            print()
            
            # Sonuç özeti
            print("🏆 OPERATION SUMMARY")
            print("-" * 20)
            print("✅ İşlem başarıyla tamamlandı!")
            print(f"🗑️ Silinen sütun: {column_to_delete}")
            print(f"📊 Dataset durumu: {final_cols} sütun, {memory_saved:.1f} MB tasarruf")
            print(f"💾 Yeni dosya: {output_filename}")
            print()
            print("🚀 NEXT STEPS:")
            print("   1. 46_ teknik raporu hazırlanacak")
            print("   2. Diğer optimization candidates analiz edilecek") 
            print("   3. Dataset quality monitoring devam edecek")
            
            return df_cleaned, {
                'deleted_column': column_to_delete,
                'memory_saved': memory_saved,
                'file_size_reduction': size_reduction,
                'null_improvement': original_null_pct - cleaned_null_pct,
                'final_columns': final_cols
            }
            
        else:
            print(f"❌ Sütun bulunamadı: {column_to_delete}")
            return df, {}
            
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        return None, {}

if __name__ == "__main__":
    cleaned_df, stats = delete_predash_following_info_urn()
    
    if cleaned_df is not None and stats:
        print(f"\n🎯 İşlem tamamlandı! Optimized dataset: {len(cleaned_df)} satır × {len(cleaned_df.columns)} sütun")
        print(f"💾 Memory tasarrufu: {stats['memory_saved']:.2f} MB")
    else:
        print("\n❌ İşlem başarısız!") 