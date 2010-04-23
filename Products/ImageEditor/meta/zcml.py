from Products.ImageEditor.utils import normalize_name
from zope.interface import Interface
from zope.configuration.fields import GlobalObject
from zope.schema import TextLine
from Products.ImageEditor.interfaces.actions import IImageEditorAction


class IEditorAction(Interface):
    """
    Fields to create an image editor action
    """

    class_ = GlobalObject(
        title=u"Class",
        description=u"The actual class that will be called when this action is selected",
        required=True
    )
    
    before = TextLine(
        title=u"Before",
        description=u"Insert this action before another action.",
        required=False
    )
    
    after = TextLine(
        title=u"After",
        description=u"Insert this action after another action.",
        required=False
    )
    

IMAGE_EDITOR_ACTIONS = {}
ACTION_ORDER = []

def get_actions():
    for name in ACTION_ORDER:
        yield name, IMAGE_EDITOR_ACTIONS[name]
    
def get_action_class(name):
    if IMAGE_EDITOR_ACTIONS.has_key(name):
        return IMAGE_EDITOR_ACTIONS[name].class_
    else:
        raise Exception("Can't find action %s" % name)
        
def get_action_names():
    for name in ACTION_ORDER:
        yield name
        
class ImageEditAction:

    def __init__(self, class_, before=None, after=None):
        self.name = normalize_name(class_.name)
        self.class_ = class_
        self.before = before
        self.after = after


def add_action(_context, class_, before=None, after=None):
    
    action = ImageEditAction(class_, before, after)
    
    IMAGE_EDITOR_ACTIONS[action.name] = action
    
    if not IImageEditorAction.implementedBy(action.class_):
        raise Exception("Class must implement IImageEditorAction")
    
    if action.before is not None:
        if action.before == "*":
            ACTION_ORDER.insert(0, action.name)
        else:
            for index in range(0, len(ACTION_ORDER)):
                if action.before == ACTION_ORDER[index]:
                    ACTION_ORDER.insert(index, action.name)
                    break
                    
    elif action.after is not None:
        if action.after == "*":
            ACTION_ORDER.insert(len(ACTION_ORDER), action.name)
        else:
            for index in range(0, len(ACTION_ORDER)):
                if action.after == ACTION_ORDER[index]:
                    ACTION_ORDER.insert(index+1, action.name)
                    break
                    
    else:
        ACTION_ORDER.append(action.name)
    