from games.queue import join_queue, get_queue_stats, get_user_queue, leave_queue
from utils.elo_utils import EloUtils
from utils.permission_utils import require_admin
from utils.player_utils import PlayerUtils
from utils.websocket_utils import send_message, extract_qq


async def handle_join_command(websocket, message_text, user_id, group_id):
    """处理加入queue"""
    parts = message_text.split()
    if len(parts) == 2:
        queue_name = parts[1]
        if queue_name in ["0", "300", "600"]:
            response_message = join_queue(user_id, queue_name)
            await send_message(websocket, response_message, user_id, group_id)
            return
        else:
            await send_message(websocket, "queue种类需为: 0 300 600", user_id, group_id)
            return

    queue_name = EloUtils.get_max_queue(PlayerUtils.get_elo(user_id))
    join_queue(user_id, queue_name)
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
    queue_name = get_user_queue(user_id)

    if queue_name == "None":
        await send_message(websocket, "queue种类需为: 0 300 600", user_id, group_id)
        return

    response_message = get_queue_stats(queue_name)
    await send_message(websocket, response_message, user_id, group_id)
    return

async def handle_leave_queue(websocket, message_text, user_id, group_id):
    await send_message(websocket, leave_queue(user_id), user_id, group_id)
    return


@require_admin
async def handle_force_join_command(websocket, message_text, user_id, group_id):
    """处理加入queue"""
    parts = message_text.split()
    if len(parts) == 3:
        qq = extract_qq(parts[1])
        queue_name = parts[2]
        if queue_name in ["0", "300", "600"]:
            response_message = join_queue(qq, queue_name, True)
            await send_message(websocket, response_message, user_id, group_id)
            return
        else:
            await send_message(websocket, "queue种类需为: 0 300 600", user_id, group_id)
            return
    elif len(parts) == 2:
        qq = extract_qq(parts[1])
        queue_name = EloUtils.get_max_queue(PlayerUtils.get_elo(qq))
        response_message = join_queue(qq, queue_name, True)
        await send_message(websocket, response_message, user_id, group_id)
        return
    else:
        queue_name = EloUtils.get_max_queue(PlayerUtils.get_elo(user_id))
        join_queue(user_id, queue_name, True)
        return