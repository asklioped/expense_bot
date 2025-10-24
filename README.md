# Телерам бот з підрахунку витрачених коштів

## Встаовлення на Debian
```bash
# Встановіть віртуальне оточення Python
sudo apt install python3-venv

# Встановіть GIT та перейдіть у директорію /opt
sudo apt install git
cd /opt

# Клонуйте репозиторій та перейдіть у директорію проекту
sudo git clone https://github.com/asklioped/expense_bot.git
cd /opt/expense_bot

# Встановіть віртуальне оточення
sudo python3 -m venv venv

# Змініть права на поточного користувача
chown -R $USER:$USER /opt/expense_bot

# Увімкніть віртуальне середовище
source venv/bin/activate

# Встановіть залежності
pip install -r reqirements.txt

# Створіть файл .env та вкладіть у нього
# BOT_TOKEN = 
# DEBUG=True

# Створіть системний сервіс 
sudo nano /etc/systemd/system/expensebot.service
# З таким вмістом:
#            [Unit]
#			Description=Expense Tracker Telegram Bot
#			After=network.target
#
#			[Service]
#			# Вкажи користувача, від імені якого запускати (не root)
#			User=debian
#			WorkingDirectory=/opt/expense_bot
#			# Активуємо віртуальне середовище та запускаємо бота
#			ExecStart=/opt/expense_bot/venv/bin/python /opt/expense_bot/bot.py
#			Restart=always
#			RestartSec=5
#			# Щоб логи писались у journalctl
#			StandardOutput=journal
#			StandardError=journal
#
#			[Install]
#			WantedBy=multi-user.target

# Запустіть сервіс
sudo systemctl daemon-reload
sudo systemctl enable expensebot
sudo systemctl start expensebot












