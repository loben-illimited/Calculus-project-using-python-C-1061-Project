#Python 微積分報告 --- 時間與影子之關係

-----

## 前言

> **數學固然存在於我們的身邊，如沒有數學，這個世界還會像現在一樣嗎？**  --- 這是我做這份報告所想到的話

而和數學一樣重要的東西還有甚麼嗎？

我抬起頭來，看著夜空，難道地球上的一切的生命能在黑夜生存，就這樣，我想起了太陽。

太陽為地球帶來了生命，人類的生命方可延續下去，而人們的作息規律也和太陽息息相關，這又讓我想起**[日晷](https://zh.wikipedia.org/zh-tw/%E6%97%A5%E6%99%B7)**

![日晷](https://i.imgur.com/xMJ07zV.png)

我們受日晷啟發便

-----

## 數學原理

本人藉由參考 `The sun shadow positioning` 並利用其提供的公式

|  **Symbols**  |             **Definitions**              |
| :-----------: | :--------------------------------------: |
|      $H$      |    **The length of the rods (物體的長度)**    |
|      $l$      | **The length of the straight rod sun shadow (物體的影子長度)** |
|   $\alpha$    |        Solar hour angle (太陽時角) OK        |
|   $\delta$    |         Solar Declination angle          |
|      $h$      |            Solar zenith angle            |
|     $ST$      |             True solar time              |
|      $T$      |                GMT+8 time                |
| $\varepsilon$ |                Longitude                 |
|    $\phi$     |                 Latitude                 |
|     $Et$      |          Time difference (min)           |
|   $\theta$    |                Day Angle                 |
|      $N$      |                 Ahargana                 |
|      $t$      |                $t=N-N_0$                 |
|    $Year$     |                   Year                   |
|   $\lambda$   |              Solar azimuth               |

###計算Solar hour angle

根據[Part 3: Calculating Solar Angles | ITACA](http://www.itacanet.org/the-sun-as-a-source-of-energy/part-3-calculating-solar-angles/#3.3.-The-Altitude-Angle)我們有兩種方法計算**Solar hour angle**

1. $$\sin \omega =  -  \dfrac{\cos \alpha \sin A_Z} {\cos \delta}$$
2. $$\sin\omega=\dfrac{\sin\alpha-\sin\delta\sin\phi}{\cos\delta\cos\phi}$$

其中參數意思如下表
| **Symbols** |     **Definitions**     |
| :---------: | :---------------------: |
|  $\omega$   |     the hour angle      |
|  $\alpha$   |   the altitude angle    |
|    $A_Z$    | the solar azimuth angle |
|  $\delta$   | Solar Declination angle |
|   $\phi$    |   observer’s latitude   |

而 **the altitude angle** 可由$\sin\alpha=\sin\delta\sin\phi+\cos\delta\cos\omega\cos\phi$ 求出

### 計算Declination Angle

$$\delta=23.45\dfrac{\pi}{180}\sin\left[2\pi\left(\dfrac{284+n}{36.25}\right)\right]$$

其中參數定義為下表
| **Symbols** |             **Definitions**              |
| :---------: | :--------------------------------------: |
|  $\delta$   |              the hour angle              |
|     $n$     | the day number, such that n = 1 on the 1st January |





------



## 程式原理

* 為了減少問題，程式運作過程將以`UTC`作為處理
* 本人將使用python的`urllib`作為取得日出日落及每一個地點的經緯度

------

## 使用的工具

* 使用`Git`作為 version control
* 使用`markdown`寫作報告
* 使用`python`
* 使用$\LaTeX$寫出公式

-----

## 心得

### 106502045



-----



## 參考

* $\LaTeX$ 參考了 [symbols.pdf](http://cs.brown.edu/about/system/managed/latex/doc/symbols.pdf)