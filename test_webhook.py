#!/usr/bin/env python3
"""
Mock webhook test - simulates an incoming email to test your agent
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app_local import process_webhook

# Mock email payload that simulates what AgentMail would send
mock_email_payload = {
    "message": {
        "message_id": "test_message_123",
        "from": "test@example.com",
        "subject": "How do I create an inbox with AgentMail?",
        "text": "Hi, I'm trying to understand how to create an inbox using the AgentMail API. Can you help me with the documentation?",
        "html": "<p>Hi, I'm trying to understand how to create an inbox using the AgentMail API. Can you help me with the documentation?</p>"
    }
}

if __name__ == "__main__":
    print("🧪 Testing webhook processing with mock email...")
    print("=" * 50)
    
    try:
        process_webhook(mock_email_payload)
        print("✅ Mock webhook test completed!")
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
