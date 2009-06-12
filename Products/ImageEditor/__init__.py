from zope.i18nmessageid import MessageFactory
imageeditor_message_factory = MessageFactory('Products.ImageEditor')

import os

cwd = os.sep.join(__file__.split(os.sep)[:-1])
dependencies = [d.strip('\n').strip() for d in open(os.path.join(cwd, 'dependencies.txt')).readlines() ]