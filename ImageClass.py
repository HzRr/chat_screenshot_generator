from PIL import Image, ImageDraw, ImageFont
from typing import Union
import re
import os
import imgkit


frame_color = (237, 237, 237, 255)  # 框架背景色
frame_width = 760                   # 框架宽度
chat_height = 1275                  # 聊天记录高度
chat_offset = 166                   # 聊天记录偏移量
message_offset = 25                 # 消息位置偏移量

avatar_html_path = "htmls/avatar"               # 头像
SimpleText_html_path = "htmls/SimpleText"       # 他人单文本消息
SimpleText2_html_path = "htmls/SimpleText2"     # 本人单文本消息

def read_and_replace_html(replace_params_dict: dict, html_path: str) -> str:
    with open(html_path, "r", encoding="utf-8") as fp:
        html = fp.read()
    for key in replace_params_dict:
        pattern = f"/{key}/"
        html = re.sub(pattern, str(replace_params_dict[key]), html)
    return html

def generate_image_by_html(replace_params_dict: dict, html_path: str) -> Image.Image:
    html = read_and_replace_html(replace_params_dict, html_path)
    out_path = "user_images/temp.png"
    imgkit.from_string(html, out_path)
    return Image.open(out_path, "r")

def get_avatar_link_by_id(id: Union[str, int]) -> str:
    path = os.getcwd().replace("\\", "/") + f"/user_images/senders_images/avatar-{str(id)}.png"
    if not os.path.exists(path):
        path = os.getcwd().replace("\\", "/") + "/user_images/senders_images/avatar-default.png"
    return path

class BasicImage:

    def __init__(self, img_type: str, img_obj: Image.Image) -> None:
        self.img_type = img_type
        self.__image = img_obj
        self.size = self.__image.size
        self.width, self.height = self.__image.size
    
    def pasteto(self, obj: Image.Image, pos: tuple) -> None:
        """将self粘贴到传入对象obj上"""
        obj.paste(self.__image, box=pos)

    def show(self) -> None:
        self.__image.show()

    def get_img_obj(self) -> Image.Image:
        return self.__image

class SimpleText(BasicImage):
    """单文本消息"""
    def __init__(self, information: dict) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="单文本消息", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        w, h = 90, 90   # 头像尺寸
        # 文本框
        # 头像
        replace_params_dict = {
            "background-color": f"rgba{frame_color}",
            "avatar-link": get_avatar_link_by_id(self.information["sender_id"]),
            "avatar-width": w,
            "avatar-height": h
        }
        avatar = generate_image_by_html(replace_params_dict, avatar_html_path).crop((0,0,w,h))
        
        if self.information["is_me"] is not True:
            # 他人消息
            replace_params_dict = {
                "background-color": f"rgba{frame_color}",
                "sender-name": self.information["sender_name"],
                "text": self.information["text"]
            }
            chat_box = generate_image_by_html(replace_params_dict, SimpleText_html_path)
            img = Image.new("RGBA", (frame_width, chat_box.height+message_offset), frame_color)
            img.paste(chat_box, (message_offset + w, 0))
            img.paste(avatar, (message_offset,0), mask=avatar)

        else:
            # 本人消息
            replace_params_dict = {
                "background-color": f"rgba{frame_color}",
                "text": self.information["text"]
            }
            chat_box = generate_image_by_html(replace_params_dict, SimpleText2_html_path)
            img = Image.new("RGBA", (frame_width, chat_box.height+message_offset), frame_color)
            img.paste(chat_box, (frame_width-message_offset-w-chat_box.width, 0))
            img.paste(avatar, (frame_width-message_offset-w, 0), mask=avatar)

        return img

class RichText(BasicImage):
    """富文本消息"""
    def __init__(self, information: dict) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="富文本消息", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass

class RedbagMessage(BasicImage):
    """红包消息"""
    def __init__(self, information: dict) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="红包", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass

class TransferMessage(BasicImage):
    """转账消息"""
    def __init__(self, information: dict) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="转账", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass

