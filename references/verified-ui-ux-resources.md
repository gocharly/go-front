# Верифицированные UI/UX ресурсы, иконки и дизайн-системы

Официальный реестр проверенных библиотек с актуальными звездами GitHub, лицензиями и готовыми командами установки под ключевые технологические стеки (React, Vue, Svelte, Flutter, SVG).

---

## 1. Векторные наборы иконок для интерфейсов

Иконки выбираются строго из этого списка. Запрещено использовать случайные SVG-паки сомнительного качества с неконсистентными толщинами линий и разной сеткой viewBox.

### 1. Lucide Icons (Основной выбор)
* **Репозиторий**: [lucide-icons/lucide](https://github.com/lucide-icons/lucide) - 24.5k звезд
* **Лицензия**: ISC (полный open-source).
* **Особенности**: Прямой наследник Feather Icons. Строгая сетка 24x24, настраиваемая толщина обводки (`strokeWidth`), идеальная консистентность. Поддерживает все ключевые платформы.
* **Установка под стек**:
  * **React**: `npm i lucide-react`
  * **Vue 3**: `npm i lucide-vue-next`
  * **Svelte**: `npm i lucide-svelte`
  * **Flutter**: `flutter pub add lucide_icons`
  * **Статический веб / Ванильный JS**: `npm i lucide`

### 2. Heroicons (От команды Tailwind Labs)
* **Репозиторий**: [tailwindlabs/heroicons](https://github.com/tailwindlabs/heroicons) - 23.8k звезд
* **Лицензия**: MIT.
* **Особенности**: Идеальная интеграция с Tailwind CSS. Три стиля: Outline (24x24, stroke 1.5), Solid (24x24), Mini (20x20 для плотных списков) и Micro (16x16 для бейджей).
* **Установка под стек**:
  * **React**: `npm i @heroicons/react`
  * **Vue 3**: `npm i @heroicons/vue`
  * **Чистый SVG**: экспорт из директории `optimized/` репозитория.

### 3. Tabler Icons (Максимальный охват)
* **Репозиторий**: [tabler/tabler-icons](https://github.com/tabler/tabler-icons) - 21.6k звезд
* **Лицензия**: MIT.
* **Особенности**: Более 6100+ иконок на все случаи жизни. Сетка 24x24, stroke 2px. Рекомендуется для масштабных CRM, аналитических панелей и сложных дашбордов.
* **Установка под стек**:
  * **React**: `npm i @tabler/icons-react`
  * **Vue 3**: `npm i @tabler/icons-vue`
  * **Svelte**: `npm i @tabler/icons-svelte`
  * **Flutter**: `flutter pub add tabler_icons`

### 4. Phosphor Icons (Гибкость стилей и весов)
* **Репозиторий**: [phosphor-icons/homepage](https://github.com/phosphor-icons/homepage) - 7.4k звезд
* **Лицензия**: MIT.
* **Особенности**: 6 вариантов начертания для каждой иконки: Regular, Bold, Duotone, Fill, Light, Thin. Отлично подходит для проектов с акцентом на выразительную типографику.
* **Установка под стек**:
  * **React**: `npm i @phosphor-icons/react`
  * **Vue 3**: `npm i @phosphor-icons/vue`
  * **Flutter**: `flutter pub add phosphor_flutter`

### 5. Eva Icons (От команды Akveo)
* **Репозиторий**: [akveo/eva-icons](https://github.com/akveo/eva-icons) - 8.8k звезд
* **Лицензия**: MIT.
* **Особенности**: Пак из 480+ открытых векторных иконок в двух стилях (Outline и Fill). Поддержка SVG, Web Font и встроенных анимаций (zoom, pulse, shake, flip). Отлично подходит для веб-интерфейсов и мобильных приложений (UI Kitten).
* **Установка под стек**:
  * **React**: `npm i react-eva-icons` или `npm i eva-icons`
  * **React Native**: `npm i @eva-design/eva-icons`
  * **Flutter**: `flutter pub add eva_icons_flutter`
  * **Статический веб / Ванильный JS**: `npm i eva-icons`

---

## 2. Компонентные UI-экосистемы

### 1. Awesome shadcn/ui
* **Репозиторий**: [birobirobiro/awesome-shadcn-ui](https://github.com/birobirobiro/awesome-shadcn-ui) - 20.5k звезд
* **Суть**: Главная курируемая база расширений, блоков и готовых шаблонов вокруг архитектуры shadcn/ui.
* **Применение**: Поиск готовых сложных компонентов (календари, комбобоксы, расширенные таблицы данных на TanStack Table).

### 2. Порты shadcn под другие фреймворки
* **Vue 3**: [unovue/shadcn-vue](https://github.com/unovue/shadcn-vue) - 10.5k звезд
  * Инициализация: `npx shadcn-vue@latest init`
* **Svelte**: [huntabyte/shadcn-svelte](https://github.com/huntabyte/shadcn-svelte) - 9.1k звезд
  * Инициализация: `npx shadcn-svelte@latest init`

### 3. Справочники каталогов компонентов
* [anubhavsrivastava/awesome-ui-component-library](https://github.com/anubhavsrivastava/awesome-ui-component-library) - 1.7k звезд: полная классификация UI-китов по всем популярным языкам и фронтенд-фреймворкам.
* [jaywcjlove/awesome-uikit](https://github.com/jaywcjlove/awesome-uikit) - 1.6k звезд: подборка фреймворков, веб-компонентов (Web Components / Custom Elements) и готовых админ-панелей.

---

## 3. UX, стайлгайды и дизайн-системы

Использовать для исследования дизайн-токенов, сеток и формулировок состояний:

* [alexpate/awesome-design-systems](https://github.com/alexpate/awesome-design-systems) - 25.9k звезд: коллекция реальных производственных дизайн-систем мировых IT-компаний (Shopify Polaris, IBM Carbon, GitHub Primer, Uber Base).
* [batoreh/awesome-ux](https://github.com/batoreh/awesome-ux) - 537 звезд: дисциплины пользовательского опыта, паттерны онбординга и проектирование взаимодействия.
* [anubhavsrivastava/awesome-ux-design-styles](https://github.com/anubhavsrivastava/awesome-ux-design-styles) - 111 звезд: структурированная база визуальных стайлгайдов, цветовых палитр и типографических шкал.

---

## 4. Правила выбора ресурсов агентом

1. **Единый источник иконок в проекте**:
   Категорически запрещено смешивать иконки из разных библиотек в одном проекте (например, брать часть из Lucide, а часть из Heroicons). Это разрушает консистентность толщины линий (`strokeWidth`) и скругления углов.
2. **Предпочтительный стек по умолчанию**:
   * Для React/Next.js/Telegram Mini Apps: `lucide-react` + `shadcn/ui`.
   * Для Vue 3/Nuxt: `lucide-vue-next` + `shadcn-vue`.
   * Для Svelte/SvelteKit: `lucide-svelte` + `shadcn-svelte`.
   * Для Tailwind-проектов с минимальным весом: `@heroicons/react`.
3. **Разрешение иконок**:
   Стандартный размер иконки внутри кнопки или поля ввода - 16x16 или 20x20 (`h-4 w-4` или `h-5 w-5`). Размер навигационных иконок - 24x24 (`h-6 w-6`).
