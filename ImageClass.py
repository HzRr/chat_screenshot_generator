from PIL import Image, ImageDraw, ImageFont


frame_color = (237, 237, 237, 255)  # 框架背景色
frame_width = 760                   # 框架宽度
text_width = 493                    # 文本框宽度

class BasicImage:

    def __init__(self, img_type: str, img_obj: Image.Image) -> None:
        self.img_type = img_type
        self.__image = img_obj
        self.width, self.height = self.__image.size
    
    def pasteto(self, obj: Image.Image, pos: tuple) -> None:
        """将self粘贴到传入对象obj上"""
        obj.paste(self.__image, box=pos)

    def show(self) -> None:
        self.__image.show()        

class SimpleText(BasicImage):
    """单文本消息"""
    def __init__(self, information) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="单文本消息", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        w, h = 81, 81   # 头像尺寸
        profile_image = Image.open(f"images/senders/{self.information['sender_id']}.png").resize(w, h)
        fnt = ImageFont.truetype(self.information["font"], self.information["font_size"])   # 自定义字体
        h = fnt.getsize()
        simple_text_image = Image.new("RGBA", (text_width, h))

class RichText(BasicImage):
    """富文本消息"""
    def __init__(self, information) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="富文本消息", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass

class RedbagMessage(BasicImage):
    """红包消息"""
    def __init__(self, information) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="红包", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass

class TransferMessage(BasicImage):
    """转账消息"""
    def __init__(self, information) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="转账", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass

class Frame(BasicImage):
    """背景框架"""
    def __init__(self, information) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="背景框架", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        """由Background、WechatHeader、PhoneHeader和WechatFooter组成"""
        phone_header = PhoneHeader(self.information["PhoneHeader"])
        wechat_header = WechatHeader(self.information["WechatHeader"])
        wechat_footer = WechatFooter()
        background_img_path = self.information["background_img_path"]
        background_img = BasicImage("背景图片", Image.new("RGBA", (frame_width, 1275), color=frame_color)) if background_img_path == "default" else self.generate_background_from_path(background_img_path)
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

    def generate_operator_img(self, information) -> Image.Image:
        w, h = self.__fnt.getsize(information)
        operator = Image.new("RGBA", (w, self.__height), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(operator)
        d.text((0, int((self.__height-h)/2)), information, font=self.__fnt, fill=(0, 0, 0, 255))
        return operator

    def generate_signal_img(self, information) -> Image.Image:
        return Image.open(f"images/bar/signal-{str(information)}.png")

    def generate_wifi_img(self, information) -> Image.Image:
        return Image.open(f"images/bar/wifi-{str(information)}.png")

    def generate_battery_img(self, information) -> Image.Image:
        battery = Image.open("images/bar/battery.png")
        d = ImageDraw.Draw(battery)
        x, y = 3, 4
        offset = 15
        radius = 8
        xy = [(x, y), (int(x+information*(battery.width-offset)), battery.height-y-1)]
        color = (0, 0, 0, 255) if information > 0.3 else (232, 191, 23, 255) if information > 0.15 else(231, 9, 8, 225)
        d.rounded_rectangle(xy, radius=radius, fill=color)
        return battery

    def generate_time_img(self, information) -> Image.Image:
        w, h = self.__fnt.getsize(information)
        time = Image.new("RGBA", (w, self.__height), color=(0, 0, 0, 0))
        d = ImageDraw.Draw(time)
        d.text((0, int((self.__height-h)/2)), information, font=self.__fnt, fill=(0, 0, 0, 255))
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
        wechat_header.paste(left_img, (offset, int((self.__height-left_img.height)/2)))
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
    def __init__(self, information) -> None:
        self.information = information
        img_obj = self.generate()
        super().__init__(img_type="时间通知", img_obj=img_obj)
    
    def generate(self) -> Image.Image:
        pass

'''
background_info = {
    "PhoneHeader": {
        "operator": "中国移动",
        "signal": 3,
        "wifi": 1,
        "battery": 0.25,
        "time": "14:02",
    },
    "WechatHeader": {
        "title": "测试(3)",
    },
    "background_img_path": "default",
}
img = Frame(background_info)
img.show()
'''

text_info = {
    "sender_id": 1,
    "font": "fonts/simfang.ttf",
    "font_size": 20,
    "text": "你好世界你好世界你好世界你好世界你好世界你好世界你好世界！！！！！",
}
img = SimpleText(text_info)
img.show()