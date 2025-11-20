from config import CONFIG
from utils.file_utils import FileUtils
from utils.permission_utils import require_admin
from utils.websocket_utils import send_message


@require_admin
async def handle_add_command(message_text, user_id, group_id, websocket):
    """处理添加群组ID命令"""
    
    # 解析命令参数
    parts = message_text.split()
    
    # 检查命令格式
    if len(parts) < 3:
        await send_message(websocket, "错误：命令格式不正确\n正确格式：=add (admin/rbw) 3289138258", user_id, group_id)
        return
    
    # 获取命令类型（yinpa或join）
    command_type = parts[2]
    
    # 检查命令类型是否有效
    if command_type not in ["admin", "rbw"]:
        await send_message(websocket, "错误：命令类型不正确，只能是 admin 或 rbw", user_id, group_id)
        return
    
    # 获取要添加的群组ID列表
    try:
        ids = [int(part) for part in parts[3:]]
    except ValueError:
        await send_message(websocket, "错误：目标必须是数字", user_id, group_id)
        return
    
    # 添加群组ID
    added_groups = []
    failed_groups = []
    
    for id in ids:
        try:
            if command_type == "admin":
                FileUtils.add_admin(id)
            elif command_type == "rbw":
                FileUtils.add_rbw_group_id(id)
            added_groups.append(str(id))
        except Exception as e:
            failed_groups.append(f"{id} ({str(e)})")
    
    # 构造响应消息
    response_message = "ID添加完成：\n"
    
    if added_groups:
        response_message += f"成功添加的目标{command_type}：{', '.join(added_groups)}\n"
    
    if failed_groups:
        response_message += f"添加失败的目标：{', '.join(failed_groups)}\n"
    
    # 显示当前所有群组ID
    if command_type == "admin":
        current_groups = CONFIG.ADMINS
    else:
        current_groups = CONFIG.GROUP_IDS
    
    response_message += f"\n当前{command_type}列表：{', '.join(map(str, current_groups))}"
    
    await send_message(websocket, response_message, user_id, group_id)