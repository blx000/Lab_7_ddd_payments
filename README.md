# Lab 7 — Architecture, Layers & DDD-lite

Проект реализует упрощённую оплату заказа с разделением на слои и доменную модель.

## Структура
- **domain**: `Order`, `OrderLine`, `Money`, `OrderStatus` и бизнес-инварианты.
- **application**: use-case `PayOrderUseCase` и интерфейсы `OrderRepository`, `PaymentGateway`.
- **infrastructure**: `InMemoryOrderRepository` и `FakePaymentGateway`.
- **tests**: тесты use-case без базы данных.

## Инварианты домена
- нельзя оплатить пустой заказ
- нельзя оплатить заказ повторно
- после оплаты нельзя менять строки заказа
- итоговая сумма равна сумме строк

## Как запустить тесты
```bash
python3 -m pip install pytest
python3 -m pytest
