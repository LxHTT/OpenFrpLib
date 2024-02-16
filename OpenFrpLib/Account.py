"""
Manage account
"""

from .NetworkController import post

APIURL = "https://of-dev-api.bfsea.xyz"
OAUTHURL = "https://openid.17a.ink"


def login(user: str, password: str):
    r"""
    Login.
    =
    Requirements:

    `user` --> str: Can be a username or an email address.

    `password` --> str

    Return:
    `data`, `Authorization`, `flag`, `msg` --> list
    """

    # POST API
    _oauthData = post(
        url=f"{OAUTHURL}/api/public/login",
        json={"user": user, "password": password},
        headers={"Content-Type": "application/json"},
    )
    if _oauthData.status_code == 200:
        _callbackData = post(
            url=f"{OAUTHURL}/api/oauth2/authorize?response_type=code&redirect_uri=https://console.openfrp.net/oauth_callback&client_id=openfrp&log=pass",
            headers={"Content-Type": "application/json"},
        )
        return _loginCallback(_callbackData.json()["data"]["code"])


def _loginCallback(code: str):
    _loginData = post(
        url=f"https://console.openfrp.net/web/oauth2/callback?code={code}",
        headers={"Content-Type": "application/json"},
    )
    _APIData = _loginData.json()
    data = _APIData["data"]  # Will be expired in 8 hours.
    flag = bool(_APIData["flag"])  # Status, true or false.
    msg = str(_APIData["msg"])  # What Msg API returned.
    # Will be expired in 8 hours.
    Authorization = str(_loginData.headers["Authorization"])

    return data, Authorization, flag, msg


def getUserInfo(Authorization: str, session: str):
    r"""
    Get a user's infomation.
    =
    Requirements:
    `Authorization` --> str: If you don't have one, use login() to get it.
    `session` --> str: If you don't have one, use login() to get it.

    Return:
    `data`, `flag`, `msg` --> list

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
    _APIData = post(
        url=f"{APIURL}/frp/api/getUserInfo",
        json={"session": session},
        headers={"Content-Type": "application/json", "Authorization": Authorization},
    )
    _userData = _APIData.json()
    data = _userData["data"]
    flag = bool(_userData["flag"])
    msg = str(_userData["msg"])

    if not _APIData.ok:
        _APIData.raise_for_status()

    return data, flag, msg


def userSign(Authorization: str, session: str):
    r"""
    Daily sign.
    =
    Requirements:
    `Authorization` --> str: If you don't have one, use login() to get it.
    `session` --> str: If you don't have one, use login() to get it.

    Return:
    `data`, `flag`, `msg` --> list
    """
    # POST API
    _APIData = post(
        url=f"{APIURL}/frp/api/userSign",
        json={"session": session},
        headers={"Content-Type": "application/json", "Authorization": Authorization},
    )
    _userSignData = _APIData.json()
    data = _userSignData["data"]
    flag = bool(_userSignData["flag"])
    msg = str(_userSignData["msg"])

    if not _APIData.ok:
        _APIData.raise_for_status()

    return data, flag, msg
