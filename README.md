Painless: a Framework for Parallel SAT Solving 
==============================================




Contenu
-------
* painless-src/:  
   Contient le code du framework.
   * clauses/:
      Contient le code pour diriger les clauses partagées.
   * working/:
      Contient le code pour organiser et lier les workers.
   * sharing/:
      Contient le code utilitaire pour traiter les clauses dans le sharer.
   * solvers/:
      Contient le wrapper de solvers séquentiels.
   * utils/:
      Contient le code pour organiser les clauses et d'autres structures utiles.

* mapleCOMSPS/:
   Contient le code de MapleCOMSPS de la Competition SAT 17 avec quelques changements mineurs.

* utils/:
   Contient des scripts utilitaires pour la manipulation de fichiers CNF.
Pour Compiler le projet
----------------------

* A la racine du projet, utiliser la commande 'make' pour compiler.

* A la racine du projet, utiliser la commande 'make clean' pour nettoyer proprement.


Pour démarrer PaInLeSS
------------------

* painless:
   ./run-data dimacs\_filename workers\_number timeout out.txt

=======


