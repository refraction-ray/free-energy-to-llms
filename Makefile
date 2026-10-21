# Build the figures, the book and the slide decks. Build files go to build/;
# the finished PDFs are copied next to their sources so that git tracks them.
#
#   make                         book: book/free-energy-to-llms.pdf
#   make figures                 figures: figures/*.pdf
#   make slides                  decks of the latest offering: slides/<offering>/*.pdf
#   make slides OFFERING=2026-10-gscaep DECK=lecture1
#   make clean                   remove build/ (tracked PDFs stay)
#
# Requires XeLaTeX, Biber and the Noto Sans CJK SC font (see book/preamble/fonts.tex).

BOOK     := free-energy-to-llms
BUILD    := build
XELATEX  := xelatex -interaction=nonstopmode -halt-on-error -file-line-error
BIBER    := biber
LOCALE   ?= en_US.UTF-8

# A fixed timestamp makes rebuilds of unchanged sources byte-identical,
# so the tracked PDFs only show up in git diff when their content changes.
export SOURCE_DATE_EPOCH ?= 1790812800
export FORCE_SOURCE_DATE := 1

FIG_SRC  := $(filter-out figures/cjk.tex,$(wildcard figures/*.tex))
FIG_PDF  := $(FIG_SRC:.tex=.pdf)
FIG_DEPS := figures/figstyle.sty figures/cjk.tex book/preamble/fonts.tex
BOOK_SRC := $(shell find book -name '*.tex') book/references.bib

# Each offering of the course has its own folder under slides/ (named
# YYYY-MM-venue, so the last one in sort order is the latest).
OFFERING ?= $(lastword $(sort $(patsubst slides/%/,%,$(dir $(wildcard slides/*/lecture*.tex)))))
DECK     ?= $(basename $(notdir $(wildcard slides/$(OFFERING)/lecture*.tex)))

# $(call run,LOG,COMMAND): run quietly into LOG and print its tail on failure.
run = $(2) > $(1) 2>&1 || { tail -n 60 $(1) >&2; exit 1; }

.PHONY: all book figures slides clean

all: book

book: book/$(BOOK).pdf

figures: $(FIG_PDF)

figures/%.pdf: figures/%.tex $(FIG_DEPS) | $(BUILD)/figures
	@echo "figure  $*"
	@cd figures && $(call run,../$(BUILD)/figures/$*.build.log,$(XELATEX) -output-directory=../$(BUILD)/figures $*.tex)
	@cp $(BUILD)/figures/$*.pdf $@

book/$(BOOK).pdf: $(BOOK_SRC) $(FIG_PDF) | $(BUILD)/book
	@echo "book    xelatex (1/3)"
	@cd book && $(call run,../$(BUILD)/book/build-xelatex-1.log,$(XELATEX) -output-directory=../$(BUILD)/book -jobname=$(BOOK) main.tex)
	@echo "book    biber"
	@cd book && $(call run,../$(BUILD)/book/build-biber.log,LC_ALL=$(LOCALE) LANG=$(LOCALE) $(BIBER) --input-directory ../$(BUILD)/book --output-directory ../$(BUILD)/book $(BOOK))
	@echo "book    xelatex (2/3)"
	@cd book && $(call run,../$(BUILD)/book/build-xelatex-2.log,$(XELATEX) -output-directory=../$(BUILD)/book -jobname=$(BOOK) main.tex)
	@echo "book    xelatex (3/3)"
	@cd book && $(call run,../$(BUILD)/book/build-xelatex-3.log,$(XELATEX) -output-directory=../$(BUILD)/book -jobname=$(BOOK) main.tex)
	@cp $(BUILD)/book/$(BOOK).pdf $@
	@echo "PDF: $@"

slides: $(FIG_PDF)
	@test -n "$(OFFERING)" || { echo "no offering folder under slides/" >&2; exit 1; }
	@mkdir -p $(BUILD)/slides/$(OFFERING)
	@for deck in $(DECK); do \
	  for pass in 1 2; do \
	    echo "slides  $(OFFERING)/$$deck ($$pass/2)"; \
	    (cd slides/$(OFFERING) && $(call run,../../$(BUILD)/slides/$(OFFERING)/$$deck.build-xelatex-$$pass.log,TEXINPUTS=.:../shared//: $(XELATEX) -output-directory=../../$(BUILD)/slides/$(OFFERING) $$deck.tex)) || exit 1; \
	  done; \
	  cp $(BUILD)/slides/$(OFFERING)/$$deck.pdf slides/$(OFFERING)/$$deck.pdf; \
	  echo "PDF: slides/$(OFFERING)/$$deck.pdf"; \
	done

$(BUILD)/figures $(BUILD)/book:
	@mkdir -p $@

clean:
	rm -rf $(BUILD)
