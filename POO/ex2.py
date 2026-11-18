from functools import singledispatchmethod
from multipledispatch import dispatch
class Processar_alerta:
    def __init__(self, alerta):
        self.alerta = alerta

    def analisar (self):
        # Lógica para analisar o alerta
        print(f"Analisando alerta sem classe : {self.alerta}")


#Alerta banco e sua subclasse Alerta_itau, que herda de Alerta_banco, que por sua vez herda de Processar_alerta.
class Alerta_banco(Processar_alerta):
    def __init__(self, alerta , nome_banco : str = "Banco"):
        super().__init__(alerta)
        self.nome = nome_banco
    def analisar(self):
        # Lógica para analisar o alerta específico do banco
        print(f"Analisando alerta do banco {self.nome}: {self.alerta}")

class Alerta_itau(Alerta_banco): #subclasse específica para o banco Itaú herda da classe Alerta_banco
    def __init__(self, alerta):
        super().__init__(alerta, nome_banco="Itaú")
    def analisar(self):
        # Lógica para analisar o alerta específico do Itaú
        print(f"Analisando alerta do Itaú : {self.alerta} com informações adicionais do banco Itaú.")



class Alerta_loja(Processar_alerta):
    def __init__(self, alerta, nome_loja: str = "Loja do zé "):
        super().__init__(alerta)
        self.nome = nome_loja
    def analisar(self):
        # Lógica para analisar o alerta específico da loja
        print(f"Analisando alerta da loja {self.nome}: {self.alerta}")

"""Daqui pra frente o polimorfismo séra com overloading, que é quando uma classe tem métodos com o mesmo nome, mas com diferentes assinaturas (número ou tipo de parâmetros). Isso permite que a mesma operação seja realizada de maneiras diferentes, dependendo dos argumentos fornecidos. """

class Processar_alerta_overloading:
    
    @singledispatchmethod
    def analisar(self, alerta):
        print(f" {alerta} Nao é um objeto de alerta válido para análise.")

    @analisar.register
    def _(self, obj_alerta: Alerta_banco):
        print(f"Analisando alerta do banco: {obj_alerta.alerta}")

    @analisar.register
    def _(self, obj_alerta: Alerta_itau):
        print(f"Analisando alerta do Itaú: {obj_alerta.alerta}")

    @analisar.register
    def _(self, obj_alerta: Alerta_loja):
        print(f"Analisando alerta da loja: {obj_alerta.alerta}")


#usando multipledispatch para criar métodos com o mesmo nome, mas com diferentes assinaturas (número ou tipo de parâmetros). Isso permite que a mesma operação seja realizada de maneiras diferentes, dependendo dos argumentos fornecidos.

    @dispatch(str,int)
    def relatorio(self, nome:str, paginas:int):
        print(f"Gerando relatório para {nome} com  {paginas} paginas")

    @dispatch(str,int,bool)
    def relatorio(self, nome:str, paginas:int, status:bool):
        print(f"Gerando relatório para {nome} com {paginas} páginas. Status: {'ENTREGUE' if status else 'PENDENTE'}")

print("=== 1. TESTANDO HERANÇA E OVERRIDE (Polimorfismo Clássico) ===")
    
alerta_geral = Processar_alerta("CPU em 95%")
alerta_geral.analisar()

alerta_banco = Alerta_banco("Tentativa de login suspeita", "Banco Central")
alerta_banco.analisar()

alerta_itau = Alerta_itau("Transação PIX estornada")
alerta_itau.analisar()  # Vai rodar o método específico do Itaú

alerta_loja = Alerta_loja("Estoque crítico de celular")
alerta_loja.analisar()

print("\n" + "="*50 + "\n")
print("=== 2. TESTANDO SINGLE DISPATCH METHOD (Sobrecarga por Tipo) ===")
    
processador_ov = Processar_alerta_overloading()
try:
    # Passando objetos de tipos diferentes para o mesmo método 'analisar'
    processador_ov.analisar(alerta_banco) # Deve cair no dispatch de Alerta_banco
    processador_ov.analisar(alerta_itau)  # Deve cair no dispatch de Alerta_itau
    processador_ov.analisar(alerta_loja)  # Deve cair no dispatch de Alerta_loja
        
    # Testando a rota padrão (fallback) com um tipo não mapeado
    processador_ov.analisar("NO FUNDO DO MAR")  # Deve disparar erro padrão

    print("\n" + "="*50 + "\n")
    print("=== 3. TESTANDO MULTIPLE DISPATCH (Sobrecarga por Múltiplos Parâmetros) ===")

    # Testando a versão do método relatorio com 2 parâmetros (str, int)
    processador_ov.relatorio("Relatório de Fraudes", 15)

    # Testando a versão do método relatorio com 3 parâmetros (str, int, bool)
    processador_ov.relatorio("Relatório de Acessos", 8, True)
    processador_ov.relatorio("Relatório de Erros", 3, False)

except Exception as e:
    print(f"Erro durante a execução: {e}")