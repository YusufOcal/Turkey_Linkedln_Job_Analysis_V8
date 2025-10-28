#!/usr/bin/env python3
"""
Extract All Column Operations (44-55): Tüm raporldaki sütun işlemlerini topla

44-55 arasındaki tüm raporlarda:
1. Silinen sütunlar
2. Üretilen sütunlar  
3. Dönüştürülen sütunlar
"""

import os
import re
from collections import defaultdict

def extract_all_column_operations():
    """44-55 arası tüm column operations'ları extract et"""
    
    print("🔍 COMPREHENSIVE COLUMN OPERATIONS EXTRACTOR (Projects 44-55)")
    print("=" * 80)
    
    # Rapor dosyalarını listele
    reports = []
    for i in range(44, 56):  # 44-55 dahil
        report_files = [f for f in os.listdir('.') if f.startswith(f"{i}_") and f.endswith('.md')]
        if report_files:
            reports.extend(report_files)
    
    print(f"📁 Found {len(reports)} report files:")
    for report in sorted(reports):
        print(f"   📄 {report}")
    print()
    
    # Operations storage
    operations = {
        'deleted_columns': [],
        'created_columns': [],
        'transformed_columns': [],
        'renamed_columns': []
    }
    
    operation_sources = defaultdict(list)
    
    # Her raporu analiz et
    for report_file in sorted(reports):
        print(f"🔍 Analyzing: {report_file}")
        
        try:
            with open(report_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            project_num = report_file.split('_')[0]
            
            # DELETED COLUMNS tespit et
            deleted_patterns = [
                r"deleted?\s*columns?\s*:?\s*([^\n]+)",
                r"eliminated?\s*columns?\s*:?\s*([^\n]+)",  
                r"removed?\s*columns?\s*:?\s*([^\n]+)",
                r"drop\s*columns?\s*:?\s*([^\n]+)",
                r"DELETE.*?columns?\s*:?\s*([^\n]+)",
                r"`([^`]+)`.*?(?:deleted|eliminated|removed)",
                r"Target columns?\s*:?\s*`([^`]+)`.*?(?:deletion|elimination)",
                r"Columns?\s*(?:to be )?(deleted|eliminated|removed)\s*:?\s*([^\n]+)",
                r"merged_companyDescription",
                r"company/followingState/followingType",
                r"company/followingState/preDashFollowingInfoUrn",
                r"company/industry/0",
                r"jobApplicantInsights/entityUrn",
                r"workRemoteAllowed",
                r"link",
                r"contentSource"
            ]
            
            for pattern in deleted_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[-1]  # Son grubu al
                    
                    # Clean up the match
                    cleaned = re.sub(r'[^\w/\-\|,\s]', '', str(match))
                    
                    # Split multiple columns
                    if ',' in cleaned or '|' in cleaned:
                        cols = re.split(r'[,|]', cleaned)
                        for col in cols:
                            col = col.strip()
                            if col and len(col) > 2:
                                operations['deleted_columns'].append(col)
                                operation_sources['deleted'].append((project_num, report_file, col))
                    else:
                        cleaned = cleaned.strip()
                        if cleaned and len(cleaned) > 2:
                            operations['deleted_columns'].append(cleaned)
                            operation_sources['deleted'].append((project_num, report_file, cleaned))
            
            # CREATED COLUMNS tespit et
            created_patterns = [
                r"created?\s*columns?\s*:?\s*([^\n]+)",
                r"new\s*columns?\s*:?\s*([^\n]+)",
                r"generated?\s*columns?\s*:?\s*([^\n]+)",
                r"added?\s*columns?\s*:?\s*([^\n]+)",
                r"`([^`]+)`.*?(?:created|generated|added)",
                r"urgency_category",
                r"job_investment_category",
                r"company_has_logo",
                r"job_functions_combined"
            ]
            
            for pattern in created_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        match = match[-1]
                        
                    cleaned = re.sub(r'[^\w/\-\|,\s]', '', str(match))
                    
                    if ',' in cleaned or '|' in cleaned:
                        cols = re.split(r'[,|]', cleaned)
                        for col in cols:
                            col = col.strip()
                            if col and len(col) > 2:
                                operations['created_columns'].append(col)
                                operation_sources['created'].append((project_num, report_file, col))
                    else:
                        cleaned = cleaned.strip()
                        if cleaned and len(cleaned) > 2:
                            operations['created_columns'].append(cleaned)
                            operation_sources['created'].append((project_num, report_file, cleaned))
            
            print(f"   ✅ Analyzed successfully")
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print()
    
    # Manual addition of known operations
    print("🔧 ADDING MANUALLY CONFIRMED OPERATIONS:")
    
    # Known deletions from our analysis
    confirmed_deletions = [
        'merged_companyDescription',
        'company/followingState/followingType', 
        'company/followingState/preDashFollowingInfoUrn',
        'company/industry/0',
        'jobApplicantInsights/entityUrn',
        'workRemoteAllowed',
        'link',
        'contentSource'
    ]
    
    # Known creations from our analysis
    confirmed_creations = [
        'job_functions_combined',
        'urgency_category', 
        'job_investment_category',
        'company_has_logo'
    ]
    
    for col in confirmed_deletions:
        if col not in operations['deleted_columns']:
            operations['deleted_columns'].append(col)
            operation_sources['deleted'].append(('MANUAL', 'confirmed_from_analysis', col))
    
    for col in confirmed_creations:
        if col not in operations['created_columns']:
            operations['created_columns'].append(col)
            operation_sources['created'].append(('MANUAL', 'confirmed_from_analysis', col))
    
    print(f"   ✅ Added confirmed operations")
    print()
    
    # Remove duplicates and clean
    operations['deleted_columns'] = list(set(operations['deleted_columns']))
    operations['created_columns'] = list(set(operations['created_columns']))
    
    # RESULTS ANALYSIS
    print("📊 COMPREHENSIVE COLUMN OPERATIONS SUMMARY (Projects 44-55)")
    print("=" * 70)
    
    print(f"\n🗑️  COLUMNS TO BE DELETED ({len(operations['deleted_columns'])}):")
    print("-" * 50)
    for i, col in enumerate(sorted(operations['deleted_columns']), 1):
        sources = [s for s in operation_sources['deleted'] if s[2] == col]
        projects = list(set([s[0] for s in sources]))
        print(f"   {i:2}. {col}")
        print(f"       📍 Source projects: {projects}")
    
    print(f"\n✨ COLUMNS TO BE CREATED ({len(operations['created_columns'])}):")
    print("-" * 50)
    for i, col in enumerate(sorted(operations['created_columns']), 1):
        sources = [s for s in operation_sources['created'] if s[2] == col]
        projects = list(set([s[0] for s in sources]))
        print(f"   {i:2}. {col}")
        print(f"       📍 Source projects: {projects}")
    
    # PROJECT-WISE BREAKDOWN
    print(f"\n📋 PROJECT-WISE BREAKDOWN:")
    print("-" * 30)
    
    project_summary = defaultdict(lambda: {'deleted': [], 'created': []})
    
    for proj, file, col in operation_sources['deleted']:
        project_summary[proj]['deleted'].append(col)
    
    for proj, file, col in operation_sources['created']:
        project_summary[proj]['created'].append(col)
    
    for project in sorted(project_summary.keys()):
        deleted = list(set(project_summary[project]['deleted']))
        created = list(set(project_summary[project]['created']))
        
        print(f"\n📊 PROJECT {project}:")
        if deleted:
            print(f"   🗑️  Deleted ({len(deleted)}): {', '.join(deleted[:3])}{'...' if len(deleted) > 3 else ''}")
        if created:
            print(f"   ✨ Created ({len(created)}): {', '.join(created[:3])}{'...' if len(created) > 3 else ''}")
    
    # VALIDATION SUMMARY
    print(f"\n🎯 VALIDATION SUMMARY:")
    print("-" * 25)
    print(f"   📊 Total deletions identified: {len(operations['deleted_columns'])}")
    print(f"   📊 Total creations identified: {len(operations['created_columns'])}")
    print(f"   📊 Net column change: {len(operations['created_columns']) - len(operations['deleted_columns'])}")
    print(f"   📊 Source reports analyzed: {len(reports)}")
    
    return operations, operation_sources

if __name__ == "__main__":
    ops, sources = extract_all_column_operations() 