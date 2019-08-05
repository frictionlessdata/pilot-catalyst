.PHONY: all install

all: list

install:
	pip install -r requirements.txt

readme:
	md_toc -p README.md github --header-levels 3
	sed -i '/(#pilot-catalyst)/,+1d' README.md

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'
