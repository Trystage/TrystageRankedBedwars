from config import RESOURCE_DIR
from utils.websocket_utils import get_image


class EloUtils:
    # 段位等级定义
    # Coal（煤炭）：0-400 ELO
    # Iron（铁）：400-800 ELO
    # Gold（金）：800-1200 ELO
    # Platinum（铂金）：1200-1600 ELO
    # Emerald（绿宝石）：1600-1800 ELO
    # Diamond（钻石）：1800-2000 ELO
    # Obsidian（黑曜石）：2000+ ELO
    
    @staticmethod
    def to_division(elo: int):
        """
        根据ELO分数转换为对应的段位
        
        Args:
            elo (int): ELO分数
            
        Returns:
            str: 对应的段位名称
        """
        if 0 <= elo < 400:
            return "Coal"
        elif 400 <= elo < 800:
            return "Iron"
        elif 800 <= elo < 1200:
            return "Gold"
        elif 1200 <= elo < 1600:
            return "Platinum"
        elif 1600 <= elo < 1800:
            return "Emerald"
        elif 1800 <= elo < 2000:
            return "Diamond"
        elif elo >= 2000:
            return "Obsidian"
        else:
            # 默认返回Coal段位（处理负数情况）
            return "Coal"
    @staticmethod
    def get_division_icon(division: str) -> str:
        if division == "Coal":
            return get_image(RESOURCE_DIR + "/divisions/Coal.png")
        elif division == "Iron":
            return get_image(RESOURCE_DIR + "/divisions/Iron.png")
        elif division == "Gold":
            return get_image(RESOURCE_DIR + "/divisions/Gold.png")
        elif division == "Platinum":
            return get_image(RESOURCE_DIR + "/divisions/Platinum.png")
        elif division == "Emerald":
            return get_image(RESOURCE_DIR + "/divisions/Emerald.png")
        elif division == "Diamond":
            return get_image(RESOURCE_DIR + "/divisions/Diamond.png")
        elif division == "Obsidian":
            return get_image(RESOURCE_DIR + "/divisions/Obsidian.png")
        else:
            return get_image(RESOURCE_DIR + "/divisions/Crying_Obsidian.png")
