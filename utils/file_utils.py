import json
import os
from typing import List, Dict, Any
from config import PROJECT_ROOT

# 定义数据文件路径
DATA_DIR = PROJECT_ROOT / "data"
GROUPS_FILE = DATA_DIR / "groups.json"
PLAYERS_FILE = DATA_DIR / "players.json"


class FileUtils:
    """文件工具类，用于处理群组ID等数据的持久化存储"""

    @staticmethod
    def initialize_data_files():
        """初始化数据文件"""
        # 确保数据目录存在
        os.makedirs(DATA_DIR, exist_ok=True)
        
        # 如果群组文件不存在，创建默认文件
        if not os.path.exists(GROUPS_FILE):
            default_data = {
                "rbw_group_ids": [695789887],
                "admins": [3289138258, 728722384, 3654280169, 2257104941]
            }
            FileUtils.save_groups_data(default_data)
            
        # 如果玩家数据文件不存在，创建空文件
        if not os.path.exists(PLAYERS_FILE):
            FileUtils.save_players_data({})

    @staticmethod
    def load_groups_data() -> Dict[str, Any]:
        """加载群组数据"""
        FileUtils.initialize_data_files()
        try:
            with open(GROUPS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或解析失败，返回默认数据
            default_data = {
                "rbw_group_ids": [695789887],
                "admins": [3289138258, 728722384, 3654280169, 2257104941]
            }
            FileUtils.save_groups_data(default_data)
            return default_data

    @staticmethod
    def save_groups_data(data: Dict[str, Any]) -> None:
        """保存群组数据到文件"""
        # 确保数据目录存在
        os.makedirs(DATA_DIR, exist_ok=True)
        
        groups_file_path = os.path.join(DATA_DIR, GROUPS_FILE)
        with open(groups_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_rbw_group_ids() -> List[int]:
        """获取需要处理入群事件的群组ID列表"""
        data = FileUtils.load_groups_data()
        return data.get("rbw_group_ids", [])

    @staticmethod
    def add_rbw_group_id(group_id: int):
        """添加入群事件处理群组ID"""
        data = FileUtils.load_groups_data()
        if group_id not in data["rbw_group_ids"]:
            data["rbw_group_ids"].append(group_id)
            FileUtils.save_groups_data(data)

    @staticmethod
    def remove_rbw_group_id(group_id: int):
        """移除入群事件处理群组ID"""
        data = FileUtils.load_groups_data()
        if group_id in data["rbw_group_ids"]:
            data["rbw_group_ids"].remove(group_id)
            FileUtils.save_groups_data(data)

    @staticmethod
    def get_admins() -> List[int]:
        """获取需要处理入群事件的群组ID列表"""
        data = FileUtils.load_groups_data()
        return data.get("admins", [])

    @staticmethod
    def add_admin(group_id: int):
        """添加入群事件处理群组ID"""
        data = FileUtils.load_groups_data()
        if group_id not in data["admins"]:
            data["admins"].append(group_id)
            FileUtils.save_groups_data(data)

    @staticmethod
    def remove_admin(group_id: int):
        """移除入群事件处理群组ID"""
        data = FileUtils.load_groups_data()
        if group_id in data["admins"]:
            data["admins"].remove(group_id)
            FileUtils.save_groups_data(data)

    @staticmethod
    def load_players_data() -> Dict[str, Any]:
        """加载玩家数据"""
        FileUtils.initialize_data_files()
        try:
            with open(PLAYERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或解析失败，返回空数据
            FileUtils.save_players_data({})
            return {}

    @staticmethod
    def save_players_data(data: Dict[str, Any]) -> None:
        """保存玩家数据到文件"""
        # 确保数据目录存在
        os.makedirs(DATA_DIR, exist_ok=True)
        
        with open(PLAYERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def get_player_data(player_id: str) -> Dict[str, Any]:
        """获取指定玩家的数据"""
        players_data = FileUtils.load_players_data()
        return players_data.get(player_id, {
            "nickname": "",
            "ign": "",
            "elo": 1000,
            "wins": 0,
            "losses": 0,
            "mvps": 0
        })

    @staticmethod
    def save_player_data(player_id: str, player_data: Dict[str, Any]) -> None:
        """保存指定玩家的数据"""
        players_data = FileUtils.load_players_data()
        players_data[player_id] = player_data
        FileUtils.save_players_data(players_data)

    @staticmethod
    def update_player_stats(player_id: str, nickname: str = "", ign: str = "", elo: int = None, 
                           wins: int = None, losses: int = None, mvps: int = None,
                           strikes: int = None, games: int = None) -> None:
        """更新玩家统计数据"""
        player_data = FileUtils.get_player_data(player_id)
        
        # 更新提供的字段
        if nickname:
            player_data["nickname"] = nickname
        if ign:
            player_data["ign"] = ign
        if elo is not None:
            player_data["elo"] = elo
        if wins is not None:
            player_data["wins"] = wins
        if losses is not None:
            player_data["losses"] = losses
        if mvps is not None:
            player_data["mvps"] = mvps
        if strikes is not None:
            player_data["strikes"] = strikes
        if games is not None:
            player_data["games"] = games
            
        FileUtils.save_player_data(player_id, player_data)