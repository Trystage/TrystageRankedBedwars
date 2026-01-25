from games.queue import join_queue, get_queue_stats, get_user_queue, leave_queue
from utils.elo_utils import EloUtils
from utils.permission_utils import require_admin
from utils.player_utils import PlayerUtils
from utils.websocket_utils import send_message, extract_qq


async def handle_join_command(websocket, message_text, user_id, group_id):
    """处理加入queue"""
    parts = message_text.split()

    qq_str = str(user_id)

    # 检查玩家是否存在
    player_data = PlayerUtils.get_player_data(qq_str)
    if not player_data:
        response_msg = f"未找到QQ号为 {user_id} 的玩家数据"
        await send_message(websocket, response_msg, user_id, group_id)
        return

    if len(parts) == 2:
        queue_name = parts[1]
        if queue_name in ["0", "300", "600"]:
            response_message = join_queue(qq_str, queue_name)
            await send_message(websocket, response_message, user_id, group_id)
            return
        else:
            await send_message(websocket, "queue种类需为: 0 300 600", user_id, group_id)
            return

    queue_name = EloUtils.get_max_queue(PlayerUtils.get_elo(qq_str))
    response_message = join_queue(qq_str, queue_name)
    await send_message(websocket, response_message, user_id, group_id)
    return

async def handle_queue_stats_command(websocket, message_text, user_id, group_id):
    """处理queue stats查询"""
    parts = message_text.split()
    if len(parts) == 2:
        queue_name = parts[1]
        if queue_name in ["0", "300", "600"]:
            response_message = get_queue_stats(queue_name)
            await send_message(websocket, response_message, user_id, group_id)
            return
        else:
            await send_message(websocket, "queue种类需为: 0 300 600", user_id, group_id)
            return
    queue_name = get_user_queue(str(user_id))

    if queue_name == "None":
        await send_message(websocket, "queue种类需为: 0 300 600", user_id, group_id)
        return

    response_message = get_queue_stats(queue_name)
    await send_message(websocket, response_message, user_id, group_id)
    return

async def handle_leave_queue(websocket, message_text, user_id, group_id):
    await send_message(websocket, leave_queue(str(user_id)), user_id, group_id)
    return


@require_admin
async def handle_force_join_command(websocket, message_text, user_id, group_id):
    """处理强制加入queue"""
    parts = message_text.split()

    if len(parts) == 3:
        # 格式: =fjoin @用户 600
        qq = str(extract_qq(parts[1]))
        queue_name = parts[2]

        # 检查玩家是否存在
        player_data = PlayerUtils.get_player_data(qq)
        if not player_data:
            response_msg = f"未找到QQ号为 {qq} 的玩家数据"
            await send_message(websocket, response_msg, user_id, group_id)
            return

        if queue_name in ["0", "300", "600"]:
            response_message = join_queue(qq, queue_name, True)
            await send_message(websocket, response_message, user_id, group_id)
            return
        else:
            await send_message(websocket, "queue种类需为: 0 300 600", user_id, group_id)
            return

    elif len(parts) == 2:
        # 格式: =fjoin @用户
        qq = str(extract_qq(parts[1]))

        # 检查玩家是否存在
        player_data = PlayerUtils.get_player_data(qq)
        if not player_data:
            response_msg = f"未找到QQ号为 {qq} 的玩家数据"
            await send_message(websocket, response_msg, user_id, group_id)
            return

        queue_name = EloUtils.get_max_queue(PlayerUtils.get_elo(qq))
        response_message = join_queue(qq, queue_name, True)
        await send_message(websocket, response_message, user_id, group_id)
        return

    else:
        # 格式: =fjoin (管理员自己加入)
        qq_str = str(user_id)

        # 检查玩家是否存在
        player_data = PlayerUtils.get_player_data(qq_str)
        if not player_data:
            response_msg = f"未找到QQ号为 {qq_str} 的玩家数据"
            await send_message(websocket, response_msg, user_id, group_id)
            return

        queue_name = EloUtils.get_max_queue(PlayerUtils.get_elo(qq_str))
        response_message = join_queue(qq_str, queue_name, True)
        await send_message(websocket, response_message, user_id, group_id)
        return