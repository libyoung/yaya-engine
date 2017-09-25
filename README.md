# yaya
The yaya is The Android Test Framework

need system : Ubuntu 14 ,Ubuntu 16，macOS
（macOS也类似如下步骤）
***********************************
1.创建一个独立的python环境
***********************************
1.$sudo apt-get install virtualenv
安装virtualenv工具

2.$virtualenv "env-path"
创建一个独立的python环境

3.$source "env-path"/bin/activate
激活这个独立的python环境

4.("env-path")$pip install atx-uiautomator
在独立的python环境里面安装atx-uiautomator

5.("env-path")$pip install opencv-python
在独立的python环境里面安装opencv-python（图片比对）

***********************************
2.修改配置文件
***********************************
1.$cd "code-path"

2.$gedit cfg/common.ini

3.modify "mdev" and "sdev" to local device serial in the "[Run Info]"

4.$python run.py  