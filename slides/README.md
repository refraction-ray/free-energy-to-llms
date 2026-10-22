# 配套幻灯片

与本书配套的课堂幻灯片。每次开课的幻灯片单独保存为一个目录（按 `年-月-地点` 命名），内含各讲源码、当次编译的 PDF 和一份简短说明；各次共用的主题和幻灯片插图放在 `shared/`，与书共用的插图直接取自 [`figures/`](../figures/)。

在仓库根目录编译：

```bash
make slides                                       # 最新一次开课的全部讲 → slides/<offering>/*.pdf
make slides OFFERING=2026-10-gscaep DECK=lecture1 # 只编译某一讲
```

也可以进入开课目录直接 `xelatex lecture1.tex`。`shared/figures/` 中的 `diff_*`、`fm_*`、`score_field`、`river_*` 和 `langevin_path.dat` 由 `python3 shared/tools/make_slide_figures.py` 生成，修改时请改脚本而不是生成的文件。
