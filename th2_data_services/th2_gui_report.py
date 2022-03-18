class Th2GUIReport:
    """Class for create gui link by event ID or message ID."""

    def __init__(self, link_provider: str):
        """Th2GUIReport constructor.

        Args:
            link_provider (str): link to provider.

        """
        self._link_provider = self.__normalize_link(link_provider)

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
        if find_http == False:
            link = "http://" + link

        if link[-1] != "/":
            link = link + "/"

        return link

    def get_event_link(self, event_id) -> str:
        """Create link with event id.

        Args:
            event_id (str): id for adding in link.

        Returns:
            Link with event id.

        """
        if event_id[-1] == "/":
            event_id = event_id[:-1:]

        return f"{self._link_provider}?eventId={event_id}"

    def get_message_link(self, message_id) -> str:
        """Create link with message id.

        Args:
            message_id (str): id for adding in link.

        Returns:
            Link with message id.

        """
        if message_id[-1] == "/":
            message_id = message_id[:-1:]

        return f"{self._link_provider}?messageId={message_id}"
