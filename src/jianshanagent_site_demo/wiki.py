"""站点插件里管查询的那一摊：这个站自己的条目怎么查。

这里示范的是最简单的一种——配置里的别名表：用户说昵称，对上页面的正式标题。
:class:`WikiProvider` 的方法都有什么都不做的默认实现，用到哪个覆盖哪个（接口见核心的
``plugins/wiki_query/provider.py``）：自己的条目种类（``kinds``、``get_page``、``format_page``）、
自己的命令和给模型用的工具（``register``）都从这里接。

建在 wiki 平台上的站（清单里写了 ``platform``）要用平台的接口时，在 ``create`` 里拿平台的实例::

    from jianshanagent.platforms.huiji.wiki import HuijiPlatform

    def create(setup: SiteSetup) -> DemoProvider:
        return DemoProvider(setup.platform(HuijiPlatform), ...)
"""

from __future__ import annotations

from collections.abc import Mapping

from jianshanagent.plugins.wiki_query.client import NameMatch
from jianshanagent.plugins.wiki_query.provider import SiteSetup, WikiProvider


class DemoProvider(WikiProvider):
    id = "demo"  # 和清单里的 id 一样

    def __init__(self, aliases: Mapping[str, str]):
        self.aliases = dict(aliases)

    async def lookup_name(self, name: str) -> list[NameMatch]:
        """``name`` 是登记过的别名时，给出它对应的页面。"""
        title = self.aliases.get(name.strip())
        if title is None:
            return []
        known = tuple(alias for alias, target in self.aliases.items() if target == title)
        return [NameMatch(title=title, aliases=known)]

    async def name_candidates(self, name: str, limit: int) -> list[NameMatch]:
        """别名里包含 ``name`` 的页面（只能当提示）。"""
        titles = dict.fromkeys(
            title for alias, title in self.aliases.items() if name and name in alias
        )
        return [NameMatch(title=title, exact=False) for title in list(titles)[:limit]]


def create(setup: SiteSetup) -> DemoProvider:
    """入口：``setup.raw`` 是这个插件自己的配置。"""
    aliases = (setup.raw.get("wiki") or {}).get("aliases") or {}
    return DemoProvider(aliases)
