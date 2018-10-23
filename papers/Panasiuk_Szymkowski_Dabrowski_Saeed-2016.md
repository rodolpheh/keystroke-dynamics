# A Multimodal Biometric User Identification System Based on Keystroke Dynamics and Mouse Movements
**Auteurs** : Panasiuk, Szymkowski, Dabrowski, Saeed

**Résumé:** Les *keystroke dynamics* sont souvent limités par la longueur du
mot de passe.
Les données biométriques comportementales (comme les mouvements de la souris et 
la frappe au clavier) sont trop imprécises pour atteindre le niveau de 
performance des données biométriques classiques comme les empreintes digitales. 
En revanche, croiser deux données biométriques comportementales peut donner 
de meilleures performance pour un faible coût d'acquisition, sans nécessiter de 
matériel supplémentaire comme un capteurs d'empreintes digitales.

## Introduction

> *Something you know* and *something you have* - these are the most common  
> methods used to prove your identity.

Les auteurs soulignent que les méthodes les plus communes pour identifier une
personne sont :

* Ce que l'on **sait** : on connait son mot de passe. Mais on peut l'oublier.
* Ce que l'on **a** : on peut avoir une carte, une liste de clés, ou un numéro de
téléphone. Cette fois-ci l'inconvénient est qu'on peut perdre, ou se faire voler
ces preuves d'identité.

La **biométrique** est le moyen d'identifier la personne par ce qu'elle **est**.
Interviennent alors deux catégories :

* la **biométrique physiologique** : rétine, empreintes digitales, empreinte de 
la main ;

* la **biométrique comportementale** : comment la personne **fait** les choses.

Comme expliqué dans le résumé, les méthodes d'identification comportementales
sont réputées assez imprécises, mais elles sont assez peu coûteuses en
implémentation et ne nécessitent pas de matériel accessoire. 

La publication cherche à montrer qu'en croisant deux sources de données 
comportementales de faible qualité, on peut tout de même réussir à obtenir des
bonnes performances, pour un coût d'acquisition et d'analyse minimes. Les modes
d'identification utilisés sont les *keystroke dynamics* et l'observation des 
mouvements de la souris. 

## Méthodes existantes
Les auteurs font l'inventaire des nouveautés de la recherche sur les méthodes
d'identification retenues. Suivent des noms d'algorithmes et de méthodologies
qu'on ne détaillera pas.

Observation des mouvements de la souris :

* Elbahi, Omri, Mahjoub, Garrouch (2016) : HMM (Hidden Markov Models) et CRF 
(Conditional Random Fields). 
* Pentel (2015) : Classification par:
  * régression logistique ;
  * SVM (Support Vector Machine)
  * RF (Random Forest)
  * C4.5 ;

avec une fidélité de 94.61 % pour la méthode SVM

* Tabedzki, Saeed (2005) : Première tentative d'analyser les mouvements de la
souris à des fins d'identification de l'utilisateur (en polonais). Les auteurs
ont utilisé la TFD pour l'analyse fréquentielle des mouvements de la souris 
associée à un algorithme k-NN pour la classification


*Keystroke dynamics* :

* Kaganov, Korolev, Krylov, Mashechkin, Petrovskii, (2015) : Amélioration de
performances sur la base de données de Maxion-Killourhy avec un algorithme
développé spécifiquement. L'apport de cette publication est de proposer une
méthodologie de normalisation des données d'entrée. Pour la classification, la
théorie des "ensembles flous" (fuzzy sets) a été mise à profit.
* Rybnik, Tabedzki, Saeed (2008) : Obtention de meilleurs résultats avec un
nombre limité d'utilisateurs, et ce avec des algorithmes de classification
simples comme k-NN voire 1-NN.
* Pasaniuk, Saeed (2009) : Influence de la qualité des données et de la longueur
des échantillons. La publication met en évidence qu'on peut obtenir de meilleurs
résultats en utilisant les caractéristiques statistiques des échantillons plutôt
que la donnée brute. La publication fait aussi le constat de la grosse 
différence dans la qualité des données pour l'entrainement de ces algorithmes.
Il y a un problème de variation d'une base à l'autre en fonction du protocole 
d'acquisition des profils.

Croisement de données biométriques comportementales:

* Mortwani, Jain, Sondhi, (2015) :  clavier/souris et plusieurs couches
d'événements de souris. Mais la méthodologie est mal décrite et ne permet pas
d'évaluer la qualité de la recherche effectuée.
* Kudlacik, Porwik, Wesolowski (2015) : Opère une distiction entre profil 
courant et profil global de l'utilisateur, le tout avec une méthode assez peu
consommatrice de ressources.

## Approche proposée
L'acquisition s'est faite au moyen d'une application web qui capture tous les 
événements de la souris à partir du début de processus d'identification, et qui
s'arrête lorsque l'utilisateur se connecte. L'utilisateur doit utiliser un mot
de passe fixe `_Y9u3elike22`, un champ de texte libre.

La publication souligne la difficulté d'acquérir de la donnée de frappe au 
clavier qui ne soit pas bruitée, surtout lorsque qu'on considère un mot de passe
précis à taper qui est de surcroit assez compliqué. Le problème est la variation
introduite par la touche majuscule et le taux d'erreur de frappe qui grèvent les
performances des algorithmes d'analyse. Les chercheurs ont fini par se 
concentrer sur certaines touches et notamment le temps de pression de la touche 
plutôt que d'utiliser le temps entre les touches.

Après ce travail de définition des données caractéristiques, la classification
des profils s'est faite avec un algorithme k-NN.
Les échantillon de données utilisés pour le calcul de la proximité sont :

