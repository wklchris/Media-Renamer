# Media Renamer <!-- omit in toc -->

一款从 The Movie Database (TMDb) 搜索信息的本地剧集文件重命名工具。

> 注：本人的[另一个仓库](https://github.com/wklchris/Movie-Info-Scraper)是该项目的 JavaScript 脚本实现，不过只有整理网页上的剧集标题并复制到剪切板的功能。如果浏览器上已有 TamperMonkey 插件，可以[点此前往安装脚本](https://greasyfork.org/en/scripts/408000-movie-info-scraper)。

1. [特性](#特性)
2. [安装与依赖项](#安装与依赖项)
3. [使用](#使用)
   1. [例1：关键词检索](#例1关键词检索)
   2. [例2：剧集 ID 检索](#例2剧集-id-检索)
4. [许可证](#许可证)

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
- [ ] 实现重命名功能。
- [ ] 从命令行传递参数。
- [ ] 对电影的检索操作。


## 安装与依赖项

目前依赖于 Python (>=3.6) 以及 [requests](https://github.com/psf/requests#requests-module-installation) 库。它可以由下述命令安装：

```cmd
pip install requests
```

安装目前通过下载该仓库中的以下文件来实现：

1. `TV.py`：本仓库的核心文件。
2. 准备一个 `settings.json` 文件，需要包含以下键。用户可以复制下面展示的范例，仅需替换 API 密钥。
   - **请自行替换 `api_key` 为自己的 API key**。用户需要自行从 TMDB [免费申请 API 密钥](https://developers.themoviedb.org/3/getting-started/introduction)；如果没有账户，请先创建一个免费 TMDB 账户。

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
<details><summary>点击展开/折叠 settings.json 的详细说明</summary>

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

## 使用

以下内容均以默认 `settings.json` 的 `filename_format_tv` 配置为准：
```
"{media_title}-S{tv_season}E{tv_episode}.{tv_eptitle}"
```

以下均以 Python 命令行为例。不过，仍然建议读者参考 `media-renamer.py` 中的内容撰写 `.py` 文件。

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

## 许可证

[MIT](./LICENSE)
