# Comparing Anomaly-Detection Algorithms for Keystroke Dynamics
Kevin S. Killourhy, Roy A. Maxion

Identifier les meilleurs algorithmes pour l'identification d'un utilisateur en 
se basant sur son rythme de frappe au clavier.

## Introduction
*Keystroke dynamics* : moyen pour différencier entre un utilisateur authentique
et un imposteur quand les deux ont accès au mot de passe.

Il y a beaucoup d'algorithmes de détection des anomalies, et il est naturel de
se demander lesquels sont les plus performants. Surtout qu'il existe un problème
d'évaluation entre les différentes techniques vu qu'elles s'accompagnent toutes
de leur propre protocole d'acquisition / évaluation.

Le standard européen pour les systèmes de contrôle d'accès (EN-50133-1) exige un
FRR en dessous de 1 % et un *miss rate* (équivalent FAR) en dessous de 0.001 %
. Et pour l'instant aucun des algorithmes utilisés n'a atteint ce score, ce qui 
motive une publication pour déterminer quelle est la voie la plus prometteuse. 

## Background and related work
### Review of keystroke dynamics
Beaucoup de choses ont déjà été faites.
Différences de méthodes dans le domaine :

* Sur quoi porte l'analyse ?
  * Analyse sur mdp
  * Analyse sur un paragraphe

* Quel type d'analyse ?
  * Détection d'anomalie = classification binaire (une seule classe)
  * Identification d'une personne parmi plusieur : classifiction à plusieurs 
classes.

Les différents types d'analyse ne peuvent pas être évaluées suivant les mêmes
critères car les objectifs et les outputs sont très différents.

### <a name="Anomaly_detectors">Anomaly detectors for password timing</a>

La publication va se concentrer sur la **détection d'imposteur sur mot de 
passe.**. L'inventaire des publications ayant porté exactement sur ce sujet 
soulève la disparité qui existe entre les méthodes utilisées, sans même parler 
des algos en eux-mêmes.

Sans surprise, la qualité des données a une influence très importante sur les 
performances.


**Le tableau est plutôt sympa pour savoir quelles *features* utiliser, quels
sont les résultats, à quoi correspondent les *features*, etc.**

Les sections intéressantes sont : **Features Sets** -> description des 
*features* courantes et à quoi elles correspondent. **Results Threshold** ->
comment le seuil a été fixé sur les *miss and false alarm rate*.

## Problem and approach
Pas possible d'évaluer les résultats des publications sur la base de ce qu'ils
rapportent dans leurs protocoles d'évaluation, il y a trop de variations
d'une expérience à l'autre. Cette publication se concentre sur la production
d'un jeu de données et d'une procédure d'évaluation commune pour les algorithmes
de détection des imposteurs.

## Password-data collection
### Choosing a password
Choix d'un mdp aléatoire sur 10 caractères.

### Data-collection apparatus
Ordi portable + clavier externe. Application Windows qui effectue la capture.
L'application ne valide que les frappes correctes et se débarrasse des autres.
Pour la précision des timestamps, le logiciel utilise une horloge de référence
externe.

Sessions de 50 samples par utilisateur : permet une grande cohérence des données
Éviter d'avoir un jeu de données qui produit des particularités.

> If some subjects typed the password more frequently than others, or if 
> different subjects used differend keyboards, these differences could make it
> artificially easier for an anomaly detector to distinguish between typists.

### Running subjects
Description de la population de test. Chaque sujet a fait 8 sessions de 50 pw,
pour un total de 400 mdp, avec des variations entre les sessions.

### Extracting timing vectors
Extraction des *features* de la donnée de frappe dans un *timing vector*. Pour
chaque mdp de 11 frappes (10 caractères + entrée), 31 features temporelles sont
extraites et insérées dans un *timing vector*. Les données qui peuvent être
corrélées n'ont pas été réduites.

