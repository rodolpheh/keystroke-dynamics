# Typing Patterns : A Key to User Identification
Alen Peacock, Xian Ke, Matthew Wilkerson, MIT

Les *Keystroke dynamics* font partie d'une nouvelle génération de solutions pour
l'identification des utilisateurs, face aux problèmes de sécurité accrus des
mots de passe. Cependant ce champ de la recherche a encore beaucoup de défis à
relever avant que ce facteur d'identification soit pleinement accepté.

Le système d'authentification habituel repose sur le nom d'utilisateur et le
mot de passe, et sa fiabilité repose sur la confidentialité du mot de passe, et
parfois du nom d'utilisateur.

> Over the past 25 years, researchers have developed authentication systems 
based on keystroke dynamics with the hope that they would improve traditional
password system security while increasing (or at least not decreasing) usability.
*Keystroke dynamics* measure typing characteristics that are believed to be
unique to an individual's physiology and behavior, and thus difficult to
duplicate.

Difficile comparaison de toutes les études indépendantes menées à ce jour.

L'intérêt commercial de cette technologie a été bien identifié par l'industrie
qui a posé plusieurs brevet en prévision. La recherche est, dans l'ensemble,
optimiste vis-à-vis de ses potentialités.

Cependant ce domaine de la recherche fait face à de nombreux problèmes que cette
publication va s'attarder à les inventorier.

## Applications
### Authentication
*Keystroke dynamics* intéressantes pour l'authentification du fait de sa
transparence : on dispose de données que l'utilisateur a l'habitude d'utiliser,
à savoir son mot de passe et son nom d'utilisateur. Le web en particulier est
un domaine intéressant pour ce genre d'application, car cela permettrait
d'ajouter un niveau de sécurité dans un contexte où on ne peut pas rajouter
de hardware supplémentaire.

[La faisabilité d'une telle utilisation a déjà été démontrée dans *Keystroke 
Dynamics: A Software-Based Biometric*, X. Ke et al. (2004)]. Le code source
est censé être disponible mais c'est difficile à trouver en ligne car l'URL 
n'est plus valable.

Problème de scalabilité des solutions d'authentification par *keystroke
dynamics* : les applications web peuvent avoir un nombre très important
d'utilisateurs alors que les systèmes de *keystroke dynamics* sont éprouvé pour
un nombre limité d'utilisateurs.

Base de données évolutives avec une question secrete quand le mot de passe est
le bon mais le *keystroke dynamics* échoue : problème du vieillissement de la
donnée.

### Identification and monitoring
Les *keystroke dynamics* sont aussi intéressants pour l'identification à savoir
déterminer l'identité d'une personne parmi un ensemble de personnes disposant
de l'autorisation d'accès.

C'est un domaine dans lequel l'identification sur une session de frappe au
clavier libre et continue est intéressante. On peut imaginer des systèmes de
sécurité qui pourraient permettre d'identifier quand l'utilisateur a changé,
par exemple quand l'utilisateur principal a oublié de verrouiller sa session
et qu'un imposteur essaye d'en profiter.

Le *keystroke monitoring* pourrait aussi permettre de détecter des changements
de l'état physique ou mental de certains opérateurs dans des activités
dangereuses, afin de compléter la supervision humaine par de la supervision
assistée par ordinateur (Voire Monrose Rubin *Keystroke Dynamics as a 
Biometric for Authentication, 2000).

### Password hardening
Créer de meilleurs mots de passe en se basant sur le profil de frappe au clavier
de l'utilisateur (Cf Monrose, Reiter, Wetzel, 1999 "Password Hardening Based 
on Keystroke Dynamics"). Cela permettrait par exemple d'inclure des caractères
invisibles dans le mot de passe final, comme des caractères qui seraient tapés
puis supprimés.

### Beyond keyboards
Possible d'étendre cette recherche aux téléphones, tactile, PINs de CB, etc.

## Evaluating previous research
La recherche en *keystroke dynamics* s'est surtout concentrée à évaluer les
différents dispositifs de classification disponibles, allant de méthodes 
d'analyse statistique aux réseaux de neurones. Le principe général est d'évaluer
la similarité entre un modèle de référence et un profil de frappe au clavier
entrant.

