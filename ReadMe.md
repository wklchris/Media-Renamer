# Media Renamer <!-- omit in toc -->

一款从 The Movie Database (TMDb) 搜索信息的本地剧集文件重命名工具。

> 注：本人的[另一个仓库](https://github.com/wklchris/Movie-Info-Scraper)是该项目的 JavaScript 脚本实现，不过只有整理网页上的剧集标题并复制到剪切板的功能。如果浏览器上已有 TamperMonkey 插件，可以[点此前往安装脚本](https://greasyfork.org/en/scripts/408000-movie-info-scraper)。

1. [特性](#特性)
2. [安装与依赖项](#安装与依赖项)
3. [快速使用](#快速使用)
4. [高级使用\*](#高级使用)
   1. [例1：关键词检索](#例1关键词检索)
   2. [例2：剧集 ID 检索](#例2剧集-id-检索)
   3. [例3：完整的测试运行示例](#例3完整的测试运行示例)
5. [许可证](#许可证)

> 声明：本仓库使用了 TMDb API，但未经TMDb认可或认证。*This product uses the TMDb API but is not endorsed or certified by TMDb.*
> 
> <img src="./TMDb-logo-alt-long.svg" alt="TMDb logo" width="40%" />
>
> *本声明旨在遵守 [TMDb API 使用条款](https://www.themoviedb.org/documentation/api/terms-of-use)的第三条“归因”（Attribution）中的要求。*

## 特性

未勾选的项是考虑在未来加入的功能。

- [x] 从给定页面读取剧集列表，并整理为默认的文件名。
- [x] 优化返回文本的语言。目前默认是简体中文（zh-CN）。 
- [x] 切换到 API 而不是从网页读取。
- [x] 实现重命名功能。
- [x] 从命令行传递参数。
- [ ] 让从命令行输入的 API 密钥能够覆盖配置文件中的密钥。
- [ ] 对特别篇剧集的特殊处理；或支持在本地文件数量与TMDB不同时，让用户自行选择对哪些文件进行重命名。


## 安装与依赖项

目前依赖于 Python (>=3.6) 以及 [requests](https://github.com/psf/requests#requests-module-installation) 库。它可以由下述命令安装：

```cmd
pip install requests
```

安装目前通过下载该仓库中的以下文件来实现：

1. `TV.py`：本仓库的核心文件，定义了 TMDB 类。
2. `settings.json` 文件：如果当前文件夹下没有该文件，会在首次运行时自动生成一个。

   用户需要自行从 TMDB [免费申请 API 密钥](https://developers.themoviedb.org/3/getting-started/introduction)；如果没有账户，请先创建一个免费 TMDB 账户。
3. `media-renamer.py`: 主执行脚本。

<details><summary>点击展开/折叠 settings.json 的语法说明</summary>

```json
{
    "api_key": "YOUR_TMDB_API_KEY_HERE",
    "filename_format_tv": "{media_title}-S{tv_season}E{tv_episode}.{tv_eptitle}",
    "language": "zh-CN",
    // 以下内容请勿更改
    "api_search": "https://api.themoviedb.org/3/search/{media_type}?api_key={api_key}&query={search_str}&language={language}",
    "api_id_series": "https://api.themoviedb.org/3/{media_type}/{media_id}?api_key={api_key}&language={language}",
    "api_id_season": "https://api.themoviedb.org/3/{media_type}/{media_id}/season/{order_season}?api_key={api_key}&language={language}"
}
```

各字段的说明：
- `api_key`: TMDB 的 API 密钥。
- `filename_format_tv`：本地剧集文件的命名格式，不包括扩展名。本仓库中的定义（见下文）符合流媒体库管理软件 [Kodi](https://kodi.tv/) 的 TMDB 检测规范，重命名后可以自动匹配 TMDB 的剧集信息。
  - `{media_title}`：剧名
  - `{tv_season}`：剧季编号，两位数字，左侧补零。一般地，`0` 表示特别篇。
  - `{tv_episode}`：剧集编号，两位数字，左侧补零。
  - `{tv_eptitle}`：本集的标题。
- `language`：返回数据的语言。

下列字段中的内容不可更改，这里仅作解释性说明。
- `api_search`：使用关键字进行检索剧。
  - `{media_type}`：对剧集来说是 `tv`；对电影来说是 `movie`（尚未支持）。
  - `{search_str}`：要检索的字符串，一般是剧集的名称。
  - `{api_key}`，`{language}`：自动引用之前定义的内容。
- `api_id_series`：使用已知的 ID 检索剧。
  - `{media_id}`：剧集在 TMDB 中的唯一标识 ID。
- `api_id_season`：使用已知的 ID 与季编号检索剧的某一季。
  - `{order_season}`：剧季编号。
</details>

## 快速使用

用法说明：

* 在第一次执行脚本时，如前文所述，用户需要准备从 TMDB 免费申请一个 API 密钥。脚本会自动在同目录下创建一个 `settings.json` 文件，然后将 API 密钥记录在其中；此后的脚本执行，便不再需要重新输入 API 密钥。
* 要对 `VIDEO_DIR` 目录下的、剧集 `TVNAME` 对应的视频文件进行重命名操作，用户可以执行：

  ```shell
  # 例：python media-renamer.py 福音战士 -d C:\Videos\EVA
  python media-renamer.py TVNAME -d VIDEO_DIR
  ```
  其中，`-d` 选项表示该剧集（的一季）所在的文件夹；如果不指定，会设置为命令行当前的路径。该文件的主目录下，不应包含该季视频与字幕外的其他文件；一般地，要求字幕文件、视频文件的数量相等，且与 TMDB 中该季的剧集数目相同。

  之后，按提示依次输入序号来选择正确的搜索结果与剧季，并在重命名前检查新旧文件名的对应是否正确。
* 除了使用剧集名称（或者剧集名称的一部分字词）来进行搜索，用户也可以使用 TMDB 上剧系列的 ID 号来进行检索。
  
  例如，《新世纪福音战士》系列（[TMDB链接](https://www.themoviedb.org/tv/890-neon-genesis-evangelion)）的剧系列 ID 号是 890（从网址中可以看出），那么用户可以输入：

  ```shell
  python media-renamer.py 890 -m -d C:\Videos\EVA
  ```
  其中，参数 `-m` 表示使用 ID 搜索模式。
* 在搜索本地文件时，默认的视频扩展名支持 `.mp4/.mkv`，而字幕扩展名支持 `.srt/.ass`。文件将会按文件名进行排列。
  
  用户可以指定用 `-v` 或 `-s` 参数指定其他的扩展名，中间用空格隔开即可：
  ```shell
  python media-renamer.py 新世纪福音战士 -d C:\Videos\EVA -v .ts .mp4 .mkv -s .ass -T
  ```
* 一个实用的、不带参数值的测试选项 `-T` 会在当前路径下（无视 `-d` 指定的路径）创建一个 `test` 文件夹，并自动生成一系列“虚假”的视频文件与字幕文件，供读者检查重命名的效果。
  
  当然，该命令通常不需要用到，因为在正常重命名的最后一步，新旧文件名会被打印在命令行中供读者检查。

最后，用户可以执行 `python media-renamer.py -h` 来查看帮助。下面是一份完整的参数列表：

| 参数 | 类型 | 释义 |
| --- | --- | --- |
| searchword | 必选参数 | 搜索字串 |
| --ID-mode, -m | 开关参数 | 切换到 ID 搜索模式 |
| --api, -a | 可选参数 | 指定一个 API 密钥。仅在初始化时启动。 |
| --config, -c | 可选参数 | 指定配置文件（默认是 `'settings.json'`） |
| --dir, -d | 可选参数 | 指定剧集文件路径（默认时当前目录） |
| --test, -T | 开关参数 | 启用测试模式（详见上文） |
| --video-exts, -v | 可选参数列表 | 指定要识别的视频文件扩展名列表（默认 `.mp4 .mkv`） |
| --subtitle-exts, -s | 可选参数列表 | 指定要识别的字幕文件扩展名列表（默认 `.ass .srt`） |
| -h | / | 显示帮助 |

- *开关参数* 表示后不接受任何输入值的非必选参数；
- *可选参数* 表示接受单项输入的、非必选的参数；
- *可选参数列表* 表示接受一或多项以空格分隔输入的、非必选的参数。

## 高级使用\*

> 本节不是必读内容。
>
> 本节面向编程人员撰写。在上述快速使用一节中，已经介绍了命令行的使用方式；本节则将主要展示如何将本项目的 Python 代码嵌入到用户自己的 Python 代码中。

本工具主要提供了以下几个供外部调用的方法：

* `search(search_str)`: 在 TMDB 上搜索 search_str 对应的剧集内容。
* `search_id_series(search_id)`: 在 TMDB 上搜索 ID 号为 search_id 的剧集。注意：剧集 ID 与剧集某一季的季 ID 并不相同。
* `rename_local_files()`: 搜索成员变量 `self.workdir` 对应目录下的视频与字幕文件，根据之前的搜索内容，将这些文件重命名。

以下均以 Python 命令行为例。不过，仍然**建议读者参考 media-renamer.py 中的内容**撰写脚本文件。

以下内容的文件命名格式，均以`settings.json` 的默认  `filename_format_tv` 配置为准：
```
"{media_title}-S{tv_season}E{tv_episode}.{tv_eptitle}"
```

### 例1：关键词检索

用 `TMDB.search(search_str)` 来检索关键词。下例是 `白色相簿` （[点此前往 TMDB 搜索页](https://www.themoviedb.org/search?query=%E7%99%BD%E8%89%B2%E7%9B%B8%E7%B0%BF)）的检索结果。
- 该关键词有两个检索匹配的剧，用户输入 `2` 来选中：`[70072] 白色相簿2` 这一部剧。
- 检索到该剧有两季，用户再次输入了 `2` 来选中 `[84675] 第 1 季`。
- 该季（剧 ID=70072，季 ID=84675）中的所有剧集被处理成规范的文件名。

```python
>>> from TV import TMDB
>>> scraper = TMDB()
>>> scraper.search("白色相簿")

Choose the one that matches:
01 ~ [28502] 白色相簿 (2009-01-04; ja; JP) 
02 ~ [70072] 白色相簿2 (2013-10-06; ja; JP)
---
Select from above (1~2): 2
Select: [70072] 白色相簿2 (2013-10-06; ja; JP)

Choose the one that matches:
01 ~ [151373] 特别篇 (Season 00, 2014-05-28; total 002 episodes)
02 ~ [84675] 第 1 季 (Season 01, 2013-10-06; total 013 episodes)
---
Select from above (1~2): 2
Select: [84675] 第 1 季 (Season 01, 2013-10-06; total 013 episodes)
>>> print('\n'.join(scraper.tv_fnames))
白色相簿2-S01E01.WHITE ALBUM
白色相簿2-S01E02.邻座的钢琴与吉他
白色相簿2-S01E03.轻音乐同好会再结成
...（省略）
白色相簿2-S01E13.传达不到的爱恋
```

### 例2：剧集 ID 检索

用 `TMDB.search_id_series(media_id)` 来检索该 ID 对应的剧。下例是 ID=890 的剧（即《新世纪福音战士》，[点此前往 TMDB 搜索页](https://www.themoviedb.org/search/tv?query=%E6%96%B0%E4%B8%96%E7%BA%AA%E7%A6%8F%E9%9F%B3%E6%88%98%E5%A3%AB)）的检索结果。

- ID 唯一匹配一部剧。
- 检索到该剧只有一季；无需用户输入，自动选中。
- 该季（剧 ID=890，季 ID=51882）中的所有剧集被处理成规范的文件名。

```python
>>> from TV import TMDB
>>> scraper = TMDB()
>>> scraper.search_id_series(890)
Select: [51882] 第 1 季 (Season 01, 1995-10-04; total 026 episodes)
>>> print('\n'.join(scraper.tv_fnames))
新世纪福音战士-S01E01.使徒、来袭（ANGEL ATTACK）
新世纪福音战士-S01E02.陌生的天花板（THE BEAST）
新世纪福音战士-S01E03.不响的电话（A transfer）
...（省略）
新世纪福音战士-S01E26.在世界中心呼唤爱的野兽（Take care of yourself.）
```

### 例3：完整的测试运行示例

新建一个 Python 文件，假设它包含下述内容：

```python
from TV import TMDB

scraper = TMDB(workdir='.')
scraper.search("白色相簿")  
scraper.make_test_files(total=13)
scraper.rename_local_files()
```

用户将在以上代码的运行过程中，执行4次键入：

1. 同例1，从两个“白色相簿”的搜索结果中，选择了“白色相簿2”。
2. 同例1，从白色相簿2下的两个搜索结果“特别篇”与“第一季”中，选择了“第一季”。
3. 询问是否重命名供测试而生成的 13 个 mkv 文件，直接回车表示确认。
4. 询问是否重命名 13 个 ass 文件，直接回车表示确认。

完整的运行结果：

```powershell
Choose the one that matches:
01 ~ [28502] 白色相簿 (2009-01-04; ja; JP)
02 ~ [70072] 白色相簿2 (2013-10-06; zh; JP)
---
Select from above (1~2): 2
Select: [70072] 白色相簿2 (2013-10-06; zh; JP)

Choose the one that matches:
01 ~ [151373] 特别篇 (Season 00, 2014-05-28; total 002 episodes)
02 ~ [84675] 第 1 季 (Season 01, 2013-10-06; total 013 episodes)
---
Select from above (1~2): 2
Select: [84675] 第 1 季 (Season 01, 2013-10-06; total 013 episodes)
Formatted filename example: 白色相簿2-S01E01.WHITE ALBUM
Testing: Fake 13 files in 'test' folder.
Old filenames           New filenames
===============         ===============
+++++1.mkv       白色相簿2-S01E01.WHITE ALBUM.mkv
+++++2.mkv       白色相簿2-S01E02.邻座的钢琴与吉他.mkv
+++++3.mkv       白色相簿2-S01E03.轻音乐同好会再结成.mkv
+++++4.mkv       白色相簿2-S01E04.SOUND OF DESTINY.mkv
+++++5.mkv       白色相簿2-S01E05.彼此相印的心与心.mkv
+++++6.mkv       白色相簿2-S01E06.学园祭开始.mkv
+++++7.mkv       白色相簿2-S01E07.最棒的 最后一天.mkv
+++++8.mkv       白色相簿2-S01E08.须臾冬至.mkv
+++++9.mkv       白色相簿2-S01E09.形如陌路的心与心.mkv
++++10.mkv       白色相簿2-S01E10.蓦然雪化且静候飞雪再临之时(前篇).mkv
++++11.mkv       白色相簿2-S01E11.蓦然雪化且静候飞雪再临之时(后篇).mkv
++++12.mkv       白色相簿2-S01E12.毕业.mkv
++++13.mkv       白色相簿2-S01E13.传达不到的爱恋.mkv
--------
Confirm above renaming? (y/n) [y]:
Successfully renamed.

Old filenames           New filenames
===============         ===============
+++++1.ass       白色相簿2-S01E01.WHITE ALBUM.ass
+++++2.ass       白色相簿2-S01E02.邻座的钢琴与吉他.ass
+++++3.ass       白色相簿2-S01E03.轻音乐同好会再结成.ass
+++++4.ass       白色相簿2-S01E04.SOUND OF DESTINY.ass
+++++5.ass       白色相簿2-S01E05.彼此相印的心与心.ass
+++++6.ass       白色相簿2-S01E06.学园祭开始.ass
+++++7.ass       白色相簿2-S01E07.最棒的 最后一天.ass
+++++8.ass       白色相簿2-S01E08.须臾冬至.ass
+++++9.ass       白色相簿2-S01E09.形如陌路的心与心.ass
++++10.ass       白色相簿2-S01E10.蓦然雪化且静候飞雪再临之时(前篇).ass
++++11.ass       白色相簿2-S01E11.蓦然雪化且静候飞雪再临之时(后篇).ass
++++12.ass       白色相簿2-S01E12.毕业.ass
++++13.ass       白色相簿2-S01E13.传达不到的爱恋.ass
--------
Confirm above renaming? (y/n) [y]:
Successfully renamed.

Check renamed files under folder: test
```

## 许可证

[MIT](./LICENSE)
