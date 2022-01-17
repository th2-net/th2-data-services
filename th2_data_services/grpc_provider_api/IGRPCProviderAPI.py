from abc import ABCMeta


class IGRPCProviderAPI(metaclass=ABCMeta):
    def _create_connection(self, url: str):
        raise NotImplementedError("Please, implement connection to the grpc-data-provider.")

    def get_event(self, event_id):
        raise NotImplementedError("Please, implement request by id for a event.")

    def get_message(self, message_id):
        raise NotImplementedError("Please, implement request by id for a message.")

    def search_messages(self, message_search_request):
        raise NotImplementedError("Please, implement stream request for messages.")

    def search_events(self, event_search_request):
        raise NotImplementedError("Please, implement stream request for events.")
