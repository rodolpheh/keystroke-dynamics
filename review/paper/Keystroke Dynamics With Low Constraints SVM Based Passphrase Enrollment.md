# Keystroke Dynamics With Low Constraints SVM Based Passphrase Enrollment

Document par Romain Giot, Mohamad El-Abed, Christophe Rosenberger.

Université de Caen, Basse-Normandie

## Résumé

Dans cet article, les auteurs utilisent du machine learning (SVM State Vector Machine) pour une authentification bi-factorielle (avec la dynamique de frappe au clavier en complément du mot de passe). Ils démontrent qu'il est possible, avec la SVM, de reconnaître un utilisateur à partir de seulement 5 enregistrements. Ils soutiennent cette étude en comparant la méthode par SVM avec 4 autres méthodes.

Les données utilisées proviennent de la base du GREYC qui contient un enregistrement des timestamps d'appuis de touche pour plus d'une centaine d'utilisateurs.

## Méthode proposée

Les auteurs utilisent une SVM avec un minimum de 5 captures. Le choix s'est porté sur 5 captures parce que c'est le nombre maximum d'enregistrements qu'un utilisateur est prêt à accepter. La SVM est une SVM a deux classes, c'est à dire qu'on adopte une démarche "one-vs-rest".

Cette méthode est comparée avec d'autres méthodes :

* Méthodes statistiques
* Méthodes d'études de la distance
* Méthodes d'études de rythme
* Méthodes par machine learning

## Résultats

Le clavier n'a pas d'influence sur le résultat de l'authentification, sauf lorsque l'enregistrement et l'authentification sont faits sur des claviers différents (dans 4 cas sur 6).

La méthode par machine learning (SVM) est la plus performante (11.96% d'EER contre 17.58% minimum pour la méthode statistique n°2).

En dessous de 10 enregistrements, l'authentification est médiocre (selon le graphe, avec une SVM, 5 enregistrements permettent d'obtenir une EER de ~14%). L'idéal pour toutes les techniques se situent à ~40 enregistrements. Au delà de 50 enregistrement, la performance décroit.

Les auteurs testent aussi différentes méthodes d'adaptation du modèle :

* sans adaptation : premiers enregistrements gardés pour toujours
* "Adaptive" : on supprime le dernier vecteur et on ajoute celui qui vient d'être approuvé
* "Progressive" : on ajoute tous les vecteurs approuvés
* "Intelligent" : en dessous de 15 enregistrements, on utilise la méthode progressive. Au délà, on utilise la méthode adaptive.

La méthode intelligente est celle qui performe le mieux sur toutes les méthodes.

L'utilisation d'un seuil individuel pour valider l'authentification permet d'améliorer sensiblement les valeurs pour les méthodes autres que machine learning. Pour une SVM, le gain est égal à 0.01%. Le seuil individuel est l'EER de l'individu calculé à partir de la validation des essais en seuil global. Cette méthode ne peut pas être appliquée sur des données composées de différents mots de passe (le seuil ne peut que se calculer lorsqu'on a des données d'imposteurs).

Le nombre d'utilisateurs dans la base de données a une influence sur la performance. En dessous de 10 utilisateurs, l'EER est inférieur à 10% mais peut être très variable. Selon Giot, 50 individus est un maximum acceptable.
