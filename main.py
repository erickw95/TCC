# coding=utf-8

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from Screens.ListScreen import ListScreen
from Screens.AddDeviceScreen import AddDeviceScreen
from Screens.DeviceScreen import DeviceScreen
from Screens.ModifyDevice import ModifyDevice
from Screens.HistoryScreen import HistoryScreen

# classe principal do app
class MonitorUVApp(App):

    # carrega as desenho das telas
    Builder.load_file('Screens/kivy/ListScreen.kv')
    Builder.load_file('Screens/kivy/AddDeviceScreen.kv')
    Builder.load_file('Screens/kivy/DeviceScreen.kv')
    Builder.load_file('Screens/kivy/ModifyDevice.kv')
    Builder.load_file('Screens/kivy/HistoryScreen.kv')

    # cria o genrenciador de telas
    screen_manager = ScreenManager()

    # adiciona uma instancia de cada tela ao gerenciador
    screen_manager.add_widget(ListScreen(name='ListScreen'))
    screen_manager.add_widget(AddDeviceScreen(name='AddDeviceScreen'))
    screen_manager.add_widget(DeviceScreen(name='DeviceScreen'))
    screen_manager.add_widget(ModifyDevice(name='ModifyDeviceScreen'))
    screen_manager.add_widget(HistoryScreen(name='HistoryScreen'))

    # tela inicial
    screen_manager.current = 'ListScreen'

    # construção do app
    def build(self):
        return self.screen_manager


# ponto de entrada da execução stand-alone
if __name__ == '__main__':
    MonitorUVApp().run()

