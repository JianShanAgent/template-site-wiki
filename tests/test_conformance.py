"""这个插件合不合 JianShanAgent 的插件规范（核心仓库 agent-core 的 docs/插件规范.md）。"""

from jianshanagent.testing.conformance import check_plugin


def test_conforms_to_the_plugin_spec() -> None:
    manifest = check_plugin("jianshanagent_site_example_demo")
    assert (manifest.id, manifest.parent) == ("demo", "example")
