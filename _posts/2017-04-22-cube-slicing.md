---
layout: post
title: "Сечение бесконечномерного куба"
date: 2017-04-22
---
<script type="text/x-mathjax-config">
	MathJax.Hub.Config({
		extensions: ["tex2jax.js"],
		jax: ["input/TeX","output/HTML-CSS"],
		tex2jax: {inlineMath:  [["$", "$"],  ["\\(", "\\)"]],
			  displayMath: [["$$","$$"], ["\\[", "\\]"]]},
	TeX: {
		extensions: ["AMSmath.js", "AMSsymbols.js"],
		equationNumbers: {autoNumber: "AMS"},
	},
	"HTML-CSS": {availableFonts: ["TeX"], preferredFont: "TeX", webFont: "TeX"},
	});
</script>

<script type="text/javascript"
    src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>

# Начнем с простого
Pассмотрим квадрат единичной длины:

<p align="center">
<img src="/assets/2017-04-cube/square-1.svg"/>
</p>

Проведем в нем диагональ и начнем двигаться вдоль нее, рассекая квадрат перпендикулярными диагонали прямыми.

<p align="center">
<img src="/assets/2017-04-cube/square-2.svg"/>
</p>

Нас будут интересовать только _главные_ сечения, проходящие через центр квадрата. Кстати, длина такого сечения для квадрата равна $\sqrt{2}$ по теореме Пифагора.

# Сечение куба
Для единичного куба так же можно провести главную диагональ, соединяющую вершины $(0,0,0)$ и $(1,1,1)$, и рассечь кубик плоскостью, 
перпендикулярной данной диагонали и проходящей через центр диагонали (точку $(\frac{1}{2},\frac{1}{2},\frac{1}{2})$).
В сечении получим фигуру с некоторой площадью:

<p align="center">
<img src="/assets/2017-04-cube/slice-1.svg"/>
</p>

# Дальше...
Запрыгнем в четырехмерное пространство и начнем рассекать тессеракты остро наточенными гиперплоскостями. В сечении будем получать трехмерные фигуры непонятной формы и объема:
[Hypercube](http://imgur.com/gallery/Frqrj).

Думаю, общая идея ясна.

Продолжим повышать размерность задачи: будем рассекать $n$-мерные кубы гиперплоскостями, ортогональными главным диагоналям и проходящими через центр диагонали.
В сечении мы будем получать *гиперповерхности* размерности $n-1$ с некоторым искомым объемом.
Вопрос данной заметки в том, какого же объема будут эти гиперповерхности при бесконечном $n$.

# Чему равен объём сечения при $n\to\infty$?
<center>
<img src="https://prepsmarter.com/blog/content/images/2016/06/deeper.jpg"/>
</center>

# Геометрия в общем случае
Рассмотрим $n$-мерный единичный куб с центром в начале координат:
\\[
\mathbf{C}=\left[-\frac{1}{2},\frac{1}{2}\right]^n\in\mathfrak{R}^n
\\]

Рассечем его какой-нибудь плоскостью.
Пусть $\mathbf{B}$---некоторая гиперплоскость размерности $n-1$, рассекающая \\(\mathbf{C}\\).

$\vec{V}$---нормаль к этой гиперплоскости $\mathbf{B}$ с координатами $\vec{V}=(v_1,v_2,\cdots,v_n),\quad v_i\neq0$.

Пересечение $\mathbf{B}$ с кубом $\mathbf{C}$ зададим поверхностью $\mathbf{X}=\mathbf{B}\cap\mathbf{C}$:

\\[
\mathbf{X}=(x_1, x_2, \cdots, x_n):\quad\sum_{i=1}^n x_i v_i = 0.
\label{isec-eq}
\\]

Также известно, что сечение полностью лежит внутри куба:
\\[
\mathbf{X}\subset\mathbf{C}\quad\implies\quad-\frac{1}{2}\leqslant x_i\leqslant\frac{1}{2}.
\\]

# Внезапный поворот: воспользуемся случайными величинами

Теперь пусть $y_k$---независимые в совокупности случайные величины, распределенные на $v_k: \left[-\frac{v_k}{2},\frac{v_k}{2}\right],\,k=\overline{1,n-1}$
с постоянной плотностью $\frac{1}{v_k}$.

Ортогонально спроецируем $\mathbf{X}$ на $n$-ую "ось" $(x_1,x_2,\cdots,x_{n{-}1},0)$.

Из $\ref{iseq-eq}$ получаем, что

\\[
-\frac{1}{2}\leqslant\sum_{i=1}^{n-1}x_i v_i\leqslant\frac{1}{2}\quad\implies\quad\left|\sum_{i=1}^{n-1}x_i v_i\right|\leqslant\frac{1}{2},
\\]

что в точности равно вероятности
$\Pr{\left( \left|\sum\limits_{i=1}^{n-1}y_i\right|\leqslant\frac{1}{2} \right)}$.

Круто! Получили, что площадь проекции равна некоторой вероятности. Но нас интересовала не проекция поверхости на некоторую ось, а объем самой поверхности сечения $X$.

Объем сечения $X$ будет равен произведению 
\\[
V(\mathbf{X})=V(\mathbf{B}\cap\mathbf{C})=\lvert\vec{V}\rvert\cdot\Pr{ \left( \left| \sum\limits_{i=1}^{n-1} y_i \right| \leqslant\frac{1}{2}\right)}.
\\]

Если бы нас интересовал объем сечения, отстоящего от центрального на некоторое заданное расстояние $a$, его можно было бы найти по формуле

\\[
V(\mathbf{X_a})=\left|\vec{v}\right|\cdot\Pr{ \left( \left| \sum_{i=1}^{n-1} y_i-a \right| \leqslant\frac{1}{2} \right)}.
\\]

Однако нас интересует центральное ортогональное сечение, заданного нормалью $\vec{V}=(1,1,\cdots,1)$.

# Погрузимся еще чуть-чуть в теорию вероятности
И отыщем характеристическую функцию $y_k$:

$$
\begin{align}
f_k(t) & =\bf{M}e^{i t y_k}=\int\limits_{-\infty}^{+\infty}e^{i t x}p(x)dx  =\\
&=\left| p(x) \quad = \quad \left\{ 
\begin{aligned}
\frac{1}{v_k},\quad  & x\in\left[-\frac{v_k}{2},\frac{v_k}{2}\right] \\
0, \quad            & \text{иначе}
\end{aligned}
\right.\right| \\
&=\int\limits_{-\frac{v_k}{2}}^{\frac{v_k}{2}}e^{i t x}\frac{1}{v_k} dx =%
\left.\frac{1}{v_k}\frac{1}{it}e^{i t x}\right|_{-\frac{v_k}{2}}^{\frac{v_k}{2}} =\\
&=\frac{e^{it\frac{v_k}{2}}-e^{-it\frac{v_k}{2}}}{itv_k} =
\frac{1}{2}\frac{e^{it\frac{v_k}{2}}-e^{-it\frac{v_k}{2}}}{it\frac{v_k}{2}}=\\
&=\frac{\sin{t\frac{v_k}{2}}}{t\frac{v_k}{2}} &.
\end{align}
$$

Рассмотрим теперь случайную величину $\eta=\sum\limits_{k=1}^{n-1}y_k.$
