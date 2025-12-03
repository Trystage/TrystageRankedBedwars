import os
import requests
from io import BytesIO

from config import CACHE_DIR, FONT_FILE, RESOURCE_DIR
from PIL import Image, ImageDraw, ImageFont
from utils.player_utils import PlayerUtils


class ImageUtils:
    @staticmethod
    def text_to_image(text: str):
        """文字转图片并保存到缓存目录,来自Chikari Yinpa

        Args:
            text (str): 要转换的文字

        Returns:
            str: 图片文件路径
        """
        # 确保缓存目录存在
        os.makedirs(CACHE_DIR, exist_ok=True)

        fontSize = 20
        lines = text.split('\n')
        max_len = 0
        for line in lines:
            max_len = max(len(line), max_len)

        image = Image.new("RGB", ((fontSize * max_len), len(lines) * (fontSize + 5)), (255, 255, 255))
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype(FONT_FILE, fontSize)
        draw.text((0, 0), text, font=font, fill="#000000", stroke_width=0)

        # 构建完整文件路径
        filepath = os.path.join(CACHE_DIR, "image.png")

        # 保存图片
        image.save(filepath, "PNG")

        return filepath

    @staticmethod
    def generate_stat(qq: int):
        """生成玩家统计数据图片
        
        Args:
            qq (int): 玩家QQ号
            
        Returns:
            str: 生成的图片文件路径
        """
        
        # 获取玩家数据
        qq_str = str(qq)
        player_data = PlayerUtils.get_player_data(qq_str)
        
        # 提取所需数据
        mvp_count = player_data.get("mvps", 0)
        wins = player_data.get("wins", 0)
        losses = player_data.get("losses", 0)
        ign = player_data.get("minecraft", {}).get("ign", "Unknown")
        
        # 计算WLR（胜率），保留两位小数
        if losses == 0:
            wlr = round(float(wins), 2) if wins > 0 else 0.0
        else:
            wlr = round(wins / losses, 2)
        
        # 获取玩家UUID并确保格式正确
        uuid = player_data.get("minecraft", {}).get("uuid", "")
        # 如果UUID存在但格式不正确，尝试格式化
        if uuid:
            try:
                from utils.uuid_utils import UUIDUtils
                uuid = UUIDUtils.format_uuid(uuid)
            except ValueError:
                # 如果格式化失败，保持原始值
                pass
        
        # 加载基础模板图片
        template_path = os.path.join(RESOURCE_DIR, "stat.png")
        base_image = Image.open(template_path)
        
        # 如果有UUID，则从网络获取皮肤图片
        skin_image = None
        if uuid:
            try:
                skin_url = f"https://api.mineatar.io/body/full/{uuid}"
                response = requests.get(skin_url, timeout=5)
                if response.status_code == 200:
                    skin_image = Image.open(BytesIO(response.content))
                    # 调整皮肤图片大小
                    skin_image = skin_image.resize((100, 200), Image.Resampling.LANCZOS)
            except Exception as e:
                print(f"获取皮肤图片失败: {e}")
        
        # 在基础图片上绘制文本和图像
        draw = ImageDraw.Draw(base_image)
        
        # 加载字体
        try:
            font_large = ImageFont.truetype(FONT_FILE, 36)
            font_medium = ImageFont.truetype(FONT_FILE, 24)
            font_small = ImageFont.truetype(FONT_FILE, 18)
        except Exception:
            # 如果无法加载自定义字体，则使用默认字体
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # 绘制玩家IGN
        draw.text((50, 30), f"Player: {ign}", font=font_large, fill=(255, 255, 255))
        
        # 绘制统计数据
        draw.text((50, 100), f"MVPs: {mvp_count}", font=font_medium, fill=(255, 255, 255))
        draw.text((50, 140), f"Wins: {wins}", font=font_medium, fill=(255, 255, 255))
        draw.text((50, 180), f"Losses: {losses}", font=font_medium, fill=(255, 255, 255))
        draw.text((50, 220), f"W/L Ratio: {wlr}", font=font_medium, fill=(255, 255, 255))
        
        # 如果获取到了皮肤图片，则将其粘贴到图片上
        if skin_image:
            # 将皮肤图片粘贴到右上角位置
            base_image.paste(skin_image, (base_image.width - 120, 30))
        
        # 构建完整文件路径
        filepath = os.path.join(CACHE_DIR, f"stat_{qq}.png")
        
        # 保存图片
        base_image.save(filepath, "PNG")
        
        return filepath