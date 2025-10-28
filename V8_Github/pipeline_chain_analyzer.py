#!/usr/bin/env python3
"""
Pipeline Chain Analyzer: Mevcut script'lerin input/output chain'ini tespit et

Tüm .py dosyalarında:
1. Input CSV dosya ismini bul
2. Output CSV dosya ismini bul  
3. Doğru chain sırasını belirle
"""

import os
import re
from pathlib import Path

def analyze_pipeline_chain():
    """Pipeline chain analizi"""
    
    print("🔍 PIPELINE CHAIN ANALYZER")
    print("=" * 60)
    
    # Workspace'deki tüm .py dosyalarını bul
    py_files = [f for f in os.listdir('.') if f.endswith('.py')]
    py_files = [f for f in py_files if not f.startswith('check_') and not f.startswith('pipeline_')]
    
    print(f"📁 Found {len(py_files)} Python scripts to analyze")
    print()
    
    script_chains = []
    
    for py_file in py_files:
        print(f"🔍 Analyzing: {py_file}")
        
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Input dosyası tespit et (pd.read_csv patterns)
            input_matches = re.findall(r"pd\.read_csv\(['\"]([^'\"]+\.csv)['\"]", content)
            
            # Output dosyası tespit et (.to_csv patterns)  
            output_matches = re.findall(r"\.to_csv\(['\"]([^'\"]+\.csv)['\"]", content)
            
            # Variable assignment patterns de kontrol et
            input_file_matches = re.findall(r"input_file\s*=\s*['\"]([^'\"]+\.csv)['\"]", content)
            output_file_matches = re.findall(r"output_file\s*=\s*['\"]([^'\"]+\.csv)['\"]", content)
            
            # Tüm input'ları birleştir
            all_inputs = list(set(input_matches + input_file_matches))
            all_outputs = list(set(output_matches + output_file_matches))
            
            script_info = {
                'script': py_file,
                'inputs': all_inputs,
                'outputs': all_outputs,
                'content_length': len(content.split('\n'))
            }
            
            script_chains.append(script_info)
            
            print(f"   📥 Inputs: {all_inputs}")
            print(f"   📤 Outputs: {all_outputs}")
            print()
            
        except Exception as e:
            print(f"   ❌ Error reading {py_file}: {e}")
            print()
    
    # Chain analizi
    print("🔗 CHAIN ANALYSIS")
    print("=" * 40)
    
    # Tüm CSV dosyalarını listele
    all_csv_files = set()
    for script in script_chains:
        all_csv_files.update(script['inputs'])
        all_csv_files.update(script['outputs'])
    
    print(f"📋 Total unique CSV files in pipeline: {len(all_csv_files)}")
    for csv_file in sorted(all_csv_files):
        print(f"   📄 {csv_file}")
    print()
    
    # Chain bağlantılarını tespit et
    print("🔗 CHAIN CONNECTIONS")
    print("-" * 30)
    
    for script in script_chains:
        print(f"📜 {script['script']}:")
        
        if script['inputs']:
            for inp in script['inputs']:
                # Bu input hangi script'in output'u?
                producers = [s['script'] for s in script_chains if inp in s['outputs']]
                if producers:
                    print(f"   📥 INPUT: {inp} ← produced by: {producers}")
                else:
                    # Bu original dataset mi?
                    if 'insights_completed' in inp or 'original' in inp:
                        print(f"   📥 INPUT: {inp} ← ORIGINAL DATASET")
                    else:
                        print(f"   📥 INPUT: {inp} ← ⚠️ ORPHANED (no producer found)")
        
        if script['outputs']:
            for out in script['outputs']:
                # Bu output hangi script'in input'u?
                consumers = [s['script'] for s in script_chains if out in s['inputs']]
                if consumers:
                    print(f"   📤 OUTPUT: {out} → consumed by: {consumers}")
                else:
                    print(f"   📤 OUTPUT: {out} → ⚠️ TERMINAL (no consumer)")
        print()
    
    # Broken chains tespit et
    print("💔 BROKEN CHAIN DETECTION")
    print("-" * 30)
    
    broken_chains = []
    
    for script in script_chains:
        for inp in script['inputs']:
            producers = [s for s in script_chains if inp in s['outputs']]
            if not producers and 'insights_completed' not in inp:
                broken_chains.append({
                    'script': script['script'],
                    'missing_input': inp,
                    'type': 'missing_producer'
                })
    
    if broken_chains:
        print("🚨 BROKEN CHAINS DETECTED:")
        for broken in broken_chains:
            print(f"   ❌ {broken['script']} expects {broken['missing_input']} but no script produces it")
    else:
        print("✅ No broken chains detected")
    
    print()
    
    # Ideal chain reconstruction
    print("🎯 IDEAL CHAIN RECONSTRUCTION")
    print("-" * 35)
    
    print("📋 Recommended Pipeline Order:")
    
    # Script'leri logical order'a koy
    logical_order = [
        'step1_job_functions_consolidation_corrected.py',
        'delete_redundant_entityUrn.py', 
        'delete_workRemoteAllowed.py',
        'delete_link_column.py',
        'create_job_investment_category_and_delete_contentSource.py',
        'convert_expireAt_and_create_urgency.py',
        'convert_logo_to_boolean.py'
    ]
    
    for i, script_name in enumerate(logical_order, 1):
        # Bu script mevcut mu?
        if script_name in [s['script'] for s in script_chains]:
            script_info = next(s for s in script_chains if s['script'] == script_name)
            current_inputs = script_info['inputs']
            current_outputs = script_info['outputs']
            
            print(f"{i}. {script_name}")
            print(f"   Current INPUT: {current_inputs}")
            print(f"   Current OUTPUT: {current_outputs}")
            
            # Önerilen input/output
            if i == 1:
                recommended_input = 'linkedin_jobs_dataset_insights_completed.csv'
                recommended_output = 'linkedin_jobs_after_step1_job_functions.csv'
            else:
                prev_script = logical_order[i-2]
                prev_script_info = next((s for s in script_chains if s['script'] == prev_script), None)
                if prev_script_info and prev_script_info['outputs']:
                    recommended_input = prev_script_info['outputs'][0]
                else:
                    recommended_input = f'linkedin_jobs_after_step{i-1}.csv'
                recommended_output = f'linkedin_jobs_after_step{i}.csv'
            
            print(f"   SHOULD BE INPUT: {recommended_input}")
            print(f"   SHOULD BE OUTPUT: {recommended_output}")
            
            needs_fix = (current_inputs != [recommended_input] or 
                        current_outputs != [recommended_output])
            print(f"   NEEDS FIX: {'🚨 YES' if needs_fix else '✅ NO'}")
            print()
        else:
            print(f"{i}. {script_name} - ❌ NOT FOUND")
            print()
    
    return script_chains

if __name__ == "__main__":
    chains = analyze_pipeline_chain() 