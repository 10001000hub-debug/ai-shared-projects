#!/usr/bin/env python3
"""
Orchestrator CLI for Affiliate AI Quality Assessment
Processes affiliate content through evaluation pipeline
"""

import json
import argparse
import sys
from datetime import datetime
from pathlib import Path
import jsonschema
from typing import Dict, Any, List

def load_schema(schema_path: Path) -> Dict[str, Any]:
    """Load JSON schema from file"""
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading schema {schema_path}: {e}", file=sys.stderr)
        sys.exit(1)

def validate_input(data: Dict[str, Any], schema: Dict[str, Any]) -> bool:
    """Validate input data against schema"""
    try:
        jsonschema.validate(instance=data, schema=schema)
        return True
    except jsonschema.ValidationError as e:
        print(f"Input validation error: {e.message}", file=sys.stderr)
        return False

def create_audit_id() -> str:
    """Generate unique audit ID"""
    return f"audit_{datetime.now().strftime('%Y%m%d%H%M%S')}"

def mock_evaluate_content(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """Mock content evaluation (placeholder for actual AI evaluation)"""
    # This would be replaced with actual AI model calls
    content_length = len(input_data.get('content', {}).get('body', ''))
    asp_links_count = len(input_data.get('asp_links', []))
    
    # Simple mock scoring based on content length and link count
    base_score = min(80, content_length // 20)  # Max 80 from content length
    link_score = min(20, asp_links_count * 5)   # Max 20 from links
    total_score = base_score + link_score
    
    # Determine grade
    if total_score >= 114:
        grade = "ELITE"
    elif total_score >= 100:
        grade = "EXCELLENT" 
    elif total_score >= 80:
        grade = "GOOD"
    elif total_score >= 60:
        grade = "FAIR"
    else:
        grade = "POOR"
    
    return {
        "audit_id": create_audit_id(),
        "timestamp": datetime.now().isoformat(),
        "overall_score": {
            "total": total_score,
            "grade": grade,
            "auto_publish_eligible": total_score >= 114
        },
        "detailed_scores": {
            "seo_optimization": min(15, total_score // 8),
            "content_quality": min(20, content_length // 50),
            "affiliate_integration": min(20, asp_links_count * 4),
            "link_validity": min(15, asp_links_count * 3),
            "user_value": min(20, content_length // 40),
            "compliance": 8,  # Mock compliance score
            "conversion_potential": min(15, asp_links_count * 3),
            "technical_quality": 4  # Mock technical score
        },
        "improvements": [
            {
                "category": "seo",
                "severity": "minor",
                "description": "Consider adding more targeted keywords",
                "impact_points": 3
            }
        ],
        "link_validation_results": [
            {
                "original_url": link["url"],
                "status": "valid",
                "redirect_count": 0,
                "response_time_ms": 250
            } for link in input_data.get('asp_links', [])
        ],
        "metadata": {
            "evaluator_version": "1.0.0",
            "processing_time_seconds": 1.2,
            "ai_model_used": "mock-evaluator",
            "content_length": content_length
        }
    }

def main():
    parser = argparse.ArgumentParser(description="Affiliate Content Quality Orchestrator")
    parser.add_argument('--input', '-i', required=True, help='Input JSON file path')
    parser.add_argument('--output', '-o', help='Output JSON file path (default: stdout)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--validate-only', action='store_true', help='Only validate input, do not evaluate')
    
    args = parser.parse_args()
    
    # Determine schema paths (relative to script location)
    script_dir = Path(__file__).parent.parent.parent
    input_schema_path = script_dir / "docs" / "audit_input_schema.json"
    output_schema_path = script_dir / "docs" / "audit_output_schema.json"
    
    if args.verbose:
        print(f"Loading input schema from: {input_schema_path}", file=sys.stderr)
        print(f"Loading output schema from: {output_schema_path}", file=sys.stderr)
    
    # Load schemas
    input_schema = load_schema(input_schema_path)
    output_schema = load_schema(output_schema_path)
    
    # Load and validate input
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading input file: {e}", file=sys.stderr)
        sys.exit(1)
    
    if not validate_input(input_data, input_schema):
        sys.exit(1)
        
    if args.verbose:
        print("Input validation passed", file=sys.stderr)
    
    if args.validate_only:
        print("Validation complete - input is valid")
        return
    
    # Process content evaluation
    if args.verbose:
        print("Starting content evaluation...", file=sys.stderr)
    
    result = mock_evaluate_content(input_data)
    
    # Validate output against schema
    try:
        jsonschema.validate(instance=result, schema=output_schema)
        if args.verbose:
            print("Output validation passed", file=sys.stderr)
    except jsonschema.ValidationError as e:
        print(f"Output validation error: {e.message}", file=sys.stderr)
        sys.exit(1)
    
    # Output result
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        if args.verbose:
            print(f"Results written to: {args.output}", file=sys.stderr)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()