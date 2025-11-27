#!/usr/bin/env python3
"""
Verification test for AIOrchestrator MODEL_CONFIG attribute fix
Run this to verify the production error is fixed
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_model_config_attribute():
    """Test that MODEL_CONFIG is accessible as a class attribute"""
    try:
        from ai_orchestrator import AIOrchestrator, QueryType, MODEL_CONFIG
        
        print("✓ Successfully imported AIOrchestrator")
        
        # Test 1: CLASS attribute access
        print("\n[Test 1] Checking class-level access:")
        if hasattr(AIOrchestrator, 'MODEL_CONFIG'):
            print("✓ AIOrchestrator.MODEL_CONFIG exists")
        else:
            print("✗ AIOrchestrator.MODEL_CONFIG NOT found")
            return False
        
        # Test 2: INSTANCE attribute access (what causes the error)
        print("\n[Test 2] Checking instance-level access (this was failing):")
        orchestrator = AIOrchestrator()
        
        if hasattr(orchestrator, 'MODEL_CONFIG'):
            print("✓ orchestrator.MODEL_CONFIG exists")
        else:
            print("✗ orchestrator.MODEL_CONFIG NOT found (THIS WAS THE BUG)")
            return False
        
        # Test 3: Access specific model config
        print("\n[Test 3] Accessing specific model configs:")
        try:
            config = orchestrator.MODEL_CONFIG[QueryType.SIMPLE_FAQ]
            print(f"✓ Simple FAQ config: {config['model']}")
            
            config = orchestrator.MODEL_CONFIG[QueryType.CODE_GENERATION]
            print(f"✓ Code Generation config: {config['model']}")
            
            config = orchestrator.MODEL_CONFIG[QueryType.REASONING]
            print(f"✓ Reasoning config: {config['model']}")
        except KeyError as e:
            print(f"✗ Failed to access model config: {e}")
            return False
        
        # Test 4: Check all query types have config
        print("\n[Test 4] Checking all query types have configurations:")
        missing = []
        for query_type in QueryType:
            if query_type not in orchestrator.MODEL_CONFIG:
                missing.append(query_type.value)
        
        if missing:
            print(f"✗ Missing configs for: {missing}")
            return False
        else:
            print(f"✓ All {len(QueryType)} query types have configurations")
        
        # Test 5: Check QUERY_CLASSIFIERS
        print("\n[Test 5] Checking QUERY_CLASSIFIERS attribute:")
        if hasattr(orchestrator, 'QUERY_CLASSIFIERS'):
            print("✓ orchestrator.QUERY_CLASSIFIERS exists")
        else:
            print("✗ orchestrator.QUERY_CLASSIFIERS NOT found")
            return False
        
        # Test 6: Simulate the server.py usage pattern
        print("\n[Test 6] Simulating server.py usage pattern:")
        try:
            # This is what server.py does
            query_type = QueryType.CODE_GENERATION
            model_config = orchestrator.MODEL_CONFIG[query_type]
            model_used = model_config["model"]
            print(f"✓ Server pattern works: model_used = {model_used}")
        except Exception as e:
            print(f"✗ Server pattern failed: {e}")
            return False
        
        # Test 7: Simulate the test pattern
        print("\n[Test 7] Simulating test suite usage pattern:")
        try:
            # This is what tests/test_orchestrator.py does
            assert query_type in orchestrator.MODEL_CONFIG
            print("✓ Test pattern works: assert query_type in orchestrator.MODEL_CONFIG")
            
            for qt, config in orchestrator.MODEL_CONFIG.items():
                assert "model" in config
                assert "temperature" in config
                assert "max_tokens" in config
            print(f"✓ All {len(orchestrator.MODEL_CONFIG)} configs have required fields")
        except Exception as e:
            print(f"✗ Test pattern failed: {e}")
            return False
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        print("\nThe production error 'AIOrchestrator' object has no")
        print("attribute 'MODEL_CONFIG' has been FIXED!")
        print("\nYou can safely deploy this version.")
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_model_config_attribute()
    sys.exit(0 if success else 1)
