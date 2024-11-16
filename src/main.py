import gi
import os
import subprocess

gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Gio, Adw, GLib

class CACManagerApp(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_default_size(600, 680)  # Adjusted height to accommodate image
        self.set_resizable(True)  # Enable window resizing, includes maximize button
        self.set_title("")  # Explicitly remove any default title

        # Main container that holds the header and the stack
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Use AdwHeaderBar for a modern look, but place it within the content area
        self.header_bar = Adw.HeaderBar()
        self.header_bar.set_show_end_title_buttons(True)
        self.header_bar.set_margin_top(0)  # Remove extra space above the header bar
        self.header_bar.add_css_class("flat")  # Make the header visually minimal
        self.header_bar.add_css_class("card")  # GNOME "card" styling for integration
        main_box.append(self.header_bar)

        # Create a stack to switch between different pages
        self.stack = Gtk.Stack()
        self.stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_transition_duration(500)

        # Home page
        self.home_page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        self.home_page.set_halign(Gtk.Align.CENTER)
        self.home_page.set_valign(Gtk.Align.CENTER)
        self.home_page.set_margin_top(30)  # Add padding to the top of the home page for spacing

        # Welcome title with adjusted font size
        welcome_label = Gtk.Label(label="CAC Manager")
        welcome_label.set_markup("<span size='20000'><b>CAC Manager</b></span>")  # 20pt size in pango markup
        welcome_label.set_halign(Gtk.Align.CENTER)
        self.home_page.append(welcome_label)

        # CAC Image
        cac_image = Gtk.Image.new_from_icon_name("accessories-contacts")
        cac_image.set_pixel_size(100)  # Set the size of the icon to 100 pixels
        cac_image.set_halign(Gtk.Align.CENTER)
        self.home_page.append(cac_image)

        # Description text
        description_label = Gtk.Label(
            label="Please use the options below to install required software, set up DoD certificates, "
                  "or configure your browser for CAC use."
        )
        description_label.set_wrap(True)
        description_label.set_justify(Gtk.Justification.CENTER)
        description_label.set_halign(Gtk.Align.CENTER)
        self.home_page.append(description_label)

        # Add buttons for each feature
        buttons_info = [
            ("Documentation", self.on_documentation_clicked),
            ("Install", self.on_install_clicked),
            ("Configure", self.on_configure_clicked),
            ("Test", self.on_test_clicked),
            ("Troubleshoot", self.on_troubleshoot_clicked)
        ]

        for label, callback in buttons_info:
            button = Gtk.Button(label=label)
            button.set_halign(Gtk.Align.CENTER)
            button.add_css_class("pill")
            button.set_margin_top(10)
            button.set_hexpand(False)  # Reduce button width by not expanding fully
            button.set_size_request(150, -1)  # Set a smaller consistent minimum width for all buttons
            button.connect("clicked", self.on_navigate_to_page, callback)
            self.home_page.append(button)

        # Add the home page to the stack
        self.stack.add_named(self.home_page, "home")

        # Create individual pages for each function
        for label, callback in buttons_info:
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
            page.set_halign(Gtk.Align.FILL)
            page.set_valign(Gtk.Align.FILL)
            page.set_margin_start(20)
            page.set_margin_end(20)
            page.set_margin_top(20)
            page.set_margin_bottom(20)

            # Add a back button to the header bar
            back_button = Gtk.Button.new_from_icon_name("go-previous-symbolic")
            back_button.add_css_class("flat")
            back_button.connect("clicked", self.on_back_to_home_clicked)

            # Page title with consistent styling
            function_label = Gtk.Label()
            function_label.set_markup(f"<span size='20000'><b>{label}</b></span>")  # 20pt size in pango markup
            function_label.set_halign(Gtk.Align.START)
            page.append(function_label)

            # Separator under the title
            separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            page.append(separator)

            # Status label for updates or content-specific information
            status_label = Gtk.Label()
            status_label.set_halign(Gtk.Align.START)
            status_label.set_margin_top(10)
            status_label.set_wrap(True)
            page.append(status_label)

            # Assign callback and status label for later use
            page.callback = callback
            page.status_label = status_label

            # Store the back button so we can add it to the header when navigating
            page.back_button = back_button

            # Add the page to the stack
            self.stack.add_named(page, label.replace(" ", "_").lower())

        # Add the stack to the main container
        main_box.append(self.stack)

        # Set the main container as the window content
        self.set_content(main_box)

    def on_navigate_to_page(self, button, callback):
        # Find the page associated with the callback and navigate to it
        page_name = button.get_label().replace(" ", "_").lower()
        page = self.stack.get_child_by_name(page_name)
        if page:
            # Add the back button to the header bar
            if hasattr(page, 'back_button'):
                self.header_bar.pack_start(page.back_button)
            self.stack.set_visible_child_name(page_name)

            # Run the callback
            if hasattr(page, 'callback'):
                page.callback(page)

    def on_back_to_home_clicked(self, button):
        # Navigate back to the home page
        self.stack.set_visible_child_name("home")
        # Remove the back button from the header bar
        self.header_bar.remove(button)

    # Button click handlers
    def on_documentation_clicked(self, page):
        with open('docs/documentation.txt', 'r') as file:
            documentation_text = file.read()
            page.status_label.set_markup(documentation_text)

    def on_install_clicked(self, page):
        page.status_label.set_markup("<span size='large'>Install button clicked. This will guide you through the necessary software installation steps.</span>")

    def on_configure_clicked(self, page):
        page.status_label.set_markup("<span size='large'>Configure button clicked. This will guide you through configuring your environment.</span>")

    def on_test_clicked(self, page):
        page.status_label.set_markup("<span size='large'>Test button clicked. This will help you verify the setup functionality.</span>")

    def on_troubleshoot_clicked(self, page):
        page.status_label.set_markup("<span size='large'>Troubleshoot button clicked. This will guide you through common troubleshooting steps.</span>")

    # Helper function to show error dialogs
    def show_error(self, message):
        error_dialog = Gtk.MessageDialog(transient_for=self,
                                         modal=True,
                                         buttons=Gtk.ButtonsType.CLOSE,
                                         message_type=Gtk.MessageType.ERROR,
                                         text="An Error Occurred",
                                         secondary_text=message)
        error_dialog.connect("response", lambda dialog, response: dialog.destroy())
        error_dialog.show()

# GTK Application setup
class CACManagerApplication(Adw.Application):
    def __init__(self):
        super().__init__(application_id="org.example.CACManager",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = CACManagerApp(application=self)
        win.present()

# Run the application
if __name__ == "__main__":
    app = CACManagerApplication()
    Adw.init()
    app.run()
