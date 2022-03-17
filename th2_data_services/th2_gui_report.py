class Th2GUIReport:
    """Class for create gui link by event ID or message ID."""

    def __init__(self, link_provider):
        """Th2GUIReport constructor.

        Args:
            link_provider: str
        """
        self._link_provider = link_provider

    def get_event_link(self, event_id):
        return f"{self._link_provider}?eventId={event_id}"

    def get_message_link(self, message_id):
        return f"{self._link_provider}?messageId={message_id}"
