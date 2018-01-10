export TEXINPUTS=.:./latex/texmf/:
mkdir -p latex/output/
pdflatex -output-directory latex/output/ course.tex
pdflatex -output-directory latex/output/ course.tex
mv latex/output/course.pdf ./
