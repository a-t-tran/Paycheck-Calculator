# Paycheck Calculator

A Python tool that connects to Google Calendar, pulls work-shift events, and calculates total hours worked — built to automate hour-tracking instead of doing it by hand.

## How it works

- `auth.py` handles Google OAuth2 login: checks for a saved session (`token.json`), refreshes it if expired, or runs the browser login flow using `credentials.json` if no valid session exists.
- `hours.py` uses that authenticated connection to pull work-shift events from Google Calendar and total up the hours worked.

## Setup

This project needs your own Google Cloud OAuth credentials to run:

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/) and enable the Calendar API.
2. Generate OAuth 2.0 credentials and download them as `credentials.json`.
3. Place `credentials.json` in the project root (it's gitignored — never commit this file).
4. Run `auth.py` once to complete the browser login flow; this generates `token.json` for future runs.

## Usage

```bash
python hours.py
```

## Files

| File | Purpose |
|---|---|
| `auth.py` | Google OAuth2 authentication and token refresh |
| `hours.py` | Pulls calendar events and calculates hours worked |

**Not included (gitignored, private to you):** `credentials.json`, `token.json` — these hold real API secrets and should never be committed to a public repo.

See [NOTES.md](NOTES.md) for build notes.
