2024-04-10
Выезд на объект. 
Цель: обновление контроллера до micropython v1.22.2 + kraxlib v1.0.5 + pyplc v0.1.7 + concrete v0.1.1
Снял контроллер, 2 аналоговых модуля (заменил на новые)
Прошивку из контроллера скачал 2мя частями (bootloader+micropython) image0x1000.bin и (vfs) image0x200000.bin
Восстановить:
python -m esptool --chip esp32 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 4MB --flash_freq 80m 0x1000 build/image0x1000.bin
python -m esptool --chip esp32 -b 460800 --before default_reset --after hard_reset write_flash --flash_mode dio --flash_size 4MB --flash_freq 80m 0x200000 build/image0x200000.bin
