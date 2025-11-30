import re
from utils.permission_utils import require_admin
from utils.player_utils import PlayerUtils
from utils.websocket_utils import send_message


@require_admin
async def handle_modify_command(websocket, message_text: str, group_id: str, user_id: str):
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