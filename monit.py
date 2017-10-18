# Author: me
# email: to@me.kz
# Скрипт проверяет доступность ресурса из массива sitelist, в случае обнаружения предупреждений, пишет сообщение в телеграм и записывает в лог
#В каталоге, на котором размещен скрипт, необходимо создать еще один каталог "log" с правами записи
import requests, time, logging
from logging.handlers import TimedRotatingFileHandler

sitelist = [
    'http://site1.kz',
    'http://site2.kz',
    'http://site_n.kz'
]

logfilename = 'log/monitoring.log'
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN)
logger = logging.getLogger()
logformat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
loggerhandler = TimedRotatingFileHandler(logfilename, when="W6", backupCount=15)
loggerhandler.setFormatter(logformat)
logger.addHandler(loggerhandler)

url = 'https://api.telegram.org/{bot_id}/sendMessage'

def sitemonit():
    state = 0
    d = {}
    for s in sitelist:
        d[s]=0
    

    while True:

        for site in sitelist:
            try:
                r = requests.get(site, timeout=10, verify=False)
                #print('%s status code = %s' %(site, r.status_code))
                if r.status_code == 200:
                    if d[site] == 0:
                        # print('status = 0')
                        pass
                    else:
                        data = {'chat_id': {your chat id in telegram}, 'text': 'Подключение к %s восстановлена' %site}
                        d[site] = 0
                        logger.warn('Подключение к %s восстановлена' %site)
                        try:
                            requests.post(url=url, data=data)
                        except:
                            logger.error('Не могу отправить сообщение в Телеграм по веб ресурсу %s' %site)

                else:
                    logger.warn('Статус сайта %s не равен 200' %site)



            except:
                logger.error('С первой попытки не удалось подключиться к ресурсу %s. Жду 10 секунд, и заново проверю' %site)
                time.sleep(10)
                try:
                    r = requests.get(site, timeout=10, verify=False)
                    logger.warn('Уф! Со 2-ой попытки удалось подключиться к ресурсу %s.' % site)

                    if r.status_code== 200:
                        if d[site] != 0:
                            data = {'chat_id': {your chat id in telegram}, 'text': 'Подключение к %s восстановлена со второй попытки' % site}
                            d[site] = 0
                            logger.warn('Подключение к %s восстановлена со второй попытки' % site)
                            try:
                                requests.post(url=url, data=data)
                            except:
                                logger.error('Не могу отправить сообщение в Телеграм по веб ресурсу %s' % site)

                    else:
                        d[site] = 1
                        logger.error('В результате 2-проверки статус сайта %s не равен 200' % site)



                except:
                    if d[site] == 0:
                        d[site] = 1
                        data = {'chat_id': {your chat id in telegram}, 'text': 'Отсутствует подключение к %s' % site}

                        logger.error('Отсутствует подключение к %s' % site)
                        try:
                            requests.post(url=url, data=data)
                        except:
                            logger.error('Не могу отправить сообщение в Телеграм по веб ресурсу %s' % site)

                    logger.error('Даже со второй попытки ресурс %s не доступен.' % site)





        time.sleep(60)

def main():
    sitemonit()
if __name__ == '__main__':
    main()
