import os
import torch
import torch.nn as nn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# =====================================================================
# BLOCO 1: INFRAESTRUTURA MATEMÁTICA E VALORES HISTÓRICOS DA IA
# =====================================================================

# RELEMBRANDO A RÉGUA HISTÓRICA: Fixamos a média e o desvio padrão exatos
# calculados no banco de dados original (as 5 casas de treinamento).
# Sem esses valores imutáveis salvos, o nosso "tradutor" de normalização falha.
X_MEDIA_HISTORICA = torch.tensor([94.0000, 10.6000], dtype=torch.float32)
X_DESVIO_HISTORICO = torch.tensor([40.2181, 12.3410], dtype=torch.float32)

# Definimos o arquivo de pesos binários que o algoritmo aprendeu
ARQUIVO_MODELO = "modelo_valoracao_casas.pt"

# PASSO DE PRODUÇÃO: Criamos o esqueleto vazio do modelo profissional.
# Ele mapeia as 4 colunas de entrada [Área, Idade, Centro, Praia] para 1 saída (Preço).
modelo_api = nn.Linear(in_features=4, out_features=1)

# VERIFICAÇÃO DE SEGURANÇA: O servidor só pode subir se o arquivo de pesos existir
if not os.path.exists(ARQUIVO_MODELO):
    raise FileNotFoundError(
        f"🚨 ERRO CRÍTICO: O arquivo '{ARQUIVO_MODELO}' não foi encontrado na pasta atual! "
        f"Certifique-se de executar a célula de salvamento do seu Jupyter Notebook antes."
    )

# Carregamos os pesos ideais descobertos no treino e injetamos no esqueleto vazio
modelo_api.load_state_dict(torch.load(ARQUIVO_MODELO))

# TRAVA DE PRODUÇÃO (.eval()): Congela os pesos em modo de avaliação pura.
# Desativa cálculos de gradiente e retropropagação, garantindo velocidade e estabilidade na nuvem.
modelo_api.eval()


# =====================================================================
# BLOCO 2: PADRONIZAÇÃO E VALIDAÇÃO DA ENTRADA DO CLIENTE
# =====================================================================
# Instanciamos o aplicativo FastAPI principal para roteamento web
app = FastAPI(
    title="API Corporativa de Valoração de Imóveis (PyTorch)",
    description="Interface de alta performance para estimativa de preços imobiliários.",
    version="1.0.0"
)

# Criamos o contrato de dados usando Pydantic. 
# Se o cliente web enviar dados corrompidos ou tipos errados, a API bloqueia o request.
class DadosImovel(BaseModel):
    area: float = Field(..., description="Área construída em m²", examples=[100.0])
    idade: float = Field(..., description="Idade do imóvel em anos", examples=[10.0])
    bairro: str = Field(..., description="Bairro do imóvel. Opções válidas: 'Centro' ou 'Praia'", examples=["Praia"])


# =====================================================================
# BLOCO 3: A ROTA DE PREVISÃO EM TEMPO REAL (O CORAÇÃO DA API)
# =====================================================================
# Rota do tipo POST: O cliente envia uma carga JSON e recebe uma resposta calculada.
@app.post("/prever-preco", summary="Estima o preço justo de mercado do imóvel solicitado")
def prever_preco(imovel: DadosImovel):
    
    # 1. TRATAMENTO DE TEXTO (ONE-HOT ENCODING) NA UNHA
    # Padronizamos o texto para minúsculas removendo espaços em branco extras
    bairro_texto = imovel.bairro.strip().lower()
    
    # Mapeamos o texto para as duas colunas binárias criadas no treino: [É_Centro, É_Praia]
    if bairro_texto == "centro":
        vetor_bairro = [1.0, 0.0]
    elif bairro_texto == "praia":
        vetor_bairro = [0.0, 1.0]
    else:
        # Se o cliente tentar injetar um bairro inexistente, devolvemos erro HTTP 400 (Bad Request)
        raise HTTPException(status_code=400, detail="Bairro inválido. Escolha estritamente entre 'Centro' ou 'Praia'.")
        
    # 2. MONTAGEM E NORMALIZAÇÃO DOS TENSORES
    # Capturamos os dados numéricos enviados na requisição web
    dados_numericos_brutos = torch.tensor([[imovel.area, imovel.idade]], dtype=torch.float32)
    
    # Traduzimos para a escala correta dividindo pela régua histórica imutável
    dados_numericos_normalizados = (dados_numericos_brutos - X_MEDIA_HISTORICA) / X_DESVIO_HISTORICO
    
    # Convertemos o vetor de texto binário em um tensor PyTorch
    tensor_bairro = torch.tensor([vetor_bairro], dtype=torch.float32)
    
    # Concatenamos as colunas numericas e categóricas formando a matriz de 4 colunas:
    # [Área_Normalizada, Idade_Normalizada, É_Centro, É_Praia]
    entrada_final_ia = torch.cat((dados_numericos_normalizados, tensor_bairro), dim=1)
    
    # 3. EXECUÇÃO DO PROCESSO MENTAL DA IA
    with torch.no_grad():
        # Jogamos a matriz tratada dentro do nosso modelo de produção carregado
        resultado_tensor = modelo_api(entrada_final_ia)
        
    # Convertemos o resultado do tensor (milhares) para Reais brutos legíveis
    preco_final_reais = resultado_tensor.item() * 1000
    
    # 4. ENTREGA DA RESPOSTA (JSON OUTPUT)
    return {
        "status": "sucesso",
        "dados_solicitados": {
            "area_m2": imovel.area,
            "idade_anos": imovel.idade,
            "bairro": imovel.bairro
        },
        "preco_estimado_reais": round(preco_final_reais, 2),
        "mensagem": "Cálculo efetuado com sucesso via motor PyTorch v2.x congelado."
    }


# =====================================================================
# BLOCO 4: INICIALIZAÇÃO INDEPENDENTE DO SERVIDOR UVICORN
# =====================================================================
# Este bloco protege a execução do script. Ele garante que o arquivo só abra o servidor
# se for executado diretamente pelo terminal (python main.py), evitando travamentos.
if __name__ == "__main__":
    import uvicorn
    
    # Definimos a porta alta 8080 para evitar qualquer barreira do seu firewall UFW
    PORTA_PRODUCAO = 8080
    
    print("\n==========================================================")
    print("        🚀 SERVIDOR INDEPENDENTE DE PRODUÇÃO INICIADO      ")
    print("==========================================================")
    print(f"🔗 ACESSE A INTERFACE DE TESTES: http://127.0.0.1:{PORTA_PRODUCAO}/docs")
    print("==========================================================\n")
    
    # Disparamos o Uvicorn de forma limpa, apontando para o app deste arquivo ("main:app")
    # O parâmetro 'reload=True' atualiza a API automaticamente se você alterar o código
    uvicorn.run("main:app", host="127.0.0.1", port=PORTA_PRODUCAO, reload=True)
