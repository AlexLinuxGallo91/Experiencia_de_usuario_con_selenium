from selenium import webdriver

path_web_driver = '/vagrant_data/geckodriver'
url_test = 'https://www.google.com'
mozilla_options = webdriver.FirefoxOptions()
mozilla_options.headless = True
mozilla_options.add_argument('--ignore-certificate-errors')
driver_mozilla = webdriver.Firefox(executable_path=path_web_driver, options=mozilla_options)

driver_mozilla.get(url_test)
print(driver_mozilla.title)
print('se ingresa al sitio {}'.format(driver_mozilla.title))

driver_mozilla.get('https://exchangeadministrado.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fexchangeadministrado.com%2fowa%2f')
print(driver_mozilla.current_url)
print('se ingresa al sitio {}'.format(driver_mozilla.title))
print(elemento_encontrado)

driver_mozilla.close()