近期学习了Flask，于是用Flask框架写了一个web版本的license生成工具，方便在测试活动中生成license文件，还可以提供一个接口给自动化用例，用于测试和license相关的业务。

考虑到lincense的敏感性，需要来访者注册、登录后才能访问lincense工具。主要流程是：管理员添加授权工号和邮箱 --> 来访者通过填写工号和邮箱获取注册链接 --> 通过访问注册链接完成用户注册 --> 登录后使用license工具 --> 日志记录每次生成的lincense信息用于追溯。

这个web使用了flask_wtf提供表单创建和验证，flask_login提供用户管理，flask_sqlalchemy提供数据库ORM模型，smtplib提供邮件发送功能。
