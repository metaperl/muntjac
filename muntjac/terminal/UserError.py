# Copyright (C) 2010 IT Mill Ltd.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from muntjac.terminal.ErrorMessage import ErrorMessage


class UserError(ErrorMessage):
    """<code>UserError</code> is a controlled error occurred in application. User
    errors are occur in normal usage of the application and guide the user.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """
    # Content mode, where the error contains only plain text.
    CONTENT_TEXT = 0

    # Content mode, where the error contains preformatted text.
    CONTENT_PREFORMATTED = 1

    # Formatted content mode, where the contents is XML restricted to the UIDL
    # 1.0 formatting markups.
    CONTENT_UIDL = 2

    def __init__(self, message, contentMode=None, errorLevel=None):
        """Creates a textual error message of level ERROR.

        @param textErrorMessage
                   the text of the error message.
        ---
        Creates a error message with level and content mode.

        @param message
                   the error message.
        @param contentMode
                   the content Mode.
        @param errorLevel
                   the level of error.
        """
        # Content mode.
        self._mode = self.CONTENT_TEXT
        # Message in content mode.
        self._msg = message
        # Error level.
        self._level = ErrorMessage.ERROR

        if contentMode is not None:
            # Check the parameters
            if (contentMode < 0) or (contentMode > 2):
                raise ValueError, 'Unsupported content mode: ' + contentMode
            self._mode = contentMode
            self._level = errorLevel


    def getErrorLevel(self):
        return self._level


    def addListener(self, listener):
        pass


    def removeListener(self, listener):
        pass


    def requestRepaint(self):
        pass


    def paint(self, target):

        target.startTag('error')

        # Error level
        if self._level >= ErrorMessage.SYSTEMERROR:
            target.addAttribute('level', 'system')
        elif self._level >= ErrorMessage.CRITICAL:
            target.addAttribute('level', 'critical')
        elif self._level >= ErrorMessage.ERROR:
            target.addAttribute('level', 'error')
        elif self._level >= ErrorMessage.WARNING:
            target.addAttribute('level', 'warning')
        else:
            target.addAttribute('level', 'info')

        # Paint the message
        if self._mode == self.CONTENT_TEXT:
            target.addText(self._msg)
        elif self._mode == self.CONTENT_UIDL:
            target.addUIDL(self._msg)
        elif self._mode == self.CONTENT_PREFORMATTED:
            target.startTag('pre')
            target.addText(self._msg)
            target.endTag('pre')

        target.endTag('error')


    def requestRepaintRequests(self):
        pass


    def toString(self):
        return self._msg


    def getDebugId(self):
        return None


    def setDebugId(self, idd):
        raise NotImplementedError, 'Setting testing id for this Paintable is not implemented'
