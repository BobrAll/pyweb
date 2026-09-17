# P2. Стресс-тест научного контента

```{raw} html
<p>Вариант этой же страницы на <a href="../../stress/index.html">MkDocs (Material)</a>.</p>
```

```{rubric} Страница собрана генератором Sphinx (тема Read the Docs, MyST-Parser)
```

## Формула

Затухающие колебания описываются уравнением {eq}`eq-damped`:

```{math}
:label: eq-damped
x(t) = A e^{-\gamma t}\cos(\omega t + \varphi)
```

где $A$ — начальная амплитуда, $\gamma$ — коэффициент затухания, $\omega$ — круговая частота.

Ссылка на формулу: см. {eq}`eq-damped` выше.

## Таблица с объединёнными ячейками

<table class="stress-table">
<caption>Таблица 1. Результаты измерений времени сборки</caption>
<thead>
<tr><th>Генератор</th><th colspan="2">Время сборки, с</th><th>Размер, КБ</th></tr>
</thead>
<tbody>
<tr><td rowspan="2">MkDocs</td><td>холодная</td><td>3.2</td><td rowspan="2">1240</td></tr>
<tr><td>инкрементальная</td><td>1.1</td></tr>
<tr><td rowspan="2">Sphinx</td><td>холодная</td><td>4.8</td><td rowspan="2">1680</td></tr>
<tr><td>инкрементальная</td><td>1.9</td></tr>
<tr><td colspan="3"><strong>Итого</strong></td><td>2920</td></tr>
</tbody>
</table>

## Статический график

```{figure} ./static_chart.png
:width: 720px

Рисунок 1. Затухающие колебания, построенные matplotlib
```

## Интерактивный график

```{raw} html
<iframe src="../_static/plotly.html" width="100%" height="460" style="border:none;" loading="lazy"></iframe>
```

## Листинг кода

```{code-block} python
:linenos:

def damping(t, gamma, omega):
    import math
    return math.exp(-gamma * t) * math.cos(omega * t)

for t in range(0, 10):
    print(t, damping(t, 0.2, 2.0))
```

## Цитирование

Поддержка BibTeX реализована расширением `sphinxcontrib-bibtex`: методика публикации описана в работе {cite:p}`ivsov2021`, базовые возможности LaTeX — в {cite:p}`knuth1986`, источник по matplotlib — {cite:t}`hunter2007`.

```{bibliography}
```

## Двухколоночный блок

```{raw} html
<div style="display:flex; gap:24px; flex-wrap:wrap; align-items:flex-start;">
  <div style="flex:1 1 320px;">
    <p>Текст слева: статические генераторы позволяют собирать научно-технические сайты
    без серверной части. Sphinx нативно работает с LaTeX-математикой и библиографией,
    а перекрёстные ссылки разрешаются на этапе сборки.</p>
  </div>
  <div style="flex:1 1 320px;">
    <figure>
      <img src="../_images/static_chart.png" alt="График" width="100%" />
      <figcaption>Иллюстрация справа</figcaption>
    </figure>
  </div>
</div>
```

## Сноски и перекрёстные ссылки

Сноска с дополнительным пояснением[^note-1]. Подробное описание методики измерений см. в разделе {doc}`/methodology`.

[^note-1]: Сноска: все измерения выполнялись на одном раннере для сопоставимости результатов.
