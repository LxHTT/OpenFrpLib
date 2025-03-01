"""
Manage account
"""

import base64
import time
from .NetworkController import post, get
import webbrowser
from nacl.public import PrivateKey, Box, PublicKey


APIURL = "https://api.openfrp.net"
OAUTHURL = "https://access.openfrp.net"


def login():
    r"""
    Login.
    =
    Requirements:

    `user` --> str: Can be a username or an email address.

    `password` --> str

    Return:
    `data`, `Authorization`, `flag`, `msg` --> list
    """
    # 生成X25519密钥对
    private_key = PrivateKey.generate()
    public_key = private_key.public_key

    # 转换公钥为URL安全的base64格式
    public_key_bytes = bytes(public_key)
    public_key_b64 = base64.b64encode(public_key_bytes).decode()
    public_key_b64 = public_key_b64.replace("+", "-").replace("/", "_")

    # 请求登录
    _oauthData = post(
        url=f"{OAUTHURL}/argoAccess/requestLogin",
        json={"public_key": public_key_b64},
        headers={"Content-Type": "application/json"},
    )

    if _oauthData.status_code != 200:
        return None, None, False, "Login request failed"

    response_data = _oauthData.json()
    request_uuid = response_data["data"]["request_uuid"]
    authorization_url = response_data["data"]["authorization_url"]  # 获取授权URL

    # 打开浏览器让用户授权
    webbrowser.open(authorization_url)

    # 轮询等待用户授权
    for _ in range(60):
        time.sleep(5)
        poll_response = get(
            url=f"{OAUTHURL}/argoAccess/pollLogin", params={"request_uuid": request_uuid}
        )

        if poll_response.status_code != 200:
            continue

        poll_data = poll_response.json()
        if poll_data["code"] != 200:
            continue

        # 获取服务器公钥
        server_public_key_b64 = poll_response.headers.get("x-request-public-key")
        if not server_public_key_b64:
            continue

        # 处理base64 URL安全格式
        server_public_key_b64 = server_public_key_b64.replace("-", "+").replace("_", "/")
        padding = len(server_public_key_b64) % 4
        if padding:
            server_public_key_b64 += "=" * (4 - padding)

        try:
            # 解密授权数据
            server_public_key_bytes = base64.b64decode(server_public_key_b64)
            server_public_key = PublicKey(server_public_key_bytes)  # 将字节转换为PublicKey对象
            encrypted_data = base64.b64decode(poll_data["data"]["authorization_data"])

            # 提取nonce和密文
            nonce = encrypted_data[:24]
            ciphertext = encrypted_data[24:]

            # 使用NaCl box解密
            box = Box(private_key, server_public_key)  # 使用PublicKey对象创建Box
            decrypted_data = box.decrypt(ciphertext, nonce)

            authorization = decrypted_data.decode()
            return poll_data["data"], authorization, True, "Login successful"

        except Exception as e:
            return None, None, False, f"Decryption failed: {str(e)}"

    return None, None, False, "Login timeout"


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
