# OSDI '27 paper workspace

An anonymous, modular LaTeX starter repository for an OSDI '27 submission. The official USENIX sample and style files supplied for this workspace are kept at the repository root; `main.tex` is the writing entry point.

## Build

Install a TeX Live distribution with `latexmk`, `pdflatex`, and BibTeX, then run:

```sh
make
```

This produces `main.pdf`. For a clean rebuild, run `make distclean && make`. The generated PDF and LaTeX auxiliary files are ignored by Git.

## Files

- `main.tex`: document class, USENIX style, title, section order, and appendix setup.
- `sections/`: one source file per paper section.
- `refs.bib`: BibTeX database.
- `figures/`, `tables/`: figures and table assets.
- `supplementary/`: optional material to upload separately; keep the paper self-contained.
- `usenix2019_v3.2.tex`, `usenix2019_v3.sty`: original USENIX sample and style from the links below.

The current draft omits external literature citations and bibliography output while reference entries are being prepared. Internal equation, theorem, and section references use LaTeX labels. Add figures under `figures/` and include them with `\includegraphics{figures/name.pdf}`. Keep each section in its own file and include it from `main.tex`.

The complete reading draft includes `sections/signal.tex`, the design, and Appendices A–F in `sections/appendix.tex`. The abstract, implementation, evaluation, discussion, related work, and conclusion still contain drafting placeholders. `sections/protection.tex` is a standalone protection-section variant used by `supplementary/protection-preview.tex`; the main design already contains this material.

The bundled `flushend` version can stall on the final page of this equation-heavy draft. The document disables final-column balancing after the package's initialization, keeping the supplied style file unchanged.

## OSDI '27 submission notes

The current [OSDI '27 Call for Papers](https://www.usenix.org/conference/osdi27/call-for-papers) specifies US Letter pages, two columns, 10-point type with 12-point leading, a 7" × 9" text block, page numbers, and a maximum of 12 pages including figures and tables, with references allowed beyond that limit. Research-track submissions must anonymize author names and institutions. Please recheck the CFP and detailed submission requirements before submitting, since USENIX can update them.

The provided USENIX sample is from 2019. This repository preserves it unchanged, uses its style file, and provides a modular entry point. The OSDI '27 CFP is the authority if any sample text conflicts with the current requirements.

The combined draft currently contains 24 pages, including 15 appendix pages. It is a full reading draft, not a 12-page submission. The CFP permits separate supplementary files for extended proofs; it does not provide an exemption for appendices embedded in the paper PDF.

Template sources:

- [USENIX sample LaTeX file](https://www.usenix.org/sites/default/files/usenix2019_v3.2.tex)
- [USENIX style file](https://www.usenix.org/sites/default/files/usenix2019_v3.sty)
