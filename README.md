# 工程數學計算機 Engineering Math Calculator

跨平台工程數學計算機桌面應用程式，提供符號數學運算功能。

## 下載

| 平台 | 下載連結 |
|------|---------|
| Windows (.zip) | [EngMathCalc-windows.zip](https://github.com/scorpio-rest/engineering-math-calculator/releases/latest/download/EngMathCalc-windows.zip) |
| macOS (.dmg) | [EngMathCalc-macos.dmg](https://github.com/scorpio-rest/engineering-math-calculator/releases/latest/download/EngMathCalc-macos.dmg) |

> 前往 [Releases 頁面](https://github.com/scorpio-rest/engineering-math-calculator/releases) 查看所有版本。

## 功能模組

### 1. 矩陣運算
- 行列式、反矩陣、轉置
- 特徵值 & 特徵向量
- 矩陣乘法、加減法
- Rank、RREF（列簡化梯形式）

### 2. 微積分
- 符號微分（任意階）
- 符號積分（不定積分 & 定積分）
- 極限計算
- Taylor 展開

### 3. 常微分方程 (ODE)
- 輸入 ODE 方程式求解析解
- 支援初始條件
- 顯示解的過程

### 4. Laplace 轉換
- 正轉換 f(t) → F(s)
- 逆轉換 F(s) → f(t)

## 技術棧

- **GUI**: PyQt6
- **符號數學**: SymPy
- **數值計算**: NumPy, SciPy
- **公式渲染**: Matplotlib (LaTeX)
- **打包**: PyInstaller
- **CI/CD**: GitHub Actions

## 從原始碼執行

```bash
# 安裝相依套件
pip install -r requirements.txt

# 啟動應用程式
python main.py
```

## 專案結構

```
├── main.py              # 程式進入點
├── core/                # 運算邏輯
│   ├── matrix_ops.py    # 矩陣運算
│   ├── calculus_ops.py  # 微積分
│   ├── ode_ops.py       # 常微分方程
│   └── laplace_ops.py   # Laplace 轉換
├── ui/                  # 介面
│   ├── main_window.py   # 主視窗 (深色主題)
│   ├── matrix_tab.py    # 矩陣運算 Tab
│   ├── calculus_tab.py  # 微積分 Tab
│   ├── ode_tab.py       # ODE Tab
│   └── laplace_tab.py   # Laplace Tab
└── utils/
    └── latex_render.py  # LaTeX 公式渲染
```

## 截圖

應用程式採用現代深色主題 (Catppuccin Mocha)，左側 Tab 導航列可切換四大功能模組，計算結果以 LaTeX 數學公式渲染顯示。

## 授權

MIT License
