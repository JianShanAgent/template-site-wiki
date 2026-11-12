"""站点插件里管知识库的那一摊：往知识库里接这个站自己的内容。

核心已经会做对任何 MediaWiki 都成立的事（列页面、取渲染结果、清洗、切片、算向量、入库、自动更新）。
这个站的清洗规则是配置，写在 ``config.yaml`` 的 ``extend`` 段里，不用写代码。
要写代码的是「核心做不了的」：页面以外的内容来源、切片上的标注、图库选图、哪些改动影响哪些页面。
:class:`SitePlugin` 的每个方法都是一个可以插手的地方，默认什么都不做，用到哪个覆盖哪个
（接口和各个方法的说明见核心的 ``plugins/knowledge/site.py``）。
"""

from __future__ import annotations

from typing import Any

from jianshanagent.plugins.knowledge.pipeline import ProcessContext
from jianshanagent.plugins.knowledge.site import SitePlugin, SiteSetup


class DemoKnowledge(SitePlugin):
    id = "demo"  # 和清单里的 id 一样

    def stats(self, ctx: ProcessContext) -> dict[str, Any]:
        """这个插件自己的统计，并进每次运行的统计里。示范用，可以删。"""
        return {"demo_plugin": True}


def create(setup: SiteSetup) -> DemoKnowledge:
    return DemoKnowledge()
