"""EXERCICIO PARA TESTAR DUCK_TYPING"""


class modoinvasao:
    def executar_protocolo(self) -> str:
        return "Executando protocolo de invasão."

class ModoDefesaPassiva:
    def executar_protocolo(self) -> str:
        return "Executando protocolo de defesa passiva."

class ModoSimulacaoLab:
    def executar_protocolo(self) -> str:
        return "Executando protocolo de simulação em laboratório."


print("TESTANDO CLASSES DE MODO DE OPERAÇÃO")

def testar_modo_operacao(modo_operacao):
    resultado = modo_operacao.executar_protocolo()
    print(f"Resultado do protocolo: {resultado}")

m1 = modoinvasao()
m2 = ModoDefesaPassiva()
m3 = ModoSimulacaoLab()

list = [m1, m2, m3]
for modo in list:
    testar_modo_operacao(modo)
