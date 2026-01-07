@echo off
title Telegram Bot (auto-reload)

echo Starting bot with auto-reload...
echo Press Ctrl+C to stop
echo.

:: Запускаем watchfiles
:: "py -m app.main" -> команда запуска бота
:: app -> папка, за которой следим
:: --ignore-paths -> папка, которую игнорируем (где лежит база данных)

py -m watchfiles "py -m app.main" app --ignore-paths "app/data"