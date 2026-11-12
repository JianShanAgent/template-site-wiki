"""装上、在配置里点了名以后，这个插件带来了什么。"""

from __future__ import annotations

from jianshanagent.core.config import load_config
from jianshanagent.core.sites import EXTENSION_WIKI, load_sites
from jianshanagent.core.wiki import load_wiki, wiki_subject
from jianshanagent.plugins.knowledge.settings import load_settings
from jianshanagent_site_example.wiki import ExamplePlatform

from jianshanagent_site_example_demo.knowledge import DemoKnowledge
from jianshanagent_site_example_demo.wiki import DemoProvider


def test_naming_the_site_brings_its_platform_and_both_additions() -> None:
    config = load_config()
    # 配置里只写了 example_demo，上级 example 顺着清单带出来、排在前面
    assert config.wiki("main").raw["site"] == "example_demo"
    assert config.sites == ["example", "example_demo"]
    # 两级对通用配置的补充都并进去了
    classes = config.plugin("knowledge")["clean"]["remove_classes"]
    assert {"example-noindex", "demo-nav"} <= set(classes)
    assert config.plugin("research")["analysis"]["topics"] == ["人物", "道具", "活动", "其它"]
    assert config.get("persona/persona.default")["name"] == "示例 Wiki 助手"
    assert wiki_subject(config).bot == "示例 wiki 机器人"


async def test_aliases_resolve_to_page_titles() -> None:
    config = load_config()
    platform, demo = load_sites(config, EXTENSION_WIKI, load_wiki(config, "main"))
    assert isinstance(platform, ExamplePlatform) and isinstance(demo, DemoProvider)
    assert demo.platform is platform  # 站插件拿到了上级的实例

    (match,) = await demo.lookup_name("示例昵称")
    assert (match.title, match.aliases, match.exact) == ("示例页面", ("示例昵称",), True)
    assert await demo.lookup_name("没登记的名字") == []
    (hint,) = await demo.name_candidates("昵称", limit=5)
    assert (hint.title, hint.exact) == ("示例页面", False)


def test_the_knowledge_base_loads_the_site() -> None:
    settings = load_settings(load_config())
    # 平台插件没接知识库这个扩展点，所以只有这个站
    assert settings.sites.ids == ("example_demo",)
    assert isinstance(settings.sites.require("example_demo"), DemoKnowledge)
