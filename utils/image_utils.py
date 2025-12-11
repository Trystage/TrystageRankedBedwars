import os
import requests
from io import BytesIO

from config import CACHE_DIR, FONT_FILE, RESOURCE_DIR, SKIN_URL
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
        mvp_count = player_data.get("mvps", -1)
        wins = player_data.get("wins", -1)
        losses = player_data.get("losses", -1)
        ign = player_data.get("minecraft", {}).get("ign", "Unknown")
        elo = player_data.get("elo", -1)

        if mvp_count == -1 or wins == -1 or losses == -1 or ign == "Unknown" or elo == -1:
            return ImageUtils.text_to_image(f"未找到玩家: {qq},该玩家未注册")
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
                skin_url = SKIN_URL.replace("{uuid}", uuid)
                response = requests.get(skin_url, timeout=5)
                if response.status_code == 200:
                    skin_image = Image.open(BytesIO(response.content)).convert("RGBA")
                    # 调整皮肤图片大小
                    skin_image = skin_image.resize((160, 360), Image.Resampling.LANCZOS)
            except Exception as e:
                print(f"获取皮肤图片失败: {e}")
        
        # 在基础图片上绘制文本和图像
        draw = ImageDraw.Draw(base_image)
        
        # 加载字体
        font_large = ImageFont.truetype(FONT_FILE, 50)
        font_medium = ImageFont.truetype(FONT_FILE, 44)
        font_small = ImageFont.truetype(FONT_FILE, 32)
        
        # 绘制玩家IGN（居中显示）
        # 获取文本边界框以计算居中位置
        bbox = draw.textbbox((0, 0), f"{ign}", font=font_medium)
        text_width = bbox[2] - bbox[0]
        # 居中计算：(图片宽度 - 文本宽度) / 2
        center_x = int(280 - (text_width // 2))
        draw.text((center_x, 130), f"{ign}", font=font_medium, fill=(255, 255, 255))
        
        # 根据玩家ELO获取段位并加载对应图标
        from utils.elo_utils import EloUtils
        division = EloUtils.to_division(elo)
        division_icon_path = EloUtils.get_division_icon(division)
        
        # 加载并绘制段位图标
        try:
            division_icon = Image.open(division_icon_path).convert("RGBA")
            # 调整图标大小
            division_icon = division_icon.resize((160, 160), Image.Resampling.LANCZOS)
            # 将图标粘贴到图片上（放在IGN下方）
            icon_x, icon_y = 640, 130
            base_image.paste(division_icon, (icon_x, icon_y), division_icon)
            
            # 在段位图标上方绘制段位名称（居中）
            division_bbox = draw.textbbox((0, 0), division, font=font_medium)
            division_width = division_bbox[2] - division_bbox[0]
            division_x = icon_x + (160 - division_width) // 2  # 图标中心对齐
            division_y = icon_y - 30  # 图标上方30像素
            draw.text((division_x, division_y), division, font=font_medium, fill=(255, 255, 255))
            
            # 在段位图标右侧绘制ELO和具体数值（都居中）
            # ELO文字
            elo_label_bbox = draw.textbbox((0, 0), "ELO", font=font_medium)
            elo_label_width = elo_label_bbox[2] - elo_label_bbox[0]
            elo_label_x = icon_x + 180 + 80 - (elo_label_width // 2)
            elo_label_y = icon_y - 20  # 图标上方部分
            draw.text((elo_label_x, elo_label_y), "ELO", font=font_medium, fill=(255, 255, 255))
            
            # ELO数值
            elo_value_bbox = draw.textbbox((0, 0), str(elo), font=font_medium)
            elo_value_width = elo_value_bbox[2] - elo_value_bbox[0]
            elo_value_x = icon_x + 180 + 80 - (elo_value_width // 2)
            elo_value_y = icon_y + 60  # 图标下方部分
            draw.text((elo_value_x, elo_value_y), str(elo), font=font_medium, fill=(255, 255, 255))
        except Exception as e:
            print(f"加载段位图标失败: {e}")
        
        # 绘制统计数据（左对齐和右对齐）
        # 定义统计数据区域
        stats_area_x_start = 625
        stats_area_x_end = 975
        stats_area_y_start = 410
        stats_area_y_end = 640
        
        # 计算行高和起始Y位置
        line_height = (stats_area_y_end - stats_area_y_start) / 4
        start_y = stats_area_y_start
        
        # 左对齐的标签
        labels = ["MVPs:", "Wins:", "Losses:", "W/L Ratio:"]
        values = [str(mvp_count), str(wins), str(losses), str(wlr)]
        
        # 绘制左对齐的标签
        for i, label in enumerate(labels):
            y_position = start_y + (i * line_height)
            draw.text((stats_area_x_start, y_position), label, font=font_small, fill=(255, 255, 255))
        
        # 绘制右对齐的数值
        for i, value in enumerate(values):
            # 获取文本宽度以计算右对齐位置
            bbox = draw.textbbox((0, 0), value, font=font_small)
            text_width = bbox[2] - bbox[0]
            x_position = stats_area_x_end - text_width
            y_position = start_y + (i * line_height)
            draw.text((x_position, y_position), value, font=font_small, fill=(255, 255, 255))
        
        # 如果获取到了皮肤图片，则将其粘贴到图片上
        if skin_image:
            # 将皮肤图片粘贴到右上角位置
            base_image.paste(skin_image, (200, 220), skin_image)
        
        # 构建完整文件路径
        filepath = os.path.join(CACHE_DIR, f"stat_{qq}.png")
        
        # 保存图片
        base_image.save(filepath, "PNG")
        
        return filepath