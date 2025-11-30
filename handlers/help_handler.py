from config import ADMIN_GROUP_ID, TEST_GROUP_ID
from utils.permission_utils import is_admin
from utils.websocket_utils import send_message


async def handle_help_command(message_text, user_id, group_id, websocket):
    """处理帮助命令"""
    
    # 构造帮助信息
    if is_admin(group_id, user_id):
        # 管理员或测试群用户帮助信息
        help_message = """Trystage RankedBedwars 帮助信息（管理员）：
    
基础命令：
=feedback <反馈内容> - 向管理组发送反馈信息 | =ref
=report <QQ> <原因> | =r

管理员专用命令：
=announce <公告内容> - 发送公告到指定群组
=mute <QQ号> <时长(秒)> <原因> - 对指定用户进行禁言操作
=add (admin/rbw) [1] [2] ... - 添加Admin或启用rbw群
=modify <stat> <QQ> <数值> - 修改玩家战绩 (stat: wins, losses, elo)

注意：您当前在管理员或测试群组中，可以使用所有命令。"""
    else:
        # 普通用户帮助信息
        help_message = """Trystage RankedBedwars 帮助信息：
    
基础命令：
=feedback <反馈内容> - 向管理组发送反馈信息 | =ref
=report <QQ> <原因> | =r"""

    await send_message(websocket, help_message, user_id, group_id)