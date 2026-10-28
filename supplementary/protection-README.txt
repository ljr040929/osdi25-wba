WAFT：延迟保护与平滑权重均衡（2026-10-29）

正文入口
  sections/design.tex 引入 sections/protection.tex。
  该小节定义：β/γ、有效RTT epoch、本地严重拥塞条件、预算映射、
  分布式尺度更新、恢复、条件平衡和服务下界。

设计说明
  supplementary/protection-note-zh.tex：中文推导与接入说明。
  supplementary/protection-preview.tex：采用论文双栏样式的本节预览。
  supplementary/check_protection.py：解析与准静态模型核验。

从论文根目录构建（生成物不放入源码目录）
  mkdir -p /home/ljr/FPCC-experiments/overload-protection-20261029
  pdflatex -interaction=nonstopmode -halt-on-error -output-directory=/home/ljr/FPCC-experiments/overload-protection-20261029 supplementary/protection-preview.tex
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=/home/ljr/FPCC-experiments/overload-protection-20261029 supplementary/protection-note-zh.tex
  /home/ljr/anaconda3/bin/python3 supplementary/check_protection.py --output /home/ljr/FPCC-experiments/overload-protection-20261029/analytic-validation.json
  为解析交叉引用，两个LaTeX命令各执行两遍。

验证口径
  1000组固定seed解析参数检查：正常预算、单调压缩、权重单位不变性、
  γ处必降、β以下恢复、理想服务下界、唯一平衡、Jacobian和局部特征值。
  另检查复制固定权重混合时的单调延迟和恢复。
  这次没有运行ns-3，也没有修改控制器实现。
  旧保护实验不能替代本扩展在当前超龄观测器上的端到端评估。

与既有公式的关系
  延续预算尺度与权重指数共同压缩的思路；新增固定w_min归一化，
  避免小权重预算对尺度的非单调性，并给出与配置权重范围对应的步长。
  q_i = a*w_min*s_i*(w_i/w_min)^s_i。
  多瓶颈中无权比例公平不要求全网等速率。

全文构建状态
  本次独立中英文片段可编译。
  main.tex 的完整编译首先停在现有 sections/background.tex 的 Markdown ## 标题。
  未改写用户正在编辑的 background.tex、signal.tex 或 appendix.tex。
