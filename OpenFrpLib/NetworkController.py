from requests import Session

class Session(Session):
    def __init__(self, BYPASS_SYSTEM_PROXY=False):
        super().__init__()
        #: Trust environment settings for proxy configuration, default
        #: authentication and similar.
        self.trust_env = BYPASS_SYSTEM_PROXY

post = Session().post
get = Session().get


def BYPASS_SYSTEM_PROXY(STATUS):
    '''
    Bypass the system proxy to allow requests to POST OpenFrp OPENAPI normally.
    '''
    global post, get
    post = Session(not STATUS).post
    get = Session(not STATUS).get
