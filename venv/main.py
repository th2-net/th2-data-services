import base64

# decode_base64('W3siZXZlbnRzIjp7InJhbmdlIjpbMTY0NTE3MjI5MTY0MiwxNjQ1MTczMTkxNjQyXSwicGFuZWxBcmVhIjoxMDB9LCJtZXNzYWdlcyI6e30sInRpbWVSYW5nZSI6WzE2NDUxNzE4NDE2MzAsMTY0NTE3MzY0MTYzMF0sImludGVydmFsIjoxNSwibGF5b3V0IjpbMTAwLDBdfV0%3D')


def create_GUI_link_by_ID(w):
    for el in w:
        for _ in el:
            for __ in el[_]:
                if __ == "selectedEventId":
                    return "http://th2-qa:30000/th2-private/?workspaces=" + el[_][__]


w = [
    {
        "events": {
            "filter": {
                "attachedMessageId": {
                    "type": "string",
                    "negative": False,
                    "values": "",
                },
                "type": {
                    "type": "string[]",
                    "values": [],
                    "negative": False,
                },
                "name": {
                    "type": "string[]",
                    "values": [],
                    "negative": False,
                },
                "body": {
                    "type": "string[]",
                    "values": [],
                    "negative": False,
                },
                "status": {
                    "type": "switcher",
                    "values": "any",
                },
            },
            "panelArea": 50,
            "selectedEventId": "fcace9a4-8fd8-11ec-98fc-038f439375a0",
            #'1d2a066c-507a-4321-b5fd-e880da0cdd2c'
            "flattenedListView": False,
        },
        "layout": [50, 50],
        "messages": {"streams": ["dirty"]},
    },
]
import json

ec = json.encoder.JSONEncoder()
j = ec.encode(w)
jbase = base64.b64encode(j.encode())
print(create_GUI_link_by_ID(w))
