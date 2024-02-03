import markdown
 
# 打开Markdown文件
with open(file = '猫猫.md', mode='r', encoding= "utf-8") as file:
    # 将内容转换为HTML格式
    print(file.read())
    print(type(file.read()))
    
# print(html)
