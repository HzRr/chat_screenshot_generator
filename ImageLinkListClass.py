from ImageClass import *
from typing import List


img_type_dict = {
    "背景框架": Frame,
    "单文本消息": SimpleText
}

class Node:
    def __init__(self, img_type, information: dict) -> None:
        self.img_type = img_type
        self.__information = information
        self.next = None
        self.prev = None

    def get_img(self) -> BasicImage:
        return img_type_dict[self.img_type](self.__information)


def concat_image(node_list: List[Node]) -> Image.Image:
    img_list: List[BasicImage] = []
    h = 0
    for node in node_list:
        img = node.get_img().get_img_obj()
        h += img.height
        img_list.append(img)
    tmp = Image.new("RGBA", (frame_width, h), frame_color)
    h = 0
    for img in img_list:
        tmp.paste(img, (0, h))
        h += img.height
    return tmp

class ImageLinkList:
    def __init__(self, background_information: dict) -> None:
        self.__head = Node("背景框架", background_information)
        self.cur = self.__head
        self.__foot = self.__head
    
    def append_node(self, img_type, information: dict) -> None:
        self.cur.next = Node(img_type, information)
        self.cur = self.cur.next

    def undo(self) -> bool:
        if self.cur.prev is not self.__head:
            self.cur = self.cur.prev
            return True
        else:
            return False

    def redo(self) -> bool:
        if self.cur.next is not None:
            self.cur = self.cur.next
            return True
        else:
            return False

    def travel(self) -> list:
        self.cur = self.__head
        node_list = []
        while self.cur.next is not None:
            self.cur = self.cur.next
            node_list.append(self.cur)
        return node_list

    def generate_image(self) -> Image.Image:
        # 生成Frame
        img = self.__head.get_img().get_img_obj()
        # 合成聊天记录
        chat = concat_image(self.travel())
        w, h = chat.size
        chat = chat.crop((0, h-chat_height, w, h))
        img.paste(chat, (0, chat_offset+chat_height-chat.height), mask=chat)
        return img

background_info = {
    "PhoneHeader": {
        "operator": "中国移动",
        "signal": 3,
        "wifi": 1,
        "battery": 0.9,
        "time": "14:02",
    },
    "WechatHeader": {
        "title": "测试(3)",
    },
    "background_img_path": "default",
}

text_info = {
    "is_me": False,
    "sender_id": 1,
    "sender_name": "测试",
    "text": "你好世界你好世界你好世界你好世界你好世界你好世界你好世界！！！！！",
}

text_info2 = {
    "is_me": True,
    "sender_id": 1,
    "sender_name": "测试",
    "text": "你好世界你好世界你好世界你好世界你好世界你好世界你好世界！！！！！",
}

image_link_list = ImageLinkList(background_info)
image_link_list.append_node("单文本消息", text_info)
image_link_list.append_node("单文本消息", text_info)
image_link_list.append_node("单文本消息", text_info2)
image_link_list.append_node("单文本消息", text_info)
image_link_list.append_node("单文本消息", text_info)
image_link_list.append_node("单文本消息", text_info)
image_link_list.append_node("单文本消息", text_info2)
import time
t1 = time.time()
image_link_list.generate_image().save("user_images/temp.png")
t2 = time.time()
print(t2-t1)