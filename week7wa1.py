# -*- coding: utf-8 -*-

import requests

r = requests.post("https://service-dev.sunday.dk/gateway/v4/homes-for-sale-search", data= {"filters":{},"sort":"salesPeriodAsc","pageSize":500,"returnViewport":"true"})

print(r.status_code, r.reason)

print(r.text)


