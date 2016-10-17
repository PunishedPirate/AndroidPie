AndroidPie
----------
以下文件是用Python3.5写的脚本，主要用于Android开发过程中的layout适配。
### print_color.py:
在命令行输出有颜色的log

### util.py:       
常用工具函数

### dimen_transformer.py:
根据values-hdpi/dimens.xml自动生成values-xxhdpi/dimens.xml，等等

### layout_adapter.py:
根据layout/\*.xml布局文件，自动生成values-hdpi/dimens_\*.xml以及values-xhdpi/dimens_\*.xml，等等

***
##使用环境：Mac + python3.5
###配置环境变量
在命令行输入 vim ~/.bash_profile
在文件末尾加入以下语句：
```
#dimen transformer & layout adapter
alias hdpi2xhdpi='python3 path-to-project/dimen_transformer.py transform_dimen_xmls hdpi 1.5 xhdpi 2.0'
alias xhdpi2hdpi='python3 path-to-project/dimen_transformer.py transform_dimen_xmls xhdpi 2.0 hdpi 1.5'
alias transform_single_dimen_xml='python3 path-to-project/dimen_transformer.py transform_single_dimen_xml'
alias transform_dimen_xmls='python3 path-to-project/dimen_transformer.py transform_dimen_xmls'
alias adapt_single_xml='python3 path-to-project/layout_adapter.py adapt_single_xml'
alias adapt_xmls='python3 path-to-project/layout_adapter.py adapt_xmls'
```

***
## 操作指南
### dimen_transformer使用说明
1.cd 到你的工程目录
```
 cd my_project
```
<br>
2.根据工程目录下的values-hdpi/\*.xml自动生成values-xhdpi/\*.xml
```
 hdpi2xhdpi
```
<br>
3. 根据工程目录下的values-xhdpi/\*.xml自动生成values-hdpi/\*.xml
```
 xhdpi2hdpi
```
<br>
4. 根据工程目录下的values-hdpi/\*.xml自动生成values-xxhdpi/\*.xml
```
 transform_dimen_xmls hdpi 1.5 xxhdpi 3.0
```
<br>
5. 根据工程目录下的path-to/res/values-hdpi/a.xml
   自动生成 path-to/res/values-xhdpi/a.xml 以及path-to/res/values-xxhdpi/a.xml
```
 transform_single_dimen_xml path-to/res/values-hdpi/a.xml xhdpi xxhdpi
```
 
## layout_adapter使用说明
<br>
1. cd 到你的工程目录
```
 cd my_project
```
<br>
2. 根据工程目录下的path-to/res/layout/a.xml自动生成标准dimen文件path-to/res/values-xhdpi/dimens_a.xml
 以及自动生成适配文件path-to/res/values-hdpi/dimens_a.xml, path-to/res/values-xxhdpi/dimens_a.xml
```
 adapter_single_xml path-to/res/layout/a.xml xhdpi hdpi xxhdpi
```
<br>
3. 自动生成工程目录下所有layout/\*.xml的标准dimen文件values-xhdpi/dimens_\*.xml
 以及自动生成适配文件 values-hdpi/dimens_\*.mxl, vlaues-xxhdpi/dimens_\*.xml
```
 adapter_xmls xhdpi hdpi xxhdpi 
```

## 备注
dimens资源参数对应关系

    |   default  |        hdpi     |      xhdpi     |       xxhdpi      |
    |:----------:|:---------------:|:--------------:|:-----------------:|
    |   values   |   values-hdpi   | values-xhdpi   |   values-xxhdpi   |
    
例如：adapt_xmls default hdpi，此命令表示，将根据layout/\*.xml里面的dp值、sp值
 自动生成标准dimen文件res/values/dimens_\*.xml，
 同时自动生成适配文件res/values-hdpi/dimens_\*.xml
## 测试
transform_single_dimen_xml
<br>
![](https://github.com/PunishedPirate/AndroidPie/blob/master/testing/transform_single_dimen_xml.jpeg)
transform_dimen_xmls
<br>
![](https://github.com/PunishedPirate/AndroidPie/blob/master/testing/transform_dimen_xmls.jpeg)
adapt_single_xml
<br>
![](https://github.com/PunishedPirate/AndroidPie/blob/master/testing/adapt_single_xml.jpeg) 
adapt_xmls
<br>
![](https://github.com/PunishedPirate/AndroidPie/blob/master/testing/adapt_xmls_0.jpeg)
<br>
...
<br>
![](https://github.com/PunishedPirate/AndroidPie/blob/master/testing/adapt_xmls_1.jpeg)
