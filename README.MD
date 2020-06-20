# LOTTO

[![N|Solid](https://gry.lotto.pl/etc/designs/interactive/ilottery/common/home/images/lottery-logo-w-bg.png)](https://nodesource.com/products/nsolid)

## Projekt zaliczeniowy stworzony na potrzeby przedmiotu Programowanie aplikacji sieciowych
### Autorzy: Piotr Małek, Łukasz Lipiński


### Opis aplikacji
Użytkownik aby mógł korzystać z wszystkich funkcji musi przede wszystkim utworzyć konto (przycisk **Zarejestruj się**). Po zarejestrowaniu się, musi zalogować się do systemu (przycisk **Zaloguj**). Tam najsampierw zobligowany jest do doładowania konta (zakładka **Moje konto**) w celu możliwości stworzenia kuponu kosztującego 5 złotych, umożliwiającego wzięcie udział w losowaniu, którego główna nagroda często przekracza kilka milionów złotych. Aby to zrobić, należy przejść do zakładki **Kup los** i wytypować sześć różnych liczb z przedziału od 1 do 49. Po zatwierdzeniu kuponu, użytkownik musi czekać do losowania w którym zostaną podane zwycięskie liczby. Informacja o godzinie losowania, puli głównej nagrodny, a także historii losowań znajdują się w zakładce **Wyniki Lotto**. Jeżeli losowanie na które użytkownik się odbyło, a zwycięskie liczby znajdowały się na jego kuponie, wygrana zostanie dopisana do jego salda, które sprawdzić może w zakładce **Moje konto**.
#### Możliwe wygrane
*Ilość trafionych liczb* | `Wygrana`
- | --- |
3 | `100 zł`
4 | `1 000 zł`
5 | `10 000 zł`
6 | `min. 1 000 000 zł`
Jeżeli w losowaniu nie padła najwyższa wygrana, pula powięszkona o milion przechodzi do kolejnego losowania.

## Zastosowane funkcjonalności:
- ### możliwa obsługa wielu użytkowników jendocześnie
- ### synchronizacja wątków
- ### zastosowanie asynchroniczności
- ### połączenie szyfrowane
