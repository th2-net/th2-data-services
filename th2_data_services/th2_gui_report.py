class Th2GUIReport:
    def __init__(self, link_provider):
        self._link_provider = link_provider
        self._event_id = None
        self._message_id = None

    def get_event_link(self, event_id):
        return f"{self._link_provider}?eventId={event_id}"

    def get_message_link(self, message_id):
        return f"{self._link_provider}?messageId={message_id}"
