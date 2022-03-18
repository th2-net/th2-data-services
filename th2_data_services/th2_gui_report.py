class Th2GUIReport:
    """Class for create gui link by event ID or message ID."""

    def __init__(self, link_provider: str):
        """Th2GUIReport constructor.

        Args:
            link_provider (str): link to provider.

        """
        self._link_provider = self.add_http(self.add_slash(link_provider))

    def add_http(self, link: str):
        """Bringing links to a single form: add 'http://' to the beginning of the link.

        Args:
            link (str): link for editing.

        Returns:
            link (str): link with 'http://' in beginning.

        """
        index_http = link.find("http", 0)
        if index_http == -1:
            link = "http://" + link

        return link

    def add_slash(self, link):
        """Bringing links to a single form: add '/' to the ending of the link.

        Args:
            link (str): link for editing.

        Returns:
            link (str): link with '/' in ending.

        """
        if link[-1] != "/":
            link = link + "/"

        return link

    def get_event_link(self, event_id):
        """Create link with event id.

        Args:
            event_id (str): id for adding in link.

        Returns:
            Link with event id.

        """
        return f"{self._link_provider}?eventId={self.add_slash(event_id)}"

    def get_message_link(self, message_id):
        """Create link with message id.

        Args:
            message_id (str): id for adding in link.

        Returns:
            Link with message id.

        """
        return f"{self._link_provider}?messageId={self.add_slash(message_id)}"
