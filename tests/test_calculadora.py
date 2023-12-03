import pytest
from src.calculadora import Calculadora

def test_soma():
    soma = Calculadora.soma(1.2,2)
    assert soma == 3.2
    assert type(soma) == float
    
def test_subtracao():
    subtracao = Calculadora.subtracao(5,20)
    assert subtracao == -15
    assert type(subtracao) == float