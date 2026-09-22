#!/bin/bash
mkdir -p temp

rm temp/* -rf

pdflatex --shell-escape ./"TPS - 3 info.tex"

pdflatex --shell-escape --jobname="TPS - 3 info SOLUTION" '\def\soluzioni{1}\input{"TPS - 3 info.tex"}'

# find . -maxdepth 1 -type f \
#     ! -name '*.tex' \
#     ! -name '*.pdf' \
#     ! -name '*.png' \
#     ! -name "$(basename "$0")" \
#     -delete