"""
Тестирование генераторов заголовков
"""
from cyberscan.header import Headers

headers = Headers().create_headers()
print(headers)
