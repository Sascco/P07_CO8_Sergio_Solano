import data
import locators
from locators import locators
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado "
                            "el código en tu aplicación.")
        return code

class UrbanRoutesPage:

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):                                           # Casilla para ingrear dirección de origen
        self.driver.find_element(*locators.from_field).send_keys(from_address)

    def set_to(self, to_address):                                               # Casilla para ingrear dirección de destino
        self.driver.find_element(*locators.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*locators.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*locators.to_field).get_property('value')

    def click_book_a_taxi_button(self):                                         # Hace click en Botón "pedir un taxi" del menu inicial
        self.driver.find_element(*locators.book_a_taxi_button).click()

    def comfort_fare_button(self):                                              # Hace click para seleccionar la Tarifa "Comfort"
        self.driver.find_element(*self.comfort_fare).click()

    def set_phone_input_box(self):                                               # Hace click en casilla Numero de telefono en menu de pedido
        self.driver.find_element(*self.phone_input_box).click()

    def phone_popup_window_input_box(self):                                      # Ingresar número de telefono en ventana emergente
        self.driver.find_element(*self.add_phone_input_box).send_keys(data.phone_number)

    def phone_popup_window_input_box_next(self):                                 # Dar click en Siguiente para con el registro del  numero de telefono
        self.driver.find_element(*self.phone_popup_window_input_box_next ).click()

    def sms_code_inputbox(self):  # Código SMS
        code_sms = retrieve_phone_code                                           # Dar click en casilla para ingresar SMS con funcion pre establecida y completar el registro del numero de teleno
        print(code_sms)                    ##############esta funcion no genera el SMS terminar el proceso ---- revisar #######################
        self.driver.find_element(*self.add_sms_code).send_keys(code_sms)

    def code_confirm_button(self):                                               # Dar click en Boton confirmar SMS en ventana emergente
        self.driver.find_element(*self.confirm_button_sms).click()

    def add_payment_method_box(self):                                            # Dar click en casilla para agregar metodo de pago - tarjeta de credito
        self.driver.find_element(*self.payment_method_box).click()

    def add_new_credit_card(self):                                               # Dar click en boton '+' en la ventana para agregar nueva tarjeta de credito
        self.driver.find_element(*self.add_cc_button).click()

    def cc_number_field(self):                                                   # Dar click en casilla para agregar numero de tarjeta de credito
        self.driver.find_element(self.add_cc_number).click()

    def add_credit_card_number(self):                                            # Se importa numero de tarjeta de credito como medio de pago desde data.py
        self.driver.find_element(self.add_cc_number).send_keys(data.card_number)

    def cc_code_field(self):                                                     # se diligencia codigo de tarjeta de credito desde data.py
        self.driver.find_element(self.add_code_input_box).send_keys(data.card_code)

    def exit_payment_popup(self):                                               # Dar click en boton (X) de la ventana emergente para vincular tarjeta como medio de pago
        self.driver.find_element(self.exit_payment_popup_window).click()

    def message_to_driver_field(self):                                          # Casilla para ingresar mensaje para el conductor, se importa desde data.py
        self.driver.find_element(self.special_request_for_driver).send_keys(data.message_for_driver)

    def blanket_and_scarves(self):                                              # Dar click en checkbox para seleccionar manta y pañuelos como pedido especial para el servicio
        self.driver.find_element(self.blanket_and_scarves_request).click()

    def click_add_ice_cream_button(self):
        self.driver.find_element(self.ice_cream_counter).click()

