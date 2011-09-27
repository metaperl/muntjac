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

from muntjac.event.MethodEventSource import MethodEventSource
from muntjac.event.ListenerMethod import ListenerMethod


class EventRouter(MethodEventSource):
    """<code>EventRouter</code> class implementing the inheritable event listening
    model. For more information on the event model see the
    {@link com.vaadin.event package documentation}.

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def __init__(self):
        # List of registered listeners.
        self._listenerList = None

    def addListener(self, eventType, obj, method):
        # Registers a new listener with the specified activation method to listen
        # events generated by this component.
        if isinstance(method, basestring):
            if self._listenerList is None:
                self._listenerList = set()
            self._listenerList.add( ListenerMethod(eventType, obj, method) )
        else:
            if self._listenerList is None:
                self._listenerList = set()
            self._listenerList.add( ListenerMethod(eventType, obj, method) )


    def removeListener(self, eventType, target, method=None):
        # Removes the event listener methods matching the given given paramaters.
        if method is None:
            if self._listenerList is not None:
                for lm in self._listenerList:
                    if lm.matches(eventType, target):
                        self._listenerList.remove(lm)
                        return
        else:
            if isinstance(method, basestring):
                methods = target.__class__.getMethods()  ## FIXME: getMethods
                method = None
                for i in range(len(methods)):
                    if methods[i].getName() == method:
                        method = methods[i]

                if method is None:
                    raise ValueError()

                # Remove the listeners
                if self._listenerList is not None:
                    for lm in self._listenerList:
                        if lm.matches(eventType, target, method):
                            self._listenerList.remove(lm)
                            return
            else:
                if self._listenerList is not None:
                    for lm in self._listenerList:
                        if lm.matches(eventType, target, method):
                            self._listenerList.remove(lm)
                            return


    def removeAllListeners(self):
        """Removes all listeners from event router."""
        self._listenerList = None


    def fireEvent(self, event):
        """Sends an event to all registered listeners. The listeners will decide if
        the activation method should be called or not.

        @param event
                   the Event to be sent to all listeners.
        """
        # It is not necessary to send any events if there are no listeners
        if self._listenerList is not None:
            # Make a copy of the listener list to allow listeners to be added
            # inside listener methods. Fixes #3605.

            # Send the event to all listeners. The listeners themselves
            # will filter out unwanted events.
            listeners = list(self._listenerList)
            for listener in listeners:
                listener.receiveEvent(event)


    def hasListeners(self, eventType):
        """Checks if the given Event type is listened by a listener registered to
        this router.

        @param eventType
                   the event type to be checked
        @return true if a listener is registered for the given event type
        """
        if self._listenerList is not None:
            for lm in self._listenerList:
                if lm.isType(eventType):
                    return True
        return False


    def getListeners(self, eventType):
        """Returns all listeners that match or extend the given event type.

        @param eventType
                   The type of event to return listeners for.
        @return A collection with all registered listeners. Empty if no listeners
                are found.
        """
        listeners = list()
        if self._listenerList is not None:
            for lm in self._listenerList:
                if lm.isOrExtendsType(eventType):
                    listeners.append(lm.getTarget())
        return listeners
