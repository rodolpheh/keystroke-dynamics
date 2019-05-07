# One-class SVM for biometric authentication by keystroke dynamics for remote evaluation

Chang C., Eude T.

Détection d'imposteur à distance basée sur un algorithme One-Class SVM (State Vector Machine)

## Intro

Dispositif qui peut échouer en deux situations : si la bonne personne se voit refuser l'accès, et si une mauvaise personne obtient l'accès.

Avantage de méthode de détection biométrique : automatique et ce qui permet l'authentification ne peut pas se perdre. Faible coût d'implémentation et de déploiement. + "non-invasiveness" : la méthode n'est pas invasive pour l'utilisateur final.

## Méthode d'identification *keystrokes dynamics*

### Données d'entrées

Dynamique ou statique. Statique permet d'atteindre des perfs bien meilleures et bien plus simple à implémenter. Ajouter à ça que les performances augmentent quand le comportement est le plus régulier possible : on choisit donc des séquences de frappe que les utilisateurs ont l'habitude de taper, comme leurs noms et prénom, et qui sont à la fois légèrement plus longues que 6 caracètres, sans que ça devienne trop long (plus d'erreurs). Cela permet d'obtenir les taux d'erreurs les plus faibles. Variabilité augmente quand on demande d'entrer un texte que l'utilisateur n'a pas l'habitude de taper.

D'où le choix de l'identifiant numérique des étudiants.

Processus comporte :

* phase d'enregistrement / *enrollment* (entraînement / *training*)
* phase de vérification / *verification* (test)

### Extraction des caractéristiques

Capture :

* *Dwell time* / Temps de pression : durée entre le moment où la touche est enfoncée jusqu'à ce qu'elle soit relachée.
* *Flight time* / Temps de transition : durée entre le moment où une touche est relachée et qu'une autre soit enfoncée.

Utilisation de JS avec une résolution d'1ms

### Classification

SVM recherche un hyperplan permettant de délimiter les vecteurs de données de l'utilisation des données d'imposteurs dans l'espace dimensionnel des données.

La recherche des hyperparamètres permettant de trouver le plan relève de maths que je ne comprends pas.

SVM très performant grâce à des optis qui permettent de travailler sur des données de dimension importante sans être aussi demandeur en ressources que les réseaux de neurones.

## Collection des données

### Données "positives"

"Ripple effect" p.4 et 5

L'avantage de collecter les séquences de frappe uniquement à chaque connexion de l'utilisateur à la plateforme web permet d'éviter d'introduire un biais dans les données qui apparaît quand quelqu'un tape plusieurs fois de suite le même texte. (On évite de biaiser les données avec des inputs "trop bons").

Mais c'est pas exactement compatible avec le cas d'utilisation qu'on présente du fait qu'ils stockent aussi la chaîne de caractère qui n'est pas une donnée confidentielle dans le cas présent.

### Données "négatives"

Utilisation de la même méthode pour créer des données d'imposteurs. Juste des personnes différentes.

Prise en considération de l'influence éventuelle des différents moments de la journée sur les données.

## Méthodologie

### Classification en classe unique

On n'a pas toujours accès à des données d'imposteur pour entraîner des systèmes de reconnaissance biométrique.

Du coup les données négatives n'ont été collectées qu'à des fins de test et pas d'entraînement. Un tel système est évalué comme performant s'il arrive à identifier les anomalies sans y avoir été préparé spécifiquement. On appelle ça de la *novelty detection* (litt. "détection de nouveauté").

Encore des considérations statistiques / mathématiques que je ne saisis pas.

### Affinement des hyper-paramètres et kernel RBF

RBF (*Radial Basis function* ou fonction de base radiale / Fonction radiale de base ?)

Encore des maths que je comprends moyen. Mais bon ça a l'air important hein.

En gros il faut affiner les paramètres pour trouver les situations dans lesquels ont évite l'*overfitting* (surapprentissage) et l'*underfitting* (sousapprentissage). Manque de pertinence dans le traitement des données par rapport à ce qu'on évalue (histoire de manque de dimensions d'évaluation).

### Protocole expérimental

Traitement préalable des données pour atténuer le bruit qu'on peut y trouver.

Une méthode statistique de Joyce et Gupta pour évaluer si les timings sont valides ou pas au moyen de la déviation standard (sigma). Permet de jeter les séquences correspondant à un comportement inhabituel.

