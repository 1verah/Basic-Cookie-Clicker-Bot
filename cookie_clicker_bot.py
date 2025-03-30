# Importar librerías necesarias
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración inicial del navegador
service = Service(executable_path="chromedriver.exe")  # Ruta al controlador de Chrome
driver = webdriver.Chrome(service=service)  # Inicializar navegador Chrome

# Abrir la página de Cookie Clicker
driver.get("https://orteil.dashnet.org/cookieclicker/")

# IDs de elementos importantes del juego
cookie_id = "bigCookie"  # ID de la galleta principal
cookies_id = "cookies"  # ID del contador de galletas
product_price_prefix = "productPrice"  # Prefijo para precios de mejoras
product_prefix = "product"  # Prefijo para elementos de mejoras

# Esperar a que cargue el selector de idioma y seleccionar inglés
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'English')]")))
language = driver.find_element(By.XPATH, "//*[contains(text(), 'English')]")
language.click()

# Esperar a que cargue la galleta principal
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, cookie_id)))
cookie = driver.find_element(By.ID, cookie_id)

# Bucle principal de automatización
while True:
    cookie.click()  # Hacer clic en la galleta
    
    # Obtener y formatear el número de galletas actuales
    cookies_count = driver.find_element(By.ID, cookies_id).text.split(" ")[0]
    cookies_count = int(cookies_count.replace(",", ""))  # Convertir a entero
    
    # Intentar comprar mejoras (hasta 4 tipos disponibles)
    for i in range(4):
        try:
            # Obtener precio de la mejora actual
            product_price = driver.find_element(
                By.ID, product_price_prefix + str(i)
            ).text.replace(",", "")
            
            if not product_price.isdigit():  # Saltar si no es un número válido
                continue
                
            product_price = int(product_price)
            
            # Comprar mejora si hay suficientes galletas
            if cookies_count >= product_price:
                product = driver.find_element(By.ID, product_prefix + str(i))
                product.click()
                break  # Salir del bucle después de comprar
                
        except Exception as e:  # Manejar errores silenciosamente
            continue