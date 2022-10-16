from plugins.db.plugin_config import *

PLUGIN_DOC = """数据库插件支持两种命令: 通用数据库命令和特殊命令.

通用数据库命令格式:
    [index] modify
    - 其中 index 用于定位, modify 表示对定位到的数据进行修改
    - 如果没有 modify 部分, 即为查询命令
    - 如果没有 [index] 部分, 即为根据 modify 新建一条数据
    示例:
    - [key=2] cm=3 (所有key=2的元素的cm设成3)
    一些特殊语法:
    - [key?233] (key属性是否包含233)
    - [key@233] (233是否包含key属性)
    - [id<2] (id<2的所有条目)
    - [] (无限制, 显示所有元素)
    - [3] (表示定位第3条数据. 也可以写成 [id=3])

特殊命令:
    - {} (查看所有已注册的数据库)
    - {} <db_name/db_id> (切换数据库)
    - {} (数据写回到文件中)
    - {} (数据备份)
    - {} (重新从文件中载回数据)
    - {} (备份回滚)

注: 部分特殊命令需要权限. """.format(SHOWDB_COMMAND, USEDB_COMMAND, COMMIT_COMMAND, BACKUP_COMMAND, RELOAD_COMMAND, ROLLBACK_COMMAND)