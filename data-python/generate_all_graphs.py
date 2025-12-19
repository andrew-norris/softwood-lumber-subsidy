#!/usr/bin/env python3
"""
Script to generate all graphs for the economics paper.
Runs all individual graph scripts and reports any errors.
"""

import subprocess
import sys
import os

def run_script(script_path, script_name):
    """Run a Python script and capture output."""
    try:
        print(f"\n{'='*50}")
        print(f"Running: {script_name}")
        print(f"{'='*50}")
        
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.getcwd())
        
        if result.returncode == 0:
            print(f"✓ SUCCESS: {script_name}")
            if result.stdout.strip():
                print("Output:")
                print(result.stdout)
        else:
            print(f"✗ ERROR: {script_name}")
            print("Error output:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"✗ EXCEPTION: {script_name} - {str(e)}")
        return False
    
    return True

def main():
    """Generate all graphs for the economics paper."""
    
    print("Starting graph generation for economics paper...")
    print(f"Working directory: {os.getcwd()}")
    
    # List of all graph scripts to run
    scripts = [
        ("employment/employment.py", "Employment Graph"),
        ("exports/export_share_piechart.py", "Export Share Pie Chart"),
        ("exports/export_value_graph.py", "Export Value Graph"),
        ("exports/housing_exports_comparison.py", "Housing vs Exports Comparison"),
        ("gdp/forestry_gdp.py", "Forestry GDP Graph"),
        ("gdp/industry_comparison.py", "Industry Comparison Graph"),
        ("lumber-output/lumber_output_graph.py", "Lumber Output Graph"),
        ("lumber-output/productivity_analysis.py", "Productivity Analysis Graph"),
        ("prices/lumber_price_graph.py", "Lumber Price Graph"),
        ("prices/material_comparison.py", "Material Comparison Graph"),
        ("sawmill-revenue/sawmill_revenue_graph.py", "Sawmill Revenue Graph"),
        ("tariffs/tariff_timeline.py", "Tariff Timeline Graph"),
        ("canada-housing-starts/housing_starts_graph.py", "Canadian Housing Starts Graph")
    ]
    
    # Track results
    successful = []
    failed = []
    
    # Run each script
    for script_path, script_name in scripts:
        if run_script(script_path, script_name):
            successful.append(script_name)
        else:
            failed.append(script_name)
    
    # Print summary
    print(f"\n{'='*60}")
    print("GRAPH GENERATION SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n✓ SUCCESSFUL ({len(successful)}/{len(scripts)}):")
    for name in successful:
        print(f"  - {name}")
    
    if failed:
        print(f"\n✗ FAILED ({len(failed)}/{len(scripts)}):")
        for name in failed:
            print(f"  - {name}")
    
    print(f"\nAll generated images saved to: ../images/")
    
    if len(successful) == len(scripts):
        print("\n🎉 All graphs generated successfully!")
    else:
        print(f"\n⚠️  {len(failed)} graph(s) had errors.")

if __name__ == "__main__":
    main()