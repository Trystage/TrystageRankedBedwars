import json
from functools import wraps

from config import ADMIN_GROUP_ID, TEST_GROUP_ID, CONFIG
from utils.websocket_utils import send_message


def require_admin(func):
    """装饰器：要求必须是主人"""

    @wraps(func)
    async def wrapper(message_text: str, group_id: str, user_id: str, websocket):

        if not ((group_id == ADMIN_GROUP_ID) or (group_id == TEST_GROUP_ID) or user_id in CONFIG.ADMINS):
            # 权限不足的处理
            response_msg = "权限不足：只有喵喵主人才能使用此命令"
            await send_message(websocket, response_msg)
            return None

        # 有权限，执行原函数
        return await func(websocket, message_text, group_id, user_id)

    return wrapper
def is_admin(group_id: str, user_id: str):
    """
    Check if user is admin or in admin group
    :param group_id:
    :param user_id:
    :return:
    """
    if not ((group_id == ADMIN_GROUP_ID) or (group_id == TEST_GROUP_ID) or user_id in CONFIG.ADMINS):
        return False
    return True