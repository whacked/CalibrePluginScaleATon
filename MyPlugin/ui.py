
from calibre.gui2.actions import InterfaceAction
from calibre.gui2 import question_dialog, info_dialog

class RightClickPlugin(InterfaceAction):

    name = 'Right Click Menu'

    action_spec = ('Right Click Menu', None,
                   'Activate the menu', None) # None = no keyboard shortcut

    action_type = 'current'

    def genesis(self):
        # skip the icon creation
        # icon = get_icons('images/icon.png')
        # self.qaction.setIcon(icon)
        self.qaction.triggered.connect(self.show_dialog)

    def show_dialog(self):
        # The base plugin object defined in __init__.py
        base_plugin_object = self.interface_action_base_plugin
        # Show the config dialog
        # The config dialog can also be shown from within
        # Preferences->Plugins, which is why the do_user_config
        # method is defined on the base plugin class
        do_user_config = base_plugin_object.do_user_config

        # self.gui is the main calibre GUI. It acts as the gateway to access
        # all the elements of the calibre user interface, it should also be the
        # parent of the dialog
        m = self.gui.library_view.model()
        selected_ids = self.gui.library_view.get_selected_ids()
        id_rows      = self.gui.library_view.ids_to_rows(selected_ids)
        if len(selected_ids) is 0: return
        
        retrieve_id = id_rows[selected_ids[0]]
        info = m.get_book_info(retrieve_id)
        str_info = "\n".join(map(lambda k: "%s: %s" % (k, info.get(k)), ['application_id', 'title', 'authors', 'timestamp']))
        info_dialog(self.gui, "Item info", str_info, show=True)
        
        # here's the telnet manhole
        from twisted.internet import reactor
        from twisted.manhole import telnet
        
        context = locals()
        
        def createShellServer():
            factory = telnet.ShellFactory()
            port = reactor.listenTCP(2222, factory)
            factory.namespace = context
            factory.username = ''
            factory.password = ''
            return port
       
        if question_dialog(self.gui, "telnet manhole section", "start shell server?"):
            reactor.callWhenRunning(createShellServer)
            reactor.run()

    def apply_settings(self):
        from calibre_plugins.myplugin.config import prefs
        # In an actual non trivial plugin, you would probably need to
        # do something based on the settings in prefs
        prefs
