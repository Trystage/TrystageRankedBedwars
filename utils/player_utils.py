import json
from typing import Dict, Any
from utils.file_utils import FileUtils


class PlayerUtils:
    """玩家工具类，用于处理玩家数据的各种操作"""

    @staticmethod
    def get_player_data(player_id: str) -> Dict[str, Any]:
        """
        获取玩家数据
        
        Args:
            player_id (str): 玩家ID
            
        Returns:
            Dict[str, Any]: 玩家数据
        """
        return FileUtils.get_player_data(player_id)

    @staticmethod
    def set_elo(player_id: str, elo: int) -> None:
        """
        设置玩家ELO分数
        
        Args:
            player_id (str): 玩家ID
            elo (int): 新的ELO分数
        """
        FileUtils.update_player_stats(player_id, elo=elo)

    @staticmethod
    def set_wins(player_id: str, wins: int) -> None:
        """
        设置玩家胜利次数
        
        Args:
            player_id (str): 玩家ID
            wins (int): 胜利次数
        """
        FileUtils.update_player_stats(player_id, wins=wins)

    @staticmethod
    def add_wins(player_id: str, count: int = 1) -> None:
        """
        增加玩家胜利次数
        
        Args:
            player_id (str): 玩家ID
            count (int): 增加的胜利次数，默认为1
        """
        player_data = FileUtils.get_player_data(player_id)
        new_wins = player_data["wins"] + count
        FileUtils.update_player_stats(player_id, wins=new_wins)

    @staticmethod
    def add_losses(player_id: str, count: int = 1) -> None:
        """
        增加玩家失败次数
        
        Args:
            player_id (str): 玩家ID
            count (int): 增加的失败次数，默认为1
        """
        player_data = FileUtils.get_player_data(player_id)
        new_losses = player_data["losses"] + count
        FileUtils.update_player_stats(player_id, losses=new_losses)

    @staticmethod
    def set_ign(player_id: str, ign: str) -> None:
        """
        设置玩家游戏内名称(IGN)
        
        Args:
            player_id (str): 玩家ID
            ign (str): 游戏内名称
        """
        FileUtils.update_player_stats(player_id, ign=ign)

    @staticmethod
    def update_nickname(player_id: str, nickname: str) -> None:
        """
        更新玩家昵称
        注意：获取玩家昵称的功能需要另外实现，这里只提供更新功能
        
        Args:
            player_id (str): 玩家ID
            nickname (str): 新昵称
        """
        FileUtils.update_player_stats(player_id, nickname=nickname)

    @staticmethod
    def set_xp(player_id: str, xp: int) -> None:
        """
        设置玩家经验值
        
        Args:
            player_id (str): 玩家ID
            xp (int): 经验值
        """
        FileUtils.update_player_stats(player_id, xp=xp)

    @staticmethod
    def add_xp(player_id: str, xp: int) -> None:
        """
        增加玩家经验值
        
        Args:
            player_id (str): 玩家ID
            xp (int): 要增加的经验值
        """
        player_data = FileUtils.get_player_data(player_id)
        new_xp = player_data["xp"] + xp
        FileUtils.update_player_stats(player_id, xp=new_xp)

    @staticmethod
    def set_mvps(player_id: str, mvps: int) -> None:
        """
        设置玩家MVP次数
        
        Args:
            player_id (str): 玩家ID
            mvps (int): MVP次数
        """
        FileUtils.update_player_stats(player_id, mvps=mvps)

    @staticmethod
    def add_mvps(player_id: str, count: int = 1) -> None:
        """
        增加玩家MVP次数
        
        Args:
            player_id (str): 玩家ID
            count (int): 增加的MVP次数，默认为1
        """
        player_data = FileUtils.get_player_data(player_id)
        new_mvps = player_data["mvps"] + count
        FileUtils.update_player_stats(player_id, mvps=new_mvps)

    @staticmethod
    def get_player_stats(player_id: str) -> Dict[str, Any]:
        """
        获取玩家完整统计数据
        
        Args:
            player_id (str): 玩家ID
            
        Returns:
            Dict[str, Any]: 玩家完整统计数据
        """
        return FileUtils.get_player_data(player_id)

    @staticmethod
    def save_player_data(player_id: str, player_data: Dict[str, Any]) -> None:
        """
        保存玩家数据（直接保存完整的玩家数据）
        
        Args:
            player_id (str): 玩家ID
            player_data (Dict[str, Any]): 玩家数据
        """
        FileUtils.save_player_data(player_id, player_data)