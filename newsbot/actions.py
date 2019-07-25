# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import json


# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message("Hello World!")

#         return []


class ActionGetNews(Action):

    def name(self):
        return 'action_get_news'
    
    def run(self, dispatcher, tracker, domain):
        category = tracker.get_slot('category')
        # print('Gautham')
        url = f'https://cricapi.com/api/matchCalendar?apikey=MxmWhJiZP2cmZslWRP6qSsYTkwZ2'
        # params = {'apikey': "MxmWhJiZP2cmZslWRP6qSsYTkwZ2"}
        response = requests.get(url).text
        print(response)
        json_data = json.loads(response)['data']
        i = 0
        for data in json_data:
            while i < 5:
                message = str(i) + "." + data['name']+data['date']
                dispatcher.utter_message(message)
            i += 1
        return []