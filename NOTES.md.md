# Build Notes

## Authentication (`auth.py`)

Uses the standard Google OAuth2 flow for installed apps:

- `google.oauth2.credentials.Credentials` — represents a saved login session.
- `google_auth_oauthlib.flow.InstalledAppFlow` — runs the browser-based login using `credentials.json` when no valid session exists yet.
- `google.auth.transport.requests.Request` — refreshes an expired token without requiring a fresh login.

Scope requested: read-only access to Calendar (`https://www.googleapis.com/auth/calendar.readonly`) — only pulling data, not modifying the calendar.

Flow: check if `token.json` exists → if yes, load and refresh if needed → if no (or invalid), run the full browser login flow and save a new `token.json` for next time.

## Hours calculation (`hours.py`)

Pulls work-shift events from the connected calendar and totals up hours worked.

## Security note

`credentials.json` and `token.json` both contain real, usable API access — treated the same as a password. Both are excluded via `.gitignore` (`*.json` catch-all) and were never committed to the public repo, confirmed by checking commit history before pushing.

## Portfolio framing

Originally built out of practical need (tracking hours from work shifts) but also demonstrates: OAuth2 flow implementation, external API integration, and handling of sensitive credentials — relevant for internship applications, especially anything touching data engineering or backend work.

## Known gaps / possible next steps

- No error handling documented yet for expired/revoked tokens beyond the basic refresh flow.
- Could extend to calculate actual pay (rate × hours) rather than just hours worked.
- Could add export to CSV or a simple summary output.
