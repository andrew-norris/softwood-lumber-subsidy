# Economics Paper: Softwood Lumber Tariffs and Subsidies

## Compilation

To compile the paper:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Or use `latexmk` for automatic compilation:

```bash
latexmk -pdf main.tex
```

## Structure

- `main.tex` - Main paper document
- `references.bib` - Bibliography file
- `figures/` - Directory for graphs and figures

## Adding Figures

Place your Python-generated graphs in the `figures/` directory and reference them in the LaTeX document using:

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{figures/your_figure.pdf}
  \caption{Your caption here}
  \label{fig:your_label}
\end{figure}
```
