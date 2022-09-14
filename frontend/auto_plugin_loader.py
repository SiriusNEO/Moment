import os
import ast

"""
    auto import and initialize the plugins
"""
class AutoPluginLoader:
    """
        preloaded_plugins: List[Plugin]
    """

    def __init__(self, plugin_dir: str):
        self.preloaded_plugins = []
        _increment = 0

        if not os.path.exists(plugin_dir):
            raise Exception("auto_plugin_loader error: plugin dir not exist")
        
        # black magic
        for root, dirs, files in os.walk(plugin_dir):
            for single_file in files:
                if single_file.endswith(".py"):
                    import_path = os.path.join(root, single_file)
                    with open(import_path, "r") as source:
                        ast_tree = ast.parse(source.read())
                        plugin_class_names = [node.name for node in ast.walk(ast_tree) if isinstance(node, ast.ClassDef) and len(node.bases) == 1 and node.bases[0].id == "Plugin"]
                        for plugin_class_name in plugin_class_names:
                            # [-3] for ".py"
                            exec("from {} import {}".format(import_path.replace('/', '.')[:-3], plugin_class_name))
                            exec("plugin_{} = {}()".format(str(_increment), plugin_class_name))
                            exec("self.preloaded_plugins.append(plugin_{})".format(str(_increment)))
                            _increment += 1