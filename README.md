## OpenFrpLib
<p align="right">based on OpenFrp OPENAPI<br>presented by LxHTT</p>

这是一个封装了OpenFrp OPENAPI的Python库。

### 安装
___
```command
pip install OpenFrpLib
```

### 开始使用
___
#### 导入
```python
import OpenFrpLib
```

#### 设置是否绕过系统代理
```python
from OpenFrpLib.NetworkController import BYPASS_SYSTEM_PROXY

BYPASS_SYSTEM_PROXY(True) # True为开启绕过, False不绕过
```

#### 登录
```python
from OpenFrpLib import Account

# 用一个列表存取，方便记录SessionID和AuthKey
LoginInfo = Account.login("用户名或邮箱", "密码")

"""
    Requirements:

    `User` --> str: Can be a username or an email address.

    `Password` --> str

    Return:
    `SessionID`, `AuthKey`, `Flag`, `Msg` --> list
"""
```
然后使用索引值获取`SessionID`和`AuthKey`。  
`SessionID`在如上示例代码的`LoginInfo[0]`, `AuthKey`在如上示例代码的`LoginInfo[0]`

#### 获取用户信息
```python
from OpenFrpLib import Account

Account.getUserInfo(AuthKey, SessionID, "token|friendlyGroup|username|traffic")
'''
Requirements:  
    `AuthKey` --> str: If you don't have one, use login() to get it.
    `SessionID` --> str: If you don't have one, use login() to get it.
    `Keyword` --> str: Can be 'all' or some other arguments like 'outLimit|used', which is splitted with '|'.
    
    Return:  
    `UserInfo` --> dict: contains the information of a user you want.
'''
```
`AuthKey`: 用Account.login()获取。  
`SessionID`: 用Account.login()获取。  
`Keyword`: 可以是"", 也可以是如上写法，用`|`隔开。如上方就是在获取`用户密钥`、`用户组名称`、`用户名`、`剩余流量`。

> 返回值解释（复制自OpenFrp OPENAPI官方文档）：
> ``data`` 下的键值
> 键名          | 值内容意
> ------------- | ----------------------------  
> outLimit      | 上行带宽（Kbps）
> used          | 已用隧道（条）
> token         | 用户密钥（32位字符）
> realname      | 是否已进行实名认证（已认证为 ``true`` ，未认证为 ``false`` 。）
> regTime       | 注册时间（Unix时间戳）
> inLimit       | 下行带宽（Kbps）
> friendlyGroup | 用户组名称（文字格式友好名称，可直接输出显示。）
> proxies       | 总共隧道条数（条）
> id            | 用户注册ID
> email         | 用户注册邮箱
> username      | 用户名（用户账户）
> group         | 用户组（系统识别标识）（``normal`` 为普通用户）
> traffic       | ~~红绿灯~~ 剩余流量（Mib）  