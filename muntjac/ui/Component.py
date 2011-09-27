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

from muntjac.terminal.VariableOwner import VariableOwner
from muntjac.terminal.Sizeable import Sizeable
from muntjac.terminal.Paintable import Paintable
from muntjac.util.event import EventObject, EventListener


class Component(Paintable, VariableOwner, Sizeable):
    """{@code Component} is the top-level interface that is and must be implemented
    by all Vaadin components. {@code Component} is paired with
    {@link AbstractComponent}, which provides a default implementation for all
    the methods defined in this interface.

    <p>
    Components are laid out in the user interface hierarchically. The layout is
    managed by layout components, or more generally by components that implement
    the {@link ComponentContainer} interface. Such a container is the
    <i>parent</i> of the contained components.
    </p>

    <p>
    The {@link #getParent()} method allows retrieving the parent component of a
    component. While there is a {@link #setParent(Component) setParent()}, you
    rarely need it as you normally add components with the
    {@link ComponentContainer#addComponent(Component) addComponent()} method of
    the layout or other {@code ComponentContainer}, which automatically sets the
    parent.
    </p>

    <p>
    A component becomes <i>attached</i> to an application (and the
    {@link #attach()} is called) when it or one of its parents is attached to the
    main window of the application through its containment hierarchy.
    </p>

    @author IT Mill Ltd.
    @version
    @VERSION@
    @since 3.0
    """

    def getStyleName(self):
        """Gets all user-defined CSS style names of a component. If the component
        has multiple style names defined, the return string is a space-separated
        list of style names. Built-in style names defined in Vaadin or GWT are
        not returned.

        <p>
        The style names are returned only in the basic form in which they were
        added; each user-defined style name shows as two CSS style class names in
        the rendered HTML: one as it was given and one prefixed with the
        component-specific style name. Only the former is returned.
        </p>

        @return the style name or a space-separated list of user-defined style
                names of the component
        @see #setStyleName(String)
        @see #addStyleName(String)
        @see #removeStyleName(String)
        """
        pass


    def setStyleName(self, style):
        """Sets one or more user-defined style names of the component, replacing any
        previous user-defined styles. Multiple styles can be specified as a
        space-separated list of style names. The style names must be valid CSS
        class names and should not conflict with any built-in style names in
        Vaadin or GWT.

        <pre>
        Label label = new Label(&quot;This text has a lot of style&quot;);
        label.setStyleName(&quot;myonestyle myotherstyle&quot;);
        </pre>

        <p>
        Each style name will occur in two versions: one as specified and one that
        is prefixed with the style name of the component. For example, if you
        have a {@code Button} component and give it "{@code mystyle}" style, the
        component will have both "{@code mystyle}" and "{@code v-button-mystyle}"
        styles. You could then style the component either with:
        </p>

        <pre>
        .myonestyle {background: blue;}
        </pre>

        <p>
        or
        </p>

        <pre>
        .v-button-myonestyle {background: blue;}
        </pre>

        <p>
        It is normally a good practice to use {@link #addStyleName(String)
        addStyleName()} rather than this setter, as different software
        abstraction layers can then add their own styles without accidentally
        removing those defined in other layers.
        </p>

        <p>
        This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.
        </p>

        @param style
                   the new style or styles of the component as a space-separated
                   list
        @see #getStyleName()
        @see #addStyleName(String)
        @see #removeStyleName(String)
        """
        pass


    def addStyleName(self, style):
        """Adds a style name to component. The style name will be rendered as a HTML
        class name, which can be used in a CSS definition.

        <pre>
        Label label = new Label(&quot;This text has style&quot;);
        label.addStyleName(&quot;mystyle&quot;);
        </pre>

        <p>
        Each style name will occur in two versions: one as specified and one that
        is prefixed wil the style name of the component. For example, if you have
        a {@code Button} component and give it "{@code mystyle}" style, the
        component will have both "{@code mystyle}" and "{@code v-button-mystyle}"
        styles. You could then style the component either with:
        </p>

        <pre>
        .mystyle {font-style: italic;}
        </pre>

        <p>
        or
        </p>

        <pre>
        .v-button-mystyle {font-style: italic;}
        </pre>

        <p>
        This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.
        </p>

        @param style
                   the new style to be added to the component
        @see #getStyleName()
        @see #setStyleName(String)
        @see #removeStyleName(String)
        """
        pass


    def removeStyleName(self, style):
        """Removes the given style name from component.

        <p>
        The parameter must be a valid CSS style name. Only user-defined style
        names added with {@link #addStyleName(String) addStyleName()} or
        {@link #setStyleName(String) setStyleName()} can be removed; built-in
        style names defined in Vaadin or GWT can not be removed.
        </p>

        @param style
                   the style name to be removed
        @see #getStyleName()
        @see #setStyleName(String)
        @see #addStyleName(String)
        """
        pass


    def isEnabled(self):
        """Tests whether the component is enabled or not. A user can not interact
        with disabled components. Disabled components are rendered in a style
        that indicates the status, usually in gray color. Children of a disabled
        component are also disabled. Components are enabled by default.

        <p>
        As a security feature, all variable change events for disabled components
        are blocked on the server-side.
        </p>

        @return <code>true</code> if the component and its parent are enabled,
                <code>false</code> otherwise.
        @see VariableOwner#isEnabled()
        """
        pass


    def setEnabled(self, enabled):
        """Enables or disables the component. The user can not interact disabled
        components, which are shown with a style that indicates the status,
        usually shaded in light gray color. Components are enabled by default.
        Children of a disabled component are automatically disabled; if a child
        component is explicitly set as disabled, changes in the disabled status
        of its parents do not change its status.

        <pre>
        Button enabled = new Button(&quot;Enabled&quot;);
        enabled.setEnabled(true); // The default
        layout.addComponent(enabled);

        Button disabled = new Button(&quot;Disabled&quot;);
        disabled.setEnabled(false);
        layout.addComponent(disabled);
        </pre>

        <p>
        This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent} for the component and, if it is a
        {@link ComponentContainer}, for all its children recursively.
        </p>

        @param enabled
                   a boolean value specifying if the component should be enabled
                   or not
        """
        pass


    def isVisible(self):
        """Tests the <i>visibility</i> property of the component.

        <p>
        Visible components are drawn in the user interface, while invisible ones
        are not. The effect is not merely a cosmetic CSS change, but the entire
        HTML element will be empty. Making a component invisible through this
        property can alter the positioning of other components.
        </p>

        <p>
        A component is visible only if all its parents are also visible. Notice
        that if a child component is explicitly set as invisible, changes in the
        visibility status of its parents do not change its status.
        </p>

        <p>
        This method does not check whether the component is attached (see
        {@link #attach()}). The component and all its parents may be considered
        "visible", but not necessarily attached to application. To test if
        component will actually be drawn, check both its visibility and that
        {@link #getApplication()} does not return {@code null}.
        </p>

        @return <code>true</code> if the component is visible in the user
                interface, <code>false</code> if not
        @see #setVisible(boolean)
        @see #attach()
        """
        pass


    def setVisible(self, visible):
        """Sets the visibility of the component.

        <p>
        Visible components are drawn in the user interface, while invisible ones
        are not. The effect is not merely a cosmetic CSS change, but the entire
        HTML element will be empty.
        </p>

        <pre>
        TextField readonly = new TextField(&quot;Read-Only&quot;);
        readonly.setValue(&quot;You can't see this!&quot;);
        readonly.setVisible(false);
        layout.addComponent(readonly);
        </pre>

        <p>
        A component is visible only if all of its parents are also visible. If a
        component is explicitly set to be invisible, changes in the visibility of
        its parents will not change the visibility of the component.
        </p>

        @param visible
                   the boolean value specifying if the component should be
                   visible after the call or not.
        @see #isVisible()
        """
        pass


    def getParent(self):
        """Gets the parent component of the component.

        <p>
        Components can be nested but a component can have only one parent. A
        component that contains other components, that is, can be a parent,
        should usually inherit the {@link ComponentContainer} interface.
        </p>

        @return the parent component
        @see #setParent(Component)
        """
        pass


    def setParent(self, parent):
        """Sets the parent component of the component.

        <p>
        This method automatically calls {@link #attach()} if the parent becomes
        attached to the application, regardless of whether it was attached
        previously. Conversely, if the parent is {@code null} and the component
        is attached to the application, {@link #detach()} is called for the
        component.
        </p>

        <p>
        This method is rarely called directly. The
        {@link ComponentContainer#addComponent(Component)} method is normally
        used for adding components to a container and it will call this method
        implicitly.
        </p>

        <p>
        It is not possible to change the parent without first setting the parent
        to {@code null}.
        </p>

        @param parent
                   the parent component
        @throws IllegalStateException
                    if a parent is given even though the component already has a
                    parent
        """
        pass


    def isReadOnly(self):
        """Tests whether the component is in the read-only mode. The user can not
        change the value of a read-only component. As only {@link Field}
        components normally have a value that can be input or changed by the
        user, this is mostly relevant only to field components, though not
        restricted to them.

        <p>
        Notice that the read-only mode only affects whether the user can change
        the <i>value</i> of the component; it is possible to, for example, scroll
        a read-only table.
        </p>

        <p>
        The read-only status affects only the user; the value can still be
        changed programmatically, for example, with
        {@link Property#setValue(Object)}.
        </p>

        <p>
        The method will return {@code true} if the component or any of its
        parents is in the read-only mode.
        </p>

        @return <code>true</code> if the component or any of its parents is in
                read-only mode, <code>false</code> if not.
        @see #setReadOnly(boolean)
        """
        pass


    def setReadOnly(self, readOnly):
        """Sets the read-only mode of the component to the specified mode. The user
        can not change the value of a read-only component.

        <p>
        As only {@link Field} components normally have a value that can be input
        or changed by the user, this is mostly relevant only to field components,
        though not restricted to them.
        </p>

        <p>
        Notice that the read-only mode only affects whether the user can change
        the <i>value</i> of the component; it is possible to, for example, scroll
        a read-only table.
        </p>

        <p>
        The read-only status affects only the user; the value can still be
        changed programmatically, for example, with
        {@link Property#setValue(Object)}.
        </p>

        <p>
        This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.
        </p>

        @param readOnly
                   a boolean value specifying whether the component is put
                   read-only mode or not
        """
        pass


    def getCaption(self):
        """Gets the caption of the component.

        <p>
        See {@link #setCaption(String)} for a detailed description of the
        caption.
        </p>

        @return the caption of the component or {@code null} if the caption is
                not set.
        @see #setCaption(String)
        """
        pass


    def setCaption(self, caption):
        """Sets the caption of the component.

        <p>
        A <i>caption</i> is an explanatory textual label accompanying a user
        interface component, usually shown above, left of, or inside the
        component. <i>Icon</i> (see {@link #setIcon(Resource) setIcon()} is
        closely related to caption and is usually displayed horizontally before
        or after it, depending on the component and the containing layout.
        </p>

        <p>
        The caption can usually also be given as the first parameter to a
        constructor, though some components do not support it.
        </p>

        <pre>
        RichTextArea area = new RichTextArea();
        area.setCaption(&quot;You can edit stuff here&quot;);
        area.setValue(&quot;&lt;h1&gt;Helpful Heading&lt;/h1&gt;&quot;
                + &quot;&lt;p&gt;All this is for you to edit.&lt;/p&gt;&quot;);
        </pre>

        <p>
        The contents of a caption are automatically quoted, so no raw XHTML can
        be rendered in a caption. The validity of the used character encoding,
        usually UTF-8, is not checked.
        </p>

        <p>
        The caption of a component is, by default, managed and displayed by the
        layout component or component container in which the component is placed.
        For example, the {@link VerticalLayout} component shows the captions
        left-aligned above the contained components, while the {@link FormLayout}
        component shows the captions on the left side of the vertically laid
        components, with the captions and their associated components
        left-aligned in their own columns. The {@link CustomComponent} does not
        manage the caption of its composition root, so if the root component has
        a caption, it will not be rendered. Some components, such as
        {@link Button} and {@link Panel}, manage the caption themselves and
        display it inside the component.
        </p>

        <p>
        This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}. A reimplementation should call the superclass
        implementation.
        </p>

        @param caption
                   the new caption for the component. If the caption is
                   {@code null}, no caption is shown and it does not normally
                   take any space
        """
        pass


    def getIcon(self):
        """Gets the icon resource of the component.

        <p>
        See {@link #setIcon(Resource)} for a detailed description of the icon.
        </p>

        @return the icon resource of the component or {@code null} if the
                component has no icon
        @see #setIcon(Resource)
        """
        pass


    def setIcon(self, icon):
        """Sets the icon of the component.

        <p>
        An icon is an explanatory graphical label accompanying a user interface
        component, usually shown above, left of, or inside the component. Icon is
        closely related to caption (see {@link #setCaption(String) setCaption()})
        and is usually displayed horizontally before or after it, depending on
        the component and the containing layout.
        </p>

        <p>
        The image is loaded by the browser from a resource, typically a
        {@link com.vaadin.terminal.ThemeResource}.
        </p>

        <pre>
        // Component with an icon from a custom theme
        TextField name = new TextField(&quot;Name&quot;);
        name.setIcon(new ThemeResource(&quot;icons/user.png&quot;));
        layout.addComponent(name);

        // Component with an icon from another theme ('runo')
        Button ok = new Button(&quot;OK&quot;);
        ok.setIcon(new ThemeResource(&quot;../runo/icons/16/ok.png&quot;));
        layout.addComponent(ok);
        </pre>

        <p>
        The icon of a component is, by default, managed and displayed by the
        layout component or component container in which the component is placed.
        For example, the {@link VerticalLayout} component shows the icons
        left-aligned above the contained components, while the {@link FormLayout}
        component shows the icons on the left side of the vertically laid
        components, with the icons and their associated components left-aligned
        in their own columns. The {@link CustomComponent} does not manage the
        icon of its composition root, so if the root component has an icon, it
        will not be rendered.
        </p>

        <p>
        An icon will be rendered inside an HTML element that has the
        {@code v-icon} CSS style class. The containing layout may enclose an icon
        and a caption inside elements related to the caption, such as
        {@code v-caption} .
        </p>

        This method will trigger a
        {@link com.vaadin.terminal.Paintable.RepaintRequestEvent
        RepaintRequestEvent}.

        @param icon
                   the icon of the component. If null, no icon is shown and it
                   does not normally take any space.
        @see #getIcon()
        @see #setCaption(String)
        """
        pass


    def getWindow(self):
        """Gets the parent window of the component.

        <p>
        If the component is not attached to a window through a component
        containment hierarchy, <code>null</code> is returned.
        </p>

        <p>
        The window can be either an application-level window or a sub-window. If
        the component is itself a window, it returns a reference to itself, not
        to its containing window (of a sub-window).
        </p>

        @return the parent window of the component or <code>null</code> if it is
                not attached to a window or is itself a window
        """
        pass


    def getApplication(self):
        """Gets the application object to which the component is attached.

        <p>
        The method will return {@code null} if the component is not currently
        attached to an application. This is often a problem in constructors of
        regular components and in the initializers of custom composite
        components. A standard workaround is to move the problematic
        initialization to {@link #attach()}, as described in the documentation of
        the method.
        </p>

        @return the parent application of the component or <code>null</code>.
        @see #attach()
        """
        pass


    def attach(self):
        """Notifies the component that it is connected to an application.

        <p>
        The caller of this method is {@link #setParent(Component)} if the parent
        is itself already attached to the application. If not, the parent will
        call the {@link #attach()} for all its children when it is attached to
        the application. This method is always called before the component is
        painted for the first time.
        </p>

        <p>
        Reimplementing the {@code attach()} method is useful for tasks that need
        to get a reference to the parent, window, or application object with the
        {@link #getParent()}, {@link #getWindow()}, and {@link #getApplication()}
        methods. A component does not yet know these objects in the constructor,
        so in such case, the methods will return {@code null}. For example, the
        following is invalid:
        </p>

        <pre>
        public class AttachExample extends CustomComponent {
            public AttachExample() {
                // ERROR: We can't access the application object yet.
                ClassResource r = new ClassResource(&quot;smiley.jpg&quot;, getApplication());
                Embedded image = new Embedded(&quot;Image:&quot;, r);
                setCompositionRoot(image);
            }
        }
        </pre>

        <p>
        Adding a component to an application triggers calling the
        {@link #attach()} method for the component. Correspondingly, removing a
        component from a container triggers calling the {@link #detach()} method.
        If the parent of an added component is already connected to the
        application, the {@code attach()} is called immediately from
        {@link #setParent(Component)}.
        </p>

        <pre>
        public class AttachExample extends CustomComponent {
            public AttachExample() {
            }

            &#064;Override
            public void attach() {
                super.attach(); // Must call.

                // Now we know who ultimately owns us.
                ClassResource r = new ClassResource(&quot;smiley.jpg&quot;, getApplication());
                Embedded image = new Embedded(&quot;Image:&quot;, r);
                setCompositionRoot(image);
            }
        }
        </pre>

        <p>
        The attachment logic is implemented in {@link AbstractComponent}.
        </p>

        @see #getApplication()
        """
        pass


    def detach(self):
        """Notifies the component that it is detached from the application.

        <p>
        The {@link #getApplication()} and {@link #getWindow()} methods might
        return <code>null</code> after this method is called.
        </p>

        <p>
        The caller of this method is {@link #setParent(Component)} if the parent
        is in the application. When the parent is detached from the application
        it is its response to call {@link #detach()} for all the children and to
        detach itself from the terminal.
        </p>
        """
        pass


    def getLocale(self):
        """Gets the locale of the component.

        <p>
        If a component does not have a locale set, the locale of its parent is
        returned, and so on. Eventually, if no parent has locale set, the locale
        of the application is returned. If the application does not have a locale
        set, it is determined by <code>Locale.getDefault()</code>.
        </p>

        <p>
        As the component must be attached before its locale can be acquired,
        using this method in the internationalization of component captions, etc.
        is generally not feasible. For such use case, we recommend using an
        otherwise acquired reference to the application locale.
        </p>

        @return Locale of this component or {@code null} if the component and
                none of its parents has a locale set and the component is not yet
                attached to an application.
        """
        pass


    def childRequestedRepaint(self, alreadyNotified):
        """The child components of the component must call this method when they
        need repainting. The call must be made even in the case in which the
        children sent the repaint request themselves.

        <p>
        A repaint request is ignored if the component is invisible.
        </p>

        <p>
        This method is called automatically by {@link AbstractComponent}, which
        also provides a default implementation of it. As this is a somewhat
        internal feature, it is rarely necessary to reimplement this or call it
        explicitly.
        </p>

        @param alreadyNotified
                   the collection of repaint request listeners that have been
                   already notified by the child. This component should not
                   re-notify the listed listeners again. The container given as
                   parameter must be modifiable as the component might modify it
                   and pass it forward. A {@code null} parameter is interpreted
                   as an empty collection.
        """
        pass


    def addListener(self, listener):
        """Registers a new (generic) component event listener for the component.

        <pre>
        class Listening extends CustomComponent implements Listener {
            // Stored for determining the source of an event
            Button ok;

            Label status; // For displaying info about the event

            public Listening() {
                VerticalLayout layout = new VerticalLayout();

                // Some miscellaneous component
                TextField name = new TextField(&quot;Say it all here&quot;);
                name.addListener(this);
                name.setImmediate(true);
                layout.addComponent(name);

                // Handle button clicks as generic events instead
                // of Button.ClickEvent events
                ok = new Button(&quot;OK&quot;);
                ok.addListener(this);
                layout.addComponent(ok);

                // For displaying information about an event
                status = new Label(&quot;&quot;);
                layout.addComponent(status);

                setCompositionRoot(layout);
            }

            public void componentEvent(Event event) {
                // Act according to the source of the event
                if (event.getSource() == ok)
                    getWindow().showNotification(&quot;Click!&quot;);

                status.setValue(&quot;Event from &quot; + event.getSource().getClass().getName()
                        + &quot;: &quot; + event.getClass().getName());
            }
        }

        Listening listening = new Listening();
        layout.addComponent(listening);
        </pre>

        @param listener
                   the new Listener to be registered.
        @see Component.Event
        @see #removeListener(Listener)
        """
        pass


    def removeListener(self, listener):
        """Removes a previously registered component event listener from this
        component.

        @param listener
                   the listener to be removed.
        @see #addListener(Listener)
        """
        pass


