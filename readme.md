# app版本
0. 修改app.py中的142行为想要输出的csv文件路径
1. 打包单个文件
```shell
pyinstaller --onefile --windowed app.py
```
2. 输出的可执行文件为./dist/app（打开的速度可能有点慢）
3. 在 gui 上输入 https://www.chinamedevice.cn/product/12/11/1128/1.html 可以爬取该目录下所有的器具信息，并保存在 0 中所指定的目录下
