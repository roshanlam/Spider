"""Tests for plugin system."""

import pytest
from spider.plugin import Plugin, PluginManager


class TestPlugin:
    """Tests for base Plugin class."""

    @pytest.mark.asyncio
    async def test_plugin_should_run_default(self):
        """Test that should_run returns True by default."""
        plugin = Plugin()
        result = await plugin.should_run("http://example.com", "<html></html>")
        assert result is True

    @pytest.mark.asyncio
    async def test_plugin_process_not_implemented(self):
        """Test that process raises NotImplementedError."""
        plugin = Plugin()
        with pytest.raises(NotImplementedError):
            await plugin.process("http://example.com", "<html></html>")


class MockPlugin(Plugin):
    """Mock plugin for testing."""

    def __init__(self):
        self.should_run_called = False
        self.process_called = False
        self.processed_content = None

    async def should_run(self, url: str, content: str) -> bool:
        self.should_run_called = True
        return True

    async def process(self, url: str, content: str) -> str:
        self.process_called = True
        self.processed_content = content
        return f"PROCESSED: {content}"


class ConditionalPlugin(Plugin):
    """Plugin that only runs on certain URLs."""

    async def should_run(self, url: str, content: str) -> bool:
        return "example.com" in url

    async def process(self, url: str, content: str) -> str:
        return content + " [PROCESSED]"


class FailingPlugin(Plugin):
    """Plugin that raises an exception."""

    async def should_run(self, url: str, content: str) -> bool:
        return True

    async def process(self, url: str, content: str) -> str:
        raise ValueError("Test error")


class TestPluginManager:
    """Tests for PluginManager class."""

    def test_plugin_manager_creation(self):
        """Test creating a plugin manager."""
        manager = PluginManager()
        assert manager is not None
        assert len(manager.plugins) == 0

    def test_plugin_manager_register(self):
        """Test registering a plugin."""
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)
        assert len(manager.plugins) == 1
        assert manager.plugins[0] == plugin

    def test_plugin_manager_register_multiple(self):
        """Test registering multiple plugins."""
        manager = PluginManager()
        plugin1 = MockPlugin()
        plugin2 = MockPlugin()
        manager.register(plugin1)
        manager.register(plugin2)
        assert len(manager.plugins) == 2

    @pytest.mark.asyncio
    async def test_plugin_manager_run_plugins(self):
        """Test running plugins through manager."""
        manager = PluginManager()
        plugin = MockPlugin()
        manager.register(plugin)

        url = "http://example.com"
        content = "<html>Test</html>"
        result = await manager.run_plugins(url, content)

        assert plugin.should_run_called
        assert plugin.process_called
        assert result == "PROCESSED: <html>Test</html>"

    @pytest.mark.asyncio
    async def test_plugin_manager_conditional_plugin(self):
        """Test that plugins with should_run=False don't process."""
        manager = PluginManager()
        plugin = ConditionalPlugin()
        manager.register(plugin)

        # Should run for example.com
        result1 = await manager.run_plugins("http://example.com", "test")
        assert "[PROCESSED]" in result1

        # Should not run for other.com
        result2 = await manager.run_plugins("http://other.com", "test")
        assert "[PROCESSED]" not in result2

    @pytest.mark.asyncio
    async def test_plugin_manager_chain(self):
        """Test that plugins are chained correctly."""
        manager = PluginManager()

        class Plugin1(Plugin):
            async def process(self, url: str, content: str) -> str:
                return content + " [P1]"

        class Plugin2(Plugin):
            async def process(self, url: str, content: str) -> str:
                return content + " [P2]"

        manager.register(Plugin1())
        manager.register(Plugin2())

        result = await manager.run_plugins("http://example.com", "content")
        assert result == "content [P1] [P2]"

    @pytest.mark.asyncio
    async def test_plugin_manager_error_handling(self):
        """Test that plugin errors are handled gracefully."""
        manager = PluginManager()
        failing_plugin = FailingPlugin()
        working_plugin = MockPlugin()

        manager.register(failing_plugin)
        manager.register(working_plugin)

        # Should not crash, should log error and continue
        result = await manager.run_plugins("http://example.com", "test")
        # Working plugin should still process
        assert working_plugin.process_called

    @pytest.mark.asyncio
    async def test_plugin_manager_empty(self):
        """Test running with no plugins registered."""
        manager = PluginManager()
        content = "<html>Test</html>"
        result = await manager.run_plugins("http://example.com", content)
        assert result == content  # Should return unchanged

    @pytest.mark.asyncio
    async def test_plugin_manager_order(self):
        """Test that plugins run in registration order."""
        manager = PluginManager()
        order = []

        class OrderPlugin1(Plugin):
            async def process(self, url: str, content: str) -> str:
                order.append(1)
                return content

        class OrderPlugin2(Plugin):
            async def process(self, url: str, content: str) -> str:
                order.append(2)
                return content

        manager.register(OrderPlugin1())
        manager.register(OrderPlugin2())
        await manager.run_plugins("http://example.com", "test")

        assert order == [1, 2]
