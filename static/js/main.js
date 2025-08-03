const AUTO_HIDE_DELAY = 5000;

document.addEventListener("DOMContentLoaded", function () {
  /* Плавный скролл по якорям */
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href");
      const targetElement = document.querySelector(targetId);

      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  /* Логика для автоматического скрытия уведомлений (alerts) */
  const alertElements = document.querySelectorAll(".alert");
  alertElements.forEach(function (element) {
    // Устанавливаем таймер для закрытия через 5 секунд (5000 миллисекунд)
    setTimeout(function () {
      // Получаем экземпляр Alert и вызываем метод close()
      const alertInstance = bootstrap.Alert.getOrCreateInstance(element);
      alertInstance.close();
    }, AUTO_HIDE_DELAY);
  });
});