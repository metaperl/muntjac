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

from muntjac.terminal.gwt.client.event_id import EventId
from muntjac.event.component_event_listener import IComponentEventListener
from muntjac.ui.component import Event as ComponentEvent


class IFocusNotifier(object):
    """The interface for adding and removing C{FocusEvent} listeners.
    By implementing this interface a class explicitly announces that it will
    generate a C{FocusEvent} when it receives keyboard focus.

    Note: The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    C{addListener} and C{removeListener} methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.

    @since 6.2
    @see: IFocusListener
    @see: FocusEvent
    """

    def addListener(self, listener, iface):
        """Adds a C{IFocusListener} to the Component which gets fired
        when a C{Field} receives keyboard focus.

        @param listener:
        @see: IFocusListener
        @since 6.2
        """
        if iface == IFocusListener:
            raise NotImplementedError
        else:
            super(IFocusNotifier, self).addListener(listener, iface)


    def addFocusListener(self, listener):
        self.addListener(listener, IFocusListener)


    def removeListener(self, listener, iface):
        """Removes a C{IFocusListener} from the Component.

        @param listener:
        @see: IFocusListener
        @since 6.2
        """
        if iface == IFocusListener:
            raise NotImplementedError
        else:
            super(IFocusNotifier, self).removeListener(listener, iface)


    def removeFocusListener(self, listener):
        self.removeListener(listener, IFocusListener)


class IBlurNotifier(object):
    """The interface for adding and removing C{BlurEvent} listeners.
    By implementing this interface a class explicitly announces that it will
    generate a C{BlurEvent} when it loses keyboard focus.

    Note: The general Java convention is not to explicitly declare that a
    class generates events, but to directly define the
    C{addListener} and C{removeListener} methods. That
    way the caller of these methods has no real way of finding out if the
    class really will send the events, or if it just defines the methods to
    be able to implement an interface.

    @since 6.2
    @see: IBlurListener
    @see: BlurEvent
    """

    def addListener(self, listener, iface):
        """Adds a C{IBlurListener} to the Component which gets fired
        when a C{Field} loses keyboard focus.

        @param listener:
        @see: IBlurListener
        @since 6.2
        """
        if iface == IBlurListener:
            raise NotImplementedError
        else:
            super(IBlurNotifier, self).addListener(listener, iface)


    def addBlurListener(self, listener):
        self.addListener(listener, IBlurListener)


    def removeListener(self, listener, iface):
        """Removes a C{IBlurListener} from the Component.

        @param listener:
        @see: IBlurListener
        @since 6.2
        """
        if iface == IBlurListener:
            raise NotImplementedError
        else:
            super(IBlurNotifier, self).removeListener(listener, iface)


    def removeBlurListener(self, listener):
        self.removeListener(listener, IBlurListener)


class FocusEvent(ComponentEvent):
    """C{FocusEvent} class for holding additional event information.
    Fired when a C{Field} receives keyboard focus.

    @since 6.2
    """
    # Identifier for event that can be used in L{EventRouter}
    EVENT_ID = EventId.FOCUS

    def __init__(self, source):
        super(FocusEvent, self).__init__(source)


class IFocusListener(IComponentEventListener):
    """C{IFocusListener} interface for listening for
    C{FocusEvent} fired by a C{Field}.

    @see: FocusEvent
    @since 6.2
    """

    def focus(self, event):
        """Component has been focused

        @param event
                   Component focus event.
        """
        raise NotImplementedError

    focusMethod = focus


class BlurEvent(ComponentEvent):
    """C{BlurEvent} class for holding additional event information.
    Fired when a C{Field} loses keyboard focus.

    @since 6.2
    """

    # Identifier for event that can be used in L{EventRouter}
    EVENT_ID = EventId.BLUR

    def __init__(self, source):
        super(BlurEvent, self).__init__(source)


class IBlurListener(IComponentEventListener):
    """C{IBlurListener} interface for listening for
    C{BlurEvent} fired by a C{Field}.

    @see: BlurEvent
    @since 6.2
    """

    def blur(self, event):
        """Component has been blurred

        @param event
                   Component blur event.
        """
        raise NotImplementedError

    blurMethod = blur


class TextChangeEvent(ComponentEvent):
    """TextChangeEvents are fired when the user is editing the text content of a
    field. Most commonly text change events are triggered by typing text with
    keyboard, but e.g. pasting content from clip board to a text field also
    triggers an event.

    TextChangeEvents differ from L{ValueChangeEvent}s so that they are
    triggered repeatedly while the end user is filling the field.
    ValueChangeEvents are not fired until the user for example hits enter or
    focuses another field. Also note the difference that TextChangeEvents are
    only fired if the change is triggered from the user, while
    ValueChangeEvents are also fired if the field value is set by the
    application code.

    The L{ITextChangeNotifier}s implementation may decide when exactly
    TextChangeEvents are fired. TextChangeEvents are not necessary fire for
    example on each key press, but buffered with a small delay. The
    L{TextField} component supports different modes for triggering
    TextChangeEvents.

    @see: ITextChangeListener
    @see: ITextChangeNotifier
    @see: TextField#setTextChangeEventMode(TextField.TextChangeEventMode)
    @since 6.5
    """

    def __init__(self, source):
        super(TextChangeEvent, self).__init__(source)


    def getText(self):
        """@return: the text content of the field after the
                L{TextChangeEvent}
        """
        pass


    def getCursorPosition(self):
        """@return: the cursor position during after the
        L{TextChangeEvent}"""
        pass


class ITextChangeListener(IComponentEventListener):
    """A listener for L{TextChangeEvent}s.

    @since 6.5
    """

    EVENT_ID = 'ie'

    def textChange(self, event):
        """This method is called repeatedly while the text is edited by a
        user.

        @param event
                   the event providing details of the text change
        """
        raise NotImplementedError


EVENT_METHOD = ITextChangeListener.textChange


class ITextChangeNotifier(object):
    """An interface implemented by a L{Field} supporting
    L{TextChangeEvent}s. An example a L{TextField} supports
    L{ITextChangeListener}s.
    """

    def addListener(self, listener, iface):
        if iface == ITextChangeListener:
            raise NotImplementedError
        else:
            super(ITextChangeNotifier, self).addListener(listener, iface)


    def addTextChangeListener(self, listener):
        self.addListener(listener, ITextChangeListener)


    def removeListener(self, listener, iface):
        if iface == ITextChangeListener:
            raise NotImplementedError
        else:
            super(ITextChangeNotifier, self).removeListener(listener, iface)


    def removeTextChangeListener(self, listener):
        self.removeListener(listener, ITextChangeListener)
