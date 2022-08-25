class Th2GUIReport:
    """Class for creating gui link by event ID or message ID."""

    def __init__(self, provider_link: str):
        """Th2GUIReport constructor.

        Args:
            provider_link (str): link to provider.
        """
        self._provider_link = self.__normalize_link(provider_link)

    def __normalize_link(self, link: str) -> str:
        """Bringing links to a single form.

        Add 'http://' to the beginning of the link.
        Add slash to the ending of link.

        Args:
            link (str): link for editing.

        Returns:
            Normalize link.
        """
        find_http = link.startswith("http", 0)
        if find_http is False:
            link = "http://" + link

        if link[-1] != "/":
            link = link + "/"

        return link

    def get_event_link(self, event_id: str) -> str:
        """Creates the link with event id.

        Args:
            event_id (str): id for adding in link.

        Returns:
            GUI link to event.
        """
        return f"{self._provider_link}?eventId={event_id}"

    def get_message_link(self, message_id: str) -> str:
        """Creates the link with message id.

        Args:
            message_id (str): id for adding in link.

        Returns:
            GUI link to message.
        """
        return f"{self._provider_link}?messageId={message_id}"
