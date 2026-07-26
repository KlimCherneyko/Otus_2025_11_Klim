# Jenkins (ДЗ-11)

Кастомный образ: `jenkins/jenkins:lts` + Python 3 (venv) для прогона тестов из `dz/`.

## 1. Инфраструктура (одна машина)

Подставь свой LAN IP вместо `<LOCAL_IP>` (например `192.168.2.143`).  
OpenCart занимает `:8080` → Jenkins на `:8082`.

### Selenoid (если ещё не запущен)

```bash
mkdir -p ~/selenoid
# browsers.json с chrome 120.0 → скопируй из dz/selenoid/browsers.json

docker network create selenoid   # если ещё нет

docker run -d --name selenoid \
  --network selenoid -p 4444:4444 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v ~/selenoid/browsers.json:/etc/selenoid/browsers.json:ro \
  aerokube/selenoid:latest-release \
  -container-network selenoid

docker run -d --name selenoid-ui \
  --network selenoid -p 8090:8080 \
  aerokube/selenoid-ui:1.10.11 \
  --selenoid-uri http://selenoid:4444
```

### OpenCart

```bash
cd dz
PHPADMIN_PORT=8081 OPENCART_PORT=8080 LOCAL_IP=<LOCAL_IP> docker compose up -d phpadmin mariadb opencart
```

### Jenkins

```bash
# из корня репозитория
docker build -t otus-jenkins ./jenkins

docker run -d --name jenkins \
  --network selenoid \
  -p 8082:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  otus-jenkins
```

- UI: http://localhost:8082  
- Initial password:

```bash
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## 2. Плагины и Allure

1. Установи плагины: **Pipeline**, **Git**, **Allure**.
2. **Manage Jenkins → Tools → Allure Commandline** → Add Allure Commandline  
   - Name: `allure`  
   - Install automatically (или путь к установленному Allure).

## 3. Pipeline job

1. **New Item** → Pipeline → OK.
2. Отметь **This project is parameterized** (параметры подтянутся из `Jenkinsfile` после первого скана SCM; либо сразу From SCM).
3. **Pipeline** → Definition: **Pipeline script from SCM**.
4. SCM: **Git**  
   - Repository URL: `https://github.com/KlimCherneyko/Otus_2025_11_Klim.git`  
   - Branch: `*/dz-11` (или ветка PR)  
   - Script Path: `Jenkinsfile`
5. Save → **Build with Parameters**.

Параметры джобы (из ДЗ):

| Параметр | Пример |
|----------|--------|
| `SELENOID_URL` | `http://selenoid:4444/wd/hub` |
| `OPENCART_URL` | `http://<LOCAL_IP>:8080` |
| `BROWSER` | `chrome` |
| `BROWSER_VERSION` | `120.0` |
| `THREADS` | `2` |

## 4. Сдача

- Лог сборки Jenkins.
- Скрин: Jenkins + открытая джоба с видимыми параметрами.
- Скрин: выполненный прогон + Allure Report.
- PR с `Jenkinsfile` (и связанными файлами).
