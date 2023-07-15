"""
Manage account
"""
from requests import post

APIURL = "https://of-dev-api.bfsea.xyz"

def login(User: str, Password: str):
    r"""
    :param User --> str
    :param Password --> str

    :return SessionID, AuthKey, Flag, Msg --> list
    """
    
    # POST API
    APIData = post(
        url=f"{APIURL}/user/login",
        json={
            "user": User,
            "password": Password
        },
        headers={'Content-Type': 'application/json'}
    )

    if APIData.ok:
        LoginData = APIData.json()

        SessionID = str(LoginData['data'])  # Will be expired in 8 hours.
        Flag = str(LoginData['flag'])  # Status, true or false.
        Msg = bool(LoginData['msg'])  # What Msg API returned.
        AuthKey = str(APIData.headers['Authorization'])  # Will be expired in 8 hours.
    else:
        APIData.raise_for_status()
        SessionID, AuthKey, Flag, Msg = ""
    return SessionID, AuthKey, Flag, Msg

def getUserInfo(AuthKey: str, SessionID: str, Keyword="all"):
    r"""
    :param AuthKey --> str: If you don't have one, use login() to get it.
    :param SessionID --> str: If you don't have one, use login() to get it.
    :param Keyword --> str: Can be 'all' or some other arguments like 'outLimit|used', which is splitted with '|'.
    :return: UserInfo --> dict: contains the information of a user you want.
    """

    # POST API
    APIData = post(
        url=f"{APIURL}/frp/api/getUserInfo",
        json={
            "session": SessionID
        },
        headers={'Content-Type': 'application/json', 'Authorization': AuthKey}
    )

    if APIData.ok:
        UserData = APIData.json()['data']
        '''
        DIFFERENCE:
        UserData is a dict from OPENFRP OPENAPI,
        while UserInfo is the dict which the function would return.
        ''' 
        UserInfo = {}
        _Keywords = ["outLimit", "used", "token", "realname", "regTime", "inLimit", "friendlyGroup", "proxies", "id", "email", "username", "group", "traffic"]
        
        if Keyword == "all":
            UserInfo = {_Keyword: UserData[_Keyword] for _Keyword in _Keywords}

        else:
            Keyword = str(Keyword).split("|")
            UserInfo = dict(sorted({key: UserData[key] for key in set(Keyword) & set(UserData.keys())}.items(), key=lambda x: _Keywords.index(x[0]) if x[0] in _Keywords else len(_Keywords)))
    else:
        APIData.raise_for_status()
    
    return UserInfo
