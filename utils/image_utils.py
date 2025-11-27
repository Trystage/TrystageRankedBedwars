import os

from config import CACHE_DIR, FONT_FILE
from PIL import Image,ImageDraw,ImageFont

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