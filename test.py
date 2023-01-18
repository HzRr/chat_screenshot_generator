from PIL import Image, ImageDraw, ImageFont

im2 = Image.new("RGBA", (760, 60), color=(237, 237, 237, 255))
fnt = ImageFont.truetype("fonts/simfang.ttf", 35)
d = ImageDraw.Draw(im2)
d.text((0, 10), "中国移动", font=fnt, fill=(0, 0, 0, 255))
d.text((680, 10), "3:02", font=fnt, fill=(0, 0, 0, 255))
signal = Image.open("images/bar/signal-4.png")
wifi = Image.open("images/bar/wifi-3.png")
im2.paste(signal, (760-85-signal.size[0], int((60-signal.size[1])/2)), mask=signal)
im2.paste(wifi, (760-85-signal.size[0]-wifi.size[0], int((60-wifi.size[1])/2)), mask=wifi)
battery = Image.open("images/bar/battery.png")
d = ImageDraw.Draw(battery)
xy = [(2, 2), (0.8*battery.size[0]-12, battery.size[1]-3)]
d.rounded_rectangle(xy, radius=8, fill=(0,0,0,255))
  
battery.show()


background_info = {
    "PhoneHeader": {
        "operator": "中国移动",
        "signal": 4,
        "wifi": 3,
        "battery": [0.80, 1],
        "time": "3:02",
    },
    "WechatHeader": {
        "title": "测试(3)",
    },
    "background_img_path": "default",
}