import pyblish.api


class ValidateNukeStudioTask(pyblish.api.InstancePlugin):
    """Validate the output range of the task.

    This compares the output range and clip associated with the task, so see
    whether there is a difference. This difference indicates that the user has
    selected to export the clip length for the task which is very uncommon to
    do.
    """

    order = pyblish.api.ValidatorOrder
    families = ["trackItem.task"]
    label = "Task"
    hosts = ["nukestudio"]
    optional = True

    def process(self, instance):

        task = instance.data["task"]
        item = instance.data["parent"]

        output_range = task.outputRange()
        first_frame = int(item.data["item"].source().sourceIn())
        last_frame = int(item.data["item"].source().sourceOut())
        clip_duration = last_frame - first_frame + 1

        difference = clip_duration - output_range[1]
        failure_message = (
            'Looks like you are rendering the clip length for the task '
            'rather than the cut length. If this is intended, just uncheck '
            'this validator after resetting, else adjust the export range in '
            'the "Handles" section of the export dialog.'
        )
        assert difference, failure_message