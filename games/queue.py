from utils.player_utils import PlayerUtils


queue0: list[str] = []
queue300: list[str] = []
queue600: list[str] = []

def join_queue(qq: str, queue_type: str = "0", force: bool = False):
    player_data = PlayerUtils.get_player_data(qq)
    if not player_data:
        return f"未找到QQ号为 {qq} 的玩家数据"

    if player_data.get("strikes") >= 2:
        return f"{qq} 已被封禁"

    if qq in queue0 or qq in queue300 or qq in queue600:
        return f"{qq} 已经在queue中了"
    current_queue = None
    if queue_type == "0":
        if player_data.get("elo") >= 0 or force:
            current_queue = queue0
        else:
            return f"elo不足, 无法加入queue"
    elif queue_type == "300":
        if player_data.get("elo") >= 300 or force:
            current_queue = queue300
        else:
            return f"elo不足, 无法加入queue"
    elif queue_type == "600":
        if player_data.get("elo") >= 600 or force:
            current_queue = queue600
        else:
            return f"elo不足, 无法加入queue"

    if current_queue is None:
        return f"Illegal queue type: {queue_type}"

    current_queue.append(qq)

    if len(current_queue) >= 8:
        current_queue_player = current_queue[:8]

        #ToDo: start gaming

        return f"创建游戏中: {current_queue_player}"

    position = len(current_queue)

    response = f"玩家 {player_data["minecraft"]["ign"]} 加入队列成功！\n当前位置：{position}\n"
    response += get_queue_stats(queue_type)
    return response


def leave_queue(qq: str) -> str:
    """
    离开队列

    Args:
        qq: 玩家QQ号

    Returns:
        返回消息字符串
    """
    # 检查是否在queue0中
    if qq in queue0:
        queue0.remove(qq)  # 从列表中移除这个QQ号
        return f"玩家 {qq} 已从 0级队列 离开"

    # 检查是否在queue300中
    if qq in queue300:
        queue300.remove(qq)
        return f"玩家 {qq} 已从 300级队列 离开"

    # 检查是否在queue600中
    if qq in queue600:
        queue600.remove(qq)
        return f"玩家 {qq} 已从 600级队列 离开"

    # 如果都不在队列中
    return f"玩家 {qq} 不在任何队列中"


def get_queue_stats(queue: str) -> str:
    """
    获取队列统计信息（简洁版）

    Args:
        queue: 队列类型 "0", "300", "600"

    Returns:
        简洁的统计信息表格：IGN | elo | wins | looses | MVPs（按elo排序）
    """
    # 检查队列类型是否有效
    if queue not in ["0", "300", "600"]:
        return "无效的queue类型，需要为 0、300 或 600"

    queue_list = None
    queue_name = None

    # 确定要显示的队列
    if queue == "0":
        queue_list = queue0
        queue_name = "0+"
    elif queue == "300":
        queue_list = queue300
        queue_name = "300+"
    elif queue == "600":
        queue_list = queue600
        queue_name = "600+"

    # 检查队列是否为空
    if not queue_list:
        return f"queue {queue_name} 为空"

    # 收集玩家统计信息（包括elo）
    player_stats = []

    for qq in queue_list:
        player_data = PlayerUtils.get_player_data(qq)
        if not player_data:
            ign = "数据缺失"
            elo = 0
            wins = 0
            losses = 0
            mvps = 0
        else:
            ign = player_data.get("minecraft", {}).get("ign", "Unknown")
            elo = player_data.get("elo", 0)
            wins = player_data.get("wins", 0)
            losses = player_data.get("losses", 0)
            mvps = player_data.get("mvps", 0)

        player_stats.append((ign, elo, wins, losses, mvps))

    # 按照elo从高到低排序
    player_stats.sort(key=lambda x: x[1], reverse=True)

    # 计算列宽
    max_ign_len = max(len(str(stat[0])) for stat in player_stats)
    max_elo_len = max(len(str(stat[1])) for stat in player_stats)
    max_wins_len = max(len(str(stat[2])) for stat in player_stats)
    max_losses_len = max(len(str(stat[3])) for stat in player_stats)
    max_mvps_len = max(len(str(stat[4])) for stat in player_stats)

    # 表头宽度
    ign_width = max(max_ign_len, 6) + 2  # "IGN" 长度
    elo_width = max(max_elo_len, 3) + 2  # "elo" 长度
    wins_width = max(max_wins_len, 3) + 2  # "wins" 长度
    losses_width = max(max_losses_len, 4) + 2  # "looses" 长度
    mvps_width = max(max_mvps_len, 4) + 2  # "MVPs" 长度

    # 构建表格
    response = f"Queue {queue_name} :\n"

    # 表头
    header = f"{'IGN':<{ign_width}}|{'elo':<{elo_width}}|{'Win':<{wins_width}}|{'Loss':<{losses_width}}|{'MVPs':<{mvps_width}}"
    response += header + "\n"
    response += "-" * len(header) + "\n"

    # 数据行
    for ign, elo, wins, losses, mvps in player_stats:
        row = f"{ign:<{ign_width}}|{elo:<{elo_width}}|{wins:<{wins_width}}|{losses:<{losses_width}}|{mvps:<{mvps_width}}"
        response += row + "\n"

    return response

def get_user_queue(qq:str) -> str:
    if qq in queue0:
        return "0"
    elif qq in queue300:
        return "300"
    elif qq in queue600:
        return "600"
    else:
        return "None"