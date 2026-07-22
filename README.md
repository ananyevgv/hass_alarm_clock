# ⏰ Alarm Clock — Будильник для Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
![version](https://img.shields.io/badge/version-1.0.0-blue)
![HA](https://img.shields.io/badge/Home%20Assistant-2023.1+-green)
![license](https://img.shields.io/badge/license-MIT-lightgrey)

Пользовательская интеграция для Home Assistant, добавляющая многофункциональные будильники с гибким расписанием, повторением по дням недели и детальными состояниями для построения сложных автоматизаций пробуждения.

---

## ✨ Возможности

- 🔔 **Несколько будильников** — создавайте неограниченное количество будильников
- 📅 **Выбор дней недели** — гибкое расписание на любой день
- ⏸️ **Временное отключение** — отключайте будильники на время отпуска без потери настроек
- 📊 **Детальные состояния** — 7 этапов будильника для точных автоматизаций
- 🌐 **Полная интеграция с HA** — работает со всеми сервисами и автоматизациями

---

## 📊 Этапы будильника

При достижении времени будильника сенсор последовательно проходит через следующие состояния:


| Состояние | Значение |
|-----------|----------|
| `off` | Будильник не активен |
| `minus_30` | За 30 минут до будильника |
| `minus_20` | За 20 минут до будильника |
| `minus_10` | За 10 минут до будильника |
| `on` | Время будильника наступило |
| `plus_10` | Через 10 минут после будильника |
| `plus_20` | Через 20 минут после будильника |
| `plus_30` | Через 30 минут после будильника |

---

## 📸 Превью

<div style="display: flex; gap: 10px; flex-wrap: wrap;">
  <img src="https://user-images.githubusercontent.com/159124/139574325-837db96c-6658-4db8-a0f0-758d95231d62.png" style="width: 430px; height: auto; border-radius: 8px;" />
  <img src="https://user-images.githubusercontent.com/159124/139574331-e91f2b73-8c6a-4500-bc20-13d017189385.png" style="width: 430px; height: auto; border-radius: 8px;" />
</div>

---

## 📦 Установка

### Способ 1 — HACS (рекомендуется)

**Шаг 1:** Добавьте пользовательский репозиторий в HACS:

[![Открыть репозиторий в HACS](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=ananyevgv&repository=alarm-clock&category=integration)

> Если кнопка не работает, добавьте вручную:
> **HACS → Интеграции → ⋮ → Пользовательские репозитории**
> → URL: `https://github.com/ananyevgv/alarm-clock` → Тип: **Интеграция** → Добавить

**Шаг 2:** Найдите **Alarm Clock** → **Установить**

**Шаг 3:** Перезапустите Home Assistant

---

### Способ 2 — Ручная установка

1. Скачайте [последний релиз](https://github.com/ananyevgv/alarm-clock/releases/latest)
2. Скопируйте папку `alarm_clock` в `/config/custom_components/`
3. Перезапустите Home Assistant

---

## 🚀 Настройка

### Через интерфейс (UI)

1. Перейдите в **Настройки → Устройства и сервисы**
2. Нажмите **➕ Добавить интеграцию**
3. Найдите **Alarm Clock**
4. Следуйте инструкциям мастера настройки

### Вручную (configuration.yaml)

```yaml
# configuration.yaml
alarm_clock:
  alarms:
    - name: "Утренний"
      time: "07:00"
      days:
        - mon
        - tue
        - wed
        - thu
        - fri
      enabled: true
    - name: "Выходной"
      time: "09:30"
      days:
        - sat
        - sun
      enabled: true

### 🎯 Примеры автоматизаций

## Плавное пробуждение со светом

За 20 минут до будильника начинаем медленно увеличивать яркость света:

```yaml
automation:
  - alias: "🌅 Плавное пробуждение"
    trigger:
      - platform: state
        entity_id: sensor.alarm_clock_state
        to: "minus_20"
    action:
      - service: light.turn_on
        target:
          entity_id: light.bedroom_lamp
        data:
          brightness: 50
          transition: 60

## Полное пробуждение (свет + музыка)

```yaml
automation:
  - alias: "🎵 Полное пробуждение"
    trigger:
      - platform: state
        entity_id: sensor.alarm_clock_state
        to: "on"
    action:
      - service: light.turn_on
        target:
          entity_id: light.bedroom_lamp
        data:
          brightness: 255
      - service: media_player.play_media
        target:
          entity_id: media_player.bedroom_speaker
        data:
          media_content_id: "https://example.com/morning_playlist.m3u"
          media_content_type: "playlist"
