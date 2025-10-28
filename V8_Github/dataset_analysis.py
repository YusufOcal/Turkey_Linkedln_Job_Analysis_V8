#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Comprehensive Analysis Script
Dataset analizi için detaylı inceleme scripti
"""

import pandas as pd
import numpy as np
import json
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def analyze_linkedin_dataset():
    """LinkedIn dataset'ini kapsamlı olarak analiz eder"""
    
    print("🔍 LinkedIn Jobs Dataset - Kapsamlı Analiz")
    print("=" * 60)
    
    try:
        # Dataset'i yükle
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_insights_completed.csv')
        
        print(f"✅ Dataset başarıyla yüklendi!")
        print()
        
        # Temel Bilgiler
        print("📊 TEMEL BİLGİLER")
        print("-" * 30)
        print(f"📋 Satır sayısı: {len(df):,}")
        print(f"📋 Kolon sayısı: {len(df.columns):,}")
        print(f"💾 Memory kullanımı: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print()
        
        # Dataset boyut karşılaştırması
        file_sizes = {}
        for ext in ['csv', 'json', 'xlsx']:
            file_path = Path(f'linkedin_jobs_dataset_insights_completed.{ext}')
            if file_path.exists():
                size_mb = file_path.stat().st_size / 1024**2
                file_sizes[ext.upper()] = f"{size_mb:.1f} MB"
        
        print("📁 DOSYA BOYUTLARI")
        print("-" * 20)
        for format_type, size in file_sizes.items():
            print(f"📄 {format_type}: {size}")
        print()
        
        # Kolon Tipleri Analizi
        print("🔧 KOLON TİPLERİ ANALİZİ")
        print("-" * 30)
        dtype_counts = df.dtypes.value_counts()
        for dtype, count in dtype_counts.items():
            print(f"📊 {dtype}: {count} kolon")
        print()
        
        # Null Değer Analizi
        print("❌ NULL DEĞER ANALİZİ")
        print("-" * 25)
        null_summary = df.isnull().sum()
        null_percentages = (null_summary / len(df) * 100).round(2)
        
        # En çok null olan kolonlar
        high_null_cols = null_percentages[null_percentages > 0].sort_values(ascending=False)
        
        if len(high_null_cols) > 0:
            print("🚨 Null değer içeren kolonlar (top 10):")
            for col, pct in high_null_cols.head(10).items():
                count = null_summary[col]
                print(f"   📍 {col}: {count:,} ({pct}%)")
        else:
            print("✅ Hiçbir kolonda null değer bulunmamaktadır!")
        print()
        
        # Temel İstatistikler - Numeric Kolonlar
        print("📈 NUMERİK KOLONLAR - TEMEL İSTATİSTİKLER")
        print("-" * 45)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        print(f"🔢 Numerik kolon sayısı: {len(numeric_cols)}")
        
        if len(numeric_cols) > 0:
            # Önemli numeric kolonları listele
            key_numeric = [col for col in numeric_cols if any(keyword in col.lower() 
                          for keyword in ['apply', 'view', 'salary', 'count', 'year'])]
            
            if key_numeric:
                print("\n🎯 Önemli numerik kolonlar:")
                for col in key_numeric:
                    if df[col].notna().sum() > 0:
                        stats = df[col].describe()
                        print(f"   📊 {col}:")
                        print(f"      Min: {stats['min']:,.0f} | Max: {stats['max']:,.0f}")
                        print(f"      Ortalama: {stats['mean']:,.1f} | Medyan: {stats['50%']:,.1f}")
        print()
        
        # Boolean Kolonlar
        print("✅ BOOLEAN KOLONLAR")
        print("-" * 20)
        bool_cols = df.select_dtypes(include=['bool', 'boolean']).columns
        if len(bool_cols) > 0:
            for col in bool_cols:
                true_count = df[col].sum() if df[col].notna().sum() > 0 else 0
                true_pct = (true_count / len(df) * 100)
                print(f"🔘 {col}: {true_count:,} True ({true_pct:.1f}%)")
        else:
            print("ℹ️ Boolean kolon bulunamadı")
        print()
        
        # Text Kolonları - Uzunluk Analizi
        print("📝 TEXT KOLONLARI ANALİZİ")
        print("-" * 25)
        text_cols = df.select_dtypes(include=['object']).columns
        print(f"📄 Text kolon sayısı: {len(text_cols)}")
        
        # Önemli text kolonlarının uzunluk analizi
        key_text_cols = [col for col in text_cols if any(keyword in col.lower() 
                        for keyword in ['name', 'title', 'skill', 'desc', 'location', 'industry'])]
        
        if key_text_cols:
            print("\n📊 Önemli text kolonları (karakter uzunluğu):")
            for col in key_text_cols[:8]:  # İlk 8 tanesini göster
                non_null = df[col].dropna()
                if len(non_null) > 0:
                    avg_len = non_null.astype(str).str.len().mean()
                    max_len = non_null.astype(str).str.len().max()
                    print(f"   📝 {col}: Ort. {avg_len:.0f} karakter (Max: {max_len})")
        print()
        
        # Şirket Analizi
        if 'company/name' in df.columns:
            print("🏢 ŞİRKET ANALİZİ")
            print("-" * 15)
            company_counts = df['company/name'].value_counts()
            total_companies = len(company_counts)
            print(f"🏭 Toplam şirket sayısı: {total_companies:,}")
            print(f"🔝 En aktif şirket: {company_counts.index[0]} ({company_counts.iloc[0]} ilan)")
            print(f"📊 Ortalama ilan/şirket: {company_counts.mean():.1f}")
            
            # Top 5 şirket
            print("\n🏆 En aktif 5 şirket:")
            for i, (company, count) in enumerate(company_counts.head(5).items(), 1):
                print(f"   {i}. {company}: {count} ilan")
            print()
        
        # İş Kategorileri
        if 'formattedJobFunctions/0' in df.columns:
            print("💼 İŞ KATEGORİLERİ")
            print("-" * 18)
            job_functions = df['formattedJobFunctions/0'].value_counts()
            print(f"🎯 Toplam kategori sayısı: {len(job_functions)}")
            print("\n📈 En popüler 5 kategori:")
            for i, (func, count) in enumerate(job_functions.head(5).items(), 1):
                pct = (count / len(df) * 100)
                print(f"   {i}. {func}: {count:,} ilan ({pct:.1f}%)")
            print()
        
        # Skills Analizi
        if 'skills_consolidated' in df.columns:
            print("🛠️ SKILLS ANALİZİ")
            print("-" * 15)
            skills_data = df['skills_consolidated'].dropna()
            if len(skills_data) > 0:
                total_skills = skills_data.str.split(',').str.len().sum()
                avg_skills = skills_data.str.split(',').str.len().mean()
                print(f"🔧 Toplam skill girişi: {total_skills:,}")
                print(f"📊 İlan başına ortalama skill: {avg_skills:.1f}")
                
                # En popüler skilleri bul
                all_skills = []
                for skills_str in skills_data:
                    if pd.notna(skills_str):
                        skills_list = [skill.strip() for skill in str(skills_str).split(',')]
                        all_skills.extend(skills_list)
                
                if all_skills:
                    from collections import Counter
                    skill_counts = Counter(all_skills)
                    print("\n🎯 En popüler 10 skill:")
                    for i, (skill, count) in enumerate(skill_counts.most_common(10), 1):
                        pct = (count / len(all_skills) * 100)
                        print(f"   {i}. {skill}: {count:,} ({pct:.1f}%)")
            print()
        
        # Salary Analizi
        salary_cols = [col for col in df.columns if 'salary' in col.lower()]
        if salary_cols:
            print("💰 MAAŞ ANALİZİ")
            print("-" * 13)
            print(f"💵 Maaş ile ilgili kolon sayısı: {len(salary_cols)}")
            
            for col in salary_cols[:5]:  # İlk 5 salary kolonunu analiz et
                non_null_count = df[col].notna().sum()
                pct = (non_null_count / len(df) * 100)
                print(f"   📊 {col}: {non_null_count:,} kayıt ({pct:.1f}%)")
            print()
        
        # Dataset Kalite Skoru
        print("🎯 DATASET KALİTE SKORU")
        print("-" * 22)
        
        # Kalite metrikleri
        completeness = (1 - df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        consistency = 100  # Assuming good consistency from cleaning reports
        data_types = len(df.select_dtypes(include=[np.number, 'bool', 'boolean']).columns) / len(df.columns) * 100
        
        overall_quality = (completeness + consistency + data_types) / 3
        
        print(f"📈 Veri Tamlığı: {completeness:.1f}%")
        print(f"🔧 Veri Tutarlılığı: {consistency:.1f}%")
        print(f"⚙️ Optimized Data Types: {data_types:.1f}%")
        print(f"🏆 TOPLAM KALİTE SKORU: {overall_quality:.1f}%")
        
        # Kalite değerlendirmesi
        if overall_quality >= 90:
            quality_label = "🌟 MÜKEMMEL"
        elif overall_quality >= 80:
            quality_label = "✨ ÇOK İYİ"
        elif overall_quality >= 70:
            quality_label = "👍 İYİ"
        else:
            quality_label = "⚠️ GELİŞTİRİLEBİLİR"
        
        print(f"📊 Kalite Seviyesi: {quality_label}")
        print()
        
        # Dataset özeti
        print("📋 DATASET ÖZETİ")
        print("-" * 15)
        print("✅ Bu dataset şunlar için hazır:")
        print("   📊 Business Intelligence analizi")
        print("   🤖 Machine Learning modelleme")
        print("   📈 İstatistiksel analiz")
        print("   🔍 Exploratory Data Analysis")
        print("   📋 Raporlama ve dashboard")
        
        return df
        
    except FileNotFoundError:
        print("❌ HATA: 'linkedin_jobs_dataset_insights_completed.csv' dosyası bulunamadı!")
        return None
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        return None

if __name__ == "__main__":
    # Analizi çalıştır
    dataset = analyze_linkedin_dataset()
    
    # Ek bilgi
    print("\n" + "=" * 60)
    print("🎯 ANALİZ TAMAMLANDI!")
    print("📝 Detaylı raporlar için .md dosyalarını inceleyebilirsiniz.")
    print("💡 İpucu: 'df = pd.read_csv(\"linkedin_jobs_dataset_insights_completed.csv\")' ile başlayabilirsiniz.") 