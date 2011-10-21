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

from warnings import warn

from muntjac.ui.abstract_component import AbstractComponent

from muntjac.ui.component import \
    IComponent, IFocusable, Event as ComponentEvent

from muntjac.terminal.stream_variable import \
    IStreamingProgressEvent, IStreamVariable, IStreamingEvent

from muntjac.terminal.gwt.server.exceptions import \
    NoInputStreamException, NoOutputStreamException


class IStartedListener(object):
    """Receives the events when the upload starts.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 5.0
    """

    def uploadStarted(self, event):
        """Upload has started.

        @param event
                   the Upload started event.
        """
        raise NotImplementedError


class IFinishedListener(object):
    """Receives the events when the uploads are ready.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def uploadFinished(self, event):
        """Upload has finished.

        @param event
                   the Upload finished event.
        """
        raise NotImplementedError


class IFailedListener(object):
    """Receives events when the uploads are finished, but unsuccessful.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def uploadFailed(self, event):
        """Upload has finished unsuccessfully.

        @param event
                   the Upload failed event.
        """
        raise NotImplementedError


class ISucceededListener(object):
    """Receives events when the uploads are successfully finished.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def uploadSucceeded(self, event):
        """Upload successfull..

        @param event
                   the Upload successfull event.
        """
        raise NotImplementedError


class IProgressListener(object):
    """IProgressListener receives events to track progress of upload."""

    def updateProgress(self, readBytes, contentLength):
        """Updates progress to listener

        @param readBytes
                   bytes transferred
        @param contentLength
                   total size of file currently being uploaded, -1 if unknown
        """
        raise NotImplementedError


_UPLOAD_FINISHED_METHOD = getattr(IFinishedListener, 'uploadFinished')
_UPLOAD_FAILED_METHOD = getattr(IFailedListener, 'uploadFailed')
_UPLOAD_STARTED_METHOD = getattr(IStartedListener, 'uploadStarted')
_UPLOAD_SUCCEEDED_METHOD = getattr(ISucceededListener, 'uploadSucceeded')


class Upload(AbstractComponent, IFocusable): #IComponent,
    """IComponent for uploading files from client to server.

    The visible component consists of a file name input box and a browse
    button and an upload submit button to start uploading.

    The Upload component needs a java.io.OutputStream to write the uploaded
    data. You need to implement the Upload.IReceiver interface and return the
    output stream in the receiveUpload() method.

    You can get an event regarding starting (StartedEvent), progress
    (ProgressEvent), and finishing (FinishedEvent) of upload by implementing
    IStartedListener, IProgressListener, and IFinishedListener, respectively.
    The IFinishedListener is called for both failed and succeeded uploads. If
    you wish to separate between these two cases, you can use
    ISucceededListener (SucceededEvenet) and IFailedListener (FailedEvent).

    The upload component does not itself show upload progress, but you can use
    the ProgressIndicator for providing progress feedback by implementing
    IProgressListener and updating the indicator in updateProgress().

    Setting upload component immediate initiates the upload as soon as a file
    is selected, instead of the common pattern of file selection field and
    upload button.

    Note! Because of browser dependent implementations of <input type="file">
    element, setting size for Upload component is not supported. For some
    browsers setting size may work to some extend.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    #CLIENT_WIDGET = ClientWidget(VUpload, LoadStyle.LAZY)

    def __init__(self, caption=None, uploadReceiver=None):
        """Creates a new instance of Upload.

        The receiver must be set before performing an upload.
        """
        super(Upload, self).__init__()

        # Should the field be focused on next repaint?
        self._focus = False

        # The tab order number of this field.
        self._tabIndex = 0

        # The output of the upload is redirected to this receiver.
        self._receiver = None

        self._isUploading = None

        self._contentLength = -1

        self._totalBytes = None

        self._buttonCaption = 'Upload'

        # ProgressListeners to which information about progress
        # is sent during upload
        self._progressListeners = None

        self._interrupted = False

        self._notStarted = None

        self._nextid = None

        # Flag to indicate that submitting file has been requested.
        self._forceSubmit = None

        if caption:
            self.setCaption(caption)

        if uploadReceiver is not None:
            self._receiver = uploadReceiver

        self._streamVariable = None


    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed.

        @see AbstractComponent.changeVariables()
        """
        if 'pollForStart' in variables:
            idd = variables.get('pollForStart')
            if not self._isUploading and idd == self._nextid:
                self._notStarted = True
                self.requestRepaint()
            else:
                pass


    def paintContent(self, target):
        """Paints the content of this component.

        @param target
                   Target to paint the content on.
        @throws PaintException
                    if the paint operation failed.
        """
        if self._notStarted:
            target.addAttribute('notStarted', True)
            self._notStarted = False
            return

        if self._forceSubmit:
            target.addAttribute('forceSubmit', True)
            self._forceSubmit = True
            return

        # The field should be focused
        if self._focus:
            target.addAttribute('focus', True)

        # The tab ordering number
        if self._tabIndex >= 0:
            target.addAttribute('tabindex', self._tabIndex)

        target.addAttribute('state', self._isUploading)

        if self._buttonCaption is not None:
            target.addAttribute('buttoncaption', self._buttonCaption)

        target.addAttribute('nextid', self._nextid)

        # Post file to this strean variable
        target.addVariable(self, 'action', self.getStreamVariable())


    def addListener(self, listener, iface):
        """Adds an event listener.

        @param listener
                   the Listener to be added.
        """
        if iface == IFailedListener:
            self.registerListener(FailedEvent,
                    listener, _UPLOAD_FAILED_METHOD)

        elif iface == IFinishedListener:
            self.registerListener(FinishedEvent,
                    listener, _UPLOAD_FINISHED_METHOD)

        elif iface == IProgressListener:
            if self._progressListeners is None:
                self._progressListeners = set()
            self._progressListeners.add(listener)

        elif isinstance(listener, IStartedListener):
            self.registerListener(StartedEvent,
                    listener, _UPLOAD_STARTED_METHOD)

        elif iface == ISucceededListener:
            self.registerListener(SucceededEvent,
                    listener, _UPLOAD_SUCCEEDED_METHOD)

        else:
            super(Upload, self).addListener(listener, iface)


    def addFailedListener(self, listener):
        self.addListener(listener, IFailedListener)


    def addFinishedListener(self, listener):
        self.addListener(listener, IFinishedListener)


    def addProgressListener(self, listener):
        self.addListener(listener, IProgressListener)


    def addStartedListener(self, listener):
        self.addListener(listener, IStartedListener)


    def addSucceededListener(self, listener):
        self.addListener(listener, ISucceededListener)


    def removeListener(self, listener, iface):
        """Removes an event listener.

        @param listener
                   the Listener to be removed.
        """
        if iface == IFailedListener:
            self.withdrawListener(FailedEvent,
                    listener, _UPLOAD_FAILED_METHOD)

        elif iface == IFinishedListener:
            self.withdrawListener(FinishedEvent,
                    listener, _UPLOAD_FINISHED_METHOD)

        elif iface == IProgressListener:
            if self._progressListeners is not None:
                self._progressListeners.remove(listener)

        elif iface == IStartedListener:
            self.withdrawListener(StartedEvent,
                    listener, _UPLOAD_STARTED_METHOD)

        elif iface == ISucceededListener:
            self.withdrawListener(SucceededEvent,
                    listener, _UPLOAD_SUCCEEDED_METHOD)

        else:
            super(Upload, self).removeListener(listener, iface)


    def removeFailedListener(self, listener):
        self.removeListener(listener, IFailedListener)


    def removeFinishedListener(self, listener):
        self.removeListener(listener, IFinishedListener)


    def removeProgressListener(self, listener):
        self.removeListener(listener, IProgressListener)


    def removeStartedListener(self, listener):
        self.removeListener(listener, IStartedListener)


    def removeSucceededListener(self, listener):
        self.removeListener(listener, ISucceededListener)


    def fireStarted(self, filename, MIMEType):
        """Emit upload received event.

        @param filename
        @param MIMEType
        @param length
        """
        evt = StartedEvent(self, filename, MIMEType, self._contentLength)
        self.fireEvent(evt)


    def fireUploadInterrupted(self, filename, MIMEType, length, e=None):
        """Emits the upload failed event.

        @param filename
        @param MIMEType
        @param length
        """
        if e is None:
            evt = FailedEvent(self, filename, MIMEType, length)
        else:
            evt = FailedEvent(self, filename, MIMEType, length, e)

        self.fireEvent(evt)


    def fireNoInputStream(self, filename, MIMEType, length):
        evt = NoInputStreamEvent(self, filename, MIMEType, length)
        self.fireEvent(evt)


    def fireNoOutputStream(self, filename, MIMEType, length):
        evt = NoOutputStreamEvent(self, filename, MIMEType, length)
        self.fireEvent(evt)


    def fireUploadSuccess(self, filename, MIMEType, length):
        """Emits the upload success event.

        @param filename
        @param MIMEType
        @param length
        """
        evt = SucceededEvent(self, filename, MIMEType, length)
        self.fireEvent(evt)


    def fireUpdateProgress(self, totalBytes, contentLength):
        """Emits the progress event.

        @param totalBytes
                   bytes received so far
        @param contentLength
                   actual size of the file being uploaded, if known
        """
        # this is implemented differently than other listeners to
        # maintain backwards compatibility
        if self._progressListeners is not None:
            for l in self._progressListeners:
                l.updateProgress(totalBytes, contentLength)


    def getReceiver(self):
        """Returns the current receiver.

        @return the IStreamVariable.
        """
        return self._receiver


    def setReceiver(self, receiver):
        """Sets the receiver.

        @param receiver
                   the receiver to set.
        """
        self._receiver = receiver


    def focus(self):
        """{@inheritDoc}"""
        super(Upload, self).focus()


    def getTabIndex(self):
        """Gets the Tabulator index of this IFocusable component.

        @see com.vaadin.ui.IComponent.IFocusable#getTabIndex()
        """
        return self._tabIndex


    def setTabIndex(self, tabIndex):
        """Sets the Tabulator index of this IFocusable component.

        @see com.vaadin.ui.IComponent.IFocusable#setTabIndex(int)
        """
        self._tabIndex = tabIndex


    def startUpload(self):
        """Go into upload state. This is to prevent double uploading on same
        component.

        Warning: this is an internal method used by the framework and should
        not be used by user of the Upload component. Using it results in the
        Upload component going in wrong state and not working. It is currently
        public because it is used by another class.
        """
        if self._isUploading:
            raise ValueError, 'uploading already started'

        self._isUploading = True
        self._nextid += 1


    def interruptUpload(self):
        """Interrupts the upload currently being received. The interruption
        will be done by the receiving tread so this method will return
        immediately and the actual interrupt will happen a bit later.
        """
        if self._isUploading:
            self._interrupted = True


    def endUpload(self):
        """Go into state where new uploading can begin.

        Warning: this is an internal method used by the framework and should
        not be used by user of the Upload component.
        """
        self._isUploading = False
        self._contentLength = -1
        self._interrupted = False
        self.requestRepaint()


    def isUploading(self):
        return self._isUploading


    def getBytesRead(self):
        """Gets read bytes of the file currently being uploaded.

        @return bytes
        """
        return self._totalBytes


    def getUploadSize(self):
        """Returns size of file currently being uploaded. Value sane only
        during upload.

        @return size in bytes
        """
        return self._contentLength


    def setProgressListener(self, progressListener):
        """This method is deprecated, use addListener(IProgressListener)
        instead.

        @deprecated Use addListener(IProgressListener) instead.
        @param progressListener
        """
        warn('use addListener() instead', DeprecationWarning)

        self.addListener(progressListener, IProgressListener)


    def getProgressListener(self):
        """This method is deprecated.

        @deprecated Replaced with addListener/removeListener
        @return listener
        """
        warn('replaced with addListener/removeListener', DeprecationWarning)

        if (self._progressListeners is None
                or len(self._progressListeners) == 0):
            return None
        else:
            return self._progressListeners.next()


    def getButtonCaption(self):
        """@return String to be rendered into button that fires uploading"""
        return self._buttonCaption


    def setButtonCaption(self, buttonCaption):
        """In addition to the actual file chooser, upload components have
        button that starts actual upload progress. This method is used to set
        text in that button.

        In case the button text is set to null, the button is hidden. In this
        case developer must explicitly initiate the upload process with
        {@link #submitUpload()}.

        In case the Upload is used in immediate mode using
        {@link #setImmediate(boolean)}, the file choose (html input with type
        "file") is hidden and only the button with this text is shown.

        <strong>Note</strong> the string given is set as is to the button.
        HTML formatting is not stripped. Be sure to properly validate your
        value according to your needs.

        @param buttonCaption
                   text for upload components button.
        """
        self._buttonCaption = buttonCaption
        self.requestRepaint()


    def submitUpload(self):
        """Forces the upload the send selected file to the server.

        In case developer wants to use this feature, he/she will most probably
        want to hide the uploads internal submit button by setting its caption
        to null with {@link #setButtonCaption(String)} method.

        Note, that the upload runs asynchronous. Developer should use normal
        upload listeners to trac the process of upload. If the field is empty
        uploaded the file name will be empty string and file length 0 in the
        upload finished event.

        Also note, that the developer should not remove or modify the upload
        in the same user transaction where the upload submit is requested. The
        upload may safely be hidden or removed once the upload started event
        is fired.
        """
        self.requestRepaint()
        self._forceSubmit = True


    def requestRepaint(self):
        self._forceSubmit = False
        super(Upload, self).requestRepaint()


    def getStreamVariable(self):
        # Handle to terminal via Upload monitors and controls the upload
        # during it is being streamed.
        if self._streamVariable is None:

            class InnerStreamVariable(IStreamVariable):

                def __init__(self, upload):
                    self._upload = upload
                    self._lastStartedEvent = None


                def listenProgress(self):
                    return (self._upload.progressListeners is not None
                            and len(self._upload.progressListeners) > 0)


                def onProgress(self, event):
                    self._upload.fireUpdateProgress(event.getBytesReceived(),
                            event.getContentLength())


                def isInterrupted(self):
                    return self._upload.interrupted


                def getOutputStream(self):
                    receiveUpload = self._upload.receiver.receiveUpload(
                            self._lastStartedEvent.getFileName(),
                            self._lastStartedEvent.getMimeType())
                    self._lastStartedEvent = None
                    return receiveUpload


                def streamingStarted(self, event):
                    self.startUpload()
                    self._upload.contentLength = event.getContentLength()
                    self._upload.fireStarted(event.getFileName(),
                            event.getMimeType())
                    self._lastStartedEvent = event


                def streamingFinished(self, event):
                    self._upload.fireUploadSuccess(event.getFileName(),
                            event.getMimeType(), event.getContentLength())
                    self._upload.endUpload()
                    self._upload.requestRepaint()


                def streamingFailed(self, event):
                    exception = event.getException()
                    if isinstance(exception, NoInputStreamException):
                        self._upload.fireNoInputStream(event.getFileName(),
                                event.getMimeType(), 0)

                    elif isinstance(exception, NoOutputStreamException):
                        self._upload.fireNoOutputStream(event.getFileName(),
                                event.getMimeType(), 0)
                    else:
                        self._upload.fireUploadInterrupted(event.getFileName(),
                                event.getMimeType(), 0, exception)

                    self._upload.endUpload()

            self._streamVariable = InnerStreamVariable(self)

        return self._streamVariable


    def getListeners(self, eventType):
        if issubclass(eventType, IStreamingEvent):
            if self._progressListeners is None:
                return list()
            else:
                return list(self._progressListeners)

        return super(Upload, self).getListeners(eventType)


class IReceiver(object):
    """Interface that must be implemented by the upload receivers to provide
    the Upload component an output stream to write the uploaded data.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def receiveUpload(self, filename, mimeType):
        """Invoked when a new upload arrives.

        @param filename
                   the desired filename of the upload, usually as specified
                   by the client.
        @param mimeType
                   the MIME type of the uploaded file.
        @return Stream to which the uploaded file should be written.
        """
        raise NotImplementedError


class FinishedEvent(ComponentEvent):
    """Upload.FinishedEvent is sent when the upload receives a file,
    regardless of whether the reception was successful or failed. If
    you wish to distinguish between the two cases, use either SucceededEvent
    or FailedEvent, which are both subclasses of the FinishedEvent.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, filename, MIMEType, length):
        """@param source
                   the source of the file.
        @param filename
                   the received file name.
        @param MIMEType
                   the MIME type of the received file.
        @param length
                   the length of the received file.
        """
        super(FinishedEvent, self).__init__(source)

        # MIME type of the received file.
        self._type = MIMEType

        # Received file name.
        self._filename = filename

        # Length of the received file.
        self._length = length


    def getUpload(self):
        """Uploads where the event occurred.

        @return the Source of the event.
        """
        return self.getSource()


    def getFilename(self):
        """Gets the file name.

        @return the filename.
        """
        return self._filename


    def getMIMEType(self):
        """Gets the MIME Type of the file.

        @return the MIME type.
        """
        return self._type


    def getLength(self):
        """Gets the length of the file.

        @return the length.
        """
        return self._length


class FailedEvent(FinishedEvent):
    """Upload.FailedEvent event is sent when the upload is received,
    but the reception is interrupted for some reason.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, filename, MIMEType, length, reason=None):
        """@param source
        @param filename
        @param MIMEType
        @param length
        @param exception
        """
        super(FailedEvent, self).__init__(source, filename, MIMEType, length)

        self._reason = reason


    def getReason(self):
        """Gets the exception that caused the failure.

        @return the exception that caused the failure, null if n/a
        """
        return self._reason


class NoOutputStreamEvent(FailedEvent):
    """FailedEvent that indicates that an output stream could not be obtained.
    """

    def __init__(self, source, filename, MIMEType, length):
        """@param source
        @param filename
        @param MIMEType
        @param length
        """
        super(NoOutputStreamEvent, self).__init__(source, filename, MIMEType, length)


class NoInputStreamEvent(FailedEvent):
    """FailedEvent that indicates that an input stream could not be obtained.
    """

    def __init__(self, source, filename, MIMEType, length):
        """@param source
        @param filename
        @param MIMEType
        @param length
        """
        super(NoInputStreamEvent, self).__init__(source, filename, MIMEType, length)


class SucceededEvent(FinishedEvent):
    """Upload.SucceededEvent event is sent when the upload is received
    successfully.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 3.0
    """

    def __init__(self, source, filename, MIMEType, length):
        """@param source
        @param filename
        @param MIMEType
        @param length
        """
        super(SucceededEvent, self).__init__(source, filename, MIMEType, length)


class StartedEvent(ComponentEvent):
    """Upload.StartedEvent event is sent when the upload is started to
    received.

    @author IT Mill Ltd.
    @author Richard Lincoln
    @version @VERSION@
    @since 5.0
    """

    def __init__(self, source, filename, MIMEType, contentLength):
        """@param source
        @param filename
        @param MIMEType
        @param length
        """
        super(StartedEvent, self).__init__(source)

        self._filename = filename

        self._type = MIMEType

        # Length of the received file.
        self._length = contentLength


    def getUpload(self):
        """Uploads where the event occurred.

        @return the Source of the event.
        """
        return self.getSource()


    def getFilename(self):
        """Gets the file name.

        @return the filename.
        """
        return self._filename


    def getMIMEType(self):
        """Gets the MIME Type of the file.

        @return the MIME type.
        """
        return self._type


    def getContentLength(self):
        """@return the length of the file that is being uploaded"""
        return self._length