class Event(EventObject):
    """Superclass of all component originated events.

    <p>
    Events are the basis of all user interaction handling in Vaadin. To
    handle events, you provide a listener object that receives the events of
    the particular event type.
    </p>

    <pre>
    Button button = new Button(&quot;Click Me!&quot;);
    button.addListener(new Button.ClickListener() {
        public void buttonClick(ClickEvent event) {
            getWindow().showNotification(&quot;Thank You!&quot;);
        }
    });
    layout.addComponent(button);
    </pre>

    <p>
    Notice that while each of the event types have their corresponding
    listener types; the listener interfaces are not required to inherit the
    {@code Component.Listener} interface.
    </p>

    @see Component.Listener
    """

    def __init__(self, source):
        """Constructs a new event with the specified source component.

        @param source
                   the source component of the event
        """
        super(Event, self)(source)


    def getComponent(self):
        """Gets the component where the event occurred.

        @return the source component of the event
        """
        return self.getSource()


class Listener(EventListener):
    """Listener interface for receiving <code>Component.Event</code>s.

    <p>
    Listener interfaces are the basis of all user interaction handling in
    Vaadin. You have or create a listener object that receives the events.
    All event types have their corresponding listener types; they are not,
    however, required to inherit the {@code Component.Listener} interface,
    and they rarely do so.
    </p>

    <p>
    This generic listener interface is useful typically when you wish to
    handle events from different component types in a single listener method
    ({@code componentEvent()}. If you handle component events in an anonymous
    listener class, you normally use the component specific listener class,
    such as {@link com.vaadin.ui.Button.ClickEvent}.
    </p>

    <pre>
    class Listening extends CustomComponent implements Listener {
        Button ok; // Stored for determining the source of an event

        Label status; // For displaying info about the event

        public Listening() {
            VerticalLayout layout = new VerticalLayout();

            // Some miscellaneous component
            TextField name = new TextField(&quot;Say it all here&quot;);
            name.addListener(this);
            name.setImmediate(true);
            layout.addComponent(name);

            // Handle button clicks as generic events instead
            // of Button.ClickEvent events
            ok = new Button(&quot;OK&quot;);
            ok.addListener(this);
            layout.addComponent(ok);

            // For displaying information about an event
            status = new Label(&quot;&quot;);
            layout.addComponent(status);

            setCompositionRoot(layout);
        }

        public void componentEvent(Event event) {
            // Act according to the source of the event
            if (event.getSource() == ok
                    &amp;&amp; event.getClass() == Button.ClickEvent.class)
                getWindow().showNotification(&quot;Click!&quot;);

            // Display source component and event class names
            status.setValue(&quot;Event from &quot; + event.getSource().getClass().getName()
                    + &quot;: &quot; + event.getClass().getName());
        }
    }

    Listening listening = new Listening();
    layout.addComponent(listening);
    </pre>

    @see Component#addListener(Listener)
    """

    def componentEvent(self, event):
        """Notifies the listener of a component event.

        <p>
        As the event can typically come from one of many source components,
        you may need to differentiate between the event source by component
        reference, class, etc.
        </p>

        <pre>
        public void componentEvent(Event event) {
            // Act according to the source of the event
            if (event.getSource() == ok &amp;&amp; event.getClass() == Button.ClickEvent.class)
                getWindow().showNotification(&quot;Click!&quot;);

            // Display source component and event class names
            status.setValue(&quot;Event from &quot; + event.getSource().getClass().getName()
                    + &quot;: &quot; + event.getClass().getName());
        }
        </pre>

        @param event
                   the event that has occured.
        """
        pass


