#!/usr/bin/env python3
"""
Simple webhook test - just echoes back the email without AI processing
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def simple_process_webhook(payload):
    email = payload["message"]
    
    print("📧 Received email:")
    print(f"From: {email['from']}")
    print(f"Subject: {email['subject']}")
    print(f"Body: {email['text']}")
    print()
    
    # Simple response without AI
    response = f"Thank you for your email about: {email['subject']}. This is an automated test response."
    
    print("📧 Would send reply:")
    print("=" * 50)
    print(response)
    print("=" * 50)

# Mock email payload
mock_email_payload = {
    "message": {
        "message_id": "test_message_123",
        "from": "test@example.com",
        "subject": "Test email",
        "text": "This is a test email to see if the webhook processing works.",
    }
}

if __name__ == "__main__":
    print("🧪 Testing simple webhook processing...")
    simple_process_webhook(mock_email_payload)
    print("✅ Simple test completed!")
