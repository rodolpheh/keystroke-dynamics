# Plan détaillé

## Définitions (Thèse de Giot)

Champ de la recherche fortement lié à la biométrique et aux méthodes
statistiques. + ML algos.

### Biométrie
Ce que l'on *sait*, ce que l'on *a*.
Mais la biométrie, c'est ce que l'on *est*.

#### Biométrique comportementale
Comment on *fait* les choses.

### *Keystroke Dynamics*

[Monrose] Identification peu coûteuse en hardware et en process. Transparente
pour les utilisateurs.

* Statique :
Identification d'un utilisateur en fonction d'un secret connu à l'avance par le
modèle.
* Dynamique :
Identification de l'utilisateur sur la base d'un texte libre.

#### Solutions commerciales
* typingdna
* keytrac

### Machine learning
En définitive les méthodes d'identification orbitent autour de deux catégories :

* Méthodologie statistique: pour tout échantillon à évaluer, on calcule des
caractéristiques statistiques de la donnée d'entrée et on parcourt toute la base
d'échantillons enregistrés pour trouver celui qui s'en rapproche le plus ;
* Utilisation d'algorithmes de Machine Learning : pour tout échantillon à
évaluer, on le traite pour le transformer en vecteur et le modèle va le
rapprocher de la classe correspondante.

Attention : les deux méthodes ne sont pas exclusives. Après tout les algorithmes
de classification en Machine Learning sont d'abord et avant tout des méthodes
statistiques automatisées. De plus, on peut utiliser des échantillons traités au
moyen de la statistique pour "entraîner" son modèle de Machine Learning.
[Hu, Ginrich]


## Problèmes récurrents

### Données

#### Protocole d'acquisition
#### Ingéniérie des caractéristiques

### Méthodes de classification

#### Classification one among many
#### Classification one vs rest
#### Différences de performances des algos en fonction des différents paramètres
* Qualité et quantité des données
  * Quantité de features
  * Quantité d'échantillons
* Objectif et seuil
* Méthode d'adapation du modèle (péremption des échantillons)

### Évaluation des modèles compliqué vs conditions réelles
* Comparaison des différentes méthodes difficile en fonction des protocoles
d'acquisition, mais aussi parce qu'on ne dispose pas de données d'imposteurs
dans la vraie vie. En pratique on n'est pas plusieurs à avoir le même mdp.


## Solutions
### Déterminer le meilleur seuil pour la méthode retenue
### 


Items : 

* Difficile comparaison des résultats d'une publication à l'autre
* Échelle des solutions : suivant qu'on veut identifier un seul utilisateur ou
plusieurs, parmi beaucoup ou peu, les solutions à utiliser ne seront pas les
mêmes
* Pas grosse différence entre les données avec imposteurs/Données sans
imposteurs.
* Évaluation de la qualité de la donnée.

Problématique : comment implémenter et évaluer un 