class ErrorEvent(Event):
    """Class of all component originated error events.

    <p>
    The component error event is normally fired by
    {@link AbstractComponent#setComponentError(ErrorMessage)}. The component
    errors are set by the framework in some situations and can be set by user
    code. They are indicated in a component with an error indicator.
    </p>
    """

    def __init__(self, message, component):
        """Constructs a new event with a specified source component.

        @param message
                   the error message.
        @param component
                   the source component.
        """
        super(ErrorEvent, self)(component)
        self._message = message


    def getErrorMessage(self):
        """Gets the error message.

        @return the error message.
        """
        return self._message


class ErrorListener(EventListener):
    """Listener interface for receiving <code>Component.Errors</code>s."""

    def componentError(self, event):
        """Notifies the listener of a component error.

        @param event
                   the event that has occured.
        """
        pass


class Focusable(Component):
    """A sub-interface implemented by components that can obtain input focus.
    This includes all {@link Field} components as well as some other
    components, such as {@link Upload}.

    <p>
    Focus can be set with {@link #focus()}. This interface does not provide
    an accessor that would allow finding out the currently focused component;
    focus information can be acquired for some (but not all) {@link Field}
    components through the {@link com.vaadin.event.FieldEvents.FocusListener}
    and {@link com.vaadin.event.FieldEvents.BlurListener} interfaces.
    </p>

    @see FieldEvents
    """

    def focus(self):
        """Sets the focus to this component.

        <pre>
        Form loginBox = new Form();
        loginBox.setCaption(&quot;Login&quot;);
        layout.addComponent(loginBox);

        // Create the first field which will be focused
        TextField username = new TextField(&quot;User name&quot;);
        loginBox.addField(&quot;username&quot;, username);

        // Set focus to the user name
        username.focus();

        TextField password = new TextField(&quot;Password&quot;);
        loginBox.addField(&quot;password&quot;, password);

        Button login = new Button(&quot;Login&quot;);
        loginBox.getFooter().addComponent(login);
        </pre>

        <p>
        Notice that this interface does not provide an accessor that would
        allow finding out the currently focused component. Focus information
        can be acquired for some (but not all) {@link Field} components
        through the {@link com.vaadin.event.FieldEvents.FocusListener} and
        {@link com.vaadin.event.FieldEvents.BlurListener} interfaces.
        </p>

        @see com.vaadin.event.FieldEvents
        @see com.vaadin.event.FieldEvents.FocusEvent
        @see com.vaadin.event.FieldEvents.FocusListener
        @see com.vaadin.event.FieldEvents.BlurEvent
        @see com.vaadin.event.FieldEvents.BlurListener
        """
        pass


    def getTabIndex(self):
        """Gets the <i>tabulator index</i> of the {@code Focusable} component.

        @return tab index set for the {@code Focusable} component
        @see #setTabIndex(int)
        """
        pass


    def setTabIndex(self, tabIndex):
        """Sets the <i>tabulator index</i> of the {@code Focusable} component.
        The tab index property is used to specify the order in which the
        fields are focused when the user presses the Tab key. Components with
        a defined tab index are focused sequentially first, and then the
        components with no tab index.

        <pre>
        Form loginBox = new Form();
        loginBox.setCaption(&quot;Login&quot;);
        layout.addComponent(loginBox);

        // Create the first field which will be focused
        TextField username = new TextField(&quot;User name&quot;);
        loginBox.addField(&quot;username&quot;, username);

        // Set focus to the user name
        username.focus();

        TextField password = new TextField(&quot;Password&quot;);
        loginBox.addField(&quot;password&quot;, password);

        Button login = new Button(&quot;Login&quot;);
        loginBox.getFooter().addComponent(login);

        // An additional component which natural focus order would
        // be after the button.
        CheckBox remember = new CheckBox(&quot;Remember me&quot;);
        loginBox.getFooter().addComponent(remember);

        username.setTabIndex(1);
        password.setTabIndex(2);
        remember.setTabIndex(3); // Different than natural place
        login.setTabIndex(4);
        </pre>

        <p>
        After all focusable user interface components are done, the browser
        can begin again from the component with the smallest tab index, or it
        can take the focus out of the page, for example, to the location bar.
        </p>

        <p>
        If the tab index is not set (is set to zero), the default tab order
        is used. The order is somewhat browser-dependent, but generally
        follows the HTML structure of the page.
        </p>

        <p>
        A negative value means that the component is completely removed from
        the tabulation order and can not be reached by pressing the Tab key
        at all.
        </p>

        @param tabIndex
                   the tab order of this component. Indexes usually start
                   from 1. Zero means that default tab order should be used.
                   A negative value means that the field should not be
                   included in the tabbing sequence.
        @see #getTabIndex()
        """
        pass
