#!/usr/bin/env python3
"""
ExpireAt Status Analyzer: expireAt sütunundaki tüm düzenlemelerin durumunu analiz et

Kontrol edilecekler:
1. expireAt data type (int64 → datetime64)
2. Urgency kategorileri
3. Temporal features (month, quarter, season, etc.)
4. Business intelligence columns
"""

import pandas as pd
from datetime import datetime

def analyze_expireAt_status():
    """expireAt transformations status analizi"""
    
    print("📅 EXPIREAT TRANSFORMATIONS STATUS ANALYZER")
    print("=" * 55)
    
    target_file = 'linkedin_jobs_dataset_optimized_step12.csv'
    
    try:
        print(f"📂 Loading dataset: {target_file}")
        df = pd.read_csv(target_file)
        print(f"✅ Dataset loaded: {len(df):,} records, {len(df.columns)} columns")
        print()
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return
    
    # ExpireAt ve urgency ile ilgili sütunları bul
    all_cols = df.columns.tolist()
    expire_related = [col for col in all_cols if any(keyword in col.lower() 
                     for keyword in ['expire', 'urgency', 'urgent'])]
    
    print("🔍 EXPIREAT & URGENCY RELATED COLUMNS")
    print("=" * 45)
    print(f"Found {len(expire_related)} expire/urgency related columns:")
    
    for i, col in enumerate(expire_related, 1):
        dtype = df[col].dtype
        non_null = df[col].count()
        total = len(df)
        null_pct = ((total - non_null) / total) * 100
        
        print(f"   {i:2}. {col}")
        print(f"       📊 Type: {dtype}")
        print(f"       📈 Non-null: {non_null:,}/{total:,} ({100-null_pct:.1f}%)")
        
        # Sample values
        if non_null > 0:
            samples = df[col].dropna().head(3).tolist()
            print(f"       📋 Samples: {samples}")
        print()
    
    # EXPIREAT CORE ANALYSIS
    if 'expireAt' in df.columns:
        print("📅 EXPIREAT CORE COLUMN ANALYSIS")
        print("=" * 40)
        
        expire_col = df['expireAt']
        
        print(f"📊 Basic Statistics:")
        print(f"   • Data Type: {expire_col.dtype}")
        print(f"   • Total Records: {len(expire_col):,}")
        print(f"   • Non-null: {expire_col.count():,}")
        print(f"   • Null: {expire_col.isnull().sum():,}")
        print(f"   • Min Value: {expire_col.min()}")
        print(f"   • Max Value: {expire_col.max()}")
        print(f"   • Unique Values: {expire_col.nunique():,}")
        print()
        
        # Check if it's datetime or timestamp
        print(f"🕐 DATETIME CONVERSION STATUS:")
        if expire_col.dtype == 'int64':
            print(f"   ❌ STILL INTEGER - Not converted to datetime")
            print(f"   🔍 Likely Unix timestamp format")
            
            # Try to understand timestamp format
            sample_values = expire_col.head(5)
            print(f"   📋 Sample timestamp values: {sample_values.tolist()}")
            
            # Check if milliseconds or seconds
            avg_value = expire_col.mean()
            if avg_value > 1e12:  # Likely milliseconds
                print(f"   🎯 Format: Unix timestamp (milliseconds)")
                print(f"   🔧 Conversion needed: pd.to_datetime(df['expireAt'], unit='ms')")
            else:  # Likely seconds
                print(f"   🎯 Format: Unix timestamp (seconds)")
                print(f"   🔧 Conversion needed: pd.to_datetime(df['expireAt'], unit='s')")
                
        elif 'datetime' in str(expire_col.dtype):
            print(f"   ✅ PROPERLY CONVERTED - Already datetime format")
            print(f"   📅 Date range: {expire_col.min()} to {expire_col.max()}")
        else:
            print(f"   ⚠️  UNEXPECTED FORMAT - Type: {expire_col.dtype}")
        print()
    
    # URGENCY ANALYSIS
    urgency_columns = [col for col in expire_related if 'urgency' in col.lower()]
    
    if urgency_columns:
        print("🚨 URGENCY CATEGORIES ANALYSIS")
        print("=" * 35)
        
        for col in urgency_columns:
            print(f"📊 {col}:")
            value_counts = df[col].value_counts()
            total_records = len(df)
            
            for value, count in value_counts.head(10).items():
                percentage = (count / total_records) * 100
                print(f"   • {value}: {count:,} ({percentage:.1f}%)")
            
            if len(value_counts) > 10:
                remaining = len(value_counts) - 10
                print(f"   • ... and {remaining} more categories")
            print()
    
    # TEMPORAL FEATURES ANALYSIS
    temporal_cols = [col for col in expire_related if any(word in col.lower() 
                    for word in ['month', 'quarter', 'day', 'week', 'season'])]
    
    if temporal_cols:
        print("📆 TEMPORAL FEATURES ANALYSIS")
        print("=" * 35)
        
        for col in temporal_cols:
            print(f"📊 {col}:")
            unique_values = df[col].unique()
            print(f"   • Unique values: {len(unique_values)}")
            print(f"   • Values: {sorted(unique_values)}")
            print()
    
    # COMPLETENESS ASSESSMENT
    print("🎯 EXPIREAT TRANSFORMATIONS COMPLETENESS ASSESSMENT")
    print("=" * 55)
    
    expected_transformations = {
        'datetime_conversion': {
            'description': 'expireAt converted from Unix timestamp to datetime',
            'check': 'expireAt' in df.columns and 'datetime' in str(df['expireAt'].dtype),
            'status': 'expireAt' in df.columns and 'datetime' in str(df['expireAt'].dtype)
        },
        'urgency_categories': {
            'description': 'Urgency categories created (CRITICAL, HIGH, MEDIUM, etc.)',
            'check': len(urgency_columns) > 0,
            'status': len(urgency_columns) > 0
        },
        'temporal_features': {
            'description': 'Temporal features extracted (month, quarter, season, etc.)',
            'check': len(temporal_cols) > 0,
            'status': len(temporal_cols) > 0
        },
        'business_intelligence': {
            'description': 'Business-friendly urgency levels for analytics',
            'check': any('level' in col.lower() for col in urgency_columns),
            'status': any('level' in col.lower() for col in urgency_columns) if urgency_columns else False
        }
    }
    
    total_transformations = len(expected_transformations)
    completed_transformations = sum(1 for t in expected_transformations.values() if t['status'])
    completion_rate = (completed_transformations / total_transformations) * 100
    
    print(f"📊 TRANSFORMATION CHECKLIST:")
    for name, info in expected_transformations.items():
        status = "✅ COMPLETED" if info['status'] else "❌ MISSING"
        print(f"   • {info['description']}")
        print(f"     Status: {status}")
        print()
    
    print(f"🎯 OVERALL COMPLETION SCORE:")
    print(f"   • Completed: {completed_transformations}/{total_transformations}")
    print(f"   • Completion Rate: {completion_rate:.1f}%")
    
    if completion_rate == 100.0:
        print(f"   🎉 PERFECT! All expireAt transformations completed.")
    elif completion_rate >= 75.0:
        print(f"   ⚠️  GOOD progress, but some transformations missing.")
    else:
        print(f"   🚨 POOR completion, major transformations needed.")
    
    # RECOMMENDATIONS
    print(f"\n🛠️  RECOMMENDATIONS:")
    print("-" * 20)
    
    missing_transformations = [name for name, info in expected_transformations.items() if not info['status']]
    
    if not missing_transformations:
        print(f"✅ No action needed! All expireAt transformations are complete.")
    else:
        print(f"❌ The following transformations need to be completed:")
        for name in missing_transformations:
            info = expected_transformations[name]
            print(f"   • {info['description']}")
        
        print(f"\n🔧 Next steps:")
        if 'datetime_conversion' in missing_transformations:
            print(f"   1. Run datetime conversion script")
        if 'urgency_categories' in missing_transformations:
            print(f"   2. Create urgency categorization")
        if 'temporal_features' in missing_transformations:
            print(f"   3. Extract temporal features")
    
    return {
        'completion_rate': completion_rate,
        'completed_transformations': completed_transformations,
        'total_transformations': total_transformations,
        'expire_related_columns': expire_related,
        'urgency_columns': urgency_columns,
        'temporal_columns': temporal_cols
    }

if __name__ == "__main__":
    results = analyze_expireAt_status() 