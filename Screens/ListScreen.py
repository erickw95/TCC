# coding=utf-8

from kivy.uix.screenmanager import Screen
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton
from Client import Dispositivo, Client


# classe da tela de lista de dispositivos
class ListScreen(Screen):

    # conversor para os elementos da lista
    def args_converter(row_index, obj):
        nome = obj.nome
        # adiciona o sufixo ' (LOCAL)' para dispositivos locais
        if obj.is_local:
            nome += ' (LOCAL)'
        return {'text': nome, 'size_hint': (1, .1), 'height': 50}

    # adaptador de lista para os dispositivos
    list_adapter = ListAdapter(data=Dispositivo.all(),
                               args_converter=args_converter,
                               propagate_selection_to_data=True,
                               cls=ListItemButton)

    # evento de mudança na seleção da lista
    def list_selection_changed(self, *args):
        for dispositivo in Dispositivo.all():
            if dispositivo.is_selected:
                # troca pra tela do dispostivo selecionado
                Client.current_dispositivo = dispositivo
                self.manager.current = 'DeviceScreen'

    # evento de entrada na tela
    def on_enter(self):
        self.list_adapter.bind(on_selection_change=self.list_selection_changed)
        # chama a requisição da lista de dispositivos
        Dispositivo.fetch_all(on_success=self.on_fetch_success, on_error=self.on_connection_error)

    # erro na recuperação da lista
    def on_connection_error(self):
        # mostra mensagem de erro no campo de estado
        self.ids['lbl_connection_failure'].text = 'Não foi possível conectar ao serviço!'

    # sucesso na recuperação
    def on_fetch_success(self):
        # atualiza os dados da lista na tela
        self.list_adapter.data = Dispositivo.all()
        # limpa o campo de estado
        self.ids['lbl_connection_failure'].text = ''


