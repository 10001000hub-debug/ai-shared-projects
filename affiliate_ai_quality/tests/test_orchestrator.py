#!/usr/bin/env python3
"""
Tests for Orchestrator CLI
"""

import pytest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, mock_open
import sys
import os

# Add the src directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from orchestrator import (
    load_schema, 
    validate_input, 
    create_audit_id, 
    mock_evaluate_content,
    main
)

@pytest.fixture
def sample_input_data():
    """Sample input data matching the schema"""
    return {
        "content": {
            "title": "Best Gaming Laptops 2024",
            "body": "Gaming laptops have evolved significantly in recent years. Here are the top recommendations for 2024, including detailed comparisons and expert reviews to help you make the best choice.",
            "meta": {
                "target_keyword": "gaming laptops 2024",
                "product_category": "electronics",
                "asp_provider": "amazon"
            }
        },
        "asp_links": [
            {
                "url": "https://example.com/affiliate/laptop1",
                "product_name": "Gaming Laptop Pro",
                "commission_rate": 5.5,
                "priority": 1
            }
        ],
        "evaluation_config": {
            "strict_mode": False,
            "target_score": 114,
            "check_link_validity": True
        }
    }

@pytest.fixture
def sample_input_schema():
    """Sample input schema structure"""
    return {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "content": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "body": {"type": "string"},
                    "meta": {
                        "type": "object",
                        "properties": {
                            "target_keyword": {"type": "string"},
                            "product_category": {"type": "string"},
                            "asp_provider": {"type": "string"}
                        },
                        "required": ["target_keyword", "product_category", "asp_provider"]
                    }
                },
                "required": ["title", "body", "meta"]
            },
            "asp_links": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "url": {"type": "string"},
                        "product_name": {"type": "string"},
                        "priority": {"type": "integer"}
                    },
                    "required": ["url", "product_name", "priority"]
                }
            }
        },
        "required": ["content", "asp_links"]
    }

class TestLoadSchema:
    """Test schema loading functionality"""
    
    def test_load_schema_success(self, tmp_path, sample_input_schema):
        """Test successful schema loading"""
        schema_file = tmp_path / "test_schema.json"
        schema_file.write_text(json.dumps(sample_input_schema))
        
        result = load_schema(schema_file)
        assert result == sample_input_schema
    
    def test_load_schema_file_not_found(self, tmp_path):
        """Test schema loading with non-existent file"""
        non_existent = tmp_path / "does_not_exist.json"
        
        with pytest.raises(SystemExit):
            load_schema(non_existent)
    
    def test_load_schema_invalid_json(self, tmp_path):
        """Test schema loading with invalid JSON"""
        invalid_json_file = tmp_path / "invalid.json"
        invalid_json_file.write_text("{invalid json")
        
        with pytest.raises(SystemExit):
            load_schema(invalid_json_file)

class TestValidateInput:
    """Test input validation functionality"""
    
    def test_validate_input_valid(self, sample_input_data, sample_input_schema):
        """Test validation with valid input"""
        result = validate_input(sample_input_data, sample_input_schema)
        assert result is True
    
    def test_validate_input_missing_required_field(self, sample_input_schema):
        """Test validation with missing required field"""
        invalid_data = {
            "content": {
                "title": "Test",
                "body": "Test content"
                # Missing "meta" field
            },
            "asp_links": []
        }
        
        result = validate_input(invalid_data, sample_input_schema)
        assert result is False
    
    def test_validate_input_wrong_type(self, sample_input_schema):
        """Test validation with wrong data type"""
        invalid_data = {
            "content": {
                "title": "Test",
                "body": "Test content",
                "meta": {
                    "target_keyword": "test",
                    "product_category": "electronics",
                    "asp_provider": "amazon"
                }
            },
            "asp_links": "should be array"  # Wrong type
        }
        
        result = validate_input(invalid_data, sample_input_schema)
        assert result is False

class TestCreateAuditId:
    """Test audit ID creation"""
    
    def test_create_audit_id_format(self):
        """Test audit ID format"""
        audit_id = create_audit_id()
        assert audit_id.startswith("audit_")
        assert len(audit_id) == 20  # "audit_" + 14 digits
        
    def test_create_audit_id_unique(self):
        """Test that audit IDs are unique (at least different timestamps)"""
        import time
        id1 = create_audit_id()
        time.sleep(1)  # Ensure different timestamp
        id2 = create_audit_id()
        assert id1 != id2

class TestMockEvaluateContent:
    """Test content evaluation functionality"""
    
    def test_mock_evaluate_content_structure(self, sample_input_data):
        """Test that evaluation returns correct structure"""
        result = mock_evaluate_content(sample_input_data)
        
        # Check required top-level fields
        assert "audit_id" in result
        assert "timestamp" in result
        assert "overall_score" in result
        assert "detailed_scores" in result
        assert "improvements" in result
        assert "link_validation_results" in result
        assert "metadata" in result
        
        # Check overall_score structure
        overall = result["overall_score"]
        assert "total" in overall
        assert "grade" in overall
        assert "auto_publish_eligible" in overall
        assert isinstance(overall["total"], int)
        assert overall["grade"] in ["ELITE", "EXCELLENT", "GOOD", "FAIR", "POOR"]
    
    def test_mock_evaluate_content_scoring_logic(self):
        """Test scoring logic with different content lengths"""
        short_content = {
            "content": {
                "body": "Short content",
                "title": "Test",
                "meta": {"target_keyword": "test", "product_category": "electronics", "asp_provider": "amazon"}
            },
            "asp_links": [{"url": "test", "product_name": "test", "priority": 1}]
        }
        
        long_content = {
            "content": {
                "body": "Very long content " * 100,  # Much longer content
                "title": "Test",
                "meta": {"target_keyword": "test", "product_category": "electronics", "asp_provider": "amazon"}
            },
            "asp_links": [{"url": "test", "product_name": "test", "priority": 1}]
        }
        
        short_result = mock_evaluate_content(short_content)
        long_result = mock_evaluate_content(long_content)
        
        # Longer content should generally score higher
        assert long_result["overall_score"]["total"] > short_result["overall_score"]["total"]

class TestMainFunction:
    """Test main CLI function"""
    
    def test_main_validate_only_flag(self, tmp_path, sample_input_data, sample_input_schema):
        """Test --validate-only flag"""
        # Create temporary files
        input_file = tmp_path / "input.json"
        input_file.write_text(json.dumps(sample_input_data))
        
        schema_dir = tmp_path / "docs"
        schema_dir.mkdir()
        input_schema_file = schema_dir / "audit_input_schema.json"
        input_schema_file.write_text(json.dumps(sample_input_schema))
        
        # Mock sys.argv
        with patch('sys.argv', ['orchestrator.py', '--input', str(input_file), '--validate-only']):
            with patch('orchestrator.load_schema') as mock_load_schema:
                mock_load_schema.return_value = sample_input_schema
                with patch('builtins.print') as mock_print:
                    with pytest.raises(SystemExit) as exc_info:
                        main()
                    # Should exit cleanly after validation
                    assert exc_info.value.code is None
    
    def test_main_missing_input_file(self):
        """Test main with missing input file"""
        with patch('sys.argv', ['orchestrator.py', '--input', '/nonexistent/file.json']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1

if __name__ == "__main__":
    pytest.main([__file__])