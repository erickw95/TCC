# coding=utf-8
from kivy.uix.screenmanager import Screen
from Client import Client
from kivy.uix.label import Label
from kivy.adapters.listadapter import ListAdapter
import datetime


# classe da tela de histórico do dispositivo, que mostra os dados das últimas 24 horas
class HistoryScreen(Screen):

    # armazena o dispositivo a que se refere a tela
    dispositivo = None
    # dados do histórico
    history = []

    # conversor para os elementos da lista
    def args_converter(row_index, obj):
        reading = obj.leituraUV
        # cria objeto de data com a string que veio pela API
        date = datetime.datetime.strptime(str(obj.data).split('.')[0], '%Y-%m-%dT%H:%M:%S')
        # exemplo do formato:
        # "2018-11-20T23:06:49"

        today = datetime.datetime.now()
        # monta um formado de data mais amigável
        date_friendly = ' '
        if date.day == today.day:
            date_friendly += 'Hoje'
        else:
            date_friendly += 'Ontem'
        date_friendly += ' às ' + date.strftime('%H:%M')
        # compõe o text ocompleto do item na lista
        text = 'Índice UV: ' + str(reading) + '\n' + date_friendly
        # define a cor do texto de acordo com o índice uv da leitura
        color = [1, 1, 0, 1]
        if 0 <= reading <= 2:
            color = [.1, .8, .1, 1] # verde
        elif 3 <= reading <= 5:
            color = [.9, .9, .0, 1] # amarelo
        elif 6 <= reading <= 7:
            color = [.9, .6, .0, 1] # amarelo-laranja
        elif 8 <= reading <= 10:
            color = [.8, .0, .0, 1] # vermelho
        elif 11 <= reading <= 14:
            color = [.7, 0, .7, 1]  # violeta
        return {'text': text, 'size_hint_y': None, 'size_hint': (1, .5),'color': color, 'font_size': '12sp'}

    # adaptador DadosDeLeitura<->ListaDeLabel
    list_adapter = ListAdapter(data=history,
                               args_converter=args_converter,
                               propagate_selection_to_data=False,
                               cls=Label)

    # evento de entrada na tela
    def on_enter(self, *args):
        self.dispositivo = Client.current_dispositivo
        self.action_update_history()

    # ação de atualizar o histórico
    def action_update_history(self):
        # coloca o estado de atualizando no campo de histórico
        self.ids['lbl_status'].text = 'Atualizando...'
        self.ids['lbl_status'].color = [1, 1, 1, 1]
        # chama a requisição do histórico do dispositivo
        self.dispositivo.fetch_history(on_success=self.on_update_history_success,
                                       on_error=self.on_update_history_error)

    # evento de mudança na seleção da lista
    def list_selection_changed(self, *args):
        pass

    # sucesso na atualização do histórico
    def on_update_history_success(self):
        # indicação do periodo no campo de status
        self.ids['lbl_status'].text = 'Últimas 24 horas:'
        self.ids['lbl_status'].color = [1, 1, 1, 1]
        # atualização da lista na tela
        self.history = self.dispositivo.history
        self.list_adapter.data = self.history

    # erro na atualização do histórico
    def on_update_history_error(self):
        # mostra mensagem de erro no campo de status
        self.ids['lbl_status'].text = 'Não foi possível obter o histórico'
        self.ids['lbl_status'].color = [1, 0, 0, 1]
