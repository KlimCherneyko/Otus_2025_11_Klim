import logging

from appium.webdriver.common.appiumby import AppiumBy

TITLE_ID = "com.csdroid.pkg:id/tv_title"
CALENDAR_NAMES = ("Календарь", "Calendar")
MAX_SWIPES = 25

logger = logging.getLogger(__name__)


class CalendarNotFoundError(Exception):
    """Элемент «Календарь» не найден до конца списка."""


def test_open_calendar(driver, report):
    previous_names: list[str] | None = None

    for swipe_num in range(MAX_SWIPES):
        elements = driver.find_elements(AppiumBy.ID, TITLE_ID)
        if len(elements) < 2:
            raise CalendarNotFoundError(
                f"В списке недостаточно элементов для свайпа "
                f"(найдено {len(elements)}, нужно минимум 2)"
            )

        element_names = [el.text for el in elements]
        logger.info("Свайп %s, видимые приложения: %s", swipe_num, element_names)

        for name in CALENDAR_NAMES:
            if name in element_names:
                target = next(el for el in elements if el.text == name)
                target.click()
                logger.info("Найден и открыт: %s", name)
                return

        if previous_names is not None and element_names == previous_names:
            raise CalendarNotFoundError(
                "Достигнут конец списка, приложение «Календарь» не найдено. "
                f"Последние видимые: {element_names}"
            )

        previous_names = element_names
        driver.swipe(
            elements[1].rect["x"],
            elements[1].rect["y"],
            elements[0].rect["x"],
            elements[0].rect["y"],
        )

    raise CalendarNotFoundError(
        f"«Календарь» не найден за {MAX_SWIPES} свайпов"
    )