### Classifier accuracy
Les métriques utilisées pour évaluer la précision du classificateur utilisé
sont :

* FRR False Rejection Rate, soit le pourcentage des tentatives d'utilisateurs 
authentiques identifiées comme des tentatives d'imposteurs ;
* FAR False Acceptance Rate, le pourcentage des tentatives d'imposteurs 
identifiées comme des tentatives de d'utilisateurs authentiques
* ERR Equal Error Rate : FAR/FRR = 1

La publication souligne l'inconstance des métriques (et de la terminologie 
qui leur est associée) utilisées par les chercheurs du domaine. Ils suggèrent
de suivre les recommandations suivient par le domaine de la biométrique en
général. (Manfield 2002, "Best Practices in Testing and Reporting Performance
of Biometric Devices").

En plus de FAR, FRR et ERR, les auteurs poussent à utiliser les courbes ROC
(Receiving Operator Characteristic) et DET (Detection Error Trade-Off).

Parmi les publications inventoriées, les systèmes les plus performants
arrivent à atteindre un AFR (Average False Rate) aux environs de 2 %, ce qui 
est une performance respectable pour un système biométrique.

### Usability

Métriques pour évaluer la commodité de mise en place d'un système biométrique.

* FTR Failure To enroll Rate : le pourcentage d'utilisateur n'arrivant pas à
s'enregistrer dans le système faute d'une qualité suffisante dans les tentatives
* FTA Failure To Acquire Rate: le pourcentage des utilisateurs pour lequel le
modèle n'arrive pas à intégré le profil, une fois l'acquisition faite.

Assez peu utilisés dans les travaux.

Les auteurs proposent des nouvelles métriques :

* CUE Cost to a User to Enroll : le nombre de tentatives à soumettre pour que
l'engagement de l'utilisateur soit considéré comme valide :
* CUA Cost to a User to Authenticate : le nombre de tentatives qu'un utilisateur
doit soumettre à chaque fois qu'il cherche à s'identifier.

Ces métriques permettent de chiffrer le travail à fournir par l'utilisateur
final.

### Confidence in reported results

La grande variété dans ce domaine de la recherche rend difficile l'évaluation
des résultats annoncés d'un papier à l'autre : par exemple est-ce qu'une
précision de 100 % d'un système qui n'a été évalué que sur un ensemble de 5
utilisateurs est préférable à une fiabilité de 99% d'un système testé sur plus
de 3000 personnes ?

Les métriques à prendre en compte pour se donner une idée de la fiabilité des
résultats sont :

* Taille de l'échantillon ;
* Nombre de tentatives d'accès d'utilisateurs authentiques ;
* Nombre de tentatives d'accès d'imposteurs ;

C'est sur ce sujet que la recherche dans le domaine fait clairement défaut :
assez peu de publications font état d'un test avec plus de 25 utilisateurs.
Cela fait qu'on est assez loin de la réalité d'un service web avec plusieurs
millions d'utilisateurs. Le manque de données pose aussi un problème
de *benchmark* des solutions étudiées.

## Intellectual property and the current market landscape
(Plus vraiment d'actualité)

On prévoit que le marché de la sécurité biométrique va passer d'un million de
dollars en 2004 à 4.6 milliards de dollars en 2008. Pourtant les *keystroke
dynamics* ne semblent pas faire partie de cette tendance, malgré les faibles
coût d'acquisition et de traitement de ce genre de données.

Les brevets sont bien présents mais pourraient être plus nocifs que bénéfiques :
l'un des auteurs s'est vu attaqué en justice pour qu'il retire le code source
associé à une de ses publications par le détenteur d'un des brevets enregistrés.

(Description extensive de certains brevets).

## Privacy and security issues
Le principal problème de sécurité est celui de la sécurité de la base de données
stockant les profils de frappe au clavier. Un attaquant disposant de cette
information pourrait arriver à déduire un mot de passe qu'il n'avait pas avant.


## Conclusion
Malgré la déjà longue histoire (+25 ans) des *keystroke dynamics*, le domaine
est toujours en pleine maturation. Le manque de bases de données de référence
commune à l'ensemble de la recherche sur le sujet, ainsi que l'absence de
métriques communes pour comparer les performance, ont empêché le développement
de la collaboration et de la vérification par les pairs dans ce champ de la 
recherche en biométrique.

Il reste que les *keystroke dynamics* sont prometteurs du fait de leur faible
coût d'acquisition et de traitement, comparativement aux autres informations
biométriques couramment utilisées. L'avantage principal restant la transparence
du point de vue de l'utilisateur, amenant à une plus grande acceptation de la
part du public.

Liste de choses à faire pour que les *keystroke dynamics* soient plus largement
adoptés : 

* Mesures de fiabilité sur des ensembles d'utilisateurs beaucoup plus larges ;
* Partage de bases de données à l'ensemble du champ de la recherche, afin 
d'éviter que les chercheurs doivent passer leur temps à réunir des échantillons
plutôt qu'à parfaire les méthodes de classification ;
* Installation de méthodes et de bonnes pratiques pour la protection des données
utilisées par les *keystroke dynamics*
* Péremption de brevets et de proprié.

## Synthèse

Depuis 25 ans, les chercheurs ont développé des systèmes d'authentification
basés sur les *keystroke dynamics* en voulant renforcer les systèmes basés sur
nom d'utilisateur et mot de passe. L'intention est de se baser sur des
caractéristiques comportementales de l'utilisateur, réputées non imitables, pour
venir renforcer le système d'authentification par mot de passe, sans en diminuer
sa commodité d'utilisation.

Cependant le champ de la recherche en *keystroke dynamics* a encore à surmonter
de nombreux défis pour que cela devienne une méthode d'authentification
biométrique plus utilisée.

Les auteurs de cette publication s'attachent à répertorier les tendances
associées aux recherches en *keystroke dynamics*, à la fois pour en souligner
certain problèmes que pour proposer des solutions.

Les applications des *keystroke dynamics* gravitent autour de :

* **l'authentification**, soit l'utilisation des *keystroke dynamics* comme 
alternative ou comme renfort au mot de passe ;
* **l'identification**, soit la distinction d'un utilisateur parmi plusieurs
connus par le système, au moyen des informations de frappe au clavier. Cette
catégorie pouvant aussi regrouper la **supervision**, soit la détection d'un
changement d'utilisateur au cours d'une session, ou l'altération du comportement
d'un utilisateur.

Les principaux problèmes de la recherche sont associés aux moyens d'évaluation
des résultats des différentes publications. Les métriques utilisées pour
évaluer les méthodes d'authentification biométriques sont assez peu maîtrisées
par les chercheurs en *keystroke dynamics* et les auteurs de l'article donnent
des références afin de consolider l'évaluation des performances des différents
systèmes développés.
De plus, le manque de base de données commune à ce champ de la recherche rend
la comparaison et la reproduction des résultats très limitée. La constitution
des échantillons est un poids à porter par les chercheurs et implique une
logistique et un protocole complexe, ce qui limite le temps dédié à améliorer
la fiabilité du système d'authentification lui-même.
Les auteurs soulignent notamment que la plupart des jeux de données constitués
par les chercheurs se limitent à environ 25 utilisateurs, tandis que la réalité
d'un service web est de fournir un accès à des millions d'utilisateurs.

Enfin, une autre catégorie de problèmes plus difficiles à évaluer regroupent :

* les brevet et la propriété intellectuelle attachée à certaines formes de
dispositifs d'authentification par *keystroke dynamics* qui empêchent les
chercheurs de diffuser leurs publications, leurs données et leur code source ;
* l'acceptation par le public de dispositifs enregistrant le comportement ;
* la protection et la confidentialité des données de frappe au clavier des
utilisateurs.

Cette publication nous apporte un tour d'horizon des challenges posés par les
*keystroke dynamics* et qui attendaient encore résolution en 2004. Aujourd'hui,
on sait que des chercheurs ont essayé de développer des bases de données pour
répondre à certains de ces problèmes. Mais cela ne signifie pas qu'ils sont
résolus pour autant. Cela nous apporte un panorama des points sur lesquels notre
travail se devra d'être exigeant.
