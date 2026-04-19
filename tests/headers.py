"""
Тестирование генераторов заголовков
"""
from cyberscan.core.header import Headers

headers = Headers().create_headers()
print(headers)
