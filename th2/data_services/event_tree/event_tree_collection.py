from typing import Type, List

from th2.data_services.event_tree import CommonEventTreeCollection
from th2.data_services.event_tree.event_tree import EventTree


class Th2EventTreeCollection(CommonEventTreeCollection[EventTree]):
    def setup_et_class(self) -> Type[EventTree]:
        return EventTree

    def get_failed_trees(self) -> List[EventTree]:
        return [t for t in self.get_trees() if t.get_root()["successful"] is False]
