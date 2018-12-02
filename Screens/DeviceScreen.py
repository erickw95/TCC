# coding=utf-8
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from Client import Client


# classe da tela do dispositivo, que mostra a ultima leitura e opções para o dispositivo
class DeviceScreen(Screen):

    # armazena qual é o dispositivo a que se refere a tela
    dispositivo = None
    # armazenamento dos botões criados dinâmicamente
    btns = []

    # evento de entreda na tela
    def on_enter(self, *args):
        self.bcolor = [.0, .0, .0, 1]
        if self.dispositivo is None:
            self.dispositivo = Client.current_dispositivo
            if self.dispositivo.is_local:
                self.ids['lbl_device_name'].text = self.dispositivo.nome + ' (LOCAL)'
                self.build_local_device_widgets()
            else:
                self.ids['lbl_device_name'].text = self.dispositivo.nome
                self.build_remote_device_widgets()
        else:
            if self.dispositivo.is_local:
                self.ids['lbl_device_name'].text = self.dispositivo.nome + ' (LOCAL)'
            else:
                self.ids['lbl_device_name'].text = self.dispositivo.nome
        self.action_update_reading(None)

    # constrói as opções para dispositivo local
    def build_local_device_widgets(self):
        self.btns.append(Button(text='Mudar Identificação do Dispositivo',
                                size_hint=(1, .1),
                                on_press=self.action_change_identifier,
                                id='btn_1'))
        self.btns.append(Button(text='Atualizar Leitura',
                                size_hint=(1, .1),
                                on_press=self.action_update_reading,
                                id='btn_2'))
        self.ids['box_layout'].add_widget(self.btns[0])
        self.ids['box_layout'].add_widget(self.btns[1])

    # constrói as opções para dispositivo remoto (API)
    def build_remote_device_widgets(self):
        self.btns.append(Button(text='Mostrar Histórico',
                                size_hint=(1, .1),
                                on_press=self.action_show_history,
                                id='btn_1'))
        self.ids['box_layout'].add_widget(self.btns[0])

    # evento de saída da tela
    def on_leave(self, *args):
        self.dispositivo.is_selected = False
        self.dispositivo = None
        # retira os botões criados
        for btn in self.btns:
            self.ids['box_layout'].remove_widget(btn)
        self.btns = []

    # ação de mostrar o histórico do dispositivo
    def action_show_history(self, instance):
        # troca pra tela de histórico
        self.manager.current = 'HistoryScreen'

    # ação de trocar o identificador do dispositivo
    def action_change_identifier(self, instance):
        # troca pra tela de modificar dispositivo
        self.manager.current = 'ModifyDeviceScreen'

    # ação de atualizar leitura
    def action_update_reading(self, instance):
        # mostra o estado de atualizando no campo de estado
        self.ids['lbl_status'].text = 'Atualizando...'
        self.ids['lbl_status'].color = [1, 1, 1, 1]
        # chama a requisição de atualização de leitura
        self.dispositivo.update_reading(on_success=self.on_update_reading_success,
                                        on_error=self.on_update_reading_error)

    # sucesso na atualização da leitura
    def on_update_reading_success(self):
        try:
            reading = self.dispositivo.last_reading
            # limpa o campo de estado
            self.ids['lbl_reading'].text = str(reading)
            self.ids['lbl_status'].text = ''
            # faz a cor de acordo com o índice UV da última leitura
            if 0 <= reading <= 2:
                self.bcolor = [.1, .3, .1, 1] # verde
            elif 3 <= reading <= 5:
                self.bcolor = [.6, .6, .0, 1] # amarelo
            elif 6 <= reading <= 7:
                self.bcolor = [.7, .4, .0, 1] # amarelo-laranja
            elif 8 <= reading <= 10:
                self.bcolor = [.5, .0, .0, 1] # vermelho
            elif 11 <= reading <= 14:
                self.bcolor = [.3, 0, .3, 1]  # violeta
        except:
            print('user exited screen')

    # erro na atualização da leitura
    def on_update_reading_error(self):
        # mostra mensagem de erro no campo de estado
        self.ids['lbl_status'].text = 'Não foi possível obter nova leitura!'
        self.ids['lbl_status'].color = [1, 0, 0, 1]

