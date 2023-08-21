"""
Manage account
"""
from .NetworkController import post
APIURL = "https://of-dev-api.bfsea.xyz"

def login(user: str, pwd: str):
    r"""
    Login.
    =
    Requirements:

    `User` --> str: Can be a username or an email address.

    `Password` --> str

    Return:
    `SessionID`, `AuthKey`, `Flag`, `Msg` --> list
    """
    
    # POST API
    APIData = post(
        url=f"{APIURL}/user/login",
        json={
            "user": user,
            "password": pwd
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
    Get a user's infomation.
    =
    Requirements:  
    `AuthKey` --> str: If you don't have one, use login() to get it.
    `SessionID` --> str: If you don't have one, use login() to get it.
    `Keyword` --> str: Can be 'all' or some other arguments like 'outLimit|used', which is splitted with '|'.
    
    Return:  
    `UserInfo` --> dict: contains the information of a user you want.

    > outLimit    | 上行带宽(Kbps)

    > used        | 已用隧道(条)

    > token       | 用户密钥(32位字符)

    > realname    | 是否已进行实名认证(已认证为True, 未认证为False)

    > regTime     | 注册时间(Unix时间戳)

    > inLimit     | 下行带宽(Kbps)

    > friendlyGroup | 用户组名称(文字格式友好名称, 可直接输出显示)

    > proxies     | 总共隧道条数(条)

    > id          | 用户注册ID

    > email       | 用户注册邮箱

    > username    | 用户名(用户账户)

    > group       | 用户组(系统识别标识) (normal为普通用户)

    > traffic     | 剩余流量(Mib)
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
