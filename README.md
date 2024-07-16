# Visual Studio C++ 项目模板创建python脚本

由于VS自己的模板非常的拉胯，很多工程性的配置每次新建项目都需要重新设置，所以写了个python脚本来创建vc++的项目。

你只需要填写部分配置文件就可以创建一个模板。

配置文件 create_config.json：

```json
{
    "projectName": "testConsole", // 项目名称
    "entryFile": "src\\main.cpp", // 入口
    "type": "console", // 项目类型，读取自当前目录下的 templates 里面的目录
    "vcpkgDir": "d:\\tools\\vcpkg", // vcpkg 的目录
    "targetDir": "d:\\projects\\cpp", // 要把模板输出到哪个文件夹
    "openDir": true // 创建完成之后是否打开目录
}
```

配置好之后只需要执行 create_project.py 就可以轻松创建一个vc++的项目。

也可以跟着一个配置文件的路径作为参数


```
create_project.py c:\create_console.json
```

# 特性

- 1、支持 vcpkg ，创建后自动关联 vcpkg 包管理器。
- 2、支持 控制台、win32、dll 项目，如果你有自己的项目模板也可以自行添加在 templates 目录里。
- 3、已经配置好工程目录结构，源代码放在 src 中，其他的中间文件和二进制文件放在 bin 目录中。
- 4、字符集默认改为多字符集。
- 5、默认支持c++20特性。
