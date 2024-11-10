# Packing

## 依赖
```shell
pip install pyinstaller
```

## 打包
```shell
pyinstaller -w -F main.py ^
--add-data simhei.ttf;. ^
--add-data image;image ^
--add-data sound;sound ^
--add-data map;map ^
--contents-directory . ^
--clean -y --log-level=INFO
```
- 找不到某个包：--hidden-import xgboost --collect-all xgboost ^
- 找不到某个文件（把左边的文件放到；右边的目录里）：--add-data models.pt;. ^
- 找不到某个目录（把左边目录下的所有文件放到；右边的目录里）：--add-data image;image ^
- pyinstaller 6输出pyinstaller 5的项目结构（对打包单文件资源无效）：--contents-directory .
- 单文件资源文件路径转换：用resource_path修正资源文件路径
- 打包成单文件：-F
- 去掉控制台：-w
- 替换文件图标（如果是png文件，需要安装pillow）：-i icon.ico
## 测试1
以项目目录作为工作目录，能读取当前python环境中的一些包，也会读取到项目中依赖的资源文件
```shell
dist\main\main.exe
```

## 测试2
以输出目录作为工作目录，测试资源是否完整，但会访问到虚拟环境的东西（例如cuda）
### 目录
```shell
pushd dist\main & main.exe & popd
```
### 单文件
```shell
pushd dist & main.exe & popd
```

## 测试3
手动进入打包好的目录双击执行