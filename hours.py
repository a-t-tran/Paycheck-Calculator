# hours.py

# reuse the login function we already built in auth.py
from auth import authenticate

# lets us build a connection to the Google Calendar API and make requests to it
from googleapiclient.discovery import build

# helps us work with calendar dates (pay period start/end)
from datetime import datetime

# pulls calendar events between a start and end date (the pay period)
def getShifts(startDate, endDate):
    # log in using the function we built in auth.py
    creds = authenticate()

    # build a connection to the Google Calendar API using our credentials
    service = build('calendar', 'v3', credentials=creds)

    # ask Google Calendar for all events between startDate and endDate
    eventsResult = service.events().list(
        calendarId='primary',
        timeMin=startDate,
        timeMax=endDate,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    # extract the list of events from the response
    events = eventsResult.get('items', [])

    # send the list of shifts back so we can use it outside this function
    return events

# only runs this test code if we run hours.py directly
if __name__ == '__main__':
    # ask the user for the pay period start and end dates
    startInput = input("Enter pay period start date (MM/DD/YYYY): ")
    endInput = input("Enter pay period end date (MM/DD/YYYY): ")

    # convert the typed date into the format Google Calendar needs
    startDate = datetime.strptime(startInput, "%m/%d/%Y").strftime("%Y-%m-%dT00:00:00Z")
    endDate = datetime.strptime(endInput, "%m/%d/%Y").strftime("%Y-%m-%dT23:59:59Z")

    # pull shifts for this pay period and filter to just work-related events
    shifts = getShifts(startDate, endDate)

    # will hold each shift's actual logged hours
    loggedShifts = []

    for shift in shifts:
        title = shift['summary']
        if 'work' in title.lower() or 'shift' in title.lower():
            # get just the date part from the shift's start time
            shiftDate = shift['start']['dateTime'][:10]

            # ask the user for actual hours worked on this shift
            actualHours = input(f"Hours worked for '{title}' on {shiftDate}: ")

            # save this shift's info together as a dictionary
            loggedShifts.append({
                'title': title,
                'date': shiftDate,
                'hours': actualHours
            })

            # print a summary of everything logged this pay period
            print("\n--- Logged Hours Summary ---")
            for entry in loggedShifts:
                print(f"{entry['date']} | {entry['title']} | {entry['hours']} hours")