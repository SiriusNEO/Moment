"""
    The class of the bot, containing necessary information for creating the bot
"""

from model.plugin import Plugin

class Bot:

    def __init__(self, name: str):
        self.name = name
        self.installed_plugins = []
        self.installed_plugins_name = []

    def install(self, plugin: Plugin, *arg):
        plugin_name = plugin.__class__.__name__

        for requirement in plugin.requirements:
            if requirement not in self.installed_plugins_name:
                raise "Requirements of Plugin {} not installed, need: {}".format(plugin_name, requirement)
        
        plugin.setup(*arg)

        self.installed_plugins.append(plugin)
        self.installed_plugins_name.append(plugin_name)
            
