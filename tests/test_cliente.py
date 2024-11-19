from unittest.mock import patch
from clientet import verificar_msj


def test_msj_vacio():
    mensaje = ""
    assert not verificar_msj(mensaje)
    