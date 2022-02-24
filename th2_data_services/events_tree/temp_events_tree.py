from typing import Union, Iterable, Generator, List, Callable, Optional


Data = Union[Iterable, Generator]
EventStruct = dict


class EventsTree:
    def __init__(self, data: Data, preserve_body: bool, event_struct: EventStruct):
        pass

    @property
    def events(self) -> List[dict]:
        pass

    @property
    def unknown_events(self) -> List[dict]:
        pass

    @property
    def roots(self) -> List[dict]:
        pass

    def build_tree(self, data: Data) -> None:
        pass

    def append_element(self, event: dict) -> None:
        pass

    def family_chain_by_event_id(self, event_id) -> List[dict]:
        pass

    def find_by_condition(self, condition: Callable) -> dict:
        pass

    def check_by_condition(self, condition: Callable) -> dict:
        pass

    def get_ancestor_by_condition(self, event: dict, condition: Callable) -> Optional[dict]:
        pass

    def is_ancestor_by_condition(self, event: dict, condition: Callable) -> Optional[dict]:
        pass

    def recover_events(self) -> None:
        pass

    def get_event_by_id(self) -> dict:
        pass

    def show(self) -> None:
        pass
