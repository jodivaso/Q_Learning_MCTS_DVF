(in-package :cat)

(load "finite-topological-spaces\\New-Smith.cl")
(load "finite-topological-spaces\\vf-order.lisp")
(load "finite-topological-spaces.lisp")
(load "finite-topological-spaces\\finite-spaces-changes.lsp")
(load "finite-topological-spaces\\finite-spaces-class.lsp")
(load "finite-topological-spaces\\finite-spaces-subdivisions.lsp")
(load "finite-topological-spaces\\finite-spaces-point-reductions.lsp")
(load "finite-topological-spaces\\finite-spaces-homology.lsp")
(load "finite-topological-spaces\\random-quasicellular.lsp")
(load "finite-topological-spaces\\finite-spaces-import-and-export.lsp")
(load "finite-topological-spaces\\constructions.lsp")
(load "finite-topological-spaces\\finding-max-strategies.lsp")
(load "finite-topological-spaces\\finite-spaces-hregularization.lsp")
(load "finite-topological-spaces\\finite-spaces-dvf-strategies.lsp")


;; Auxiliary function to read the contents of a file
(DEFUN FILE-GET-CONTENTS (filename)
  (with-open-file (stream filename)
    (let ((contents (make-string (file-length stream))))
      (read-sequence contents stream)
      contents)))

;; Strategies we consider for row and column indexes
(setf strategies '(:standard 
                     :indegree :reverse-indegree
                             :outdegree :reverse-outdegree))

;; Function to apply the 25 strategies to compute discrete vector fields
;; Folder contains the different spaces we want to compute the discrete vector fields on
;; csv is the file where we write the results

(DEFUN STRATEGIES-TO-CSV (folder csv)
  (with-open-file (stream  csv 
                          :direction :output
                          :if-exists :overwrite
                          :if-does-not-exist :create )
    (format stream "space;size;s-s;i-s;ri-s;o-s;ro-s;s-i;i-i;ri-i;o-i;ro-i;s-ri;i-r;ri-ri;o-ri;ro-ri;")
    (format stream "s-o;i-o;ri-o;o-o;ro-o;s-ro;i-ro;ri-ro;o-ro;ro-ro;maximo~%")
     (dolist (file (directory folder))
      (print (file-namestring file))
      (let* ((l (read-from-string (file-get-contents file)))
             (finspace     (build-finite-space  :stong (edges-to-stong-mtrx (list-to-vector l))))
             (dvfs-all (dvfield-strategies-noprint finspace strategies strategies))
             (max-length (max-in-list (mapcar #'(lambda (x) (car x)) dvfs-all)))
             (dvfs (mapcar #'(lambda (l1)
                               (first l1))
                     dvfs-all)))
        (format stream (file-namestring file))
        (format stream ";")
        (format stream (write-to-string (length l)))
        (format stream ";")
        (dolist (i1 dvfs)
          (format stream (write-to-string i1))
          (format stream ";"))
        (format stream (write-to-string max-length))
        (format stream "~%")))))                 
