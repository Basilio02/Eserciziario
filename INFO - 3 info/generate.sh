#!/bin/bash
mkdir -p temp

rm temp/* -rf

pdflatex --shell-escape ./"INFO - 3 info.tex"

pdflatex --shell-escape --jobname="INFO - 3 info SOLUTION" '\def\soluzioni{1}\input{"INFO - 3 info.tex"}'

# find . -maxdepth 1 -type f \
#     ! -name '*.tex' \
#     ! -name '*.pdf' \
#     ! -name '*.png' \
#     ! -name "$(basename "$0")" \
#     -delete