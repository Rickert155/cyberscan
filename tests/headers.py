"""
Тестирование генераторов заголовков
"""
from cyberwarn.core.header import Headers

headers = Headers().create_headers()
print(headers)
