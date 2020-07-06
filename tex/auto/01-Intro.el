(TeX-add-style-hook
 "01-Intro"
 (lambda ()
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperref")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperimage")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "hyperbaseurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "nolinkurl")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (LaTeX-add-labels
    "fig:tms-figure"
    "eq:1"
    "eq:2"
    "eq:3"
    "eq:4"
    "eq:5"
    "eq:6"
    "eq:7"
    "eq:8"
    "tab:max-min"
    "fig:corr-resp"
    "eq:10"
    "osec:Correlation-of-a-non-point-source"
    "eq:9"
    "eq:19"
    "eq:11"
    "eq:12"
    "eq:13"
    "eq:14"
    "eq:15"
    "eq:16"
    "eq:17"
    "eq:21"
    "sec:visualising-result"
    "eq:25"
    "fig:03-dirac-vis"
    "fig:04-gauss-vis"
    "eq:27"
    "fig:05-fin-band"
    "eq:30"
    "eq:31"
    "fig:uv-lm-coords"
    "eq:18"
    "eq:20"
    "eq:22"
    "eq:23"
    "eq:24"
    "eq:26"
    "fig:06-array2uv-triangle"
    "fig:07-array2uv-meerkat"
    "fig:xy-uv"
    "eq:28"
    "eq:29"
    "tab:uv-summary"))
 :latex)

