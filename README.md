# Fogbugz - Trello connector.
Rudimentary cron script to synchronize comments between Trello boards and FogBugz cases. Leverages Trello card ID to link data via case tag in Fogbugz.

## Setup
A number of exports are needed in the environment:
```
TRELLO_API_KEY
TRELLO_USER_TOKEN (private boards only)
TRELLO_BOARD_TO_PARSE
TRELLO_LABEL_TO_PARSE
FOGBUGZ_URL
FOGBUGZ_USER
FOGBUGZ_PASSWORD
FOGBUGZ_DEFAULT_PROJECT
```

## Use Outline
- Automatically create a new case in Fogbugz by adding TRELLO_LABEL_TO_PARSE to Trello card.
- Link an existing Fogbugz case to a Trello card by tagging Fogbugz case with card ID and adding TRELLO_LABEL_TO_PARSE to Trello card.

## Requirements
### python
- FogBugz API (https://pypi.python.org/pypi/fogbugz/)
- trello (https://pypi.python.org/pypi/trello)
