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
    return f"玩家 {qq} 加入队列成功！当前位置：{position}"


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


def get_queue_status(qq: str = None, queue: str = None) -> str:
    """
    获取队列状态

    Args:
        qq: 可选，指定玩家QQ号
        queue: 可选，指定队列类型 "0", "300", "600"

    Returns:
        队列状态字符串，格式：qq - ign - elo
    """
    # 检查参数
    if qq is None and queue is None:
        return "请指定queue类型"

    # 辅助函数：获取玩家信息字符串
    def get_player_info(player_qq: str) -> str:
        """获取单个玩家的信息字符串：qq - ign - elo"""
        player_data = PlayerUtils.get_player_data(player_qq)
        if not player_data:
            return f"{player_qq} - 数据缺失 - 数据缺失"

        ign = player_data.get("minecraft", {}).get("ign", "Unknown")
        elo = player_data.get("elo", -1)
        return f"{player_qq} - {ign} - {elo}"

    # 情况1：指定queue类型，显示该队列所有玩家
    if queue is not None:
        if queue == "0":
            queue_list = queue0
            queue_name = "0级队列"
        elif queue == "300":
            queue_list = queue300
            queue_name = "300级队列"
        elif queue == "600":
            queue_list = queue600
            queue_name = "600级队列"
        else:
            return f"错误的队列类型: {queue}"

        if not queue_list:
            return f"{queue_name} 为空"

        response = f"{queue_name} 中的所有玩家：\n"
        for i, player_qq in enumerate(queue_list, 1):
            player_info = get_player_info(player_qq)
            response += f"  {i}. {player_info}\n"

        return response

    # 情况2：指定qq，显示该玩家所在的队列所有玩家
    if qq is not None:
        # 查找玩家在哪个队列
        if qq in queue0:
            queue_list = queue0
            queue_name = "0级队列"
        elif qq in queue300:
            queue_list = queue300
            queue_name = "300级队列"
        elif qq in queue600:
            queue_list = queue600
            queue_name = "600级队列"
        else:
            return f"请指定queue类型"

        # 显示该队列所有玩家
        response = f"玩家 {get_player_info(qq)} 所在的 {queue_name}：\n"
        for i, player_qq in enumerate(queue_list, 1):
            player_info = get_player_info(player_qq)
            # 标记当前查询的玩家
            marker = " <- 您" if player_qq == qq else ""
            response += f"  {i}. {player_info}{marker}\n"

        return response

    # 不应该执行到这里
    return "参数错误"