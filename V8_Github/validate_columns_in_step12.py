#!/usr/bin/env python3
"""
Column Operations Validator for linkedin_jobs_dataset_optimized_step12.csv

44-55 arası projelerde komut verilen tüm sütun işlemlerinin
linkedin_jobs_dataset_optimized_step12.csv'de uygulanıp uygulanmadığını kontrol et.
"""

import pandas as pd

def validate_column_operations_in_step12():
    """Step12 dataset'te column operations validation"""
    
    print("🔍 COLUMN OPERATIONS VALIDATOR FOR STEP12 DATASET")
    print("=" * 65)
    
    target_file = 'linkedin_jobs_dataset_optimized_step12.csv'
    
    try:
        print(f"📂 Loading target dataset: {target_file}")
        df = pd.read_csv(target_file)
        print(f"✅ Dataset loaded: {len(df):,} records, {len(df.columns)} columns")
        print()
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return
    
    current_columns = set(df.columns)
    
    # 44-55 arası projelerde verilen komutlar
    operations = {
        'should_be_deleted': [
            'merged_companyDescription',                    # Proje 45
            'company/followingState/followingType',         # Proje 45  
            'company/followingState/preDashFollowingInfoUrn', # Proje 46
            'company/industry/0',                           # Proje 47
            'jobApplicantInsights/entityUrn',               # Proje 53
            'workRemoteAllowed',                            # Proje 54
            'link',                                         # Proje 55
            'contentSource'                                 # Proje 50
        ],
        'should_be_created': [
            'job_functions_combined',       # Proje 52 - 6 job function sütunundan
            'urgency_category',             # Proje 51 - expireAt'tan urgency
            'job_investment_category',      # Proje 50 - contentSource'dan business kategori  
            'company_has_logo'              # Proje 48 - logo URL'den boolean
        ]
    }
    
    print("🔍 DELETION COMMANDS VALIDATION")
    print("=" * 40)
    print("Checking if commanded deletions were properly executed...")
    print()
    
    deletion_results = {
        'properly_deleted': [],
        'still_exists': [],
        'never_existed': []
    }
    
    for i, col in enumerate(operations['should_be_deleted'], 1):
        if col in current_columns:
            deletion_results['still_exists'].append(col)
            status = "🚨 STILL EXISTS (NOT DELETED)"
        else:
            deletion_results['properly_deleted'].append(col)
            status = "✅ PROPERLY DELETED"
        
        print(f"   {i:2}. {col}")
        print(f"       Status: {status}")
        print()
    
    print("✨ CREATION COMMANDS VALIDATION")
    print("=" * 40)
    print("Checking if commanded creations were properly executed...")
    print()
    
    creation_results = {
        'properly_created': [],
        'missing': [],
        'already_existed': []
    }
    
    for i, col in enumerate(operations['should_be_created'], 1):
        if col in current_columns:
            creation_results['properly_created'].append(col)
            status = "✅ PROPERLY CREATED"
        else:
            creation_results['missing'].append(col)
            status = "🚨 MISSING (NOT CREATED)"
        
        print(f"   {i:2}. {col}")
        print(f"       Status: {status}")
        print()
    
    # SUMMARY ANALYSIS
    print("📊 COMPREHENSIVE VALIDATION SUMMARY")
    print("=" * 45)
    
    total_deletions = len(operations['should_be_deleted'])
    successful_deletions = len(deletion_results['properly_deleted'])
    failed_deletions = len(deletion_results['still_exists'])
    
    total_creations = len(operations['should_be_created'])
    successful_creations = len(creation_results['properly_created'])
    failed_creations = len(creation_results['missing'])
    
    print(f"\n🗑️  DELETION COMMANDS ANALYSIS:")
    print(f"   • Total deletion commands (Projects 44-55): {total_deletions}")
    print(f"   • Successfully executed: {successful_deletions} ({(successful_deletions/total_deletions*100):.1f}%)")
    print(f"   • Failed (still exist): {failed_deletions} ({(failed_deletions/total_deletions*100):.1f}%)")
    
    if deletion_results['still_exists']:
        print(f"\n   ❌ COLUMNS THAT SHOULD BE DELETED BUT STILL EXIST:")
        for col in deletion_results['still_exists']:
            print(f"      • {col}")
    
    print(f"\n✨ CREATION COMMANDS ANALYSIS:")
    print(f"   • Total creation commands (Projects 44-55): {total_creations}")
    print(f"   • Successfully executed: {successful_creations} ({(successful_creations/total_creations*100):.1f}%)")
    print(f"   • Failed (missing): {failed_creations} ({(failed_creations/total_creations*100):.1f}%)")
    
    if creation_results['missing']:
        print(f"\n   ❌ COLUMNS THAT SHOULD BE CREATED BUT ARE MISSING:")
        for col in creation_results['missing']:
            print(f"      • {col}")
    
    # OVERALL COMPLIANCE SCORE
    total_commands = total_deletions + total_creations
    successful_commands = successful_deletions + successful_creations
    compliance_rate = (successful_commands / total_commands) * 100
    
    print(f"\n🎯 OVERALL COMPLIANCE ANALYSIS:")
    print(f"   • Total commands issued (Projects 44-55): {total_commands}")
    print(f"   • Successfully executed: {successful_commands}")
    print(f"   • Failed commands: {total_commands - successful_commands}")
    print(f"   • Compliance rate: {compliance_rate:.1f}%")
    
    if compliance_rate == 100.0:
        print(f"   🎉 PERFECT COMPLIANCE! All commands executed correctly.")
    elif compliance_rate >= 75.0:
        print(f"   ⚠️  GOOD COMPLIANCE but some issues need attention.")
    else:
        print(f"   🚨 LOW COMPLIANCE - Major issues detected!")
    
    # DATASET CURRENT STATE
    print(f"\n📋 DATASET CURRENT STATE:")
    print(f"   • Total columns in step12: {len(current_columns)}")
    print(f"   • Records: {len(df):,}")
    
    # Memory usage
    memory_usage = df.memory_usage(deep=True).sum() / (1024*1024)
    print(f"   • Memory usage: {memory_usage:.2f} MB")
    
    # PROJECT-SPECIFIC BREAKDOWN
    print(f"\n📊 PROJECT-SPECIFIC VALIDATION:")
    print("-" * 35)
    
    project_mapping = {
        'merged_companyDescription': 'Project 45',
        'company/followingState/followingType': 'Project 45',
        'company/followingState/preDashFollowingInfoUrn': 'Project 46', 
        'company/industry/0': 'Project 47',
        'contentSource': 'Project 50',
        'urgency_category': 'Project 51',
        'job_functions_combined': 'Project 52',
        'jobApplicantInsights/entityUrn': 'Project 53',
        'workRemoteAllowed': 'Project 54',
        'link': 'Project 55',
        'company_has_logo': 'Project 48',
        'job_investment_category': 'Project 50'
    }
    
    project_scores = {}
    for col, project in project_mapping.items():
        if project not in project_scores:
            project_scores[project] = {'total': 0, 'success': 0}
        
        project_scores[project]['total'] += 1
        
        # Check if command was executed correctly
        if col in operations['should_be_deleted']:
            if col not in current_columns:  # Should be deleted and is deleted
                project_scores[project]['success'] += 1
        elif col in operations['should_be_created']:
            if col in current_columns:  # Should be created and is created
                project_scores[project]['success'] += 1
    
    for project in sorted(project_scores.keys()):
        total = project_scores[project]['total']
        success = project_scores[project]['success']
        score = (success / total) * 100
        
        print(f"   📊 {project}: {success}/{total} commands executed ({score:.0f}%)")
    
    # NEXT STEPS RECOMMENDATION
    print(f"\n🛣️  NEXT STEPS RECOMMENDATION:")
    print("-" * 35)
    
    issues_found = len(deletion_results['still_exists']) + len(creation_results['missing'])
    
    if issues_found == 0:
        print(f"✅ NO ISSUES FOUND! Step12 dataset perfectly complies with all commands.")
        print(f"🎯 Dataset is ready for production use.")
    else:
        print(f"❌ {issues_found} ISSUES DETECTED requiring immediate attention:")
        
        if deletion_results['still_exists']:
            print(f"\n1. DELETE these {len(deletion_results['still_exists'])} remaining columns:")
            for col in deletion_results['still_exists']:
                print(f"   - {col}")
        
        if creation_results['missing']:
            print(f"\n2. CREATE these {len(creation_results['missing'])} missing columns:")
            for col in creation_results['missing']:
                print(f"   - {col}")
        
        print(f"\n🔧 Recommended action: Execute corrective pipeline to address {issues_found} remaining issues.")
    
    return {
        'compliance_rate': compliance_rate,
        'deletion_results': deletion_results,
        'creation_results': creation_results,
        'issues_count': issues_found,
        'current_columns': len(current_columns)
    }

if __name__ == "__main__":
    results = validate_column_operations_in_step12() 