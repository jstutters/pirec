"""
plumbium.recorders.slack
************************
"""

try:
    from slackclient import SlackClient
except:
    pass


class Slack(object):
    """Post a message to a Slack channel on pipeline completion

    :param channel: The channel name e.g. ``#general``
    :type channel: str
    """

    def __init__(self, channel, token, message):
        self.channel = channel
        self.message = message
        self.token = token

    def write(self, results):
        """Send a message to the Slack channel chosen at init

        :param results: A dictionary of the results
        :type results: dict
        """

        sc = SlackClient(self.token)
        sc.api_call(
            'chat.postMessage',
            channel=self.channel,
            text=self.message.format(results),
            username='plumbiumbot',
            icon_emoji=':robot_face:'
        )
