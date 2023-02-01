import time
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

campeoes_db = []
classe_db = []

def gravar(nome, hab, func, data_lancamento, ult_mudanca, essencia_azul, rp):
    f = open("campeoes.txt", "a")
    f.writelines('({}, {}, {}, {}, {}, {}, {})\n'.format(nome, hab, func, data_lancamento, ult_mudanca, essencia_azul, rp))
    f.close()

def gravarHab(nome, habilidade):
    f = open("hab_db_lol.txt", "a")
    f.writelines('({}, {})\n'.format(nome, habilidade))
    f.close()


def gravarClasse(nome, classe):
    f = open("classe_db_lol.txt", "a")
    try:
        classes = classe.split(',')
        for classe in classes:
            f.writelines('({}, {})\n'.format(nome, classe))
    except:
        f.writelines('({}, {})\n'.format(nome, classe))

    f.close()


navegador = webdriver.Chrome('chromedriver')
navegador.maximize_window()

action = ActionChains(navegador)

navegador.get('https://leagueoflegends.fandom.com/pt-br/wiki/Lista_de_campe%C3%B5es')

WebDriverWait(navegador, 100).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, 'tr')))
bloco = navegador.find_element(By.XPATH, '(//tbody)[2]')
campeoes = bloco.find_elements(By.TAG_NAME, 'tr')

for i in range(len(campeoes)):
    infos = campeoes[i].find_elements(By.TAG_NAME, 'td')
    nome = infos[0].get_attribute('data-sort-value')
    classe = infos[1].get_attribute('data-sort-value')

    gravarClasse(nome, classe)

    try:
        data_lancamento = infos[2].find_element(By.TAG_NAME, 'span')
        data_lancamento = data_lancamento.get_attribute("innerHTML")
    except:
        data_lancamento = infos[2].get_attribute("innerHTML")
        
    data_lancamento = data_lancamento.replace("\n", '')

    ult_mudanca = infos[3].find_element(By.TAG_NAME, 'span')
    ult_mudanca = ult_mudanca.get_attribute("innerHTML")

    essencia_azul = infos[4].get_attribute('innerHTML')
    essencia_azul = essencia_azul.replace("\n", "")

    try:
        rp = infos[5].find_element(By.TAG_NAME, 'span')
        rp = rp.get_attribute('innerHTML')
    except:
        rp = infos[5].get_attribute('innerHTML')
        
    rp = rp.replace("\n", '')
    
    campeoes_db.append([nome, data_lancamento, ult_mudanca, essencia_azul, rp])


navegador.switch_to.new_window('tab')
navegador.get('https://www.leagueoflegends.com/pt-br/champions/')


bloco = navegador.find_element(By.TAG_NAME, 'section')
secoes = bloco.find_elements(By.TAG_NAME, 'a')

func = ''
dificuldade = ''
for i in range(len(secoes)):

    WebDriverWait(navegador, 100).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'section')))
    bloco = navegador.find_element(By.TAG_NAME, 'section')
    #WebDriverWait(navegador, 100).until(EC.element_to_be_clickable((By.CLASS_NAME, 'style__Name-n3ovyt-2 cMGedC')))
    secoes = bloco.find_elements(By.TAG_NAME, 'a')

    action.move_to_element(secoes[i])

    secoes[i].click()

    WebDriverWait(navegador, 100).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-testid="overview:role"]')))
    
    n_bloco = navegador.find_element(By.TAG_NAME, 'ul')
    n_bloco = n_bloco.find_elements(By.TAG_NAME, 'li')

    map_div = n_bloco[0].find_elements(By.TAG_NAME, 'div')
    func = map_div[2].get_attribute('innerHTML')

    map_div = n_bloco[1].find_elements(By.TAG_NAME, 'div')
    dificuldade = map_div[2].get_attribute('innerHTML')

    navegador.back()

    campeoes_db[i].append(func)
    campeoes_db[i].append(dificuldade)

    time.sleep(3   )
    WebDriverWait(navegador, 100).until(EC.visibility_of_all_elements_located((By.TAG_NAME, 'section')))

    bloco = navegador.find_element(By.TAG_NAME, 'section')



for campeao in campeoes_db:
    gravar(campeao[0], campeao[1], campeao[2], campeao[3],
    campeao[4], campeao[5], campeao[6])
   



navegador.switch_to.new_window('tab')
navegador.get('https://leagueoflegends.fandom.com/pt-br/wiki/Lista_de_habilidades')
bloco = navegador.find_element(By.TAG_NAME, 'tbody')

linhas = navegador.find_elements(By.TAG_NAME, 'tr')

camp = ''
hab = ''
for i in range(len(linhas)):

    linha = linhas[i].find_elements(By.TAG_NAME, 'td')

    if len(linha) != 0:
        if len(linha) > 1:
            span = linha[1].find_element(By.TAG_NAME, 'span')
            camp = span.get_attribute('data-champion')
            hab = span.get_attribute('data-habilidade')
        else:       
            span = linha[0].find_element(By.TAG_NAME, 'span') 
            hab = span.get_attribute('data-habilidade')
        gravarHab(camp, hab)

                