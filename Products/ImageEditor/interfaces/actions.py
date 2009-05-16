from zope.interface import Interface, Attribute

class IImageEditorAction(Interface):
    """
    The base action for all image editor actions
    """
    name = Attribute("""The name of the action.""")
    description = Attribute("""A description of what it does.""")
    skip_apply = Attribute("""Whether the button should skip the apply button and immediately perform.""")
    options = Attribute("""The FormFields of options that the action has.""")
    icon = Attribute("""The icon for the button to use.""")
    
    def action_parameters():
        """
        javascript that will gather the parameters to be sent
        to request.  Return false and do not implement to just use
        standard options.  This is mostly just for complex actions.
        The javascript here should be a method that returns a JSON
        object of parameters.
        """
        
    def on_setup():
        """
        extra javascript that will be added for any extra setup needed
        for button actions.
        """
        
    def __call__():
        """
        This is the heavy lifter and will perform the actual action.
        """