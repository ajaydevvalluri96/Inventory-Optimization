
import os
import anthropic

# STEP 1: Check that the API key is available
api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("ERROR: Anthropic API key not found.")
    raise SystemExit(1)

# STEP 2: Connect to Anthropic
client = anthropic.Anthropic(api_key=api_key)

# STEP 3: Send a small test request
print("Connecting to Claude AI...")

try:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=100,
        messages=[
            {
                "role": "user",
                "content": (
                    "In one sentence, explain why a business "
                    "should monitor its inventory reorder point."
                )
            }
        ]
    )

    print("\nCLAUDE AI RESPONSE:")
    for block in response.content:
        if block.type == "text":
            print(block.text)


except anthropic.AuthenticationError as error:
    print("Authentication failed.")
    print("HTTP status:", error.status_code)

    # Show only the error type, not credentials
    try:
        details = error.response.json()
        print("Error type:", details.get("error", {}).get("type"))
    except (ValueError, AttributeError):
        print("Error details unavailable.")


except anthropic.RateLimitError:
    print("Rate limit or usage restriction reached.")

except anthropic.APIStatusError as error:
    print("API request failed:", error.status_code)
    print("Check your Anthropic billing and API access.")

except anthropic.APIConnectionError:
    print("Could not connect to Anthropic. Check your internet.")
