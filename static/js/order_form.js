// Ждем, пока весь HTML-документ будет загружен и разобран.
// Это стандартная практика, чтобы гарантировать, что все DOM-элементы доступны для манипуляций.
document.addEventListener("DOMContentLoaded", function () {
  // Находим выпадающий список мастеров и контейнер для чекбоксов услуг по их ID.
  const masterSelect = document.getElementById("id_master");
  const servicesContainer = document.getElementById("services-container");

  // Выполняем код, только если оба элемента найдены на странице.
  if (masterSelect && servicesContainer) {
    // Добавляем обработчик события, который сработает каждый раз, когда пользователь меняет выбранного мастера.
    masterSelect.addEventListener("change", function () {
      // Получаем ID выбранного мастера. 'this.value' ссылается на атрибут 'value' выбранного <option>.
      const masterId = this.value;

      // Если пользователь выбрал "пустой" вариант (например, "Выберите мастера..."), у которого нет value,
      // очищаем список услуг и показываем подсказку.
      if (!masterId) {
        servicesContainer.innerHTML =
          '<p class="text-muted">Выберите мастера, чтобы увидеть список услуг.</p>';
        return; // Прекращаем дальнейшее выполнение функции.
      }

      // Формируем URL для нашего API-эндпоинта. ID мастера добавляется к базовому URL.
      const url = `/ajax/services/${masterId}/`;

      // Используем современный Fetch API для выполнения асинхронного GET-запроса на сервер.
      fetch(url)
        .then((response) => {
          // Проверяем, успешен ли HTTP-ответ (статус в диапазоне 200-299).
          if (!response.ok) {
            // Если нет, создаем ошибку, которая будет перехвачена блоком .catch().
            throw new Error("Network response was not ok");
          }
          // Парсим JSON-тело ответа. Этот метод также возвращает Promise.
          return response.json();
        })
        .then((data) => {
          // Этот блок выполняется, когда JSON-данные успешно распарсены.
          // Сначала полностью очищаем контейнер от старых чекбоксов.
          servicesContainer.innerHTML = "";

          // Проверяем, есть ли в ответе услуги и не пустой ли массив.
          if (data.services && data.services.length > 0) {
            // Проходимся в цикле по каждому объекту услуги, полученному от сервера.
            data.services.forEach((service) => {
              // --- Создание чекбоксов, совместимых с Django ---
              // Чтобы корректно отправить данные для поля ManyToManyField с виджетом CheckboxSelectMultiple,
              // каждый <input type="checkbox"> должен иметь одинаковый атрибут 'name' (например, 'services')
              // и уникальный 'value' (ID услуги). При отправке формы браузер передаст
              // список всех выбранных ID услуг под ключом 'services'.

              // Создаем <div> для обертки чекбокса и его метки, чтобы соответствовать структуре Bootstrap.
              const div = document.createElement("div");
              div.className = "col-6 form-check";

              // Создаем сам элемент <input> для чекбокса.
              const input = document.createElement("input");
              input.type = "checkbox";
              // ВАЖНО: 'name' должен совпадать с именем поля в Django-форме ('services').
              input.name = "services";
              // 'value' будет первичным ключом (id) экземпляра модели Service.
              input.value = service.id;
              // Генерируем уникальный ID для самого input, чтобы связать его с <label>.
              input.id = `id_services_${service.id}`;
              input.className = "form-check-input";

              // Создаем <label> для чекбокса.
              const label = document.createElement("label");
              // Атрибут 'for' связывает метку с чекбоксом, улучшая доступность (клики по тексту метки).
              label.htmlFor = `id_services_${service.id}`;
              label.className = "form-check-label";
              label.textContent = service.name; // Отображаем название услуги.

              // Собираем конструкцию: добавляем <input> и <label> внутрь <div>.
              div.appendChild(input);
              div.appendChild(label);
              // Добавляем готовый элемент чекбокса в контейнер на странице.
              servicesContainer.appendChild(div);
            });
          } else {
            // Если у мастера нет услуг, отображаем сообщение.
            servicesContainer.innerHTML =
              '<p class="text-muted">У этого мастера нет доступных услуг.</p>';
          }
        })
        .catch((error) => {
          // Этот блок перехватывает ошибки из fetch-запроса (например, проблемы с сетью, ошибки сервера).
          console.error("Error fetching services:", error);
          // Отображаем сообщение об ошибке пользователю прямо в контейнере.
          servicesContainer.innerHTML =
            '<p class="text-danger">Не удалось загрузить услуги. Попробуйте позже.</p>';
        });
    });
  }
});