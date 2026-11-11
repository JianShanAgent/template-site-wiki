<p align="center"><img src="assets/icon.svg" width="96" alt="JianShanAgent"></p>

# template-site-wiki

> JianShanAgent · 模板 · 站点插件 · 站 · 接一个新的 wiki 时，从这里开始
>
> Template for a JianShanAgent site plugin: start here to teach the bot about one specific MediaWiki site.

| | |
|---|---|
| 层 | 站点插件 · 站（模板） |
| id | `demo`（占位，要改；上级 `example`） |
| 包 | 发行包 `jianshanagent-site-example-demo` / Python 包 `jianshanagent_site_example_demo` |
| 依赖 | 核心 `jianshanagent`、上级插件 `jianshanagent-site-example`（[`template-site-platform`](https://github.com/JianShanAgent/template-site-platform)） |
| 登记 | entry points `jianshanagent.sites`：`demo = "jianshanagent_site_example_demo"` |

## 这是什么

一个能装、能跑测试、能通过规范自检的最小站插件，名字都是占位的。站插件放的是**某一个 wiki** 特有的东西。
不写站插件，机器人也能服务一个 MediaWiki（只认页面）；写它是为了让机器人懂这个站自己的数据和说法。

模板里三种能力各示范了一个：

- **查询**（`wiki`）：配置里的别名表——用户说昵称，对上页面的正式标题。
- **知识库**（`knowledge`）：一个空的接入点，列出了可以插手的地方。
- **对通用配置的补充**（`extend`）：这个站的清洗规则、问题分类、提示词里的说法、人设。很多站只靠这一段就够了，不用写代码。

实际的例子：[`site-huiji-yys`](https://github.com/JianShanAgent/site-huiji-yys)（灰机平台上的阴阳师 wiki）。

## 在整套里的位置

JianShanAgent 由几个仓库拼成（并排放在开发机的同一个目录下）：

| 仓库 | 层 | 管什么 |
|---|---|---|
| [`agent-core`](https://github.com/JianShanAgent/agent-core) | 核心 | 机器人本体：QQ 网关、七个功能插件（查询、知识库、查证、对话、记忆、群聊记录、安全兜底）、管理后台、部署工具 |
| [`site-huiji`](https://github.com/JianShanAgent/site-huiji) | 站点插件 · 平台 | 灰机 wiki 平台在 MediaWiki 之上多出来的东西 |
| [`site-huiji-yys`](https://github.com/JianShanAgent/site-huiji-yys) | 站点插件 · 站 | 阴阳师 wiki 特有的东西（建在灰机平台上） |
| [`instance-yys`](https://github.com/JianShanAgent/instance-yys) | 实例 | 阴阳师 wiki 机器人这个部署：配置、用哪个版本、运维备忘 |
| [`template-site-platform`](https://github.com/JianShanAgent/template-site-platform) | 模板 · 站点插件 · 平台 | 接一个新的 wiki 平台时，从它开始 |
| **[`template-site-wiki`](https://github.com/JianShanAgent/template-site-wiki)（这里）** | 模板 · 站点插件 · 站 | 接一个新的 wiki 时，从它开始 |
| [`template-instance`](https://github.com/JianShanAgent/template-instance) | 模板 · 实例 | 新建一个部署时，从它开始 |

## 目录

```
src/jianshanagent_site_example_demo/
  plugin.yaml      清单（kind: site，parent: example）
  config.yaml      默认配置：wiki 段（别名表）、extend 段（对通用配置的补充）
  wiki.py          查询扩展点：DemoProvider，入口 create(setup)
  knowledge.py     知识库扩展点：DemoKnowledge，入口 create(setup)
tests/
  config/          「一个用了这个插件的部署」的配置，测试里用；实例的 core.wiki.yaml 照它写
  test_conformance.py   规范自检
  test_plugin.py        装上以后带来了什么
```

## 安装和启用

**从模板开始**：在 GitHub 上点「Use this template」建一个新仓库，名字照规范取 `site-<平台>-<站>`
（不建在任何平台上的站是 `site-<站>`）。然后把占位的名字换掉（下面以平台 `acme`、站 `foo` 为例），
这几处要一起改，改完跑测试，规范自检会指出漏掉的地方：

| 在哪 | 改什么 |
|---|---|
| `src/jianshanagent_site_example_demo/` | 目录改名为 `jianshanagent_site_acme_foo`（不建在平台上：`jianshanagent_site_foo`） |
| `pyproject.toml` | `name`、`dependencies` 里的上级、entry points 那一行（`foo = "jianshanagent_site_acme_foo"`）、`packages`、`[tool.uv.sources]` 里上级的目录 |
| `plugin.yaml` | `id`、`name`、`description`、`parent`（不建在平台上：删掉这一行） |
| `wiki.py`、`knowledge.py` | 类的 `id` 和类名；从上级导入的那一行（不建在平台上：去掉 `setup.parent(...)`） |
| `config.yaml`、`tests/` | 配置名 `site.foo`、`site: foo`、导入路径 |
| `README.md` | 这份文档：照 [插件规范](https://github.com/JianShanAgent/agent-core/blob/main/docs/插件规范.md) 第 6 节的骨架改写 |

**启用**：装进和核心同一个 Python 环境（实例仓库的 `pyproject.toml` 和 `components.lock` 里列上它和它的上级）。
实例的 `config/core.wiki.yaml` 照 [`tests/config/core.wiki.yaml`](tests/config/core.wiki.yaml) 写：wiki 的地址，和 `site: <站的 id>`
（只写这一级，上级会自动带出来）。

## 配置

配置名 `site.<id>`，默认值在插件目录的 `config.yaml`；某个部署要改，在实例的 `config/site.<id>.yaml` 里只写要改的项。
`extend` 段不能在管理后台里改（它在读配置时就并进了 `plugin.knowledge`、`plugin.research`、`plugin.chat` 等通用配置）。

## 开发和测试

```bash
uv sync --extra dev      # 核心和上级插件用旁边目录里的源码（../agent-core、../template-site-platform）
uv run pytest
uv run ruff check . && uv run ruff format --check .
```

对真实的 wiki 取数要守规矩：那是别人的站点，限速和并发不要调高。

## 相关文档

- [插件规范](https://github.com/JianShanAgent/agent-core/blob/main/docs/插件规范.md)：分层和命名、清单、登记、各种插件要提供什么、文档格式
- 核心的 `src/jianshanagent/plugins/wiki_query/provider.py`、`src/jianshanagent/plugins/knowledge/site.py`：两个扩展点的接口
- 许可：[MIT](LICENSE)
