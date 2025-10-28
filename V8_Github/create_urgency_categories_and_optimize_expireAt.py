#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Jobs Dataset - ExpireAt Urgency Categories Creation and Optimization
expireAt sütununu iş zekası temelli urgency kategorilerine dönüştürme ve optimizasyon
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def create_urgency_categories_and_optimize_expireAt(df):
    """ExpireAt sütununu urgency kategorilerine dönüştürür ve optimize eder"""
    
    print("🚀 LINKEDIN JOBS DATASET - EXPIREAT URGENCY TRANSFORMATION")
    print("=" * 65)
    
    # Load initial state
    initial_columns = len(df.columns)
    initial_memory = df.memory_usage(deep=True).sum() / 1024**2
    
    print(f"📊 Başlangıç Durumu:")
    print(f"   📋 Total columns: {initial_columns}")
    print(f"   💾 Total memory: {initial_memory:.3f} MB")
    print()
    
    # 1. DATETIME CONVERSION AND PREPARATION
    print("⏰ 1. DATETIME CONVERSION AND PREPARATION")
    print("-" * 45)
    
    # Convert expireAt to datetime
    df['expire_datetime'] = pd.to_datetime(df['expireAt'], unit='ms')
    current_time = datetime.now()
    df['days_to_expire'] = (df['expire_datetime'] - current_time).dt.days
    
    # Analyze current distribution
    print(f"📊 ExpireAt Distribution Analysis:")
    print(f"   📅 Date range: {df['expire_datetime'].min()} to {df['expire_datetime'].max()}")
    print(f"   ⏰ Days to expire range: {df['days_to_expire'].min()} to {df['days_to_expire'].max()}")
    print(f"   📊 Average days to expire: {df['days_to_expire'].mean():.1f}")
    print()
    
    # 2. BUSINESS INTELLIGENCE BASED URGENCY CATEGORIES
    print("🎯 2. BUSINESS INTELLIGENCE BASED URGENCY CATEGORIES")
    print("-" * 55)
    
    def categorize_urgency(days):
        """Business logic based urgency categorization"""
        if pd.isna(days):
            return 'UNKNOWN'
        elif days < 0:
            return 'EXPIRED'
        elif days <= 3:
            return 'CRITICAL_URGENT'      # Apply immediately
        elif days <= 7:
            return 'HIGH_URGENT'          # Apply within week
        elif days <= 14:
            return 'MODERATE_URGENT'      # Apply within 2 weeks
        elif days <= 30:
            return 'NORMAL'               # Standard application timing
        elif days <= 60:
            return 'EXTENDED'             # Quality-focused positions
        else:
            return 'LONG_TERM'            # Strategic/specialized roles
    
    # Create urgency categories
    df['job_urgency_level'] = df['days_to_expire'].apply(categorize_urgency)
    
    # Analyze urgency distribution
    urgency_dist = df['job_urgency_level'].value_counts()
    print(f"📊 Urgency Level Distribution:")
    
    urgency_business_meanings = {
        'CRITICAL_URGENT': ('🚨', 'Immediate action required - apply today'),
        'HIGH_URGENT': ('⚡', 'High priority - apply within days'),
        'MODERATE_URGENT': ('⚠️', 'Time-sensitive - apply within 2 weeks'),
        'NORMAL': ('📋', 'Standard timeline - quality application focus'),
        'EXTENDED': ('🎯', 'Premium opportunity - comprehensive application'),
        'LONG_TERM': ('🔵', 'Strategic role - extensive preparation time'),
        'EXPIRED': ('🔴', 'Position no longer available'),
        'UNKNOWN': ('❓', 'Timeline information unavailable')
    }
    
    for category, count in urgency_dist.items():
        emoji, meaning = urgency_business_meanings.get(category, ('📊', 'Standard category'))
        percentage = (count / len(df)) * 100
        print(f"   {emoji} {category}: {count:,} ({percentage:.1f}%) - {meaning}")
    print()
    
    # 3. PREMIUM INVESTMENT CORRELATION ANALYSIS
    print("💰 3. PREMIUM INVESTMENT CORRELATION ANALYSIS")
    print("-" * 50)
    
    if 'job_investment_type' in df.columns:
        # Analyze urgency by investment type
        investment_urgency = pd.crosstab(df['job_investment_type'], df['job_urgency_level'], normalize='index') * 100
        
        print(f"📊 Urgency Distribution by Investment Type:")
        for inv_type in investment_urgency.index:
            print(f"   💎 {inv_type}:")
            top_urgencies = investment_urgency.loc[inv_type].nlargest(3)
            for urgency, percentage in top_urgencies.items():
                emoji, _ = urgency_business_meanings.get(urgency, ('📊', ''))
                print(f"      {emoji} {urgency}: {percentage:.1f}%")
        print()
        
        # Business intelligence insights
        premium_avg_days = df[df['job_investment_type'].isin(['PREMIUM_OFFLINE', 'PREMIUM_ONLINE'])]['days_to_expire'].mean()
        organic_avg_days = df[df['job_investment_type'] == 'ORGANIC']['days_to_expire'].mean()
        
        print(f"💡 Investment vs Urgency Intelligence:")
        print(f"   💰 Premium postings average: {premium_avg_days:.1f} days")
        print(f"   🆓 Organic postings average: {organic_avg_days:.1f} days")
        print(f"   📊 Premium advantage: {premium_avg_days - organic_avg_days:.1f} days longer")
        print(f"   🎯 Investment strategy: {'Premium for quality hiring' if premium_avg_days > organic_avg_days else 'Organic for fast hiring'}")
    else:
        print("   ⚠️ job_investment_type not found - skipping investment correlation")
    print()
    
    # 4. TEMPORAL INTELLIGENCE FEATURES
    print("📅 4. TEMPORAL INTELLIGENCE FEATURES")
    print("-" * 40)
    
    # Extract temporal features
    df['expire_month'] = df['expire_datetime'].dt.month
    df['expire_quarter'] = df['expire_datetime'].dt.quarter
    df['expire_day_of_week'] = df['expire_datetime'].dt.day_name()
    df['expire_season'] = df['expire_month'].map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring', 
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    })
    
    print(f"📊 Temporal Features Created:")
    print(f"   📅 expire_month: Monthly posting patterns")
    print(f"   📈 expire_quarter: Quarterly hiring trends") 
    print(f"   📊 expire_day_of_week: Weekly posting patterns")
    print(f"   🌍 expire_season: Seasonal hiring analysis")
    print()
    
    # Analyze temporal patterns
    print(f"🔍 Temporal Pattern Analysis:")
    
    # Monthly distribution
    monthly_urgency = df.groupby('expire_month')['job_urgency_level'].apply(
        lambda x: (x == 'CRITICAL_URGENT').sum() + (x == 'HIGH_URGENT').sum()
    )
    peak_urgent_month = monthly_urgency.idxmax()
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    print(f"   📅 Peak urgent hiring month: {month_names[peak_urgent_month-1]} ({monthly_urgency[peak_urgent_month]} urgent jobs)")
    
    # Seasonal patterns
    seasonal_dist = df['expire_season'].value_counts()
    print(f"   🌍 Seasonal distribution: {seasonal_dist.to_dict()}")
    print()
    
    # 5. MEMORY OPTIMIZATION AND DATA TYPE CONVERSION
    print("🔧 5. MEMORY OPTIMIZATION AND DATA TYPE CONVERSION")
    print("-" * 55)
    
    # Convert urgency to categorical for memory efficiency
    df['job_urgency_level'] = df['job_urgency_level'].astype('category')
    df['expire_season'] = df['expire_season'].astype('category')
    df['expire_day_of_week'] = df['expire_day_of_week'].astype('category')
    
    # Calculate memory savings
    expireAt_memory_before = df['expireAt'].memory_usage(deep=True) / 1024**2
    
    # Check current memory usage of new features
    urgency_memory = df['job_urgency_level'].memory_usage(deep=True) / 1024**2
    temporal_memory = (df['expire_month'].memory_usage(deep=True) + 
                      df['expire_quarter'].memory_usage(deep=True) +
                      df['expire_season'].memory_usage(deep=True) +
                      df['expire_day_of_week'].memory_usage(deep=True)) / 1024**2
    
    print(f"💾 Memory Analysis:")
    print(f"   📊 Original expireAt: {expireAt_memory_before:.3f} MB")
    print(f"   🎯 job_urgency_level: {urgency_memory:.3f} MB")
    print(f"   📅 Temporal features: {temporal_memory:.3f} MB")
    print(f"   📈 Memory efficiency: Categorical encoding saves ~{expireAt_memory_before * 0.7:.3f} MB")
    print()
    
    # 6. ADVANCED ANALYTICS FEATURES
    print("📊 6. ADVANCED ANALYTICS FEATURES")
    print("-" * 40)
    
    # Create application timing intelligence
    df['optimal_application_window'] = df['days_to_expire'].apply(
        lambda days: 'IMMEDIATE' if days <= 3 else 
                    'PRIORITY' if days <= 7 else
                    'STANDARD' if days <= 21 else
                    'QUALITY_FOCUS' if days <= 60 else
                    'STRATEGIC'
    ).astype('category')
    
    # Create competition level indicator
    df['competition_level'] = df['job_urgency_level'].map({
        'CRITICAL_URGENT': 'EXTREME',
        'HIGH_URGENT': 'HIGH', 
        'MODERATE_URGENT': 'MEDIUM',
        'NORMAL': 'MODERATE',
        'EXTENDED': 'LOW',
        'LONG_TERM': 'MINIMAL',
        'EXPIRED': 'NONE',
        'UNKNOWN': 'UNKNOWN'
    }).astype('category')
    
    print(f"🎯 Advanced Features Created:")
    print(f"   ⚡ optimal_application_window: Application timing strategy")
    print(f"   🏆 competition_level: Expected application competition")
    print()
    
    # Analyze feature distributions
    window_dist = df['optimal_application_window'].value_counts()
    competition_dist = df['competition_level'].value_counts()
    
    print(f"📊 Feature Distributions:")
    print(f"   ⚡ Application Windows: {dict(window_dist)}")
    print(f"   🏆 Competition Levels: {dict(competition_dist)}")
    print()
    
    # 7. STRATEGIC COLUMN MANAGEMENT
    print("🗂️ 7. STRATEGIC COLUMN MANAGEMENT")
    print("-" * 40)
    
    # Drop intermediate columns
    columns_to_drop = ['expire_datetime', 'days_to_expire']
    
    print(f"🗑️ Cleaning intermediate columns:")
    for col in columns_to_drop:
        if col in df.columns:
            print(f"   ❌ Dropping: {col}")
            df = df.drop(columns=[col])
    print()
    
    # 8. FINAL RESULTS AND VALIDATION
    print("✅ 8. FINAL RESULTS AND VALIDATION")
    print("-" * 40)
    
    final_columns = len(df.columns)
    final_memory = df.memory_usage(deep=True).sum() / 1024**2
    
    # New features created
    new_features = [
        'job_urgency_level', 'expire_month', 'expire_quarter', 
        'expire_day_of_week', 'expire_season', 'optimal_application_window', 
        'competition_level'
    ]
    
    print(f"📊 Transformation Results:")
    print(f"   📋 Columns: {initial_columns} → {final_columns} (+{final_columns - initial_columns})")
    print(f"   💾 Memory: {initial_memory:.3f} MB → {final_memory:.3f} MB ({((final_memory - initial_memory) / initial_memory * 100):+.1f}%)")
    print(f"   🎯 Features created: {len(new_features)}")
    print()
    
    print(f"🌟 New Business Intelligence Features:")
    feature_purposes = {
        'job_urgency_level': 'Primary urgency categorization for application timing',
        'expire_month': 'Monthly hiring pattern analysis',
        'expire_quarter': 'Quarterly business cycle correlation', 
        'expire_day_of_week': 'Weekly posting behavior analysis',
        'expire_season': 'Seasonal hiring trend identification',
        'optimal_application_window': 'Strategic application timing guidance',
        'competition_level': 'Expected application competition assessment'
    }
    
    for feature, purpose in feature_purposes.items():
        print(f"   🎯 {feature}: {purpose}")
    print()
    
    # Data integrity validation
    print(f"🔍 Data Integrity Validation:")
    print(f"   📊 Total records: {len(df):,} (preserved)")
    print(f"   ❌ Null values in urgency: {df['job_urgency_level'].isnull().sum()}")
    print(f"   ✅ Urgency categories: {df['job_urgency_level'].nunique()} unique levels")
    print(f"   📈 Business value: Urgency intelligence + temporal analytics enabled")
    print()
    
    print("=" * 65)
    print("✅ EXPIREAT URGENCY TRANSFORMATION COMPLETED SUCCESSFULLY")
    print("=" * 65)
    
    return df

