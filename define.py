import re


def get_message(message_content):
    result = re.search(r'\*\*(.+?)\s', message_content)
    if result:
        content = result.group(1)
        return content
    else:
        return ""
