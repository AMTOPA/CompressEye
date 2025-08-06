<div align="center">
<h1>压缩感知图像重建（DCT + SPGL1）📊🔍</h1>

<a href="README_zh.md">简体中文</a> | <a href="README.md">ENGLISH</a>

[![GitHub release](https://img.shields.io/github/release/AMTOPA/CompressEye.svg)](https://github.com/AMTOPA/CompressEyeo/releases)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows-blue)](https://www.microsoft.com/windows)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/AMTOPA/CompressEyeo/graphs/commit-activity)
[![Language](https://img.shields.io/badge/语言-简体中文-red)](README_zh.md)
[![Blog](https://img.shields.io/badge/📖_我的博客-math--enthusiast.top-FF5733)](https://math-enthusiast.top/)

</div>

一个基于 **离散余弦变换 (DCT)** 稀疏性和 **SPGL1** 优化算法的**压缩感知 (Compressive Sensing)** 图像重建的 **Demo 实现**。本项目展示了如何从远少于原始像素数量的随机测量中恢复图像。

> ⚠️ **注意**：此为 **Demo 版本**，仅用于教学和研究目的，不适用于生产环境。

## ✨ 主要功能

- 🖼️ **图像预处理**：加载并调整标准测试图像（`skimage.astronaut`）大小
- 🔀 **DCT 稀疏表示**：将图像变换到 DCT 域以利用其稀疏性
- 📏 **高斯随机测量**：使用 `m << n` 的线性测量模拟压缩感知
- 🧮 **SPGL1 求解器**：在 DCT 域中使用 `spgl1` 求解 LASSO/BPDN 问题
- 📈 **可视化结果**：显示原始图像、重建图像和误差图
- 📊 **定量评估**：计算 L2、L∞ 误差、PSNR 和压缩比

## 🚀 快速开始

1. 克隆仓库：
   
   ```bash
   git clone https://github.com/AMTOPA/CompressEye.git
   cd cs-image-dct
   ```
2. 安装依赖：
   
   ```bash
   pip install numpy matplotlib scikit-image scipy spgl1
   ```
3. 运行脚本：
   
   ```bash
   python main.py
   ```
   
   🖼️ 重建结果

-----

---

以下是图像重建结果：

### 综合输出图

<div align="center"><img src="./fig/output.png"></img></div>

#### 原始图像

<div align="center"><img src="./fig/original.png"></img></div>

#### 重建图像

<div align="center"><img src="./fig/reconstructed.png"></img></div>

#### 误差图

<div align="center"><img src="./fig/error_map.png"></img></div>

-----------

> 💡 **提示**：增加 `m`（测量数量）可提升重建质量。

🧩 工作原理
-------

1. **稀疏化**：将图像进行二维 DCT 变换（`s_true = dct2d(image)`）
2. **测量**：使用随机高斯矩阵 `A` 获取测量值 `y = A @ x_true`
3. **恢复**：通过 SPGL1 求解 `min ||s||_1 s.t. ||A @ idct2d(s) - y||_2 ≤ σ`
4. **重建**：对恢复的系数进行逆 DCT 得到图像

📜 许可证
------

本项目采用 MIT 许可证，详见 [LICENSE](https://chat.qwen.ai/c/LICENSE) 文件。
🤝 贡献

-----

欢迎提交问题、改进建议或功能请求！

* * *

⭐ 如果你觉得这个 Demo 有帮助，请考虑在 GitHub 上给个 Star！






