Шарипова Аделя, 11-904

- Для запуска необходимо загрузить фотографию с расширением `jpg` в `itis-2022-2023-vvot14-photos` 
- Обратиться к боту `vvot14_bot` с командой `/get_face`, которая предложит дать имя лицу 
- Командой `/find {name}` можно посмотреть фотографии с этим именем

### Используются:
- **Сервисные аккаунты:**
  - function-invoker-vvot14	
  - face-detection-vvot14	
  - face-cut-invoker-vvot14 
  - boot-function-vvot14 
  - api-gateway-vvot14 
  - face-cut-container-vvot14
- **Бакеты:**
  - itis-2022-2023-vvot14-faces
  - itis-2022-2023-vvot14-photos
- **База данных:**
  - vvot14-db-photo-face
- **Очередь:**
  - vvot14-tasks
- **Облачные функции:**
  - vvot14-boot
  - vvot14-face-detection
- **Триггеры:**
  - vvot14-task-trigger _(источник: vvot14-tasks)_
  - vvot14-photo-trigger _(источник: itis-2022-2023-vvot14-photos)_
- **Контейнер (+реестр):**
  - vvot14-face-cut
- **API-шлюз:**
  - api-gateway-vvot14