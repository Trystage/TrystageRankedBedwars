from utils.permission_utils import require_admin
from utils.websocket_utils import send_message
from config import TARGET_GROUP_ID, ADMIN_GROUP_ID, TEST_GROUP_ID

@require_admin
async def handle_announce_command(message_text, group_id, websocket):
    """处理公告命令"""
    # 解析命令参数
    parts = message_text.split()
    if len(parts) >= 3:
        message = " ".join(parts[2:])  # 公告内容（合并剩余部分）
        # 构造反馈消息
        feedback_msg = f"成功发送公告: {message}"
        
        await send_message(websocket, feedback_msg, group_id=group_id)
        feedback_msg = f"{message}\n如有疑惑或Bug可使用/try ref反馈"
        await send_message(websocket, feedback_msg, group_id=TARGET_GROUP_ID)
        return True
    else:
        # 命令格式错误反馈
        error_feedback = "命令格式错误！正确格式: /try announce 公告内容"
        await send_message(websocket, error_feedback, group_id=group_id)
        return False