* *keyboardDistance* : distance de Manatthan entre les temps de pression des
touches.
* *mouseDistance* : distance de Manatthan entre les différents de pression des
boutons de la souris
* *moveDistance* : distance Euclidienne de la distance parcourue par le curseur. 

Toutes ces distances sont normalisées par rapport à la dimensionalité des
données caractéristiques utilisées pour constituer les échantillons de données.

La formule qui calcule la distance totale pondère les différentes
caractéristiques. Les poids sont dit être choisis empiriquement. On ne sait pas 
pourquoi la distance de Manatthan est utilisée pour le calcul de la proximité 
des *caractéristiques* orientées pression d'une touche et la distance 
euclidienne est utilisée pour la distance parcourue par le curseur.

## Résultats
La base de données a un nombre irrégulier d'échantillons par utilisateur. Les
utilisateurs ayant trop peu d'échantillons ont été évacués de la base de données.

La figure 1 montre que la fiabilité de l'identification croît surtout en 
fonction de la disponibilité de données de movements de souris et de frappe au
clavier. Les clics de la souris paraissent avoir peu d'influence.

Les auteurs soulignet que la classification avec l'algorithme k-NN est limitée à
la fois par le nombre de *features* (caractéristiques de la donnée) utilisées et
le nombre d'utilisateurs différents.

Chaque expérience a été répétée 100 fois avec à chaque fois une sélection
aléatoire entre données d'entrainement et données de tests.

### Sélection de la pondération des *features*
Individuelement les *features* ont été, de la moins fiable à la plus fiable :

* Le *dwell time* des clics de souris, avec un score moyen de 12 % 
* La distance de la souris avec un score moyen de 31 %
* La frappe au clavier, avec un score moyen de 44 %

En adaptant le poids des *features* les moins fiables à 0.2 pour la distance et
0.8 pour les clics de souris, on arrive à une prédiction aux alentours de 40 %
pour les seules données de la souris.

Avec le clavier à 2, 0.4 pour les clics de souris et 0.1 pour la distance de la
souris, les auteurs sont arrivés à 68.8%, ce qu'ils considèrent comme étant un
très bon score pour très peu d'échantillons (10) par utilisateur.

## Conclusion
L'algorithme k-NN est adapté à la recherche rapide et fiable d'un profil
utilisateur dans une base existante. Les *keystroke dynamics* sont sécurisés car
l'utilisateur n'a pas de moyen de savoir que son identité est en train d'être 
vérifiée, et connaître le mot de passe ne suffit pas car il est extrêmement 
difficile d'imiter le profil de telle manière à tromper l'algorithme 
d'identification.

Le problème concernant la chute de précision sur les données clavier doit venir
de la taille réduite de l'échantillon utilisé. D'habitude le *flight time* aide
à l'identification alors que dans le cas de cette recherche, il a fait chuter
la perf de 44% sans à 11 % avec.

Les données de la souris peuvent être combinées pour arriver à une fiabilité
comparable aux données du clavier seul.

La fusion de ces données biométriques donne des résultats impressionnants malgré
un échantillon très peu qualitatif et de très petite taille et un grand nombre
d'utilisateurs.

Cela permet d'envisager des algorithmes moins coûteux en faisant des k-NN à 
faible dimensionalité plutôt que de s'embarrasser d'un grand nombre de 
*features*.

## Synthèse

Cette publication essaye de résoudre le problème des *keystroke dynamics* en ce
qui concerne la qualité des données. En effet, les données biométriques 
comportementales (comme les mouvements de la souris et la frappe au clavier) 
sont trop imprécises pour atteindre le niveau de performance des données 
biométriques classiques comme les empreintes digitales. 
En revanche, croiser deux données biométriques comportementales peut donner 
de meilleures performance pour un faible coût d'acquisition, sans nécessiter de 
matériel supplémentaire comme un capteurs d'empreintes digitales.

Pour la mise en pratique de solution d'identification, la captation des 
événements de clavier est d'autant plus problématique que l'échantillon est
réduit. La donnée captée inclut souvent du bruit qui n'est pas réductible du 
fait des différentes manières de taper : un texte avec des majuscules, par 
exemple, peut être capitalisé avec la touche majuscule gauche ou droite. 
L'analyse des données du clavier donne de meilleurs résultats quand on limite le
nombre de caractéristiques analysées. Notamment, le temps entre deux touches 
varie trop pour être utile sur un faible nombre d'échantillons, contrairement au
 *dwell time*, soit le temps de pression d'une touche spécifique.

Les auteurs montrent qu'en croisant et en pondérant de manière *ad hoc* les 
différentes données de biométrie comportementale (clavier et souris), on peut 
arriver à des  résultats très satisfaisants, même avec un nombre réduit 
d'échantillons. 
Cela permet de constituer une base de données et d'entraîner une IA beaucoup 
plus rapidement. La limite de la publication réside dans la méthode empirique
de trouver les pondérations donnant les meilleurs résultats.

Mais l'approche k-NN dont la dimension suit le nombre d'échantillon limite
rapidement le nombre de classes possibles et on ne peut pas faire plus de 50
classes pour 10 échantillons par utilisateur, par exemple. La méthode empirique
utilisée implique aussi une recherche à tâtons des meilleurs poids pour les 
caractéristiques extraites. Cette méthode n'apporte pas de protocole rigoureux 
pour l'identification des poids, et ne permet pas de savoir si les poids 
utilisés sont adaptés dans toutes les situations, ou pour les données collectées
pour cette publication spécifiquement (surinterprétation).

Les auteurs ont rencontré les difficultés habituelles de l'acquisition de 
données de clavier. Cela souligne la difficulté de généraliser les méthodes 
d'acquistion pour des solutions d'identification grand public.
