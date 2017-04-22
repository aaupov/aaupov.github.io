---
layout: post
title: "Сечение бесконечномерного куба"
date: 2017-04-22
---
    <script type="text/javascript"
            src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
    <script type="text/x-mathjax-config">
  MathJax.Ajax.config.path["Extra"] = "https://github.com/mathjax/MathJax-third-party-extensions";
 MathJax.Hub.Config({
   extensions: ["tex2jax.js","[Extra]/xyjax.js"],
   jax: ["input/TeX","output/HTML-CSS"],
   tex2jax: {inlineMath: [["$","$"],["\\(","\\)"]],
             displayMath: [ ['$$','$$'], ['\\[','\\]'] ]
   },
   TeX: {extensions: ["AMSmath.js","AMSsymbols.js"]}
 });
 </script>
    
    
# Задача
Представьте себе единичный квадрат с проведенной диагональю.
\\[
\begin{xy}
\xymatrix{
  A \ar[r] \ar[d] & B \ar[d] \\
  C \ar[r] & D
}
\end{xy}
\\]
Известно, что длина диагонали такого квадрата составляет $\sqrt{2}$.

Диагональ можно провести не только через центр квадрата: 
(картинка с меньшей диагональю).

Для единичного куба так же можно провести диагональ, соединяющую вершины $(0,0,0)$ и $(1,1,1)$, и рассечь кубик плоскостью, перпендикулярной данной диагонали и проходящей через точку $(\frac{1}{2},\frac{1}{2},\frac{1}{2})$ (центр диагонали).
В сечении получим плоскость с некоторой площадью. Попробуем отыскать эту площадь:

Представьте себе, что мы продолжим повышать размерность задачи, рассекая $n$-мерные кубы гиперплоскостями, ортогональными главным диагоналям и проходящим через центр диагонали. В сечении мы будем получать *поверхности* размерности $n-1$ с некоторым искомым объемом. 

![And now we need to go deeper](https://prepsmarter.com/blog/content/images/2016/06/deeper.jpg)

## Каков будет этот объём при бесконечном $n$?

# Геометрия
Рассмотрим $n$-мерный единичный куб с центром в начале координат:
\\[
\mathbf{C}=[-\frac{1}{2},\frac{1}{2}]^n\in\mathfrak{R}^n
\\]
Пусть $\mathbf{B}$--гиперплоскость размерности $n-1$, рассекающая \\(\mathbf{C}\\).
