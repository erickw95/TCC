# coding=utf-8
from kivy.network.urlrequest import UrlRequest

# classe para guardar os dados consumidos na aplicação
class Client:
    # url da api a ser consumida
    base_url = 'http://monitoruv.herokuapp.com/api/'
    # armazena o dispositivo manipulado atualmente na aplicação
    current_dispositivo = None
    # lista de dispositivos
    dispositivos = []
    # lista dos dispositivos locais
    local_dispositivos = []


# classe que representa uma leitura uv armazenada no banco
class Dado:
    def __init__(self, leituraUV=0, data='', dispositivo_id=1):
        self.leituraUV = leituraUV
        self.data = data
        self.dispositivo_id = dispositivo_id


# classe que representa um dispositivo(arduino + sensor + wifi)
class Dispositivo:

    # historico de leituras do dispositivo
    history = []

    def __init__(self, nome='', longitude=0.0, latitude=0.0, is_local=False, ip_addr='', db_id=0, last_reading=0):
        self.nome = nome
        self.longitude = longitude
        self.latitude = latitude
        self.is_selected = False
        self.is_local = is_local
        self.ip_addr = ip_addr
        self.db_id = db_id
        self.last_reading = last_reading

    # devolve a lista de todos os dispositivos cadastrados no banco
    @staticmethod
    def all():
        return Client.dispositivos

    # ========================================================
    # Histórico
    # ========================================================

    # obtém o histórico das últimas 24 horas de leitura do dispositivo
    def fetch_history(self, on_success=None, on_error=None):
        Client.dispositivos_on_fetch_history_success = on_success
        Client.dispositivos_on_fetch_history_error = on_error

        UrlRequest(Client.base_url + "dispositivos/" + str(self.db_id) + '/last_day/',
                   on_success=self.__on_fetch_history_success,
                   on_failure=self.__on_fetch_history_error,
                   on_error=self.__on_fetch_history_error)

    def __on_fetch_history_success(self, req, res):
        self.history = []
        for item in res:
            self.history.append(Dado(leituraUV=item['leituraUV'],
                                     data=item['data'],
                                     dispositivo_id=item['dispositivo']))

        if Client.dispositivos_on_fetch_history_success:
            Client.dispositivos_on_fetch_history_success()

    def __on_fetch_history_error(self, req, res):
        print('ERROR on fetch history')

        if Client.dispositivos_on_fetch_history_error:
            Client.dispositivos_on_fetch_history_error()

    # ========================================================
    # Última leitura
    # ========================================================

    # pega a última leitura leitura realizada pelo dispositivo
    def update_reading(self, on_success=None, on_error=None):
        Client.dispositivos_on_update_reading_success = on_success
        Client.dispositivos_on_update_reading_error = on_error
        if self.is_local:
            UrlRequest('http://' + self.ip_addr + '/read',
                       on_success=self.__on_update_reading_success,
                       on_failure=self.__on_update_reading_error,
                       on_error=self.__on_update_reading_error)
        else:
            UrlRequest(Client.base_url + "dispositivos/" + str(self.db_id) + '/last/',
                       on_success=self.__on_update_reading_success,
                       on_failure=self.__on_update_reading_error,
                       on_error=self.__on_update_reading_error)

    def __on_update_reading_success(self, req, res):
        if self.is_local:
            self.last_reading = int(str(res).split(':')[1])
        else:
            self.last_reading = res[0]['leituraUV']

        if Client.dispositivos_on_update_reading_success:
            Client.dispositivos_on_update_reading_success()

    def __on_update_reading_error(self, req, res):
        print('ERROR on update reading')

        if Client.dispositivos_on_update_reading_error:
            Client.dispositivos_on_update_reading_error()

    # ========================================================
    # Alterar nome de dispositivo local
    # ========================================================

    # troca para um novo nome um dispositivo local
    def change_name(self, new_name, on_success=None, on_error=None):
        if self.is_local:
            Client.dispositivos_on_change_name_success = on_success
            Client.dispositivos_on_change_name_error = on_error

            UrlRequest('http://' + self.ip_addr + '/id/' + new_name,
                       on_success=self.__on_change_name_success,
                       on_failure=self.__on_change_name_error,
                       on_error=self.__on_change_name_error)
        else:
            print('can\'t change name of a remote device')

    def __on_change_name_success(self, req, res):
        self.nome = str(res).splitlines()[0]

        if Client.dispositivos_on_change_name_success:
            Client.dispositivos_on_change_name_success()

    def __on_change_name_error(self, req, res):
        print('ERROR on change name')

        if Client.dispositivos_on_change_name_error:
            Client.dispositivos_on_change_name_error()

    # ========================================================
    # Descoberta
    # ========================================================

    # tenta uma conexão com um dispositivo local, perguntando seu ID
    @staticmethod
    def discover(address, on_success=None, on_error=None):
        Client.dispositivos_on_discover_success = on_success
        Client.dispositivos_on_discover_error = on_error

        Client.local_device = Dispositivo(ip_addr=address, is_local=True)

        UrlRequest('http://' + address + '/id',
                   on_success=Dispositivo.__on_discover_success,
                   on_failure=Dispositivo.__on_discover_error,
                   on_error=Dispositivo.__on_discover_error)

    @staticmethod
    def __on_discover_success(req, res):

        Client.local_device.nome = str(res).splitlines()[0]

        Client.local_dispositivos.append(Client.local_device)

        if Client.dispositivos_on_discover_success:
            Client.dispositivos_on_discover_success()

    @staticmethod
    def __on_discover_error(req, res):
        print('ERROR on discovery')

        if Client.dispositivos_on_discover_error:
            Client.dispositivos_on_discover_error()

    # ========================================================
    # Todos os dispositivos
    # ========================================================

    # obtém a lista completa de dispositivos cadastrados
    @staticmethod
    def fetch_all(on_success=None, on_error=None):
        Client.dispositivos_on_fetch_all_success = on_success
        Client.dispositivos_on_fetch_all_error = on_error

        UrlRequest(Client.base_url + 'dispositivos/',
                   on_success=Dispositivo.__on_fetch_all_success,
                   on_failure=Dispositivo.__on_fetch_all_error,
                   on_error=Dispositivo.__on_fetch_all_error)

    @staticmethod
    def __on_fetch_all_success(req, res):
        Client.dispositivos = []

        count = 1

        for item in res:
            Client.dispositivos.append(Dispositivo(nome=item['nome'],
                                                   longitude=item['longitude'],
                                                   latitude=item['latitude'],
                                                   db_id=count))
            count += 1

        for item in Client.local_dispositivos:
            Client.dispositivos.append(item)

        if Client.dispositivos_on_fetch_all_success:
            Client.dispositivos_on_fetch_all_success()

    @staticmethod
    def __on_fetch_all_error(req, err):
        print('failure')

        if Client.dispositivos_on_fetch_all_error:
            Client.dispositivos_on_fetch_all_error()
