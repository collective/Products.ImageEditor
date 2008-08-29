# Copyright (c) 2006-2007
# Authors: KSS Project Contributors (see docs/CREDITS.txt)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.

from kss.core.kssview import CommandSet
from zope.interface import implements

from zope.interface import Interface

class IImageEditorCommands(Interface):
    """The commands"""

    def setImage(selector, url, canUndo, canRedo, canSave, size, width, height, withKssSetup='True'):
        """
        """

class ImageEditorCommands(CommandSet):
    implements(IImageEditorCommands)
        
    def setImage(self, selector, url, canUndo, canRedo, canSave, size, width, height, withKssSetup='True'):
        """ see interfaces.py """
        command = self.commands.addCommand('setImage', selector)
        data = command.addParam('url', url)
        data = command.addParam('canUndo', canUndo)
        data = command.addParam('canRedo', canRedo)
        data = command.addParam('canSave', canSave)
        data = command.addParam('size', size)
        data = command.addParam('width', width)
        data = command.addParam('height', height)
        data = command.addParam('withKssSetup', withKssSetup)