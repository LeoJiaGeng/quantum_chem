
# 点击到开始的图片上，启动视频播放
# 鼠标来回移动一下，必须在视频窗口内，获取当前截图
# 重复上面操作，进行判断，如果有区别，继续，没有区别，点击下一个图片
# 记录点击次数，点击十次就要滑动一次滚轮

import pyautogui
import time



#pyautogui.moveTo(200,400,duration=1)
#
#pyautogui.click(100,100,button='left') 
##pyautogui.scroll(30000) 
#pyautogui.moveRel(800,500,duration=2)
#
#oneLocation = pyautogui.locateOnScreen(r'E:\Python_Files\learn\photo\end4.png')
#print(oneLocation) 
#pyautogui.click(oneLocation.left + 20,oneLocation.top + 10,button='left') 

from PIL import Image
from PIL import ImageChops

def compare_images(path_one, path_two):
    """
    比较图片，如果有不同则生成展示不同的图片

    @参数一: path_one: 第一张图片的路径

    @参数二: path_two: 第二张图片的路径
    """
    image_one = Image.open(path_one)

    image_two = Image.open(path_two)
    
    diff = ImageChops.difference(image_one, image_two)

    if diff.getbbox() is None:
        print("Image is the same")
        return True
    else:
        print("Image not same")
        return False

def test():
    while True:
        name1 = 'screenshot1.png'
        name2 = 'screenshot2.png'        
        pyautogui.moveTo(200,400,duration=1)
        pyautogui.moveRel(800,500,duration=2)
        time.sleep(5)  # 延时0.5s
        screenshot1 = pyautogui.screenshot()  # 获取当前屏幕截图
        screenshot1.save(name1)
        time.sleep(0.5)  # 延时0.5s
        pyautogui.moveTo(200,400,duration=1)
        pyautogui.moveRel(800,500,duration=2)
        time.sleep(5)  # 延时0.5s
        screenshot2 = pyautogui.screenshot()  # 再次获取当前屏幕截图
        screenshot2.save(name2)

        if compare_images(name2, name1):
        # 如果屏幕发生改变，则打印信息并退出循环
            print("屏幕没有变化")
            break
        else:
            print("屏幕已经发生变化了")
            break

#compare_images()
test()