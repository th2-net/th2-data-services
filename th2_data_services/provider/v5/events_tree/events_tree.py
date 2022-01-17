from th2_data_services.et_interface import IEventsTree
from th2_data_services.provider.v5.struct import provider5_event_struct


class EventsTree5(IEventsTree):
    def __init__(
        self,
        data: Union[Iterator, Generator[dict, None, None], Data] = None,
        preserve_body: Optional[bool] = False,
        event_struct=provider5_event_struct,
    ):
        """TBU by Sviatoslav"""
