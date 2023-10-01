import tkinter as tk
import pandas as pd
import numpy as np
import datetime as dt
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


# 读取CSV文件
rang = pd.read_csv('ash_1.csv')

# 获取行数
num_row = len(rang)+1

# 创建主窗口并设置标题
root = tk.Tk()
root.title(f"第{num_row}次输入")


# 创建label
#label_accuracy = tk.Label(root, text="准确度: ")
label_ash_clean = tk.Label(root, text="上次检测的精煤灰分:")
label_exa_den_mid = tk.Label(root, text="上次实际的悬浮液密度:")
#entry
entry_ash_clean = tk.Entry(root)
entry_exa_den_mid = tk.Entry(root)



  


  # 定义tihuan数据函数
def Substitute_data():
    # 读取csv
    df = pd.read_csv("ash_1.csv")

# 替换倒数第1行的ash_clean值et den_medium
    df.loc[len(df) - 1, "ash_clean"] = entry_ash_clean.get()
    df.loc[len(df) - 1, "den_medium"] = entry_exa_den_mid.get()
    

# 将修改后的数据保存到csv文件中
    df.to_csv("ash_1.csv", index=False)

    entry_ash_clean.delete(0, tk.END)
    entry_exa_den_mid.delete(0, tk.END)
button_Substitute = tk.Button(root, text="保存上次数据", command=Substitute_data)   




# acc
def accuracy_data():
    try:
        df = pd.read_csv("ash_1.csv")
        ash_data = df.loc[:, 'ash_clean'].tail(10).to_numpy()
        top = tk.Toplevel()
        ash_req = df.loc[1, 'ash_req']
        reference_data = np.full((10,), ash_req)
        mse = mean_squared_error(reference_data, ash_data)
        top.title("MSE：" + str(mse))
        text = tk.Text(top)
        text.insert(tk.END, df.to_string())
        text.pack()
        df.loc[len(df) - 1, "accuracy"] = mse
    except FileNotFoundError:
        tk.messagebox.showerror("错误", "未找到CSV文件")
        df.to_csv("ash_1.csv", index=False)


button_acc = tk.Button(root, text="计算MSE", command=accuracy_data) 



# 创建预览按钮
def preview_data():
    # 读取当前CSV文件并显示预览
    try:
        df = pd.read_csv("ash_1.csv")
        top = tk.Toplevel()
        top.title("CSV文件预览")
        text = tk.Text(top)
        text.insert(tk.END, df.to_string())
        text.pack()
    except FileNotFoundError:
        tk.messagebox.showerror("错误", "未找到CSV文件")

button_preview = tk.Button(root, text="预览数据", command=preview_data)

# 设置标签和输入框位置
label_ash_clean.grid(row=0, column=0, padx=10, pady=10)
entry_ash_clean.grid(row=0, column=1, padx=10, pady=10)
label_exa_den_mid.grid(row=1, column=0, padx=10, pady=10)
entry_exa_den_mid.grid(row=1, column=1, padx=10, pady=10)
button_preview.grid(row=1, column=2, padx=10, pady=10)
button_acc.grid(row=1, column=3, padx=10, pady=10)
button_Substitute.grid(row=0, column=2, padx=10, pady=10)
#label_accuracy.grid(row=2, column=0, padx=10, pady=10)

# La partie 2
# 读取数据文件
data = pd.read_csv('ash_1.csv', header=0, nrows=6)


# 创建标签 第六次的原煤灰分
label_ash_raw = tk.Label(root, text="原煤灰分:")

# 创建输入框
entry_ash_raw = tk.Entry(root)



# 提取特征和目标变量
data.dropna(subset=['ash_clean'], inplace=True)
X = data[['ash_raw', 'ash_clean']].values
y = data['den_medium'].values

# 划分训练集和验证集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# 创建支持向量机模型
model = svm.SVR(kernel='rbf')

# 训练模型
model.fit(X_train, y_train)

#初始化predicted_den_medium
predicted_den_medium = 0

# 使用新数据进行预测
def predict():
    global predicted_den_medium
    new_ash_raw = entry_ash_raw.get()
    new_ash_req = data.iloc[1]['ash_req']
    new_data = np.array([[new_ash_raw, new_ash_req]])
    predicted_den_medium = model.predict(new_data)
    print(predicted_den_medium)
    print(type(predicted_den_medium))


# 创建按钮
predict_button = tk.Button(root, text="预测", command=predict)

predict_button.grid(row=3, column=2, columnspan=1, padx=10, pady=10)

label_ash_raw.grid(row=3, column=0, padx=10, pady=10)
entry_ash_raw.grid(row=3, column=1, padx=10, pady=10)


#定义保存数据函数
def save_data():
    global predicted_den_medium # 声明要使用全局变量
    # 获取当前时间
    now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

     #将数据保存到csv文件中
    data = {
        "ash_raw": [entry_ash_raw.get()],
        "ash_clean": [0],
        "den_medium": [predicted_den_medium[0]],
        "time": [now],
        "ash_req": [0],
        "accuracy": [0]
    }
    df = pd.DataFrame(data)
    file_name = "ash_1.csv"
    df.to_csv(file_name, mode='a',header=False, index=False)
    print(data)
    
    # 清空输入框
    entry_ash_raw.delete(0, tk.END)

# 创建保存按钮
button_save = tk.Button(root, text="保存数据", command=save_data)
button_save.grid(row=4, column=0, padx=10, pady=10)





# 创建预览按钮
def rec_data():
    # 读取当前CSV文件并显示预览
    try:
        df = pd.read_csv("ash_1.csv")
        latest_den_medium = df['den_medium'].iloc[-1]
        top = tk.Toplevel()
        top.title("建议的den_medium值为：" + str(latest_den_medium))
        text = tk.Text(top)
        text.insert(tk.END, df.to_string())
        text.pack()
    except FileNotFoundError:
        tk.messagebox.showerror("错误", "未找到CSV文件")

button_rec = tk.Button(root, text="显示建议的密度值并查看数据", command=rec_data)
button_rec.grid(row=4, column=1, padx=10, pady=10)

# 创建继续按钮
def continue_to_next():
    root.destroy() # 销毁当前界面
    import input_11ui.py # 加载下一个界面

button_continue = tk.Button(root, text="继续", command=continue_to_next)
button_continue.grid(row=4, column=2, padx=10, pady=10)

root.mainloop()
