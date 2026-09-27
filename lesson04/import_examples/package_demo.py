"""Import a package, then one of its submodules, in a fresh interpreter."""

import urllib

print("После import urllib:", hasattr(urllib, "parse"))

from urllib import parse

print("После from urllib import parse:", hasattr(urllib, "parse"))
print("Один подмодуль:", parse is urllib.parse)
print(parse.urlsplit("https://example.org/books?page=2").path)
