from th2.data_services.event_tree import CommonEventTree

Th2Event = dict  # TODO - move to types. Also this class knows that th2-event is a dict, but it cannot to know.

# TODO - should and can only work via special options.resolver


class EventTree(CommonEventTree[Th2Event]):
    def __init__(self, event_name: str, event_id: str, data: dict = None):
        super().__init__(event_name, event_id, data=data)
        self._status: bool = self.get_root()["successful"]
        self._false_func = lambda e: e["successful"] is False

    @property
    def status(self) -> bool:
        return self._status

    def append_th2event(self, e: Th2Event) -> None:
        self.append_event(event_name=e["eventName"], event_id=e["eventId"], parent_id=e["parentEventId"], data=e)

    def _calc_failed_num(self) -> int:
        i = 0
        for e in self.get_failed_events_iter():
            i += 1
        return i

    def get_failed_events_iter(self):
        yield from self.findall_iter(self._false_func)

    def get_failed_events(self) -> list:
        return list(self.get_failed_events_iter())

    def __repr__(self) -> str:
        st = "P" if self.status else "F"
        if st == "F":
            f = self._calc_failed_num()
            p = len(self) - f
            repr_str = (
                f"{st} | {self.__class__.__name__}(name='{self.get_root_name()}', "
                f"root_id='{self.get_root_id()}', events={len(self)}[P={p}, F={f}])"
            )
        else:
            repr_str = (
                f"{st} | {self.__class__.__name__}(name='{self.get_root_name()}', "
                f"root_id='{self.get_root_id()}', events={len(self)})"
            )
        return repr_str
