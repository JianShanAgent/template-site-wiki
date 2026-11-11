<p align="center"><img src="assets/icon.svg" width="88" alt="JianShanAgent"></p>

<h1 align="center">template-site-wiki</h1>

<p align="center">让<a href="https://github.com/JianShanAgent/agent-core">见山</a>读懂你的 wiki，从这里开始。</p>

<p align="center">
  <img src="https://img.shields.io/badge/模板-站点插件%20·%20站-2f6b5a?style=flat-square&labelColor=1f3b34" alt="模板：站点插件 · 站">
  <img src="https://img.shields.io/github/license/JianShanAgent/template-site-wiki?label=License&color=2f6b5a&style=flat-square&labelColor=1f3b34" alt="License">
</p>

<sub>Template for a JianShanAgent site plugin: teach the bot about one specific MediaWiki site. Documentation is in Chinese.</sub>

## 这是什么

不写任何插件，见山也能服务一个 MediaWiki，只是它只认得「页面」。它不知道这个站的人管某个角色叫什么外号，不知道页面上哪块是导航、哪块是正文，说话也是对什么 wiki 都通用的口气。

**站点插件**就是把一个 wiki 自己的东西教给它。这个模板是一个最小的、能装能测的站点插件，名字都是占位的（平台 `example`，站 `demo`）。

## 先看这个：多半只用写配置

打开 [`config.yaml`](src/jianshanagent_site_example_demo/config.yaml)。它的 `extend` 段是「对通用配置的补充」，读配置时自动并进去，不用写一行代码：

```yaml
extend:
  plugin.knowledge:
    clean:
      remove_classes: [demo-nav]            # 这个站的导航模板：不进知识库
  plugin.research:
    analysis:
      topics: [人物, 道具, 活动, 其它]         # 问题分成哪几类
  persona/persona.default:
    name: "示例 Wiki 助手"                    # 人设
```

清洗规则、问题怎么分类、提示词里的说法、人设，都是这样写的。很多站做到这一步就够了。

## 要写代码的两处

| 文件 | 接在哪 | 模板里示范的 | 还能做什么 |
|---|---|---|---|
| [`wiki.py`](src/jianshanagent_site_example_demo/wiki.py) | 查询 | 别名表：用户说昵称，对上页面的正式标题 | 这个站自己的条目种类、结构化的回复、自己的命令和给模型用的工具 |
| [`knowledge.py`](src/jianshanagent_site_example_demo/knowledge.py) | 知识库 | 一个空的接入点 | 页面以外的内容来源、切片上的标注、图库选图、哪些改动影响哪些页面 |

两边的基类里每个方法都有「什么都不做」的默认实现，用到哪个覆盖哪个。走得最远的例子是阴阳师 wiki 的 [`site-huiji-yys`](https://github.com/JianShanAgent/site-huiji-yys)。

## 从模板开始

点「Use this template」，新仓库叫 `site-<平台>-<站>`；不建在任何平台上的站叫 `site-<站>`。然后把占位的名字换掉。下面以平台 `acme`、站 `foo` 为例，这几处要一起改：

| 在哪 | 改成什么 |
|---|---|
| 目录 `src/jianshanagent_site_example_demo/` | `jianshanagent_site_acme_foo` |
| `pyproject.toml` | 包名、依赖里的上级、登记那一行 `foo = "jianshanagent_site_acme_foo"`、上级的目录 |
| `plugin.yaml` | `id: foo`、`parent: acme`、名字和说明 |
| `wiki.py`、`knowledge.py` | 类里的 `id`、从上级导入的那一行 |
| `config.yaml`、`tests/` | `site.foo`、`site: foo`、导入路径 |

不建在平台上的站：去掉 `plugin.yaml` 的 `parent`、`pyproject.toml` 里的上级、代码里的 `setup.parent(...)`。

不用怕改漏——跑一遍测试，里面的**规范自检**会指出哪里的名字对不上、该叫什么：

```bash
uv sync --extra dev      # 核心和上级插件用旁边目录里的源码（../agent-core、../template-site-platform）
uv run pytest
```

## 装上它

在实例仓库里加上它（和它的上级），然后 `config/core.wiki.yaml` 照 [`tests/config/core.wiki.yaml`](tests/config/core.wiki.yaml) 写：

```yaml
site: foo          # 只写这一级，上级会被自动带出来
```

插件的规矩见[插件规范](https://github.com/JianShanAgent/agent-core/blob/main/docs/插件规范.md)。全部仓库的目录在[组织主页](https://github.com/JianShanAgent)。

## 许可

[MIT](LICENSE)
