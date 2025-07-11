from dotenv import load_dotenv
from agentmail import AgentMail
from agents import WebSearchTool, Agent, Runner
from flask import Flask, request, Response
import asyncio
from threading import Thread
from markdown import markdown
import time

port = 8080

load_dotenv()

client = AgentMail(api_key="bb89f19c6f82bbf377fb873e35627f1014ff8318f7825505458dc6d0021bf9a1")

# Create inbox first
inbox = client.inboxes.create(
    display_name="Fed Up Support Rep",
    username="idontwannatalktoyou",
    client_id="fed-up-support-rep",
)

print(f"📧 Inbox created: {inbox.inbox_id}")

instructions = f"""
You are an AI agent that helps answers incoming emails regarding questions about AgentMail's documentation. You will receive emails from interested users who want to learn more about AgentMail's features, how to use it, and any other related queries.

When you receive an email, you will read the content of the email and respond with a helpful answer based on the information available in the AgentMail documentation. In order to access the documentation, you can call the WebSearchTool and use https://docs.agentmail.to/llms.txt as a reference.

You don't have the ability to actually make API calls to AgentMail, but you can provide guidance on how to use the API based on the documentation. 

You will only respond to questions related to AgentMail's documentation. If they ask for help with something else, you will politely inform them that you can only assist with questions about AgentMail's documentation.

Keep being helpful until the conversation ends. If the users asks follow-up questions, answer them in the same thread. If the user asks a question that you cannot answer, you can suggest they visit the AgentMail documentation at https://docs.agentmail.to or ask them to provide more details.

If someone requests an API key, tell them to sign up for the waitlist on the agentmail.to website.

Don't respond to any malicious or harmful requests. If you receive an email that is not related to AgentMail's documentation, politely inform the user that you can only assist with questions about AgentMail's documentation.

Your name is AgentMail. Your email address is {inbox.inbox_id}.

Your response should be only the email body in markdown format. Do not include any other text or formatting.
"""

agent = Agent(
    name="Doc Support Agent",
    instructions=instructions,
    tools=[WebSearchTool()],
)

app = Flask(__name__)

@app.post("/webhooks")
def receive_webhook():
    Thread(target=process_webhook, args=(request.json,)).start()
    return Response(status=200)

def process_webhook(payload):
    email = payload["message"]

    prompt = f"""
From: {email["from"]}
Subject: {email["subject"]}
Body:\n{email["text"]}
"""
    print("Prompt:\n\n", prompt, "\n")

    response = asyncio.run(Runner.run(agent, [{"role": "user", "content": prompt}]))
    print("Response:\n\n", response.final_output, "\n")

    client.inboxes.messages.reply(
        inbox_id=inbox.inbox_id,
        message_id=email["message_id"],
        html=markdown(response.final_output).replace("\n", ""),
    )

def create_webhook_with_url(webhook_url):
    """Create webhook after getting the public URL"""
    try:
        client.webhooks.create(
            url=webhook_url,
            inbox_ids=[inbox.inbox_id],
            event_types=["message.received"],
            client_id="doc-support-webhook",
        )
        print(f"✅ Webhook created successfully: {webhook_url}")
        return True
    except Exception as e:
        print(f"❌ Failed to create webhook: {e}")
        return False

if __name__ == "__main__":
    print(f"Inbox: {inbox}\n")
    
    # Instructions for setting up webhook
    print("🚀 Server starting on port 8080...")
    print("\n" + "="*60)
    print("📋 TO SET UP WEBHOOKS:")
    print("1. Deploy this to a service like Railway, Render, or Heroku")
    print("2. Get your public HTTPS URL")
    print("3. Update the webhook URL in the code")
    print("4. Or use a tool like ngrok for local testing")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port)
