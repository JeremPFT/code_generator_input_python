;; a simple major mode for domain specific langage *.dsl

;; see http://ergoemacs.org/emacs/elisp_syntax_coloring.html


(defvar dsl-mode-syntax-table nil "Syntax table for `dsl-mode'.")

(setq dsl-mode-syntax-table
      (let ( (synTable (make-syntax-table)))
        (modify-syntax-entry ?- ". 12b" synTable)
        (modify-syntax-entry ?\n "> b" synTable)
        (modify-syntax-entry ?_ "w" synTable)
        synTable))

;; (setq dsl-highlights
;;       '(("project\\|package\\|value_object" . font-lock-function-name-face)
;;         ("output_directory\\|is\\|abstract\\|limited\\|with\\|use\\|pre\\|post\\|end_implementation\\|implementation" . font-lock-constant-face)))

(setq dsl-font-lock-keywords
      (let* (
            ;; define several category of keywords
            (x-keywords '(
                          "abstract"
                          "and"
                          "or"
                          "end"
                          "command"
                          "implementation"
                          "initialize"
                          "is"
                          "package"
                          "post"
                          "pre"
                          "project"
                          "query"
                          "return"
                          "value_object"
                          "vector"
                          ))
            ;; (x-types '("is" "abstract" "vector"))
            ;; (x-constants '("ACTIVE" "AGENT" "ALL_SIDES" "ATTACH_BACK"))
            ;; (x-events '("at_rot_target" "at_target" "attach"))
            ;; (x-functions '("implementation)"))

            ;; generate regex string for each category of keywords
            (x-keywords-regexp (regexp-opt x-keywords 'words))
            ;; (x-types-regexp (regexp-opt x-types 'words))
            ;; (x-constants-regexp (regexp-opt x-constants 'words))
            ;; (x-events-regexp (regexp-opt x-events 'words))
            ;; (x-functions-regexp (regexp-opt x-functions 'words))
            )

        `(
          (,x-keywords-regexp . font-lock-keyword-face)
          ;; (,x-types-regexp . font-lock-type-face)
          ;; (,x-constants-regexp . font-lock-constant-face)
          ;; (,x-events-regexp . font-lock-builtin-face)
          ;; (,x-functions-regexp . font-lock-function-name-face)

          ;; note: order above matters, because once colored, that part won't change.
          ;; in general, put longer words first
          )))

(define-derived-mode dsl-mode text-mode "dsl"
  "major mode for editing Domain Specific Langage code."
  (setq font-lock-defaults '(dsl-font-lock-keywords)))


(provide 'dsl-mode)

(add-to-list 'auto-mode-alist '("\\.dsl\\'" . dsl-mode))

;;; mylsl-mode.el ends here