On sépare les données positives : entrainement / test. Test est associé aux données négatives qui ne font de toute façons pas partie des données d'entrainement. Proportion équivalente d'imposteurs et de données légitimes dans les tests.

Avec les données d'entraînement l'algorithme affine les hyper-paramètres du modèle en utilisant une méthode appelée ***5-fold cross-validation** (litt. "Quintuple Validation Croisée"). On cherche la paire de paramètres qui fonctionne le mieux sur les données d'entraînement.

Puis on évalue le modèle face aux données de tests. L'évaluation de la performance pour l'algorithme One-class SVM s'appelle "*recall*" plutôt que le plus classique "*accuracy*". C'est dû au fait qu'il n'y a pas d'imposteurs sur lesquels l'évaluer il me semble. C'est pas vraiment expliqué.

D'après un [article de Wikipédia](https://en.wikipedia.org/wiki/Precision_and_recall) ([Version française précision/rappel](https://fr.wikipedia.org/wiki/Pr%C3%A9cision_et_rappel))la différence relève de :

* *precision* = nombre d'échantillons pertinements sélectionnés / tous les échantillons sélectionnés
* *recall* = nombre d'échantillons pertinement sélectionnés / nombre d'échantillons pertinents qui pouvaient être seletionnés.

Attention :

*precision* : Vrais positifs / population d'échantillons positifs
*accuracy* : Vrais positifs + vrais négatifs / population totale

Il faut voir ce que ce papier appelle "*accuracy*" parce que j'ai l'impression qu'ils parlent de précision en fait.

## Résultats

Chiffres sur les données sélectionnées.

RQ : Nous on avait pas vraiment les mêmes moyens organisationnels et temporels.

### Recherche par quadrillage (*grid search*)

Il n'y a pas d'algo opti pour la recherche des hyper-paramètres du modèle.

Explication du quadrillage utilisé :

* Variation de $\gamma$ sur $[2^{-40} ; 2^{-13}]$par pas de $2^{1}$
* Variation de $\nu$ sur $[2^{-10} ; 2^{-10}]$par pas de $2^{0.1}$

Je comprends pas si ces hyper-paramètres sont sélectionnés **pour chaque IDUL** (numéro d'identification utilisé comme donnée), ou **pour toutes les situations dans lesquelles on utilise un IDUL**.

Suit l'explication de l'évaluation des modèles une fois sélectionnés les meilleurs hyper paramètres. D'abord recall en l'absence de données d'imposteurs, puis évaluation de l'*accuracy* avec les données d'imposteurs générées.

Corrélation entre diminution du nombre d'échantillons sur lequels travailler et la précision finale du modèle. Mais difficile de faire une corrélation entre *recall* et *accuracy*.

Problème de la recherche par quadrillage est le coût qui explose par nombre d'hyper-paramètres à affiner.

### Méthode indirecte dite "DFN"

Trouver des meilleures méthodes que recherche par quadrillage

Celle-ci est assez peu adaptée aux données (à cause d'une grande dispersion des données et de leur caractéristique temporelle)

### Méthode directe dite "DTL"

Espèce de recherche binaire pour trouver les bons paramètres.

Mais marche surtout pour l'affinage d'un seul paramètre avec l'autre fixé.

### Recherche DTL "gloutone" (*greedy search*)

Permet d'exploiter l'avantage de la méthode précédente tout en pouvant varier l'autre paramètre.

Comparaison avec les perf de la recherche par quadrillage. Cette méthode est plus robuste que la méthode par quadrillage (métrique : déviation standard). C'est aussi la méthode qui minimise les faux positifs.

## Conclusion

Super papier qui nous apporte beaucoup d'information, notamment sur la méthodologie à avoir lors de la constitution d'un jeu de données tels, de leur exploitation et sur la manière d'évaluer les modèles en découlant. Et aussi comment optimiser la recherche des paramètres.

Surtout trois méthodes d'évaluation qui reposent **uniquement sur les données d'utilisateurs légitimes**.

Problématiques d'entraînement de modèles pour l'identification d'utilisateurs dans un tel contexte ne repose pas nécessairement sur la quantité d'échantillons capturés pendant la phase d'entraînement. L'homogénéité des échantillons capturés est beaucoup plus importante.

**Il y a donc de l'ingénierie à réaliser et des études d'acceptabilités à mener** pour trouver les cas d'utilisation adaptés à ce type d'identification sans que ça ne devienne par trop invasif.

Bons résultats des modèles produits mais pas du niveau des normes de certification.