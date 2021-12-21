from codecs import register_error


def handler(err: UnicodeDecodeError):
    return chr(err.object[err.start]), err.end


UNICODE_REPLACE_HANDLER = "unicode_replace"

register_error(UNICODE_REPLACE_HANDLER, handler)
