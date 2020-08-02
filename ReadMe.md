# Media Renamer <!-- omit in toc -->

一款从 The Movie Database (TMDb) 搜索信息的本地剧集文件重命名工具。

1. [特性](#特性)
2. [安装与依赖项](#安装与依赖项)
3. [使用](#使用)
4. [许可证](#许可证)


## 特性

未勾选的项是考虑在未来加入的功能。

- [x] 从给定页面读取剧集列表，并整理为默认的文件名。
- [ ] 优化返回文本的语言。目前默认是简体中文（zh-CN）。 
- [ ] 切换到 API 而不是从网页读取。
- [ ] 实现重命名功能。


## 安装与依赖项

目前依赖于 Python (>=3.6) 以及 [requests](https://github.com/psf/requests#requests-module-installation) 与 [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html#id5) 库。

这两个库可以由下述命令安装：

```cmd
pip install requests
pip install beautifulsoup4
```

安装目前通过下载该仓库中所有 `.py` 文件来实现。


## 使用

当前版本仅支持输出结果到控制台（默认请求简体中文结果）：

```cmd
C:\> python -u "media-renamer.py"

新世纪福音战士-S01E01.使徒、来袭（ANGEL ATTACK）
新世纪福音战士-S01E02.陌生的天花板（THE BEAST）
新世纪福音战士-S01E03.不响的电话（A transfer）
...（省略）
新世纪福音战士-S01E26.在世界中心呼唤爱的野兽（Take care of yourself.）
```


## 许可证

[MIT](./LICENSE)
