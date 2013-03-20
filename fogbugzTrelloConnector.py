#! /usr/bin/env python
"""Synchronizes comments between Trello boards and FogBugz cases. Leverages Trello card ID to link data via case tag in Fogbugz.
"""

from fogbugz import FogBugz
import os
from trello import TrelloApi

__author__ = "Jacob Sanford"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Jacob Sanford"
__email__ = "jsanford@unb.ca"
__status__ = "Development"


# Explicit testing / error would be nice here.
trello = TrelloApi(os.environ['TRELLO_API_KEY'])
if not os.environ['TRELLO_USER_TOKEN']=='' :
    trello.set_token(os.environ['TRELLO_USER_TOKEN'])
fb = FogBugz(os.environ['FOGBUGZ_URL'])
fb.logon(os.environ['FOGBUGZ_USER'],os.environ['FOGBUGZ_PASSWORD'])

# Find cards in board with specified label.
for cur_card in trello.boards.get_card(os.environ['TRELLO_BOARD_TO_PARSE']):
    for cur_card_label in cur_card['labels']:
        if cur_card_label['name'] == os.environ['TRELLO_LABEL_TO_PARSE'] :

            # Create case in Fogbugz if not exist
            fogbugz_response=fb.search(q='tag:"' + cur_card['id'] + '"',cols='ixBug')
            if len(fogbugz_response.cases) == 0 :
                fb.new(sTitle=cur_card['name'], sTags=cur_card['id'], ixProject=os.environ['FOGBUGZ_DEFAULT_PROJECT'])

            # Get ixBug value
            fogbugz_response=fb.search(q='tag:"' + cur_card['id'] + '"',cols='ixBug')
            fogbugz_id=fogbugz_response.ixbug.string

            # Load fogbugz updates into dictionary.
            fogbugz_updates=[]
            messages_response=fb.search(q=fogbugz_id,cols='sTitle,events')
            for case in messages_response.cases.childGenerator() :
                for event in case.events.childGenerator():
                    current_string=str(event.shtml.string)
                    # Fogbugz stores all shtml data in CDATA container, we need to strip this out. There must be a way to parse this
                    # with BeautifulSoup...
                    if current_string != 'None' and current_string !='<![CDATA[None]]>' :
                        fogbugz_updates.append(current_string.replace('<br  />\n',"\n").replace('<![CDATA[','').replace(']]>',''))

            trello_updates=[]
            # Iterate through Trello card actions and update FogBugz.
            for cur_action in trello.cards.get_action(cur_card['id']) :
                if cur_action['type'] == 'commentCard' :
                    trello_updates.append(cur_action['data']['text'])
                    if not cur_action['data']['text'] in fogbugz_updates :
                        fb.edit(ixbug=fogbugz_id, sEvent=cur_action['data']['text'])

            # Iterate through fogbugz_updates and update trello.
            for cur_fogbugz_update in fogbugz_updates:
                if not cur_fogbugz_update in trello_updates:
                    trello.cards.new_action_comment(cur_card['id'], cur_fogbugz_update)