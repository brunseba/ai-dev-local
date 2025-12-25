#!/usr/bin/env python3
"""Test script for vector store functionality"""

import requests
import json
import sys

# Configuration
VECTOR_STORE_URL = "http://localhost:8000"
VECTOR_STORE_KEY = "sk-3zQNqmUvQBzpVeZbJRiZQA"

def test_health():
    """Test health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{VECTOR_STORE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_create_vector_store():
    """Test creating a vector store"""
    print("\nTesting vector store creation...")
    
    headers = {
        "Authorization": f"Bearer {VECTOR_STORE_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "name": "test-store",
        "metadata": {
            "project": "ai-dev-local",
            "test": "true"
        }
    }
    
    response = requests.post(
        f"{VECTOR_STORE_URL}/v1/vector_stores",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error creating vector store: {response.text}")
        return None

def test_list_vector_stores():
    """Test listing vector stores"""
    print("\nTesting vector store listing...")
    
    headers = {
        "Authorization": f"Bearer {VECTOR_STORE_KEY}"
    }
    
    response = requests.get(
        f"{VECTOR_STORE_URL}/v1/vector_stores",
        headers=headers
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    return response.status_code == 200

def test_search(vector_store_id):
    """Test searching a vector store (this will trigger embedding generation)"""
    print(f"\nTesting vector store search (will test LiteLLM authentication)...")
    
    headers = {
        "Authorization": f"Bearer {VECTOR_STORE_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "query": "test query",
        "limit": 5
    }
    
    response = requests.post(
        f"{VECTOR_STORE_URL}/v1/vector_stores/{vector_store_id}/search",
        headers=headers,
        json=data
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    # Check for authentication errors in response
    if "Authentication Error" in response.text or "Invalid proxy server token" in response.text:
        print("\n❌ AUTHENTICATION ERROR DETECTED!")
        return False
    
    return response.status_code in [200, 404]  # 404 is ok if vector store doesn't exist yet

if __name__ == "__main__":
    print("=" * 60)
    print("Vector Store Test Suite")
    print("=" * 60)
    
    # Test 1: Health check
    if not test_health():
        print("\n❌ Health check failed!")
        sys.exit(1)
    print("✅ Health check passed")
    
    # Test 2: List vector stores
    if not test_list_vector_stores():
        print("\n❌ List vector stores failed!")
        sys.exit(1)
    print("✅ List vector stores passed")
    
    # Test 3: Create vector store
    vector_store = test_create_vector_store()
    if vector_store:
        print(f"✅ Vector store created: {vector_store.get('id', 'unknown')}")
        
        # Test 4: Search (tests LiteLLM authentication)
        if test_search(vector_store.get('id')):
            print("✅ Search test passed (no authentication errors)")
        else:
            print("❌ Search test failed")
            sys.exit(1)
    else:
        print("⚠️  Could not create vector store, skipping search test")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)
