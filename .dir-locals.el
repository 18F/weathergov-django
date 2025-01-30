((web-mode . (
              (web-mode-markup-indent-offset . 2)
              (web-mode-code-indent-offset . 2)
              (python-flymake-command '("docker compose exec web flake8 ."))
              (eval web-mode-set-engine 'django)
              (eval drupal-mode)
              (eval electric-pair-mode nil)
              (eval hl-line-mode)))
 (auto-mode-alist . (
                     ("\\.html\\'" . web-mode)
                     ("\\.py\\'" . python-ts-mode))))
