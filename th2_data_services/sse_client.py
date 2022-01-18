import sseclient
from sseclient import _FIELD_SEPARATOR


class SSEClient(sseclient.SSEClient):
    """Patch for sseclient-py to get availability to configure decode error handler."""

    def __init__(self, event_source, char_enc="utf-8", decode_errors_handler="strict"):
        super(SSEClient, self).__init__(event_source, char_enc)
        self._decode_errors_handler = decode_errors_handler

    def events(self):
        for chunk in self._read():
            event = sseclient.Event()
            # Split before decoding so splitlines() only uses \r and \n
            for line in chunk.splitlines():
                # Decode the line.
                line = line.decode(self._char_enc, self._decode_errors_handler)

                # Lines starting with a separator are comments and are to be
                # ignored.
                if not line.strip() or line.startswith(_FIELD_SEPARATOR):
                    continue

                data = line.split(_FIELD_SEPARATOR, 1)
                field = data[0]

                # Ignore unknown fields.
                if field not in event.__dict__:
                    self._logger.debug("Saw invalid field %s while parsing " "Server Side Event", field)
                    continue

                if len(data) > 1:
                    # From the spec:
                    # "If value starts with a single U+0020 SPACE character,
                    # remove it from value."
                    if data[1].startswith(" "):
                        value = data[1][1:]
                    else:
                        value = data[1]
                else:
                    # If no value is present after the separator,
                    # assume an empty value.
                    value = ""

                # The data field may come over multiple lines and their values
                # are concatenated with each other.
                if field == "data":
                    event.__dict__[field] += value + "\n"
                else:
                    event.__dict__[field] = value

            # Events with no data are not dispatched.
            if not event.data:
                continue

            # If the data field ends with a newline, remove it.
            if event.data.endswith("\n"):
                event.data = event.data[0:-1]

            # Empty event names default to 'message'
            event.event = event.event or "message"

            # Dispatch the event
            self._logger.debug("Dispatching %s...", event)
            yield event
