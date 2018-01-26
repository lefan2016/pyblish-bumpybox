from pyblish import api


class ExtractLocal(api.ContextPlugin):
    """ Extracts nodes locally. """

    families = ["local"]
    order = api.ExtractorOrder
    label = "Local"
    optional = True
    hosts = ["houdini"]

    def process(self, instance):
        import os

        node = instance[0]

        node.parm("execute").pressButton()

        # raising any errors
        if node.errors():
            raise ValueError(node.errors())

        # gather extracted files
        collection = instance.data["collection"]
        for f in collection:
            if not os.path.exists(f):
                collection.remove(f)