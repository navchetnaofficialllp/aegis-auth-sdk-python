#!/usr/bin/env python3
"""
Test script for Aegis Auth Python SDK
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from aegis_auth import AegisAuth, AegisAuthError, create_client

def test_sdk():
    print("🧪 Testing Aegis Auth Python SDK...")
    
    # Test 1: SDK initialization
    try:
        aegis = AegisAuth(api_key="test-key")
        print("✅ SDK initialization successful")
    except Exception as e:
        print(f"❌ SDK initialization failed: {e}")
        return False
    
    # Test 2: Check methods exist
    methods = ['login', 'register', 'logout', 'is_authenticated', 'get_user', 'get_profile']
    for method in methods:
        if hasattr(aegis, method) and callable(getattr(aegis, method)):
            print(f"✅ {method} method exists")
        else:
            print(f"❌ {method} method missing")
            return False
    
    # Test 3: Event system
    test_event_fired = False
    def test_handler(data):
        nonlocal test_event_fired
        test_event_fired = True
    
    aegis.on('login', test_handler)
    aegis._emit('login', 'test_data')
    
    if test_event_fired:
        print("✅ Event system works")
    else:
        print("❌ Event system failed")
        return False
    
    # Test 4: Authentication state
    if not aegis.is_authenticated():
        print("✅ Authentication state check works")
    else:
        print("❌ Authentication state check failed")
        return False
    
    # Test 5: Convenience function
    try:
        aegis2 = create_client(api_key="test-key-2")
        print("✅ Convenience function works")
    except Exception as e:
        print(f"❌ Convenience function failed: {e}")
        return False
    
    # Test 6: Error handling
    try:
        AegisAuth(api_key="")
        print("❌ Error handling failed - should require API key")
        return False
    except AegisAuthError:
        print("✅ Error handling works")
    except Exception as e:
        print(f"❌ Unexpected error type: {e}")
        return False
    
    print("🎉 All tests passed - Python SDK is ready!")
    return True

if __name__ == "__main__":
    success = test_sdk()
    sys.exit(0 if success else 1)