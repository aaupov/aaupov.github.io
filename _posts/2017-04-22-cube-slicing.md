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
\mathbf{C}=\left[-\frac{1}{2},\frac{1}{2}\right]^n\in\mathfrak{R}^n
\\]

Рассечем его какой-нибудь плоскостью.
Пусть $\mathbf{B}$---некоторая гиперплоскость, рассекающая \\(\mathbf{C}\\).

$\vv{V}$---нормаль к этой гиперплоскости $\mathbf{B}$ с координатами $\vec{V}=(v_1,v_2,\cdots,v_n),\quad v_i\neq0$.

Пересечение $\mathbf{B}$ с кубом $\mathbf{C}$ зададим поверхностью $\mathbf{X}=\mathbf{B}\cap\mathbf{C}$:

\\[
\mathbf{X}=(x_1, x_2, \cdots, x_n):\quad\sum_{i=1}^n x_i v_i = 0.
\\]

Объем сечения равен интегралу $V(\mathbf{X})=\int_\mathbf{X}dV$.

Также известно, что сечение полностью лежит внутри куба:
\\[
\begin{equation}
V(\mathbf{X})=\{\Large\int\limits_\mathbf{C}\}
\left\\{x\in\mathbf{X}:\sum\limits_{i=1}^n x_i v_i =0\right\\}\,\mathrm{d}x
\label{isec_eq}
\end{equation}
\\]

<!--
\mathbf{X}\subset\mathbf{C}\quad\implies\quad-\frac{1}{2}\leqslant x_i\leqslant\frac{1}{2}.
Ортогонально спроецируем $\mathbf{X}$ на $n$-ую "ось" $A_n=(x_1,x_2,\cdots,x_{n{-}1},0)$ (гиперплоскость с $x_n=0$) и рассмотрим "площадь" проекции:
\\[
P=\frac{(\mathbf{X},A_n)}{\left\|\left\|A_n\right\|\right\|^2}=\sum_{i=1}^{n-1}x_i v_i
\\]

Из \eqref{isec_eq} имеем следующее:

\\[
-\frac{1}{2}\leqslant\sum_{i=1}^{n-1}x_i v_i\leqslant\frac{1}{2}\quad\implies\quad \left|P\right|\leqslant\frac{1}{2},
\\]
-->

# Внезапный поворот: воспользуемся случайными величинами

Точнее, воспользуемся чем-то похожим на метод Монте-Карло, только без численного интегрирования.
Пусть $y_k$---независимые в совокупности случайные величины, распределенные на $v_k: \left[-\frac{v_k}{2},\frac{v_k}{2}\right],\,k=\overline{1,n}$
с постоянной плотностью $\frac{1}{v_k}$.

Тогда \eqref{isec_eq} будет совпадать с вероятностной мерой случайной величины $\sum\limits_{i=1}^n y_i$:
Из \eqref{isec_eq} имеем следующее:

\\[
-\frac{1}{2}\leqslant\sum_{i=1}^{n-1}x_i v_i\leqslant\frac{1}{2}\quad\implies\quad\left|\sum_{i=1}^{n-1}x_i v_i\right|\leqslant\frac{1}{2},
\\]

что в точности равно вероятности
$\Pr{\left( \left|\sum\limits_{i=1}^{n-1}y_i\right|\leqslant\frac{1}{2} \right)}$.

Круто! Получили, что площадь проекции равна некоторой вероятности. Но нас интересовала не проекция поверхости на некоторую ось, а объем самой поверхности сечения $X$.

Объем сечения $X$ будет равен произведению
\\[
V(\mathbf{X})=\lvert\vec{V}\rvert\cdot\Pr{ \left( \left| \sum\limits_{i=1}^{n-1} y_i \right| \leqslant\frac{1}{2}\right)}.
\\]

Если бы нас интересовал объем сечения, отстоящего от центрального на некоторое заданное расстояние $a$, его можно было бы найти по формуле

\\[
V(\mathbf{X_a})=\left|\vec{V}\right|\cdot\Pr{ \left( \left| \sum_{i=1}^{n-1} y_i-a \right| \leqslant\frac{1}{2} \right)}.
\\]

# Погрузимся еще чуть-чуть в теорию вероятности
И отыщем характеристическую функцию $y_k$:

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
f_\eta(t)=\prod\limits_{k=1}^{n-1}f_k(t)=\left(\frac{2}{t}\right)^{n-1}\prod\limits_{k=1}^{n-1}\frac{\sin{t\frac{v_k}{2}}}{v_k}
$$

Воспользуемся тем, что нас интересует центральное ортогональное сечение, заданное нормалью $\vec{V}=(1,1,\cdots,1)$:

$$
f_\eta^*(t)=\left(\frac{2}{t}\right)^{n-1}\prod\limits_{k=1}^{n-1}\sin{\frac{t}{2}}=\left(\frac{\sin{t/2}}{t/2}\right)^{n-1}.
$$


# Литература
- D. Hensley, _Slicing the cube in $R^n$ and probability (bounds for the measure of a central cube slice in $R^n$ by probability methods)_,
Proceedings of the American Mathematical Society, Vol. 73, No. 1 (Jan., 1979)
- Б. В. Гнеденко, _Курс теории вероятностей_

# Примечания
Эта задача была одной из двух зачетных задач по курсу теории вероятностей (Животов С.Д., ФАЛТ МФТИ).
Первому решившему полагался зачет "автоматом" без сдачи заданий, и я стал таким счастливчиком (из-за чего так и не заботал теорвер как следует...)
