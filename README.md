# Personal Assistant n8n Workflows

A small collection of exported n8n workflows for an AI-assisted personal assistant.

## Included workflows

- `Personal_Assistant.json` — main assistant workflow with tool-based actions and a knowledge-base connection
- `CalendarAgent.JSON` — creates, updates, and queries calendar events
- `EmailAgent.json` — works with email messages through Gmail tools
- `PhoneCallAgent.json` — places and checks phone calls through Vapi

## Credentials

The workflow exports do not contain live service keys. Service-specific values are read from n8n environment variables where needed:

```text
VAPI_API_KEY
GOOGLE_CALENDAR_ID
GOOGLE_SHEETS_DOCUMENT_ID
```

The imported workflows also reference n8n credential entries. After importing them into your own n8n instance, map those credential nodes to credentials available in your instance.

Never commit API keys, OAuth tokens, passwords, or other service credentials to this repository.

## Importing into n8n

1. Open n8n and choose **Import from File**.
2. Import the JSON workflow you want to use.
3. Reconnect the Google, OpenAI, Gmail, Telegram, or Vapi credentials to accounts available in your n8n instance.
4. Set the required environment variables before activating workflows that use them.
5. Test each workflow with non-sensitive sample data before enabling it for real accounts.

## Scope

These files are workflow exports rather than a standalone application. Their behavior depends on the n8n version, configured credentials, external services, and any parent workflow that invokes them.
