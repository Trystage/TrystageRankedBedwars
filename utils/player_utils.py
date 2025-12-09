import json
from typing import Dict, Any
from utils.file_utils import FileUtils
from utils.uuid_utils import UUIDUtils
from datetime import datetime


class PlayerUtils:
    """玩家工具类，用于处理玩家数据的各种操作"""

    @staticmethod
    def add_player_raw(qq: str, ign: str, uuid: str, skin: str = "", nickname: str = "") -> None:
        """
        添加新玩家并初始化数据结构
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            nickname (str): 玩家昵称
            ign (str): 游戏内昵称
            uuid (str): 游戏内UUID
            skin (str): 皮肤UUID
        """
        # 格式化UUID为带连字符的标准格式
        formatted_uuid = UUIDUtils.format_uuid(uuid)
        
        if skin == "":
            skin = formatted_uuid
        else:
            # 也格式化皮肤UUID
            skin = UUIDUtils.format_uuid(skin)

        player_data = {
            "nickname": nickname,
            "minecraft": {
                "ign": ign,
                "uuid": formatted_uuid,
            },
            "elo": 0,
            "strikes": 0,
            "games": 0,
            "wins": 0,
            "losses": 0,
            "mvps": 0,
            "registeredAt": datetime.now().isoformat(),
            "skin": skin,
        }
        FileUtils.save_player_data(qq, player_data)

    @staticmethod
    def get_player_data(qq: str) -> Dict[str, Any]:
        """
        获取玩家数据
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            Dict[str, Any]: 玩家数据
        """
        players_data = FileUtils.load_players_data()
        return players_data.get(qq, {})

    @staticmethod
    def set_minecraft(qq: str, key: str, value: str) -> None:
        """
        设置玩家Minecraft信息
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            key (str): Minecraft信息键名 ("ign" 或 "uuid")
            value (str): 对应的值
        """
        player_data = FileUtils.get_player_data(qq)
        if "minecraft" not in player_data:
            player_data["minecraft"] = {"ign": "", "uuid": ""}
        player_data["minecraft"][key] = value
        FileUtils.save_player_data(qq, player_data)

    @staticmethod
    def set_elo(qq: str, elo: int) -> None:
        """
        设置玩家ELO分数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            elo (int): 新的ELO分数
        """
        FileUtils.update_player_stats(qq, elo=elo)

    @staticmethod
    def get_elo(qq: str) -> int:
        """
        获取玩家ELO分数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            int: 玩家ELO分数
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("elo", 1000)

    @staticmethod
    def add_elo(qq: str, elo: int) -> None:
        """
        增加玩家ELO分数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            elo (int): 要增加的ELO分数
        """
        current_elo = PlayerUtils.get_elo(qq)
        PlayerUtils.set_elo(qq, current_elo + elo)

    @staticmethod
    def set_strikes(qq: str, strikes: int) -> None:
        """
        设置玩家违规次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            strikes (int): 违规次数
        """
        FileUtils.update_player_stats(qq, strikes=strikes)

    @staticmethod
    def get_strikes(qq: str) -> int:
        """
        获取玩家违规次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            int: 玩家违规次数
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("strikes", 0)

    @staticmethod
    def add_strikes(qq: str, strikes: int = 1) -> None:
        """
        增加玩家违规次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            strikes (int): 要增加的违规次数，默认为1
        """
        current_strikes = PlayerUtils.get_strikes(qq)
        PlayerUtils.set_strikes(qq, current_strikes + strikes)

    @staticmethod
    def set_games(qq: str, games: int) -> None:
        """
        设置玩家游戏场次
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            games (int): 游戏场次
        """
        FileUtils.update_player_stats(qq, games=games)

    @staticmethod
    def get_games(qq: str) -> int:
        """
        获取玩家游戏场次
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            int: 玩家游戏场次
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("games", 0)

    @staticmethod
    def add_games(qq: str, games: int = 1) -> None:
        """
        增加玩家游戏场次
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            games (int): 要增加的游戏场次，默认为1
        """
        current_games = PlayerUtils.get_games(qq)
        PlayerUtils.set_games(qq, current_games + games)

    @staticmethod
    def set_wins(qq: str, wins: int) -> None:
        """
        设置玩家胜利次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            wins (int): 胜利次数
        """
        FileUtils.update_player_stats(qq, wins=wins)

    @staticmethod
    def get_wins(qq: str) -> int:
        """
        获取玩家胜利次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            int: 玩家胜利次数
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("wins", 0)

    @staticmethod
    def add_wins(qq: str, count: int = 1) -> None:
        """
        增加玩家胜利次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            count (int): 增加的胜利次数，默认为1
        """
        current_wins = PlayerUtils.get_wins(qq)
        PlayerUtils.set_wins(qq, current_wins + count)

    @staticmethod
    def set_losses(qq: str, losses: int) -> None:
        """
        设置玩家失败次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            losses (int): 失败次数
        """
        FileUtils.update_player_stats(qq, losses=losses)

    @staticmethod
    def get_losses(qq: str) -> int:
        """
        获取玩家失败次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            int: 玩家失败次数
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("losses", 0)

    @staticmethod
    def add_losses(qq: str, count: int = 1) -> None:
        """
        增加玩家失败次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            count (int): 增加的失败次数，默认为1
        """
        current_losses = PlayerUtils.get_losses(qq)
        PlayerUtils.set_losses(qq, current_losses + count)

    @staticmethod
    def set_nickname(qq: str, nickname: str) -> None:
        """
        设置玩家昵称
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            nickname (str): 玩家昵称
        """
        FileUtils.update_player_stats(qq, nickname=nickname)

    @staticmethod
    def get_nickname(qq: str) -> str:
        """
        获取玩家昵称
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            str: 玩家昵称
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("nickname", "")

    @staticmethod
    def set_ign(qq: str, ign: str) -> None:
        """
        设置玩家游戏内名称(IGN)
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            ign (str): 游戏内名称
        """
        PlayerUtils.set_minecraft(qq, "ign", ign)

    @staticmethod
    def get_ign(qq: str) -> str:
        """
        获取玩家游戏内名称(IGN)
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            str: 玩家游戏内名称
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("minecraft", {}).get("ign", "")

    @staticmethod
    def set_uuid(qq: str, uuid: str) -> None:
        """
        设置玩家UUID
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            uuid (str): 玩家UUID
        """
        # 格式化UUID为带连字符的标准格式
        formatted_uuid = UUIDUtils.format_uuid(uuid)
        PlayerUtils.set_minecraft(qq, "uuid", formatted_uuid)

    @staticmethod
    def get_uuid(qq: str) -> str:
        """
        获取玩家UUID
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            str: 玩家UUID
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("minecraft", {}).get("uuid", "")

    @staticmethod
    def set_mvps(qq: str, mvps: int) -> None:
        """
        设置玩家MVP次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            mvps (int): MVP次数
        """
        FileUtils.update_player_stats(qq, mvps=mvps)

    @staticmethod
    def get_mvps(qq: str) -> int:
        """
        获取玩家MVP次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            
        Returns:
            int: 玩家MVP次数
        """
        player_data = FileUtils.get_player_data(qq)
        return player_data.get("mvps", 0)

    @staticmethod
    def add_mvps(qq: str, count: int = 1) -> None:
        """
        增加玩家MVP次数
        
        Args:
            qq (str): 玩家QQ号（作为玩家ID）
            count (int): 增加的MVP次数，默认为1
        """
        current_mvps = PlayerUtils.get_mvps(qq)
        PlayerUtils.set_mvps(qq, current_mvps + count)

    @staticmethod
    def get_player(ign: str) -> Dict[str, Any]:
        """
        通过游戏内名称(IGN)获取玩家数据

        Args:
            ign (str): 游戏内名称

        Returns:
            Dict[str, Any]: 包含玩家QQ号和数据的字典，格式为 {"qq": qq_number, "data": player_data}
                          如果未找到则返回空字典
        """
        # 获取所有玩家数据
        players_data = FileUtils.load_players_data()

        # 遍历所有玩家查找匹配的IGN
        for player_id, player_data in players_data.items():
            if player_data.get("minecraft", {}).get("ign", "").lower() == ign.lower():
                return player_data

        # 如果未找到匹配的玩家，返回空字典
        return {}