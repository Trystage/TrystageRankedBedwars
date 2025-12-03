import re

from utils.image_utils import ImageUtils
from utils.permission_utils import require_admin
from utils.player_utils import PlayerUtils
from utils.websocket_utils import send_message, get_image


@require_admin
async def handle_modify_command(websocket, message_text: str, user_id: str = None, group_id: str = None):
    """处理修改玩家数据命令
    命令格式: =modify <stat> @user/qq <number>
    允许修改的stat: wins, losses, elo
    """
    
    # 解析命令参数
    # 移除命令前缀 "=modify "
    command_args = message_text[8:].strip()
    
    # 使用正则表达式匹配命令格式
    # 匹配: stat @user/qq number 或 stat qq number
    match = re.match(r'^(\w+)\s+(?:@)?(\d+)\s+(-?\d+)$', command_args)
    
    if not match:
        response_msg = "命令格式错误！正确格式: =modify <stat> [@]qq <数值>\n允许修改的stat: wins, losses, elo"
        await send_message(websocket, response_msg, user_id, group_id)
        return
    
    stat, qq, number_str = match.groups()
    number = int(number_str)
    
    # 验证stat参数
    allowed_stats = ['wins', 'losses', 'elo']
    if stat not in allowed_stats:
        response_msg = f"不允许修改的统计项: {stat}\n允许修改的stat: wins, losses, elo"
        await send_message(websocket, response_msg, user_id, group_id)
        return
    
    # 验证QQ号是否存在
    player_data = PlayerUtils.get_player_data(qq)
    if not player_data:
        response_msg = f"未找到QQ号为 {qq} 的玩家数据"
        await send_message(websocket, response_msg, user_id, group_id)
        return
    
    # 根据stat类型调用相应的方法修改数据
    try:
        if stat == 'wins':
            PlayerUtils.set_wins(qq, number)
        elif stat == 'losses':
            PlayerUtils.set_losses(qq, number)
        elif stat == 'elo':
            PlayerUtils.set_elo(qq, number)
        
        # 获取更新后的数据
        updated_player_data = PlayerUtils.get_player_data(qq)
        current_wins = updated_player_data.get('wins', 0)
        current_losses = updated_player_data.get('losses', 0)
        current_elo = updated_player_data.get('elo', 1000)
        
        response_msg = f"玩家 {qq} 的数据已更新:\n"
        response_msg += f"wins: {current_wins}\n"
        response_msg += f"losses: {current_losses}\n"
        response_msg += f"elo: {current_elo}"
        
        await send_message(websocket, response_msg, user_id, group_id)
    except Exception as e:
        response_msg = f"更新玩家数据时出错: {str(e)}"
        await send_message(websocket, response_msg, user_id, group_id)

async def handle_info_command(websocket, message_text: str, user_id: str = None, group_id: str = None):
    if len(message_text.split(' ')) > 1:
        target = int(message_text.split(' ')[1])
    else:
        target = user_id
    try:
        response = get_image(ImageUtils.generate_stat(target))
        await send_message(websocket, response, user_id, group_id)
    except Exception as e:
        response_msg = f"查询战绩时出错: {str(e)}"
        await send_message(websocket, response_msg, user_id, group_id)

async def handle_reg_command(websocket, message_text: str, user_id: str = None, group_id: str = None):
    response_msg = f"注册功能需与服务器一起使用,服务器已停机,请找管理员强制注册"
    await send_message(websocket, response_msg, user_id, group_id)
    return

@require_admin
async def handle_freg_command(websocket, message_text: str, user_id: str = None, group_id: str = None):
    """处理强制注册玩家命令
    命令格式: =freg <qq> <ign> <uuid> [nickname]
    """
    # 解析命令参数
    command_parts = message_text.split()
    
    # 检查参数数量
    if len(command_parts) < 4:
        response_msg = "命令格式错误！正确格式: =freg <qq> <ign> <uuid> [nickname]"
        await send_message(websocket, response_msg, user_id, group_id)
        return
    
    # 提取参数
    qq = command_parts[1]
    ign = command_parts[2]
    uuid = command_parts[3]
    nickname = command_parts[4] if len(command_parts) > 4 else ""
    
    # 简单验证QQ号是否为数字
    if not qq.isdigit():
        response_msg = "QQ号必须是数字！"
        await send_message(websocket, response_msg, user_id, group_id)
        return
    
    # 验证并格式化UUID
    try:
        from utils.uuid_utils import UUIDUtils
        formatted_uuid = UUIDUtils.format_uuid(uuid)
    except ValueError as e:
        response_msg = f"UUID格式不正确: {str(e)}"
        await send_message(websocket, response_msg, user_id, group_id)
        return
    
    try:
        # 使用add_player_raw方法注册玩家
        PlayerUtils.add_player_raw(qq, ign, formatted_uuid, formatted_uuid, nickname)
        
        response_msg = f"玩家已成功强制注册:\nQQ: {qq}\nIGN: {ign}\nUUID: {formatted_uuid}"
        if nickname:
            response_msg += f"\n昵称: {nickname}"
    except Exception as e:
        response_msg = f"注册玩家时出错: {str(e)}"
    
    await send_message(websocket, response_msg, user_id, group_id)
    return