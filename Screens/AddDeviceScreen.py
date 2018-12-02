# coding=utf-8
from kivy.uix.screenmanager import Screen
from Client import Dispositivo

# classe da tela de adicionar dispositivo local
class AddDeviceScreen(Screen):

    # evento de entrada na tela
    def on_enter(self, *args):
        # limpa os campos do ip e estado
        self.ids['txt_ip'].text = ''
        self.ids['lbl_status'].text = ''

    # descoberta do dispositivo local bem sucedida
    def on_discovery_success(self):
        # limpa o campo de estado
        self.ids['lbl_status'].text = ''
        # retorna para a tela anterior
        self.manager.current = 'ListScreen'

    # falha na descoberta de dispositivo local
    def on_discovery_error(self):
        # coloca o campo de estado com mensagem de falha
        self.ids['lbl_status'].text = 'Dispositivo não respondeu!'
        self.ids['lbl_status'].color = [1, 0, 0, 1]

    # ação de procurar um dispositivo local
    def action_find_device(self):
        # armazena erro durante o processo de verificação
        error = False

        # o campo de texto onde foi inserido o ip do dispositivo
        text_input = self.ids['txt_ip']
        # divide os campos do ip pelos pontos '.'
        fields = str(text_input.text).split('.')
        # devem ser 4 campos no ip
        if len(fields) != 4:
            error = True
        else:
            for field in fields:
                try:
                    value = int(field)
                    # o valor de cada campo deve estar entre 0 e 255
                    if not(0 <= value < 256):
                        error = True
                        break
                except:
                    error = True

        if error:
            # mostra no campo de estado um erro de ip inválido
            self.ids['lbl_status'].text = 'Endereço IP inválido!'
            self.ids['lbl_status'].color = [1, 0, 0, 1]
        else:
            # mostra no campo de estado a situação de procurando...
            self.ids['lbl_status'].text = 'Procurando dispositivo...'
            self.ids['lbl_status'].color = [1, 1, 1, 1]
            Dispositivo.discover(text_input.text,
                                 on_success=self.on_discovery_success,
                                 on_error=self.on_discovery_error)

