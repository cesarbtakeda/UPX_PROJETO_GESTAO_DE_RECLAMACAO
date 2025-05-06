import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def obter_urls():
    options = uc.ChromeOptions()
    # Removi --headless pra testar visível primeiro
    options.add_argument("--disable-gpu")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)
    arquivo_links = "url.txt"
    url = "https://www.reclameaqui.com.br/empresa/prefeitura-sorocaba/lista-reclamacoes/"
    
    driver.get(url)
    time.sleep(random.uniform(5, 8))
    pagina = 1
    links_coletados = []
    
    with open(arquivo_links, "w", encoding="utf-8") as file:
        while pagina <= 50:
            print(f"📄 Coletando links da página {pagina}...")
            try:
                # Aumentei o timeout pra 20s e mudei o seletor pra algo mais genérico
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='reclameaqui.com.br']"))
                )
                time.sleep(random.uniform(3, 5))

                # Novo seletor mais amplo pra pegar links de reclamações
                titulos = driver.find_elements(By.CSS_SELECTOR, "a[href*='reclameaqui.com.br']")
                links = [titulo.get_attribute("href") for titulo in titulos if "lista-reclamacoes" not in titulo.get_attribute("href")]
                links_coletados.extend(links)

                for link in links:
                    file.write(link + "\n")
                print(f"✅ {len(links)} links coletados e salvos.")

                try:
                    botao_proximo = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'próxima')]"))
                    )
                    driver.execute_script("arguments[0].click();", botao_proximo)
                    time.sleep(random.uniform(5, 8))
                    pagina += 1
                except:
                    print("🚀 Não há mais páginas disponíveis ou erro ao navegar.")
                    break
            except Exception as e:
                print(f"⚠ Erro ao carregar a página {pagina}: {e}")
                print(f"HTML da página: {driver.page_source[:500]}")  # Mostra o HTML pra debug
                break

    driver.quit()
    print(f"✅ Coleta finalizada. Links salvos em '{arquivo_links}'")
    return links_coletados

if __name__ == "__main__":
    urls = obter_urls()
    print(f"Teste: {urls}")

## Desenvolvido por Enzo e Cesar Augusto- Ideia De Enzo Parra e Cesar
