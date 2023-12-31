# PPP_PAI_OiRPOS
Projekt zrealizowany w ramach przedmiotów na Politechnice Śląskiej.

## Co to jest?
Projekt aplikacji internetowej działającej na aplikacji na ASP.Net łączącej się z serwerem aplikacji Flask, która umożliwia uruchomienie wykrywania obiektów na obrazach.

## Jak użyć?
1. Zainstaluj python3
1. Zainstaluj CUDA ``` https://developer.nvidia.com/cuda-downloads ```
1. Pobierz repozytorium
1. Zainstaluj wymagania ``` pip install -r requirements.txt  ```
1. Uruchom aplikacje flask ``` python3 ./Flask/flask.py ```
1. Uruchom aplikacje ASP.NET:
   - WINDOWS: ``` ASPNET/PPP_PAI_OiRPOS.exe ```
   - LINUX: 
	```
		chmod 777 PPP_PAI_OiRPOS
		./PPP_PAI_OiRPOS
	```
1. W przeglądarce internetowej przejść pod adress: ``` 127.0.0.1:5000 ```

## Jak działa?
Są 2 serwery http, ASP.NET działający jako komunikator z użytkownikiem. Drugi Flask działający jako usługa dla pierwszego serwera aby udostępnić możliwośi skryptów działających na sieci YOLOv8 do wykrywania oraz Histogram Based Outliner Score dla wykrytych obrazów.
