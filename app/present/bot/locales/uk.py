START_MESSAGE = (
    "Привіт, {name}!\n"
    "Я бот, який допоможе тобі відстежувати твої вхідні транзакції в BSC.\n"
    "Для початку роботи, тобі потрібно надіслати адресу свого гаманця.\n"
)

SEND_WALLET_ADDRESS_BUTTON = "Надіслати адресу гаманця"

WALLET_INPUT_MESSAGE = (
    "Відправ мені адресу свого гаманця, щоб я міг відстежувати твої вхідні транзакції.\n"
    "Адреса гаманця повинна починатися з 0x."
)
WALLET_INPUT_ERROR_MESSAGE = (
    "Неправильний формат адреси гаманця.\n"
    "Надішли мені адресу гаманця, щоб я міг відстежувати твої вхідні транзакції.\n"
)
WALLET_INPUT_SUCCESS_MESSAGE = "Гаманець успішно додано.\n"

SETTINGS_MESSAGE = "Тут ти можеш налаштувати бота.\n"

TRANSACTION_BUTTON = "Транзакція {short_hash}\n"

TRANSACTION_LIST_MESSAGE = "Список транзакцій:\n"

TRANSACTION_MESSAGE = (
    "Транзакція: {hash}\n"
    "Кількість: {amount_in_bnb} BNB({amount_in_usd}$))\n"
    "Тип: {type}\n"
    "Дата: {date}\n"
    "Статус: {status}\n"
)
TYPE_TO_UK = {
    "deposit": "Депозит",
    "withdraw": "Виведення",
    "mint": "Мінт",
    "approve": "Апрув",
    "other": "Інша транзакція",
}
STATUS_TO_UK = {
    "success": "Успішно",
    "error": "Помилка",
}
