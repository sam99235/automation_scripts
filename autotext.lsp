(defun c:SwapTextMT ( / ss i ent txt oldnum newtxt upper srnum)
  (setq ss (ssget "X" '((0 . "TEXT,MTEXT"))))
  (if ss
    (progn
      (setq i 0)
      (while (< i (sslength ss))
        (setq ent (ssname ss i))
        
        ;; Get text
        (setq txt
              (cond
                ((= (cdr (assoc 0 (entget ent))) "TEXT") (cdr (assoc 1 (entget ent))))
                ((= (cdr (assoc 0 (entget ent))) "MTEXT") (vla-get-TextString (vlax-ename->vla-object ent)))
              )
        )
        
        (if txt
          (progn
            ;; Remove formatting codes
            (setq txt (vl-string-subst "" "{" (vl-string-subst "" "}" txt)))
            (setq txt (vl-string-subst "" ";" txt))
            
            ;; Convert to uppercase - FIXED: removed the 't' parameter
            (setq upper (strcase txt))
            (princ (strcat "\nProcessing text: " upper))
            
            ;; Generalized match: starts with CA + 2 digits + /SR1 or SR2 + -CFA-
            (if (and (>= (strlen upper) 8)
                     (= (substr upper 1 2) "CA")
                     (wcmatch upper "CA??/SR?-CFA-*"))
              (progn
                (setq oldnum (substr upper 3 2))
                ;; Preserve SR1 or SR2 from original
                (setq srnum (substr upper 6 3))  ; "SR1" or "SR2"
                ;; Build new text
                (setq newtxt (strcat srnum "/CA" oldnum "-CFA-P" oldnum))
                (princ (strcat "  --> MATCHED! Replacing with: " newtxt))
                
                ;; Replace entity
                (cond
                  ((= (cdr (assoc 0 (entget ent))) "TEXT")
                   (entmod (subst (cons 1 newtxt) (assoc 1 (entget ent)) (entget ent))))
                  ((= (cdr (assoc 0 (entget ent))) "MTEXT")
                   (vla-put-TextString (vlax-ename->vla-object ent) newtxt))
                )
              )
              (princ "  --> does not match.")
            )
          )
        )
        (setq i (1+ i))
      )
    )
  )
  (princ "\nFinished processing all texts.")
  (princ)
)