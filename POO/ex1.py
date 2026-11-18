from abc import ABC, abstractmethod

class DispositivoRede(ABC):
    """Classe abstrata que representa um dispositivo de rede com funcionalidades básicas.
    Feito para testar os pilares de POO: Abstração, Herança e Encapsulamento (@property).

    explixaçao:

    @property: Permite que métodos sejam acessados como atributos, promovendo encapsulamento e controle sobre o acesso a dados.
    @nome.setter: Permite definir o valor de um atributo de forma controlada, garantindo que as regras de validação sejam aplicadas.

    super().__init__(): Chama o construtor da classe base (DispositivoRede) para inicializar atributos herdados, garantindo que a inicialização seja consistente em toda a hierarquia de classes.
    porem tambem pode ser usado para chamar métodos da classe base, permitindo que a subclasse estenda ou modifique o comportamento da classe base.
    exemplo: super().metodo_da_classe_base() chama um método da classe base a partir de uma subclasse, permitindo que a subclasse utilize ou modifique o comportamento definido na classe base.

    objeto.bateria = valor: Utiliza o setter definido para o atributo 'bateria', permitindo que o valor seja definido de forma controlada, aplicando validações e encapsulamento.
    """
    def __init__(self,nivel_bateria):
        self.bateria = nivel_bateria

    @abstractmethod
    def diagnostico(self):
        pass

    def conectar(Self):
        print("Conectando ao dispositivo de rede...")

    @property
    def bateria(self):
        return self._bateria

    @bateria.setter
    def bateria(self, nivel_bateria):
        if nivel_bateria < 0 or nivel_bateria > 100:
            raise ValueError("O nível de bateria deve estar entre 0 e 100.")
        self._bateria = nivel_bateria


class Roteador(DispositivoRede):
    def __init__(self, nivel_bateria):
        super().__init__(nivel_bateria)

    def diagnostico(self):
        print("Realizando diagnóstico do roteador...")
        if self.bateria < 20:
            print("Bateria baixa! Roteador será desligado em breve.")
        else:
            print("Roteador funcionando normalmente.")


class Firewall(DispositivoRede):
    def __init__(self, nivel_bateria):
        super().__init__(nivel_bateria)

    def diagnostico(self):
        print("Realizando diagnóstico do firewall...")
        if self.bateria < 20:
            print("Bateria baixa! Firewall será desligado em breve.")
        else:
            print("Firewall funcionando normalmente.")


print("Teste do Roteador:")
roteador = Roteador(50)
roteador.conectar()
roteador.diagnostico()

print("\nTeste do Firewall:")
firewall = Firewall(10)
firewall.conectar()
firewall.diagnostico()

print("\nTeste de bateria inválida/valida:")

try:
    dispositivo_invalido = Roteador(90)
    print(f"Nível de bateria válido: {dispositivo_invalido.bateria}")
    print("Tentando definir nível de bateria inválido...")
    roteador.bateria = 150  # Nível de bateria inválido
except ValueError as e:
    print(f"Erro: {e}")