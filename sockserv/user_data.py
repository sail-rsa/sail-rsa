class UserData:
    def __init__(self, username, pub_key):
        self.username = username
        self.pub_key = pub_key

    def __str__(self):
        return '{} ({})'.format(self.username)
