"""装上、在配置里点了名以后，这个插件带来了什么。"""

from __future__ import annotations

from jianshanagent.core.config import load_config
from jianshanagent.core.sites import EXTENSION_WIKI, load_sites
from jianshanagent.core.wiki import load_wiki, wiki_subject
from jianshanagent.plugins.knowledge.settings import load_settings

from jianshanagent_site_demo.knowledge import DemoKnowledge
from jianshanagent_site_demo.wiki import DemoProvider


def test_naming_the_site_brings_its_additions() -> None:
    config = load_config()
    entry = config.wiki("main")
    # 配置里只写了站点插件；是哪个平台跟着它的清单走（没写 platform：自己架的 MediaWiki）
    assert entry.site is not None
    assert (entry.site.id, entry.platform.id) == ("demo", "mediawiki")
    assert config.sites == ["demo"]
    # 它对通用配置的补充并进去了
    assert "demo-nav" in config.plugin("knowledge")["clean"]["remove_classes"]
    assert config.plugin("research")["analysis"]["topics"] == ["人物", "道具", "活动", "其它"]
    assert config.get("persona/persona.default")["name"] == "示例 Wiki 助手"
    assert wiki_subject(config).bot == "示例 wiki 机器人"


async def test_aliases_resolve_to_page_titles() -> None:
    config = load_config()
    (demo,) = load_sites(config, EXTENSION_WIKI, load_wiki(config, "main"))
    assert isinstance(demo, DemoProvider)

    (match,) = await demo.lookup_name("示例昵称")
    assert (match.title, match.aliases, match.exact) == ("示例页面", ("示例昵称",), True)
    assert await demo.lookup_name("没登记的名字") == []
    (hint,) = await demo.name_candidates("昵称", limit=5)
    assert (hint.title, hint.exact) == ("示例页面", False)


def test_the_knowledge_base_loads_the_site() -> None:
    settings = load_settings(load_config())
    assert settings.sites.ids == ("demo",)
    assert isinstance(settings.sites.require("demo"), DemoKnowledge)
