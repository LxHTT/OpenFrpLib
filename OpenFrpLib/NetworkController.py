from requests import Session

from requests import Session

class Session(Session):
    def __init__(self):
        super().__init__()
        #: Trust environment settings for proxy configuration, default
        #: authentication and similar.
        self.trust_env = False

post = Session().post
get = Session().get


def BYPASS_SYSTEM_PROXY(STATUS):
    '''
    Bypass the system proxy to allow requests to POST OpenFrp OPENAPI normally.
    '''
    if STATUS:
        Session.trust_env = False
    elif not STATUS:
        Session.trust_env = True
