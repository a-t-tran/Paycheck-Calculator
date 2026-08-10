# Build Notes

## 08/05/2026

1. Google Cloud Console
   - Enabled the Calendar API
   - Created the OAuth 2.0 credentials
     - Registered the app itself as a known entity to Google
   - Chose the type as "Desktop App"
   - Downloaded the `credentials.json` file
     - Basically it is my app's ID card; it contains a Client ID and Client Secret
     - My Python script will read this file and "introduce" itself to Google
2. Preparing VS Code
   - Installed Python and Python Extensions
   - Created a Project Folder
   - Ran `pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client`
     - Pip is Python's package manager
     - The command downloaded pre-written libraries, so I didn't have to hand-type OAuth2 or Google API request logic myself
     - These libraries are what `auth.py` will import and use
3. Part 1.1: Writing `auth.py` (line by line)
   - Added imports
     - `os` - built-in library to check if files exist
     - `Credentials` (from `google.oauth2`) - represents a saved login session
     - `InstalledAppFlow` (from `google_auth_oauthlib`) - runs the browser login
     - `Request` (from `google.auth.transport`) - refreshes an expired token without a full re-login
   - Defined `SCOPES`
     - Set access to read-only calendar - limits what the app is allowed to do
   - Built the `authenticate()` function
     - Checks if `token.json` already exists (means I've logged in before)
     - If it exists, loads the saved credentials from it
     - If no valid credentials, checks if the token is just expired but refreshable - refreshes it quietly if so
     - If there's no token at all (or refresh isn't possible), runs a full browser login using `credentials.json`
     - Saves the new/refreshed credentials into `token.json` so I don't have to login again next time
     - Returns the credentials so files can use them later
   - Added test code (`if __name__ == '__main__':`)
     - Only runs when I run `auth.py` directly, not when it's imported elsewhere later
     - Calls `authenticate()` and prints "Authentication successful!" to confirm it worked
4. Fixed Google Cloud Console access errors
   - Got "Access Blocked" error (403: access denied) on first run
     - App is in "Testing" mode - only approved test users can log in
     - Fix: went to Google Auth Platform → Audience → added my own email as a test user
   - Got "Google hasn't verified this app" warning
     - Expected since the app isn't publicly verified - safe to click Continue since I'm the developer
5. Ran `auth.py` successfully
6. Built `hours.py` (line by line)
   - Added imports
     - `authenticate` (from `auth.py`) — reused the login function instead of rewriting it
     - `build` (from `googleapiclient.discovery`) — creates the connection to Google Calendar API
     - `datetime` — helps convert typed dates into the format Google's API requires
   - Built the `getShifts(startDate, endDate)` function
     - Logs in using `authenticate()`
     - Builds a connection ("service") to the Calendar API
     - Requests all events between the given start/end dates
     - Extracts just the event list from Google's response
     - Returns that list
   - Built the input/test section
     - Asks user to type pay period start/end dates (MM/DD/YYYY)
     - Converts those into Google's required date format (ISO 8601)
     - Calls `getShifts()` with the converted dates
   - Added filtering logic
     - Only keeps calendar events where the title contains "work" or "shift" (case-insensitive)
     - Learned: events titled "Work @ [location]" = new job (pays weekly, Fridays) — different from old job's biweekly Wednesday schedule
   - Added actual hours logging
     - For each filtered shift, asks the user to type in actual hours worked
     - Saves title, date, and hours together as a dictionary
     - Appends each entry into a list called `loggedShifts`
   - Added summary printout
     - After all shifts are logged, prints a clean list: date | title | hours
7. Debugged an indentation issue
   - Accidentally created a duplicate/misplaced `if` block outside the loop
   - Fixed by consolidating the hour-logging logic inside the original for loop
   - Learned: Python relies on indentation to know what's "inside" a function/loop/if — misplaced indentation causes errors or unexpected behavior
8. Successfully ran `hours.py` end-to-end
   - Entered a real pay period (08/01/2026–08/14/2026)
   - Script pulled real shifts from Google Calendar, filtered correctly
   - Logged actual hours for each shift via terminal input
   - Got a clean summary printout — Part 1.2 (Shift Input and Hours Logging) is done
9. Clarified project details
   - Kawasaki and Tacobell are the same company, different locations — no separate pay rate logic needed
   - Still need to confirm (before Part 1.3): new job's hourly rate, weekend premium, overtime rules, tips/bonus structure, and how pay period dates should work given new weekly Friday payday

## 08/10/2026

1. Set up version control
   - Installed/confirmed Git, created a GitHub account
   - Used GitHub Desktop to track the project folder
   - Hit a nested-folder issue twice (GitHub Desktop created an empty subfolder instead of using the real project folder) — fixed by locating the actual tracked folder and moving source files into it directly
   - Added a `.gitignore` (`__pycache__/`, `*.json`) so compiled bytecode and real credentials never get committed
   - Pushed `auth.py` and `hours.py` to a public GitHub repo — confirmed `credentials.json`/`token.json` were never exposed

## Next up

- Confirm new job's hourly rate, weekend premium, overtime rules, tips/bonus structure
- Figure out pay period dates given new weekly Friday payday
- Part 1.3 (pay calculation logic)
