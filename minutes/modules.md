# Modules

## Module d'acquisition du profil
Capture du profil utilisateur : Protocole de capture nombre de tentatives, rejet
des échecs ou pas

Application de Rodolphe pour la captation des événements de clavier.

Une fois qu'il est validé on utilise Python et Scikit-learn avec ses algorithmes

Si on ne connaît pas le mdp et qu'on le capture à l'aveugle, comment on fait
pour capturer des échantillons sans erreurs (avec des events backspace) ?

=> on ignore les tentatives avec backspace.

Si on favorise la capture de frappe exacte (uniquement le minimum d'évenements
clavier) alors on exclut les tentatives légèrement ratées dans l'utilisation
quotidienne -> moins agréable
Si on accepte aussi les mdp valides mais avec des events surnuméraires
(backspace), alors c'est plus dur à traiter et avoir des meilleures perfs mais
c'est plus pratique d'utilisation. => on essaye sans d'abord et on verra ensuite


## Stockage du profil
BDD ? Comment qu'on fait ? Chiffrer. Sécurité importante etc.

## Interface avec la saisie de mdp
Comment on laisse la main au système **après** avoir récupéré les événements ?
Est-ce que c'est possible ?

## Vérification du mot de passe préalable
Qui doit le faire ? Le système ou nous ? Si c'est nous :

### Stockage du mdp
Hashage du mdp AES 256 avec le mdp de l'utilisateur.

## Module de vérification du profil

Extraction du modèle de ML entraîné depuis sa version chiffrée.
Puis vérification de la donnée entrante sur le modèle.
Validation ou pas

## Vieillissement du profil
On utilise une question secrète ?
Gestion des faux négatifs ?
Répétition de tentatives doit rester acceptable

Au bout de 3 fois (par exemple) => question secrète.

Tentatives ratées précédant une tentative réussie => stockée. (Avec une durée
de validité max par ex: les trois tentatives sont espacées max de 1 min).

# Critères d'évaluation
## S'insérer dans les benchmarks qui existent

* Killourhy & Maxion
* GREYC

-> Évaluer les performances des algos utilisés avec ces bases. 
Utiliser les mêmes métriques d'évaluation que ces travaux.

## Deux évaluations différentes
### Recherche du meilleur algo pour faire ce qu'on veut
### Démonstration de la généricité de l'algo
Est-ce que l'algo est capable d'être efficace y compris sur des mdp qui ne sont
pas dans les BDD publiques ?
Quelle data ? Comment qu'on fait ?

#### Protocole et Module d'acquisition d'autres data que les BDD publiques
Problème d'acquisition de la donnée supplémentaire
