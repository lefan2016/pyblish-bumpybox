import os

import pyblish.api
import pymel.core
import clique


class BumpyboxMayaCollectSets(pyblish.api.ContextPlugin):
    """ Collects all sets in scene """

    order = pyblish.api.CollectorOrder
    label = "Sets"
    hosts = ["maya"]

    def process(self, context):

        for object_set in pymel.core.ls(type="objectSet"):

            # Skip all default sets.
            default_sets = ["defaultLightSet", "defaultObjectSet",
                            "initialParticleSE", "initialShadingGroup"]
            if str(object_set) in default_sets:
                continue

            extensions = {
                "mayaAscii": "ma", "mayaBinary": "mb", "alembic": "abc"
            }

            # Add an instance per format supported.
            for fmt in ["mayaBinary", "mayaAscii", "alembic"]:

                instance = context.create_instance(name=object_set.name())
                instance.add(object_set)
                instance.data["families"] = [fmt, "local", "cache"]

                label = "{0} - {1}".format(object_set.name(), fmt)
                instance.data["label"] = label

                # Adding/Checking publish attribute
                instance.data["publish"] = False
                if hasattr(object_set, fmt):
                    attr = pymel.core.Attribute(object_set.name() + "." + fmt)
                    instance.data["publish"] = attr.get()
                else:
                    pymel.core.addAttr(object_set,
                                       longName=fmt,
                                       defaultValue=False,
                                       attributeType="bool")
                    attr = pymel.core.Attribute(object_set.name() + "." + fmt)
                    pymel.core.setAttr(attr, channelBox=True)

                # Generate collection
                filename = os.path.splitext(
                    os.path.basename(context.data["currentFile"])
                )[0]
                path = os.path.join(
                    os.path.dirname(context.data["currentFile"]),
                    "workspace", filename
                )
                head = "{0}_{1}.".format(path, object_set.name())
                tail = "." + extensions[fmt]
                collection = clique.Collection(head=head, padding=4, tail=tail)

                frame_start = int(
                    pymel.core.playbackOptions(query=True, minTime=True)
                )
                collection.add(head + str(frame_start).zfill(4) + tail)

                instance.data["collection"] = collection