## Detector implementation
Implémentation la plus fidèle possible des différents algos de détection 
d'imposteurs décrits dans le tableau de la section 
[Anomaly detectors for password timing](#Anomaly_detectors)

Chaque détecteur subit une phase d'entraînement basée sur un ensemble de
vecteurs de timing associés à un utilisateur, puis sune phase de test avec des
nouvelles données auxquel le détecteur associe un score d'anomalie (taux de
détection d'un imposteur).

La pondération des paramètres s'est faite suivant les publications d'origine
des détecteurs reproduits. Le problème de la pondération des paramètres est
qu'elle introduit tout de suite un biais qui favorise la méthode pour laquelle
elle avait été conçue.

**Liste des différentes implémentations avec une description concise de chaque
algorithme** :

### Euclidean
Calcul du vecteur moyen du nuage de points du set d'entrainement, puis anomalie
= (distance euclidienne entre le vecteur testé et le vecteur moyen) au carré.

### Euclidean (normed)
aka "normalized minimum distance classifier". Pareil que précedemment sauf qu'on
normalise la distance en la divisant par le produit de la norme des deux 
vecteurs.

### Manhattan
On calcule le vecteur moyen en phase d'entrainement, puis distance de Manhattan
entre le vecteur testé et le vecteur moyen.
[Distance de Manhattan](https://en.wikipedia.org/wiki/Taxicab_geometry)

### Manhattan (filtered)
On a filtré les *outliers* de la donnée d'entrainement avant de faire le vecteur
moyen (on fait une première moyenne, pui son calcule la déviation standard, tout
point au dessus de 3 déviations standard est considéré comme un *outlier* puis
est viré du set, et on recalcule une meilleure moyenne).

### Manhattan (scaled)
Distance de M. mais l'anomalie est divisée par la déviation standard moyenne (
une dev stand par dimension).

### Mahalanobis
Calcul de la distance plus complexe. En gros distance Euclidienne avec des
mécanisme d'atténuation des effets des corrélations entre certaines *features*.

### Mahalanobis (normed)
aka "Normalized Bayes classifier"
Même normalisation qu'Euclide.

### Nearest-neighbor (Mahalanobis)
Distance de Mahalanobis entre chaque vecteur et le vecteur testé. L'anomalie
retournée est la distance avec le NN.

### Neural-network (standard)
IMBITABLE.

### Neural-network (auto-assoc)
PAS MIEUX.

La structure de ce réseau de neurones est adapté à la détection d'anomalies,
contrairement au détecteur précédent. En gros produit des nouveaux vecteurs
en accentuant le score d'anomalie des imposteurs.

### Fuzzy logic
On associe des intervalles de timing à des ensembles "flous". Chaque élément
peut partiellement appartenir à plusieurs ensembles. 
On calcule l'appartenance la plus forte de chacune des features à un ensemble.
L'anomalie est calculée comme la moyenne de non appartenance au set auquel la
feature appartenait le plus fortement en moyenne de toutes les features.

### Outlier-counting (z-score)
aka "Statistical technique" => pour chaque feature différence vecteur moyen /
vecteur testé, le tout divisé par la deviation standard de chaque feature.

Anomalie = combien de z-score des features on dépassé un certain seuil.

### SVM (one-class)
Imbitable

### k-means
Clustering puis est-ce que le vecteur peut appartenir à un de ces clusters.

## Evaluation methodology
### Training and testing the detectors
Sur les 51 utilisateurs, on entraine le modèle à en considérer un comme
l'authentique, et on désigne les autres comme des imposteurs.

On teste le modèle contre la moitié des tentatives utilisateurs pour faire un
*user score*, càd un score de détection des anomalies sur des samples qui n'en
sont pas.

Puis on le teste sur autant de samples d'imposteurs, pour obtenir un score
d'anomalie vs des "vrais" imposteurs.

Une itération par utilisateur est faite, avec chaque utilisateur étant considéré
comme étant l'utilisateur authentique.

### Calculating detector performance
ROC curve (Receiver Operating Characteristic = tracer FPR (False Positive Rate
== False Alarm Rate == fall-out) vs TPR (True Positive Rate == Hit rate ), 
métrique classique pour l'évaluation des performance des détecteurs.
[Voir cette page]
(https://en.wikipedia.org/wiki/Receiver_operating_characteristic)

Pour délimiter entre les anomalies et les utilisateurs authentiques, il faut
définir un *seuil* qui fixe un taux d'anomalie à partir duquel on déclenche une
alarme.🗯

Le rapport entre FPR et TPR est donc situé sur un continuum dont la valeur
finale va dépendre du seuil. Les méthodes choisies pour fixer le seuil sont :

* *equal-error rate* : les taux d'erreur sont égaux
* *zero-miss false alarm rate* : le *miss rate* est à zéro **et** on prend la
valeur minimale de *false alarm rate* en respectant cette contrainte.

## Results and analysis
### Finding the top-performing detectors
J'ai rien compris à cette partie. En gros un détecteur n'est un *top
performer* que s'il est compétitif avec le *best performer* ? 

### Detector performance comparison
Aucun des détecteurs n'atteint la performance requise par le standard européen.

Globalement les détecteurs qui performent le mieux emploient une pondération des
*features* qui varient beaucoup, avec une méthode comme Mahalanobis, ou la 
distance de Manhattan pondérée.

La méthode du Nearest Neighbor en distance de Mahalanobis est la seule méthode
qui performe bien sur les deux méthodes de sélection du seuil.

Globalement l'ensemble des méthodes évaluée est nettement divisé entre la moitié
qui performe le mieux, et la moitié qui est bof.

## Discussion and future work
### Shared data and methods
Manque criant de données et de méthodes partagées dans ce champ de la recherche.

### Extensions to the evaluation method
On peut utiliser la base de données pour évaluer autre chose que la détection
d'anomalie.

On peut aussi exclure certaines *features* du set de données qui est très 
complet, de manière à observer la performance des détecteurs avec et sans ces 
*features*.

### Detector variability across data sets
Des variations de perf majeurs peuvent résulter différences mineures dans

* l'implémentation des détecteurs;
* la donnée d'entraînement;
* la méthodologie d'évaluation (seuil de détection)

> Keystroke-dynamics is a sensitive instrument in a noisy domain.

On se retrouve avec des conclusions inverses sur les comparaisons d'algo que
les publications sur lesquelles elles s'appuient.

## Synthèse

Il existe une multitude de publications sur l'identification d'un utilisateur
sur la base de sa manière d'écrire au clavier. Chaque publication cherche à
déterminer quels algorithmes sont les plus performants, mais a aussi son propre
protocole d'acquisition des données, rendant la comparaison directe de deux
algorithmes impossible.

Cela pose un problème car le standard européen pour les systèmes de contrôle 
d'accès est très exigeant : FRR <= 1%, FAR <= 0.001 % (EN-50133-1).

Avec les techniques de biométrie comportementale actuelles, ce standard est 
assez loin d'être respecté. Cela rend impossible la commercialisation de 
dispositifs permettant d'identifier une personne uniquement sur la manière dont 
elle frappe au clavier.

Cette publication propose d'apporter à la recherche une base de données et une
méthodologie reproductible, afin de permettre les comparaisons entre les
algorithmes utilisés par les chercheurs en *keystroke dynamics*.

La méthodologie proposée se limite à l'identification d'une personne tapant un
mot de passe fixe, et les algorithmes de classifications qu'on appelle les
**détecteurs d'anomalie**. Ces algorithmes n'identifient pas une personne parmi
plusieurs possibles mais identifient si la personne est bien la bonne personne
ou non. On a donc une classification de la donnée entre deux classes :

* Utilisateur authentique ;
* Imposteurs.

Même si cette méthodologie limite quelque peu les comparaisons à une partie
spécifique de la recherche dans le champ des *keystroke dynamics*, les auteurs
soulignent que la base de données pourrait être utilisée pour des algorithmes de
classification à plusieurs classes (identifier un utilisateur parmi plusieurs).
Si la donnée rendue publique ne comporte que des utilisateurs tapant un mot de
passe fixe, les auteurs argumentent que la méthodologie pourrait être
généralisée pour acquérir la donnée d'utilisateurs tapant du texte libre.

La publication soulève un problème de taille pour l'évaluation des performances
de systèmes d'identification par frappe au clavier : un utilisateur va rentrer
son mot de passe plusieurs fois pour constituer un profil reconnaissable par
l'algorithme de détection. Cependant, pour vérifier si l'algorithme est bien
capable de discriminer un imposteur essayant de se connecter en utilisant le 
même mot de passe, il faut des données de personnes tapant le même mot de passe,
ce qui n'est pas une donnée dont on dispose dans la vraie vie. Par conséquent
constituer une base de données où tous les échantillons de tous les utilisateurs
sont basés sur le même mot de passe est artificiel, mais offre une facilité
d'évaluation des performances des algorithmes. Il faut arriver à évaluer les
performances de ces algorithmes, tout en évitant d'entraîner un modèle qui
surinterprête sur le mot de passe retenu.

La publication apporte aussi des orientations sur les protocole d'acquisition de
la donnée, notamment en soulignant l'utilisation d'une horloge externe pour
une plus grande précision, et qu'ils ont choisi de ne pas retenir les tentatives
erronnées dans la base de données. Les auteurs parlent aussi de la mise en
forme des données, soit le processus de prendre une tentative d'identification
d'un utilisateur et le transformer en échantillon exploitable par le système.

Une fois la méthodologie détaillée et le protocole de comparaison mis en place,
les auteurs présentent les différents algorithmes comparés. Ils en expliquent le
principe général et référencent les publications qui les ont implémentés.

Enfin, la publication utilise une méthode statistique pour déterminer quels sont
les algorithmes les plus performants suivant deux critères : la limitation des
faux positifs (FAR) avec  et la limitation des faux négatifs (FRR).

L'apport de cette publication est plus la méthodologie de comparaison que les
résultats de la comparaison qui sont amenés à évoluer avec la recherche. On
retiendra notamment que dans la détection entre utilisateur authentique et 
imposteur, le seuil de discrimination et la performance visée peut avoir une
forte influence. De même, le protocole d'acquisition des données peut introduire
une très forte variation des performances d'un algorithme. Donc pour évaluer
la performance d'un algorithme, il faudrait pouvoir le tester sur plusieurs 
bases de données différentes.

## Ce que je retiens

Attention au jargon et à ses définitions:
False-alarm Rate = False Rejection Rate
Miss rate = False Acceptance rate.

Attention :
Choix du pw en fonction de ce qu'il se faisait avant fait qu'on reste sur des
mdp des années 2000, trop faibles.
Travailler sur un set de données avec des utilisateurs qui rentrent le même mot
de passe ne correspond pas vraiment à la réalité, mais ça simplifie l'évaluation
des performances.

Méthode d'acquisition de la donnée :
Utilisation d'une horloge de référence externe pour augmenter la précision des
timestamps. Alors que nous on aimerait travailler uniquement sur de la
keystroke dynamics sans rajouter de hardware. (Après ils étaient sur du Windows)

Méthodologie de constitution d'un *timing vector* floue mais peut nous mettre
dans la bonne direction.

Liste des implémentations des détecteurs : explication succincte et relativement
compréhensible des algorithmes utilisés.

L'apport de cette publication est plus la méthodologie de comparaison que les
résultats de la comparaison elle-même.

Globalement le champ de la recherche est incapable de fournir une évaluation des
performances des algos utilisés qui soit directement comparable d'une
publication à l'autre.

Les conditions d'acquisition, de formalisation de la donnée, d'implémention des
algos, d'évaluation des performances sont autant de variables dont la **moindre
modification** peut entraîner une divergeance des performances finales. Il faut
donc réfléchir à des conditions qui se rapprochent de la réalité plutôt que de
conditions de laboratoires pour évaluer des systèmes amenés à être utilisés
pour de vrai.






