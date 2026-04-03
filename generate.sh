#!/bin/bash
pdflatex --shell-escape a.tex
rm -f *.toc *.log *.aux *.fls *.fdb_latexmk *.out *.lof *.lot *.bbl *.blg *.synctex.gz *.nav *.snm *.vrb *.dvi *.run.xml *.bcf *.idx *.ilg *.ind *.ptc