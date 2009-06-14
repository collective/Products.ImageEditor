import random

def normalize_name(name):
    return name.lower().replace(' ', '-').replace(':', "-")

def generate_random_url(context):
    return context.absolute_url() + "/currenteditedimage.jpg?" + str(random.randint(0, 1000000))
    
def get_image_information(editor):
    image_info = editor.get_current_image_info()
    return {
        'url' : generate_random_url(editor.context),
        'can_undo' : editor.can_undo(),
        'can_redo' : editor.can_redo(),
        'can_save' : editor.pos > 0,
        'size' : image_info['sizeformatted'],
        'width' : image_info['width'],
        'height' : image_info['height']
    }
    
def json(d):
    
    def convert_type(value):
        if type(value) == bool:
            return str(value).lower()
        elif type(value) == str:
            return "'%s'" % value
        elif type(value) == dict:
            return json(value)
        elif type(value) == list or type(value) == tuple:
            return "[%s]" % ','.join([convert_type(v) for v in value])
        else:
            return value
        
    return "{%s}" % (', '.join(["%s : %s" % (name, convert_type(value)) for name, value in d.items()]))
    
    