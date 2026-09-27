"""Rebinding a name and changing a shared object are different actions."""

import settings
from settings import labels, limit

settings.limit = 10
settings.labels.append("пример")

print("settings.limit:", settings.limit)
print("limit:", limit)
print("settings.labels:", settings.labels)
print("labels:", labels)
print("Один список:", labels is settings.labels)