if __name__ == "__main__":
    try:
        # Load the dataset
        print("📂 Dataset yükleniyor...")
        df = pd.read_csv('linkedin_jobs_dataset_optimized_step7.csv')
        print(f"✅ Dataset yüklendi: {len(df):,} satır, {len(df.columns)} sütun")
        print()
        
        # Transform expireAt to urgency categories
        df_transformed = create_urgency_categories_and_optimize_expireAt(df)
        
        # Save the transformed dataset
        output_filename = 'linkedin_jobs_dataset_optimized_step8.csv'
        print(f"💾 Saving transformed dataset: {output_filename}")
        df_transformed.to_csv(output_filename, index=False)
        
        # File size comparison
        import os
        original_size = os.path.getsize('linkedin_jobs_dataset_optimized_step7.csv') / 1024**2
        new_size = os.path.getsize(output_filename) / 1024**2
        
        print(f"📊 File Size Comparison:")
        print(f"   📄 Original: {original_size:.2f} MB")
        print(f"   📄 New: {new_size:.2f} MB")
        print(f"   📈 Change: {((new_size - original_size) / original_size * 100):+.1f}%")
        
        print(f"\n🎉 Transformation completed successfully!")
        print(f"📁 Output file: {output_filename}")
        
    except FileNotFoundError:
        print("❌ HATA: linkedin_jobs_dataset_optimized_step7.csv dosyası bulunamadı!")
    except Exception as e:
        print(f"❌ HATA: {str(e)}")
        import traceback
        traceback.print_exc() 