class Frame(BasicImage):
    """背景框架"""
    def __init__(self, information: dict) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="背景框架", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        """由Background、WechatHeader、PhoneHeader和WechatFooter组成"""
        phone_header = PhoneHeader(self.information["PhoneHeader"])
        wechat_header = WechatHeader(self.information["WechatHeader"])
        wechat_footer = WechatFooter()
        background_img_path = self.information["background_img_path"]
        background_img = BasicImage("背景图片", Image.new("RGBA", (frame_width, chat_height), color=frame_color)) if background_img_path == "default" else self.generate_background_from_path(background_img_path)
        self.__size = (frame_width, 1560)
        self.__frame = Image.new("RGBA", self.__size, color=(160, 160, 160, 255))
        offset = 0
        for img in (phone_header, wechat_header, background_img, wechat_footer):
            img.pasteto(self.__frame, (0, offset))
            offset = offset + img.height + (1 if img.img_type in ("微信顶部图片", "背景图片") else 0)
        return self.__frame

    def generate_background_from_path(self, background_img_path) -> Image.Image:
        return Image.open(background_img_path, "RGBA").resize(frame_width, 1275)

class PhoneHeader(BasicImage):
    """手机顶部通知栏"""
    def __init__(self, information: dict) -> None:
        self.__fnt = ImageFont.truetype("fonts/simfang.ttf", 35)
        self.__width = frame_width
        self.__height = 60
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="通知栏", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        operator = self.generate_operator_img(self.information["operator"])
        wifi = self.generate_wifi_img(self.information["wifi"])
        signal = self.generate_signal_img(self.information["signal"])
        battery = self.generate_battery_img(self.information["battery"])
        time = self.generate_time_img(self.information["time"])
        
        # 拼接通知栏
        phone_header = Image.new("RGBA", (self.__width, self.__height), color=frame_color)
        phone_header.paste(operator, (0, 0), mask=operator)
        x = self.__width
        for img in [time, battery, wifi, signal]:
            x = x - img.width
            y = int((self.__height - img.height)/2)
            phone_header.paste(img, box=(x, y), mask=img)
        return phone_header

    def generate_operator_img(self, information: dict) -> Image.Image:
        w, h = self.__fnt.getsize(information)
        operator = Image.new("RGBA", (w, self.__height), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(operator)
        d.text((0, int((self.__height-h)/2)), information, font=self.__fnt, fill=(0, 0, 0, 255))
        return operator

    def generate_signal_img(self, information: dict) -> Image.Image:
        return Image.open(f"images/bar/signal-{str(information)}.png")

    def generate_wifi_img(self, information: dict) -> Image.Image:
        return Image.open(f"images/bar/wifi-{str(information)}.png")

    def generate_battery_img(self, information: dict) -> Image.Image:
        battery = Image.open("images/bar/battery.png")
        d = ImageDraw.Draw(battery)
        x, y = 3, 4
        offset = 15
        radius = 8
        xy = [(x, y), (int(x+information*(battery.width-offset)), battery.height-y-1)]
        color = (0, 0, 0, 255) if information > 0.3 else (232, 191, 23, 255) if information > 0.15 else(231, 9, 8, 225)
        d.rounded_rectangle(xy, radius=radius, fill=color)
        return battery

    def generate_time_img(self, information: dict) -> Image.Image:
        w, h = self.__fnt.getsize(information)
        time = Image.new("RGBA", (w, self.__height), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(time)
        d.text((0, int((self.__height-h)/2-5)), information, font=self.__fnt, fill=(0, 0, 0, 255))
        return time

class WechatHeader(BasicImage):
    """微信顶部图片"""
    def __init__(self, information: dict) -> None:
        self.__fnt = ImageFont.truetype("fonts/simhei.ttf", 55)
        self.__width = frame_width
        self.__height = 105
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="微信顶部图片", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        wechat_header = Image.new("RGBA", (self.__width, self.__height), color=frame_color)
        d = ImageDraw.Draw(wechat_header)
        title = self.information["title"]
        w, h = self.__fnt.getsize(title)
        d.text((int((self.__width-w)/2), int((self.__height-h)/2)), title, font=self.__fnt, fill=(0, 0, 0, 255))
        left_img = Image.open("images/wechat-nav-back.png")
        right_img = Image.open("images/wechat-nav-right.png")
        offset = 20
        wechat_header.paste(left_img, (offset, int((self.__height-left_img.height)/2)), mask=left_img)
        wechat_header.paste(right_img, (int(self.__width-right_img.width), int((self.__height-left_img.height)/2+offset)))
        return wechat_header

class WechatFooter(BasicImage):
    """微信底部图片"""
    def __init__(self) -> None:
        img_obj = self.generate()
        super().__init__(img_type="微信底部图片", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        return Image.open("images/bar/wechat_footer.png")

class TimeNotice(BasicImage):
    """时间通知"""
    def __init__(self, information: dict) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="时间通知", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass