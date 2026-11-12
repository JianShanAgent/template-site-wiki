<p align="center"><img src="assets/icon.svg" width="88" alt="JianShanAgent"></p>

<h1 align="center">template-site-wiki</h1>

<p align="center"><a href="https://github.com/JianShanAgent/agent-core">JianShanAgent（见山）</a>站点插件脚手架模板：让机器人读懂你的 Wiki。</p>

<p align="center">
  <img src="https://img.shields.io/badge/模板-站点插件-2f6b5a?style=flat-square&labelColor=1f3b34" alt="模板：站点插件">
  <img src="https://img.shields.io/github/license/JianShanAgent/template-site-wiki?label=License&color=2f6b5a&style=flat-square&labelColor=1f3b34" alt="License">
</p>

<sub>Starter template for a JianShanAgent site plugin: customize HTML cleaning rules, domain terminology, persona, entity aliases, and structured wiki lookups for a specific MediaWiki site.</sub>

## 什么时候需要站点插件

不装任何站点插件时，见山也能直接连接任意标准 MediaWiki 站点工作，但那时它只认识通用的“词条页面”——它不知道玩家们管某个角色叫什么外号，不知道页面里哪块是全站共用的顶部导航栏噪声，回答语气也是中规中矩的通用助手。

**站点插件**用来把某一个具体 Wiki 的领域规则教给机器人。Wiki 平台（灰机、BWiki）在 MediaWiki 之上多出来的接口和约定核心自带，站点插件只写这一个站特有的东西。

> **提示：不一定非要单独建仓库！**
> - 如果这个插件**只给你自己的机器人实例用**，你可以直接把本模板里的插件目录拷进你实例仓库的 `sites/<你的id>/` 下（无需 `pyproject.toml` 打包），改完跟着实例仓库一起 `git push` 就能同步生效。
> - 如果你希望**把插件独立开源分享、写完整的单元测试，或者在多个实例之间复用**，则使用本仓库点击 **Use this template** 创建独立的插件仓库。

## 先看最省事的做法：只写 YAML 配置，不写代码

打开模板里的 [`config.yaml`](src/jianshanagent_site_demo/config.yaml)。其中的 `extend` 段会在机器人启动读配置时自动合并进核心的通用配置里，**一行 Python 代码都不用写**就能完成大部分单站定制：

```yaml
extend:
  plugin.knowledge:
    clean:
      remove_classes: [demo-nav]            # 抓取知识库时剔除该站特有的导航栏/折叠框模板噪声
  plugin.research:
    analysis:
      topics: [人物, 道具, 活动, 其它]         # 告诉查证工作流这个站的问题分哪几类
  persona/persona.default:
    name: "某某 Wiki 助手"                    # 修改机器人的名字与说话语气人设
```

提示词里的术语注意事项（比如提醒模型“同名活动每年都有一期，注意区分年份”）同样通过 `extend` 注入。对很多中小型 Wiki 来说，配好这一段就已经很好用了。

## 需要深度定制时再写这两处 Python 代码

当你的站点有结构化数据接口、圈内黑话外号或者需要以图搜图时，再按需编写以下两个模块（基类所有方法都有默认空实现，用到哪个覆盖哪个）：

| 模块文件 | 挂载扩展点 | 本模板已写好的示范 | 你还可以继续扩展的能力 |
|---|---|---|---|
| [`wiki.py`](src/jianshanagent_site_demo/wiki.py) | `wiki`（查询侧） | **别名映射表**：用户搜外号/简称时自动对齐到正式词条标题 | 结构化属性卡片排版、专属指令（如 `/筛选`）以及暴露给对话模型的查询工具 |
| [`knowledge.py`](src/jianshanagent_site_demo/knowledge.py) | `knowledge`（知识库侧） | 最小可运行的空接入点 | 抓取页面之外的数据源（如站外公告、JSON 剧情表）、切片实体消歧标注、图库选图规则、增量同步关联页面计算 |

功能最完整的实战范例可参考灰机上的阴阳师 Wiki 插件 [`site-huiji-yys`](https://github.com/JianShanAgent/site-huiji-yys)；BWiki 上的站可参考 [`site-bwiki-yys`](https://github.com/JianShanAgent/site-bwiki-yys)。

## 操作步骤

### 路线 A：做成独立插件仓库（推荐用于开源分享与运行自检测试）

**1. 创建仓库并克隆**
点击右上角 **Use this template** 创建新仓库：
- Wiki 建在核心认识的平台上（灰机 `huiji`、BWiki `bwiki`）：仓库命名为 `site-<平台>-<站>`（如 `site-huiji-mygame`），插件 id 是 `<平台>_<站>`（`huiji_mygame`）；
- 自己架的 MediaWiki：仓库命名为 `site-<站>`（如 `site-mygame`），插件 id 就是 `<站>`。

**2. 替换模板中的占位名称**
模板里占位的是一个自己架的站 `demo`。假设你的站是灰机上的 `foo`（id 是 `huiji_foo`；自己架的站就是 `foo`），把以下几处一起替换：

| 文件或目录 | 修改内容 |
|---|---|
| `src/jianshanagent_site_demo/` | 目录重命名为 `src/jianshanagent_site_huiji_foo/` |
| `pyproject.toml` | 修改 `[project].name`（`jianshanagent-site-huiji-foo`）、`[project.entry-points."jianshanagent.sites"]` 里的 `huiji_foo = "jianshanagent_site_huiji_foo"`、打包的目录 |
| `plugin.yaml` | 修改 `id: huiji_foo`、`name` 与 `description`；平台上的站把 `platform: huiji` 那一行的注释去掉（**自己架的站不写 `platform`**） |
| `wiki.py`、`knowledge.py` | 类属性 `id = "huiji_foo"`；要用平台的接口时，在 `create` 里 `setup.platform(HuijiPlatform)`（写法见 `wiki.py` 开头） |
| `config.yaml`、`tests/` | 里面的 `site.demo`、`site: demo`、`check_plugin("jianshanagent_site_demo")` 与包导入路径 |

**3. 运行测试与规范自检**
不用担心漏改名字——本模板自带核心提供的 `check_plugin` 规范自检，哪里包名、id 或平台对不上会直接给出中文修复提示（本地测试时请将 [`agent-core`](https://github.com/JianShanAgent/agent-core) 放在同级目录 `../agent-core`）：

```bash
uv sync --extra dev
uv run pytest
```

**4. 安装到你的机器人实例中**
在你的实例仓库（由 [`template-instance`](https://github.com/JianShanAgent/template-instance) 创建）里：
1. 在 `pyproject.toml` 的 `dependencies` 加入你的插件仓库 Git 地址：
   ```toml
   "jianshanagent-site-huiji-foo @ git+https://github.com/<你的用户名>/site-huiji-foo.git",
   ```
2. 在 `config/core.wiki.yaml` 的 `wikis` 名单里，给这个 wiki 填入插件 `id`（它在哪个平台上写在它的清单里，核心带着的平台会先加载）：
   ```yaml
   wikis:
     - id: main
       api_url: "https://your.wiki/api.php"
       site: huiji_foo
   ```
3. 重新执行 `uv sync` 或 `docker compose up -d --build` 即可生效。

**5. 发版，进站点目录（可选）**
模板带着发版流程（[`.github/workflows/release.yml`](.github/workflows/release.yml)）：改 `pyproject.toml` 里的 `version` 并提交，打一个带附注的标签 `v<版本>` 推上来，就会跑测试、打安装包（`jianshanagent_site_<id>-<版本>-py3-none-any.whl` 和 `SHA256SUMS`）并发一个 Release。

JianShanAgent 组织下的站点插件发过版以后，在[站点目录](https://github.com/JianShanAgent/catalog)的 `sites.yaml` 里加一项，所有实例的管理后台「Wiki」页里就能按平台找到它、一键添加（机器人自己下载安装包，不用改实例的 `pyproject.toml`）。

---

### 路线 B：直接放进实例仓库的 `sites/` 目录（免建新仓、免打包）

如果不想多维护一个仓库：
1. 把 `src/jianshanagent_site_demo/` 整个文件夹复制到你实例仓库的 `sites/<你的id>/`（例如 `sites/huiji_foo/`，目录名就是插件 id）。
2. 把里面的 `plugin.yaml` 和 `wiki.py` / `knowledge.py` 里的 `id` 改成 `huiji_foo`，清单里写 `platform: huiji`（自己架的站就叫 `foo`，不写 `platform`）。
3. 在实例仓库的 `config/core.wiki.yaml` 里给这个 wiki 写上 `site: huiji_foo`，直接启动机器人即可加载。

详细规范请查阅 [`agent-core` 插件规范](https://github.com/JianShanAgent/agent-core/blob/main/docs/插件规范.md)。全部仓库目录见 [JianShanAgent 组织主页](https://github.com/JianShanAgent)。

## 开源许可

[MIT License](LICENSE)
