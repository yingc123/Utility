import numpy as np
import matplotlib.pyplot as plt
import matplotlib
plt.rcParams['font.sans-serif']=['SimHei','Times New Roman'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False

def draw_main():
    zhfont1 = matplotlib.font_manager.FontProperties(fname=r"C:\Users\ying.chen02\Downloads\SourceHanSansSC-Regular.otf")
    x = np.array(["正常", "动脉瘤", "钙化", "血管畸形",
                  "栓塞", "夹层", "支架"])
    y = np.array([342, 76, 47, 38, 10, 9, 4])

    plt.bar(x,y)
    for a,b,i in zip(x,y,range(len(x))): # zip 函数
        plt.text(a,b,"%d"%y[i],ha='center',fontsize=10) # plt.text 函数
    #plt.show()
    plt.xticks(range(len(x)),x,fontproperties=zhfont1)
    plt.savefig(r'F:\3月_文档\联合应用文档\data\head.jpg')

def draw_single():
    plt.figure(figsize=(10, 8))
    zhfont1 = matplotlib.font_manager.FontProperties(
        fname=r"C:\Users\ying.chen02\Downloads\SourceHanSansSC-Regular.otf")
    x = np.array(["正常", "动脉瘤", "钙化", "血管畸形", "栓塞", "夹层", "支架"])
    y = np.array([342, 76, 47, 38, 10, 9, 4])
    y_train = [int(y[i]/342*292) for i in range(len(y))]
    y_test = [int(y[i]/342*40) for i in range(len(y))]
    y_val = [(y[i] - y_train[i] - y_test[i]) for i in range(len(y))]
    print(sum(y_train), sum(y_val), sum(y_test))

    total_width, n = 0.9, 3
    width = total_width / n
    x1 = np.arange(len(x)) - width
    x2 = x1 + width
    x3 = x2 + width
    plt.bar(x1, y_train, width=width, label='训练', color='blue')
    plt.bar(x2, y_val, width=width, label='调优', color='green')
    plt.bar(x3, y_test, width=width, label='测试', color='red')
    for a, b in zip(x1, y_train):
        plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(x2, y_val):
        plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    for a, b in zip(x3, y_test):
        plt.text(a, b + 0.1, '%.0f' % b, ha='center', va='bottom', fontsize=10)
    plt.legend()
    plt.xticks(range(len(x)), x, fontproperties=zhfont1)
    plt.savefig(r'F:\3月_文档\联合应用文档\data\test.jpg')

