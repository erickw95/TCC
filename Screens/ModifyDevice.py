# coding=utf-8
from kivy.uix.screenmanager import Screen
from Client import Client


# classe para a tela de modificar dispositivo
class ModifyDevice(Screen):

    # armazena o dispositivo a que se refere a tela
    dispositivo = None

    # evento de entrada na tela
    def on_enter(self, *args):
        self.dispositivo = Client.current_dispositivo
        self.ids['txt_nome'].text = self.dispositivo.nome

    # ação de alteração de nome do dispositivo
    def action_change_name(self):
        # novo nome do campo de texto
        new_name = self.ids['txt_nome'].text
        # verifica se há alterações no nome
        if new_name == self.dispositivo.nome:
            self.ids['lbl_status'].text = 'Sem alterações!'
        else:
            self.ids['lbl_status'].text = 'Alterando nome!'
            # chama a requisição de alteração de nome
            self.dispositivo.change_name(new_name=new_name,
                                         on_success=self.on_change_name_success,
                                         on_error=self.on_change_name_error)

    # sucesso na alteração do nome
    def on_change_name_success(self):
        # retorna para a tela anterior
        self.manager.current = 'DeviceScreen'

    # falha na alteração do nome
    def on_change_name_error(self):
        # mostra mensagem de erro no campo de estado
        self.ids['lbl_status'].text = 'Não foi possível renomear o dispositivo!'
