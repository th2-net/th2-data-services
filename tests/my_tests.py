from th2_data_services.interfaces.data_source import DataSource
from th2_data_services.data import Data
from datetime import datetime

# [1] Create DataSource object to connect to rpt-data-provider.
from th2_data_services.events_tree import EventsTree, ParentEventsTree

# DEMO_HOST = "10.64.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
# DEMO_PORT = "30999"  # Node port of rpt-data-provider.
# data_source = DataSource(f"http://th2-qa:30000/th2-commonv3/backend")
# r = data_source.find_events_by_id_from_data_provider('98915b62-5f39-11ec-a7ff-fd9b1e1140e5')
from th2_data_services.provider.v5.events_tree import EventsTree2

DEMO_HOST = "10.64.66.66"  # th2-kube-demo  Host port where rpt-data-provider is located.
DEMO_PORT = "30999"  # Node port of rpt-data-provider.
data_source = DataSource(f"http://{DEMO_HOST}:{DEMO_PORT}")

START_TIME = datetime(
    year=2021, month=6, day=17, hour=9, minute=44, second=41, microsecond=692724
)  # object given in utc format
END_TIME = datetime(year=2021, month=6, day=17, hour=12, minute=45, second=49, microsecond=28579)

# [2] Get _events from START_TIME to END_TIME.
events: Data = data_source.get_events_from_data_provider(
    startTimestamp=START_TIME, endTimestamp=END_TIME, metadataOnly=False, attachedMessages=True, cache=True
)

et2 = EventsTree2(events, data_source)

desired_event = "9ce8a2ff-d600-4366-9aba-2082cfc69901:ef1d722e-cf5e-11eb-bcd0-ced60009573f"

data_source.find_events_by_id_from_data_provider(desired_event)  # Returns 1 event (dict).

print(events)
exit(1)

et = EventsTree(events)
print(et.unknown_events)

pet = ParentEventsTree(events)
print(pet.unknown_events)
pet.recover_unknown_events(data_source)
for e in events:
    if e["parentEventId"] is not None:
        assert pet.events[e["parentEventId"]]

print()

tree: dict = pet.events


class A:
    """@DynamicAttrs"""

    a = 1


z = A()
setattr(z, "b", 0)
x = z.b


class ConnPins(PinsContainer):
    to_send = Pin(attributes=[...])


class Conn(Box):
    pins = ConnPins()


def test(env, csv1):
    row: dict
    for idx, row in enumerate(csv1):
        # ACT
        act_pin_name = f"to_send_conn_{row['CounterParty']}"
        act_pin = Pin(
            connection_type="mq",
            attributes=["publish", "parsed"],
            filters=[
                {
                    "metadata": [
                        {
                            "field-name": "session_alias",
                            "expected-value": f"conn-{row['CounterParty']}",
                            "operation": "EQUAL",
                        }
                    ]
                },
            ],
        )
        setattr(env.act.pins, act_pin, act_pin)
        act_pin + env.schema.codec.pins.in_codec_encode

        # CONN
        conn = Conn(name=f"conn-{row['CounterParty']}")  # Create Conn class
        env.schema.codec.pins.out_codec_encode + conn.pins.to_send  # Linking Conn with Codec
        setattr(env.schema, f"conn-{idx}", conn)
