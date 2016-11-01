try:
    import requests
except:
    pass


class Slack(object):
    """Send a Slack notification when a pipeline completes"""

    def __init__(self, url, channel, values):
        self.url = url
        self.channel = channel
        self.values = values

    def write(self, results):
        msg = ['Plumbium task complete']
        for field in self.values:
            msg.append('{0}: {1}'.format(field, self.values[field](results)))
        payload = {
            'text': '\n'.join(msg),
            'channel': self.channel,
        }
        requests.post(self.url, json=payload)
