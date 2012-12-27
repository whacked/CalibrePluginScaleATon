
from calibre.customize import InterfaceActionBase

class MyPlugin(InterfaceActionBase):

    name                = 'Right click plugin'
    description         = 'Create an action menu that appears on right click'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Sir Skeleton'
    version             = (0, 0, 1)
    minimum_calibre_version = (0, 7, 53)

    actual_plugin       = 'calibre_plugins.myplugin.ui:RightClickPlugin'

    def is_customizable(self):
        return True

    def config_widget(self):
        from calibre_plugins.myplugin.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        '''
        Save the settings specified by the user with config_widget.

        :param config_widget: The widget returned by :meth:`config_widget`.
        '''
        config_widget.save_settings()

        # Apply the changes
        ac = self.actual_plugin_
        if ac is not None:
            ac.apply_settings()
