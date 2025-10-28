#!/usr/bin/env python3
"""
Comprehensive Column Issues Check

Tüm silme kararlarını kontrol eder ve toplu silme için hazırlar.
"""

import pandas as pd

def check_all_column_issues():
    """Tüm sütun problemlerini kontrol et"""
    
    print("🚨 KAPSAMLI SÜTUN SORUN KONTROLÜ")
    print("=" * 60)
    
    # Son dataset'i yükle
    try:
        df = pd.read_csv('linkedin_jobs_cleaned_no_redundant_links.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} kayıt, {len(df.columns)} sütun")
    except Exception as e:
        print(f"❌ Dataset yüklenemedi: {e}")
        return
    
    # Kullanıcının bahsettiği problemli sütunlar
    user_mentioned_issues = [
        'company/followingState/followingType',
        'company/followingState/preDashFollowingInfoUrn', 
        'company/industry/0'
    ]
    
    # Daha önce silmeye karar verdiğimiz ama hâlâ var olan sütunlar
    previously_decided_to_delete = [
        'jobApplicantInsights/entityUrn',  # Zaten silinmiş
        'workRemoteAllowed',  # Zaten silinmiş  
        'link'  # Zaten silinmiş
    ]
    
    print(f"\n📊 KULLANICININ BAHSETTİĞİ PROBLEMLİ SÜTUNLAR:")
    for col in user_mentioned_issues:
        if col in df.columns:
            print(f"   😱 {col}: VAR (silinmeli!)")
        else:
            print(f"   ✅ {col}: YOK")
    
    print(f"\n📊 DAHA ÖNCE SİLDİĞİMİZ SÜTUNLAR (kontrol):")
    for col in previously_decided_to_delete:
        if col in df.columns:
            print(f"   😱 {col}: VAR (hâlâ duruyor!)")
        else:
            print(f"   ✅ {col}: SİLİNMİŞ")
    
    # Tüm sütunları listele - yüksek null oranları için
    print(f"\n📋 YÜKSEK NULL ORANLI SÜTUNLAR (>90% null):")
    null_analysis = df.isnull().sum()
    high_null_columns = []
    
    for col in df.columns:
        null_count = null_analysis[col]
        null_pct = (null_count / len(df)) * 100
        if null_pct > 90:
            high_null_columns.append((col, null_pct))
            print(f"   🔥 {col}: %{null_pct:.1f} null")
    
    # Company related sütunları bul
    print(f"\n🏢 COMPANY İLE İLGİLİ TÜM SÜTUNLAR:")
    company_columns = [col for col in df.columns if 'company' in col.lower()]
    for col in company_columns:
        unique_count = df[col].nunique()
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        print(f"   • {col}: {unique_count:,} benzersiz, %{null_pct:.1f} null")
    
    # Potansiyel silinecek sütunları topla
    columns_to_delete = []
    
    # Kullanıcının bahsettiği problemli sütunlar
    for col in user_mentioned_issues:
        if col in df.columns:
            columns_to_delete.append(col)
    
    # Yüksek null oranlı sütunlar (>95% null)
    for col, null_pct in high_null_columns:
        if null_pct > 95:
            columns_to_delete.append(col)
    
    print(f"\n💡 TOPLU SİLME ÖNERİSİ:")
    print(f"   📊 Toplam silinecek sütun: {len(set(columns_to_delete))}")
    
    if columns_to_delete:
        print(f"   🗑️  Silinecek sütunlar:")
        for col in sorted(set(columns_to_delete)):
            print(f"      - {col}")
        
        print(f"\n   📈 Sonuç:")
        print(f"      • Mevcut: {len(df.columns)} sütun")  
        print(f"      • Sonrası: {len(df.columns) - len(set(columns_to_delete))} sütun")
        print(f"      • Azalma: {len(set(columns_to_delete))} sütun")
    
    return sorted(set(columns_to_delete))

if __name__ == "__main__":
    columns_to_delete = check_all_column_issues()
    print(f"\n🎯 SONUÇ: {len(columns_to_delete)} sütun silinmeye hazır!") 