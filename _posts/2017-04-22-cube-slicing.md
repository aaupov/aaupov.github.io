---
layout: post
title: "Сечение бесконечномерного куба"
date: 2017-04-22
---
<script type="text/x-mathjax-config">
	MathJax.Hub.Config({
		extensions: ["tex2jax.js"],
		jax: ["input/TeX", "output/HTML-CSS"],
        tex2jax: {inlineMath:  [["$", "$"],  ["\\(", "\\)"]],
                  displayMath: [["$$","$$"], ["\\[", "\\]"]]},
		TeX: {extensions:      ["AMSmath.js", "AMSsymbols.js"],
              equationNumbers: {autoNumber: "AMS"}},
        "HTML-CSS": {availableFonts: ["TeX"],
                     preferredFont: "TeX",
                     webFont: "TeX"},
	});
</script>

<script type="text/javascript"
    src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

<div style="display:none">
  $
    \newcommand{\vv}[1]{\overset{→}#1}
  $
</div>

# Начнем с простого
Рассмотрим квадрат единичной длины:

<p align="center">
<img src="/assets/2017-04-cube/square-1.svg"/>
</p>

Проведем в нем диагональ и начнем двигаться вдоль нее, рассекая квадрат перпендикулярными прямыми.

<p align="center">
<img src="/assets/2017-04-cube/square-2.svg"/>
</p>

Нас будет интересовать только _главное_ сечение, проходящее через центр квадрата.
Как все мы помним со школы, длина такого сечения для квадрата равна $\sqrt{2}$ по теореме Пифагора.

# Сечение куба
Для единичного куба так же можно провести главную диагональ, соединяющую вершины $(0,0,0)$ и $(1,1,1)$, и рассечь кубик плоскостью, 
перпендикулярной данной диагонали и проходящей через центр диагонали (точку $(\frac{1}{2},\frac{1}{2},\frac{1}{2})$).
В сечении получим фигуру с некоторой площадью:

<p align="center">
<img src="/assets/2017-04-cube/slice-1.svg"/>
</p>
<center><i>Похоже на правильный шестиугольник</i></center>

# Дальше...
Запрыгнем в четырехмерное пространство и начнем рассекать тессеракты остро заточенными гиперплоскостями.
В сечении будем получать трехмерные фигуры непонятной формы и объема, которые по-умному называются [политопами](https://ru.wikipedia.org/wiki/%D0%9F%D0%BE%D0%BB%D0%B8%D1%82%D0%BE%D0%BF).

Наглядно сечения тессеракта представлены в галерее здесь: [Hypercube](http://imgur.com/gallery/Frqrj).

Думаю, что на данный момент идея уже ясна. Что же будет в общем случае?

Продолжим повышать размерность задачи: будем рассекать $n$-мерные кубы гиперплоскостями, ортогональными главным диагоналям и проходящими через центр диагонали.
В сечении мы будем получать *гиперповерхности* размерности $n-1$ с некоторым искомым объемом.
Вопрос данной заметки в том, какого же объема будут эти гиперповерхности при бесконечном $n$.

<center>
<img src="http://static2.channels.com/thumbnails/Radu-Inception-trailer-HD-TV-e10127230.jpg"/>
</center>
<br>

# Геометрия в общем случае
<center>Переместимся в $n$-мерное пространство.</center>
<br>
Рассмотрим единичный куб с центром в начале координат:
\\[
\mathbf{C}=\left[-\frac{1}{2},\frac{1}{2}\right]^n\in\mathbb{R}^n
\\]

Рассечем его какой-нибудь плоскостью.
Пусть $\mathbf{B}$---некоторая гиперплоскость, рассекающая \\(\mathbf{C}\\).

$\mathbf{v}$---нормаль к этой гиперплоскости $\mathbf{B}$ с координатами $\mathbf{v}=(v_1,v_2,\cdots,v_n),\quad v_i\neq0$.

Пересечение $\mathbf{B}$ с кубом $\mathbf{C}$ зададим поверхностью $\mathbf{X}=\mathbf{B}\cap\mathbf{C}$:

\\[
\begin{equation}
\mathbf{X}=(x_1, x_2, \cdots, x_n):\quad\sum_{i=1}^n x_i v_i = 0.
\label{isec_eq}
\end{equation}
\\]

Ортогонально спроецируем $\mathbf{X}$ на гиперплоскость с $x_n=0$ и рассмотрим "площадь" проекции:
\\[
P=\left\\{(x_1, x_2, \ldots, x_{n-1}):\quad-\frac{1}{2}\leqslant\sum_{i=1}^{n-1}x_i v_i\leqslant\frac{1}{2}\right\\}
\label{proj}
\\]

Объем сечения будет равен
$V(\mathbf{X})=|\mathbf{v}|P$.

# Вероятностная постановка

Переформулируем задачу в вероятностных терминах.

Пусть $y_k$---независимые в совокупности случайные величины, распределенные на $v_k: \left[-\frac{v_k}{2},\frac{v_k}{2}\right],\,k=\overline{1,n-1}$
с постоянной плотностью $\frac{1}{v_k}$.

Тогда мера множества $P$ будет совпадать с вероятностью 
$\Pr{\left( \left|\sum\limits_{i=1}^{n-1}y_i\right|\leqslant\frac{1}{2} \right)}$.

Искомый объем сечения $X$ будет равен произведению
\begin{equation}
V(\mathbf{X})=\lvert\mathbf{v}\rvert\cdot\Pr{ \left( \left| \sum\limits_{i=1}^{n-1} y_i \right| \leqslant\frac{1}{2}\right)}.
\label{vol}
\end{equation}

<!--
Если бы нас интересовал объем сечения, отстоящего от центрального на некоторое заданное расстояние $a$, его можно было бы найти по формуле

\\[
V(\mathbf{X_a})=\left|\vec{V}\right|\cdot\Pr{ \left( \left| \sum_{i=1}^{n-1} y_i-a \right| \leqslant\frac{1}{2} \right)}.
\\]
-->

Как найти чему равна эта вероятность?

Можно быть внимательными и обратить внимание, что выполнены все условия [центральной предельной теоремы](https://ru.wikipedia.org/wiki/%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F_%D1%82%D0%B5%D0%BE%D1%80%D0%B5%D0%BC%D0%B0):

> Пусть $X_1, \ldots, X_n, \ldots$ --- бесконечная последовательность независимых одинаково распределенных случайных величин с конечным матожиданием и дисперсией.
>
> Тогда имеет место сходимость по распределению $\frac{\sum_{i=1}^n X_i-\mu n}{\sigma\sqrt{n}}\xrightarrow[n\to\infty]{d}N(0,1)$.

Но если внимательность не относится к нашим сильным сторонам (в отличие от усидчивости и упертости),
то получить тот же результат можно и самостоятельно, немного погрузившись в теорию вероятности.

# Продолжаем погружение
Будем следовать общей логике доказательства ЦПТ и воспользуемся инструментом характеристической функции.
Для начала найдем характеристическую функцию $y_k$:

$$
\begin{align*}
f_k(t) & ={\bf M}e^{i t y_k}=\int\limits_{-\infty}^{+\infty}e^{i t x}p(x)dx  =\\
&=\left| p(x) \quad = \quad \left\{ 
\begin{array}{cl}
\frac{1}{v_k},\quad  & x\in\left[-\frac{v_k}{2},\frac{v_k}{2}\right] \\
0, \quad            & \text{иначе}
\end{array}
\right.\right| \\
&=\int\limits_{-\frac{v_k}{2}}^{\frac{v_k}{2}}e^{i t x}\frac{1}{v_k} dx =%
\left.\frac{1}{v_k}\frac{1}{it}e^{i t x}\right|_{-\frac{v_k}{2}}^{\frac{v_k}{2}} =\\
&=\frac{e^{it\frac{v_k}{2}}-e^{-it\frac{v_k}{2}}}{itv_k} =
\frac{1}{2}\frac{e^{it\frac{v_k}{2}}-e^{-it\frac{v_k}{2}}}{it\frac{v_k}{2}}=\\
&=\frac{\sin{t\frac{v_k}{2}}}{t\frac{v_k}{2}}
\end{align*}
$$

Рассмотрим теперь случайную величину $\eta=\sum\limits_{k=1}^{n-1}y_k.$

Характеристическая функция $\eta$ будет равна произведению характеристических функций $y_k$:

$$
f_\eta(t)=\prod\limits_{k=1}^{n-1}f_k(t)=\left(\frac{2}{t}\right)^{n-1}\prod\limits_{k=1}^{n-1}\frac{\sin{t\frac{v_k}{2}}}{v_k}.
$$

Воспользуемся тем, что нас интересует центральное ортогональное сечение, заданное нормалью $\vec{V}=(1,1,\cdots,1)$:

$$
f_\eta(t)=\left(\frac{2}{t}\right)^{n-1}\prod\limits_{k=1}^{n-1}\sin{\frac{t}{2}}=\left(\frac{\sin{t/2}}{t/2}\right)^{n-1}.
$$

Теперь воспользуемся формулой обращения:
$$
\begin{align}
P\left(|\eta|\leqslant\frac{1}{2}\right)&=P\left(-\frac{1}{2}\leqslant\eta\leqslant\frac{1}{2}\right)= && \text{для абс.непр. сл.в.}\nonumber\\
&=P\left(-\frac{1}{2}\leqslant\eta\lt\frac{1}{2}\right)=F_{\eta}\left(\frac{1}{2}\right)-F_{\eta}\left(-\frac{1}{2}\right)= && \text{формула обращения}\nonumber\\
&=\frac{1}{2\pi}\;v.p.\int\limits_{-\infty}^{\infty}\frac{e^{it\frac{1}{2}}-e^{-it\frac{1}{2}}}{it}\left(\frac{\sin{t/2}}{t/2}\right)^{n-1}dt=\nonumber\\
&=\frac{1}{2\pi}\:v.p.\int\limits_{-\infty}^{\infty}\left(\frac{\sin{t/2}}{t/2}\right)^{n}dt.\label{prob}
\end{align}
$$

# Собираем части воедино
Начнем собирать части выражения объема сечения $\eqref{vol}$:

- Норма нашего вектора нормали равна $\lvert\mathbf{v}\rvert=\sqrt{n}$.
- Вероятность мы отыскали в $\eqref{prob}$.

Подставляя все в одно выражение и устремляя $n$ к бесконечности, получаем

$$
\begin{equation}
V(\mathbf{X})=\lim_{n\to\infty}\frac{1}{2\pi}\;v.p.\int\limits_{-\infty}^{+\infty}\sqrt{n}\left(\frac{\sin{t/2}}{t/2}\right)^n dt
\label{closed_form}
\end{equation}
$$

Теперь отыскать объем - дело техники...
# Дело техники

* Произведем замену переменной: $x=\frac{t\sqrt{n}}{2},\;t=\frac{2x}{\sqrt{n}},\;dt=\frac{2}{\sqrt{n}}dx$:

$$
\begin{align*}
V(\mathbf{X})&=\lim_{n\to\infty}\frac{1}{2\pi}\int\limits_{-\infty}^{+\infty}\sqrt{n}\left(\frac{\sin{\frac{x}{\sqrt{n}}}}{\frac{x}{\sqrt{n}}}\right)^n\frac{2}{\sqrt{n}}dx \\
&=\frac{1}{\pi}\lim_{n\to\infty}\int\limits_{-\infty}^{+\infty}\left(\frac{\sin{\frac{x}{\sqrt{n}}}}{\frac{x}{\sqrt{n}}}\right)^n dx\\
&=\frac{1}{\pi}\int\limits_{-\infty}^{+\infty}\lim_{n\to\infty}\left(\frac{\sin{\frac{x}{\sqrt{n}}}}{\frac{x}{\sqrt{n}}}\right)^n dx\\
\end{align*}
$$

* Для отыскания предела под интегралом воспользуемся разложением в ряд Тейлора:

$$
\begin{align*}
I&=\lim_{n\to\infty}\left(\frac{\sin{\frac{x}{\sqrt{n}}}}{\frac{x}{\sqrt{n}}}\right)^n=\\
&=\lim_{n\to\infty}\left(\frac{ \frac{x}{\sqrt{n}}-\frac{1}{6}\left(\frac{x}{\sqrt{n}}\right)^3+o\left(\left(\frac{x}{\sqrt{n}}\right)^3\right) }{\frac{x}{\sqrt{n}}}\right)^n=\\
&=\lim_{n\to\infty}\left(1-\frac{1}{6}\left(\frac{x}{\sqrt{n}}\right)^2+o\left(\left(\frac{x}{\sqrt{n}}\right)^2\right)\right)^n
\end{align*}
$$

* Немного упростим последнее выражение ([второй замечательный предел](https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%BC%D0%B5%D1%87%D0%B0%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D1%8B%D0%B5_%D0%BF%D1%80%D0%B5%D0%B4%D0%B5%D0%BB%D1%8B)):

$$
\begin{align*}
I&=\lim_{n\to\infty}\left(1-\frac{1}{6}\left(\frac{x}{\sqrt{n}}\right)^2+o\left(\left(\frac{x}{\sqrt{n}}\right)^2\right)\right)^n=\\
&=\lim_{n\to\infty}\left(1-\frac{x^2}{6n}+o\left(\frac{x^2}{n}\right)\right)^n=\\
&=\lim_{n\to\infty}\exp\left(n \ln\left(1-\frac{x^2}{6n}+o\left(\frac{x^2}{n}\right)\right)\right)=\\
&=\lim_{n\to\infty}\exp n \left(\frac{x^2}{6n}\right)=e^{-x^2/6}.
\end{align*}
$$

* Наконец, осталось взять [любимый интеграл первокурсников](https://ru.wikipedia.org/wiki/%D0%93%D0%B0%D1%83%D1%81%D1%81%D0%BE%D0%B2_%D0%B8%D0%BD%D1%82%D0%B5%D0%B3%D1%80%D0%B0%D0%BB):

$$
\begin{align*}
V(\mathbf{X})&=\frac{1}{\pi}\int\limits_{-\infty}^{+\infty}e^{-x^2/6}dx=\sqrt{\frac{6}{\pi}}.
\end{align*}
$$


# Заключение
Мы получили результат, который заключается в следующем: центральное ортогональное сечение бесконечномерного куба имеет конечный объем.
В других работах доказывается также и конечность _любых_ сечений.
Противоречащий интуиции результат!

# Литература
- D. Hensley, _Slicing the cube in $R^n$ and probability (bounds for the measure of a central cube slice in $R^n$ by probability methods)_,
Proceedings of the American Mathematical Society, Vol. 73, No. 1 (Jan., 1979)
- Б. В. Гнеденко, _Курс теории вероятностей_

# Примечания
Эта задача была одной из двух зачетных задач по курсу теории вероятностей (Животов С.Д., ФАЛТ МФТИ).
Первому решившему полагался зачет "автоматом" без сдачи заданий, и я стал таким счастливчиком (из-за чего так и не заботал теорвер как следует...)
