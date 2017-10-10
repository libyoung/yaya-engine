# **yaya介绍**
yaya目前是一个基于Google UI Automator的android手机测试框架。
The yaya is The Android Test Engine. Based on [atx-uiautomator](https://github.com/openatx/atx-uiautomator) in the current。

目的：让写脚本变得简单。

## **思想：少就是多**
让写脚本人做的少，框架本身做的多。让写脚本的人只需关注测试case的步骤即可，其他事情交给框架。
看如下例子：

```python
test_call_from_history_3G = [ 
     'Test Call from History in 3G Network',
     '1.打开Phone App', OpenAPP('Dialer'),
     '2.点击第一条Call History记录的拨号按钮', {'resourceId':'com.android.dialer:id/call_back_action'},
     '3.验证是否有电话拨打出去', IsInCall(8),
     '4.辅测监听来电并接听', SDevice( IsRinging(10), CallAnswer ),
     '5.保持通话5秒中', InCallStay(5),
     '6.主测挂断电话', EndCall
     ]
```

**OpenAPP**, **IsInCall**, **SDevice**, **InCallStay**, **EndCall**这几个关键字是yaya框架提供的功能函数，很好理解它们，从它们字面意义就能知道是干什么用的。

   - **OpenAPP** 打开某一个APP
   - **IsInCall** 检测手机是否在通话中
   - **SDevice** 切换到辅测
   - **InCallStay** 保持通话多少秒
   - **EndCall** 挂断电话

第2步中，**{ 'resourceId':'com.android.dialer:id/call\_back_action' }**是表示一个需要点击控件，**{ }**中**'resourceId'**和**'com.android.dialer:id/call\_back_action'**分别是控件的属性和属性值，当你在**{ }**中给定属性和属性值时，yaya可以定位到手机界面中具体控件，并点击它。

写脚本的人只需要根据case步骤，一步一走实现就可以了，没有过多的语法，也不需要过多语法。yaya中所有功能函数不超过50个，常用不超过20个，就是说你只需要记住20个关键字和**{ }**简单用法，就可以很愉快的写测试case。


## **概念**
 - Step： 单个步骤，比如：打印一个句log，点击一个控件，launch一个APP
 - Flow：有步骤流，比如：步骤组成列表[“Start Test”, OpenAPP(“Call”), Home]'
   比如前面的**test\_call\_from\_history\_3G**就是一个Flow
 - Template：业务流，根据业务需求对**Flow**进行封装,比如：StabilityTestTemplate ，根据Stability Test要求去控制Flow的执行

## **其他功能**
   - log记录
   - 导出测试数据，
   - 出错截图，dump
   - ANR和Crash监控

## **当前状态**
现在还是beta阶段，需要大家一起完善它。
 
## **安装**
**need system : Ubuntu 14 ,Ubuntu 16，macOS**

### **1.创建一个独立的python环境**
    $ pip install atx-uiautomator

    $ pip install opencv-python
    
这里还需要安装其它python包，我这里没有列出来，等日后完善了，

### **2.修改配置文件**
    $ cd "code-path"

    $ gedit cfg/common.ini

    $ modify "mdev" and "sdev" to local device serial in the "[Run Info]"

    $ python run.py  

