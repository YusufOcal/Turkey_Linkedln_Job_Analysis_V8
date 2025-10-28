#!/usr/bin/env python3
"""
Pipeline Issues Checker: Son dataset'teki problemleri tespit et

Kontrol edilecekler:
1. Silinmesi gereken ama hala var olan sütunlar
2. Üretilmesi gereken ama eksik olan sütunlar
"""

import pandas as pd

def check_pipeline_issues():
    """Pipeline issues kontrolü"""
    
    print("🔍 PIPELINE ISSUES CHECKER")
    print("=" * 60)
    
    # Son üretilen dataset
    latest_file = 'linkedin_jobs_after_step1_job_functions.csv'
    
    try:
        print(f"📂 Loading latest dataset: {latest_file}")
        df = pd.read_csv(latest_file)
        print(f"✅ Dataset loaded: {len(df):,} records, {len(df.columns)} columns")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return
    
    current_columns = set(df.columns)
    print(f"\n📊 Current columns count: {len(current_columns)}")
    
    # BEKLENTİLER vs GERÇEKLER
    print(f"\n" + "="*60)
    print("📋 EXPECTED vs ACTUAL ANALYSIS")
    print("="*60)
    
    # 1. SİLİNMESİ GEREKEN AMA HALA VAR OLAN SÜTUNLAR
    print(f"\n❌ COLUMNS THAT SHOULD BE DELETED BUT STILL EXIST:")
    print("-" * 50)
    
    should_be_deleted = [
        'company/followingState/followingType',
        'company/followingState/preDashFollowingInfoUrn',
        'company/industry/0',
        'jobApplicantInsights/entityUrn',  # Project 53
        'workRemoteAllowed',  # Project 54
        'link'  # Project 55
    ]
    
    still_exists = []
    for col in should_be_deleted:
        if col in current_columns:
            still_exists.append(col)
            print(f"   🚨 {col} - STILL EXISTS!")
        else:
            print(f"   ✅ {col} - Correctly deleted")
    
    # 2. ÜRETİLMESİ GEREKEN AMA EKSİK OLAN SÜTUNLAR
    print(f"\n✨ COLUMNS THAT SHOULD BE CREATED BUT ARE MISSING:")
    print("-" * 50)
    
    should_be_created = [
        'job_functions_combined',  # Step 1 output
        'urgency_category',  # expireAt transformation
        'job_investment_category',  # contentSource transformation
        'company_has_logo'  # logo boolean transformation
    ]
    
    missing_columns = []
    for col in should_be_created:
        if col in current_columns:
            print(f"   ✅ {col} - Correctly created")
        else:
            missing_columns.append(col)
            print(f"   🚨 {col} - MISSING!")
    
    # 3. YÜKSEK NULL ORANLI SÜTUNLAR (>95%)
    print(f"\n🔍 HIGH NULL RATE COLUMNS (>95%):")
    print("-" * 50)
    
    high_null_columns = []
    for col in df.columns:
        null_pct = (df[col].isnull().sum() / len(df)) * 100
        if null_pct > 95:
            high_null_columns.append((col, null_pct))
            print(f"   ⚠️  {col}: {null_pct:.1f}% null")
    
    # 4. ÖZET RAPOR
    print(f"\n" + "="*60)
    print("📊 SUMMARY REPORT")
    print("="*60)
    
    print(f"\n🚨 CRITICAL ISSUES:")
    print(f"   • Columns that should be deleted but still exist: {len(still_exists)}")
    for col in still_exists:
        print(f"     - {col}")
    
    print(f"\n   • Columns that should be created but are missing: {len(missing_columns)}")
    for col in missing_columns:
        print(f"     - {col}")
    
    print(f"\n⚠️  PERFORMANCE ISSUES:")
    print(f"   • High null rate columns (>95%): {len(high_null_columns)}")
    for col, pct in high_null_columns:
        print(f"     - {col}: {pct:.1f}% null")
    
    # 5. ACTION ITEMS
    print(f"\n" + "="*60)
    print("🎯 REQUIRED ACTIONS")
    print("="*60)
    
    total_issues = len(still_exists) + len(missing_columns) + len(high_null_columns)
    
    if total_issues == 0:
        print(f"✅ NO ISSUES FOUND! Pipeline is perfect.")
    else:
        print(f"❌ TOTAL ISSUES: {total_issues}")
        
        if still_exists:
            print(f"\n1. DELETE these columns in next steps:")
            for col in still_exists:
                print(f"   - {col}")
        
        if missing_columns:
            print(f"\n2. CREATE these columns in pipeline:")
            for col in missing_columns:
                print(f"   - {col}")
        
        if high_null_columns:
            print(f"\n3. CONSIDER DELETING high null columns:")
            for col, pct in high_null_columns:
                print(f"   - {col} ({pct:.1f}% null)")
    
    # 6. NEXT STEPS RECOMMENDATION
    print(f"\n" + "="*60)
    print("🛣️  NEXT STEPS RECOMMENDATION")
    print("="*60)
    
    if still_exists or high_null_columns:
        total_deletions = len(still_exists) + len(high_null_columns)
        print(f"STEP 2: Column Cleanup - Delete {total_deletions} problematic columns")
        print(f"  Input: {latest_file}")
        print(f"  Output: linkedin_jobs_after_step2_cleanup.csv")
        print(f"  Expected: {len(current_columns)} → {len(current_columns) - total_deletions} columns")
    else:
        print(f"✅ Ready for Step 2: EntityUrn Redundancy Elimination")

if __name__ == "__main__":
    check_pipeline_issues() 