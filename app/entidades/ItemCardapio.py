from dataclasses import dataclass


@dataclass
class ItemCardapio():
    
        id :int = None
        nome :str = None
        descricao :str = None
        preco :float = None
        disponivel :bool = None



        @property
        def preco_formatado(self):
            return f"R${self.preco}"
        



