#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - Job Investment Category Creation & ContentSource Deletion
ContentSource sütunundan business-friendly kategori oluşturup orijinal sütunu silen script yazıyorum.
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def create_job_investment_category_and_delete_source(df):
    """ContentSource'dan yeni kategori oluştur ve orijinal sütunu sil"""
    
    print("🏗️ JOB INVESTMENT CATEGORY CREATION & CONTENTSOURCE DELETION")
    print("=" * 65)
    
    source_column = 'contentSource'
    new_column = 'job_investment_type'
    
    # Check if source column exists
    if source_column not in df.columns:
        print(f"❌ HATA: {source_column} sütunu bulunamadı!")
        return None
    
    # 1. ORIGINAL DATA ANALYSIS
    print("📊 1. ORİJİNAL VERİ ANALİZİ")
    print("-" * 30)
    
    original_stats = df[source_column].value_counts()
    print("📋 Mevcut ContentSource Dağılımı:")
    for value, count in original_stats.items():
        percentage = (count / len(df)) * 100
        print(f"   📊 {value}: {count:,} ilan ({percentage:.1f}%)")
    print()
    
    # 2. NEW CATEGORY MAPPING STRATEGY
    print("🎯 2. YENİ KATEGORİ MAPPING STRATEJİSİ")
    print("-" * 40)
    
    print("💡 Business-Friendly Kategori Mapping:")
    
    category_mapping = {
        'JOBS_PREMIUM_OFFLINE': 'PREMIUM_OFFLINE',
        'JOBS_PREMIUM': 'PREMIUM_ONLINE', 
        'JOBS_CREATE': 'ORGANIC'
    }
    
    business_explanations = {
        'PREMIUM_OFFLINE': {
            'meaning': 'Ücretli İlan (Offline İşlenmiş)',
            'description': 'Şirketlerin LinkedIn\'e para ödediği, toplu işlenmiş premium ilanlar',
            'investment': 'PAID - Company Investment',
            'quality': 'HIGH - Premium features',
            'visibility': 'High visibility, priority listing'
        },
        'PREMIUM_ONLINE': {
            'meaning': 'Ücretli İlan (Online İşlenmiş)',
            'description': 'Şirketlerin LinkedIn\'e para ödediği, gerçek zamanlı premium ilanlar',
            'investment': 'PAID - Company Investment',
            'quality': 'HIGH - Premium features + Real-time',
            'visibility': 'High visibility, immediate processing'
        },
        'ORGANIC': {
            'meaning': 'Ücretsiz/Organik İlan',
            'description': 'Şirketlerin ücretsiz olarak oluşturduğu temel seviye ilanlar',
            'investment': 'FREE - No cost to company',
            'quality': 'STANDARD - Basic features',
            'visibility': 'Standard visibility'
        }
    }
    
    for old_value, new_value in category_mapping.items():
        old_count = original_stats.get(old_value, 0)
        old_percentage = (old_count / len(df)) * 100 if old_count > 0 else 0
        explanation = business_explanations[new_value]
        
        print(f"🔄 {old_value} → {new_value}")
        print(f"   📊 Count: {old_count:,} ilan ({old_percentage:.1f}%)")
        print(f"   📝 Meaning: {explanation['meaning']}")
        print(f"   💼 Description: {explanation['description']}")
        print(f"   💰 Investment: {explanation['investment']}")
        print(f"   🎯 Quality: {explanation['quality']}")
        print(f"   👁️ Visibility: {explanation['visibility']}")
        print()
    
    # 3. CREATE NEW COLUMN
    print("🏗️ 3. YENİ SÜTUN OLUŞTURMA")
    print("-" * 25)
    
    print(f"📝 Yeni sütun oluşturuluyor: {new_column}")
    
    # Apply mapping
    df[new_column] = df[source_column].map(category_mapping)
    
    # Verify mapping success
    unmapped_count = df[new_column].isnull().sum()
    if unmapped_count > 0:
        print(f"⚠️ UYARI: {unmapped_count} değer map edilemedi!")
        unmapped_values = df[df[new_column].isnull()][source_column].unique()
        print(f"📋 Map edilemeyen değerler: {unmapped_values}")
    else:
        print("✅ Tüm değerler başarıyla map edildi!")
    
    # Convert to category type for memory optimization
    df[new_column] = df[new_column].astype('category')
    
    print(f"✅ Yeni sütun oluşturuldu ve 'category' tipine çevrildi")
    print()
    
    # 4. NEW COLUMN VERIFICATION
    print("🔍 4. YENİ SÜTUN VERİFİKASYONU")
    print("-" * 30)
    
    new_stats = df[new_column].value_counts()
    new_memory = df[new_column].memory_usage(deep=True) / 1024**2
    
    print("📊 Yeni Job Investment Type Dağılımı:")
    for value, count in new_stats.items():
        percentage = (count / len(df)) * 100
        print(f"   📊 {value}: {count:,} ilan ({percentage:.1f}%)")
    
    print(f"\n📈 Yeni sütun özellikleri:")
    print(f"   🔧 Data Type: {df[new_column].dtype}")
    print(f"   🎯 Unique Values: {df[new_column].nunique()}")
    print(f"   💾 Memory Usage: {new_memory:.3f} MB")
    print()
    
    # 5. MEMORY COMPARISON BEFORE DELETION
    print("📊 5. MEMORY COMPARISON (DELETE ÖNCESİ)")
    print("-" * 40)
    
    original_memory = df[source_column].memory_usage(deep=True) / 1024**2
    
    print(f"📋 Memory Karşılaştırması:")
    print(f"   📊 Original ({source_column}): {original_memory:.3f} MB (object)")
    print(f"   📊 New ({new_column}): {new_memory:.3f} MB (category)")
    print(f"   💾 Memory Difference: {original_memory - new_memory:.3f} MB")
    print(f"   📈 Memory Efficiency: {((original_memory - new_memory) / original_memory * 100):.1f}% improvement")
    print()
    
    # 6. SAFE DELETION PROTOCOL
    print("🗑️ 6. SAFE DELETION PROTOCOL")
    print("-" * 30)
    
    print("📋 Deletion Safety Checklist:")
    
    # Verify data integrity
    data_integrity_check = len(new_stats) == len(original_stats)
    print(f"   ✅ Category count preserved: {data_integrity_check}")
    
    # Verify no data loss
    original_total = original_stats.sum()
    new_total = new_stats.sum()
    data_loss_check = original_total == new_total
    print(f"   ✅ No data loss: {data_loss_check} ({original_total} → {new_total})")
    
    # Verify business logic preserved
    premium_offline_preserved = new_stats.get('PREMIUM_OFFLINE', 0) == original_stats.get('JOBS_PREMIUM_OFFLINE', 0)
    premium_online_preserved = new_stats.get('PREMIUM_ONLINE', 0) == original_stats.get('JOBS_PREMIUM', 0)
    organic_preserved = new_stats.get('ORGANIC', 0) == original_stats.get('JOBS_CREATE', 0)
    
    business_logic_check = premium_offline_preserved and premium_online_preserved and organic_preserved
    print(f"   ✅ Business logic preserved: {business_logic_check}")
    
    # Overall safety assessment
    safe_to_delete = data_integrity_check and data_loss_check and business_logic_check
    print(f"   🎯 Safe to delete: {safe_to_delete}")
    print()
    
    if safe_to_delete:
        print("🗑️ DELETING ORIGINAL COLUMN...")
        
        # Get baseline metrics before deletion
        columns_before = len(df.columns)
        memory_before = df.memory_usage(deep=True).sum() / 1024**2
        
        # Delete original column
        df.drop(columns=[source_column], inplace=True)
        
        # Get metrics after deletion
        columns_after = len(df.columns)
        memory_after = df.memory_usage(deep=True).sum() / 1024**2
        
        print("✅ Original contentSource column deleted successfully!")
        print()
        
        # 7. DELETION RESULTS
        print("📈 7. DELETION RESULTS")
        print("-" * 20)
        
        column_reduction = columns_before - columns_after
        memory_saved = memory_before - memory_after
        memory_saved_percentage = (memory_saved / memory_before) * 100
        
        print(f"📊 Schema Changes:")
        print(f"   📋 Columns Before: {columns_before}")
        print(f"   📋 Columns After: {columns_after}")
        print(f"   📉 Column Reduction: {column_reduction}")
        
        print(f"\n💾 Memory Optimization:")
        print(f"   📊 Memory Before: {memory_before:.2f} MB")
        print(f"   📊 Memory After: {memory_after:.2f} MB")
        print(f"   📉 Memory Saved: {memory_saved:.3f} MB")
        print(f"   📈 Memory Improvement: {memory_saved_percentage:.2f}%")
        print()
        
        # 8. FINAL BUSINESS VALUE ASSESSMENT
        print("🎯 8. FINAL BUSINESS VALUE ASSESSMENT")
        print("-" * 35)
        
        print("✅ ACHIEVED IMPROVEMENTS:")
        print(f"   🏗️ Business-Friendly Categories: Technical → Business terms")
        print(f"   💾 Memory Optimization: {memory_saved:.3f} MB saved")
        print(f"   🔧 Data Type Optimization: object → category")
        print(f"   📊 Enhanced Analytics: Clear investment classification")
        print(f"   🎯 Improved Usability: Intuitive category names")
        
        print(f"\n📈 NEW COLUMN ADVANTAGES:")
        print(f"   💰 PREMIUM_OFFLINE: Clear paid content identification")
        print(f"   ⚡ PREMIUM_ONLINE: Real-time paid content distinction")
        print(f"   🌱 ORGANIC: Free content clear classification")
        print(f"   📊 Analytics Ready: Perfect for business analysis")
        
        return {
            'success': True,
            'new_column': new_column,
            'deleted_column': source_column,
            'columns_before': columns_before,
            'columns_after': columns_after,
            'memory_saved_mb': memory_saved,
            'memory_improvement_pct': memory_saved_percentage,
            'category_distribution': dict(new_stats),
            'business_categories': list(category_mapping.values())
        }
    else:
        print("❌ SAFETY CHECK FAILED - Deletion aborted!")
        print("🔍 Please review data integrity issues before proceeding")
        return {
            'success': False,
            'reason': 'Safety check failed',
            'data_integrity_check': data_integrity_check,
            'data_loss_check': data_loss_check,
            'business_logic_check': business_logic_check
        }

if __name__ == "__main__":
    try:
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step6.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} kayıt, {len(df.columns)} sütun")
        print()
        
        result = create_job_investment_category_and_delete_source(df)
        
        if result and result['success']:
            print("🎉 İŞLEM BAŞARILI!")
            print(f"✅ Yeni sütun '{result['new_column']}' oluşturuldu")
            print(f"🗑️ Eski sütun '{result['deleted_column']}' silindi") 
            print(f"💾 {result['memory_saved_mb']:.3f} MB memory tasarrufu sağlandı")
            
            # Save the updated dataset
            output_file = 'linkedin_jobs_dataset_optimized_step7.csv'
            df.to_csv(output_file, index=False)
            print(f"💾 Güncellenmiş dataset kaydedildi: {output_file}")
        else:
            print("❌ İşlem başarısız!")
            
    except Exception as e:
        print(f"❌ HATA: {str(e)}") 