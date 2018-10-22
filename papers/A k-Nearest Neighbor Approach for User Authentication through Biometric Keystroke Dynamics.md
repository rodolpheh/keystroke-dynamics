# A k-Nearest Neighbor Approach for User Authentication through Biometric Keystroke Dynamics

J.Hu, D.Gingrich

School of Computer Science and IT, RMIT University, Melbourne, Australia

## Abstract

FAR et FRR trop hauts dans le domaine des keystroke dynamics. Améliorés avec les travaux de Gunetti et Picardi mais problème de scalabilité. Les auteurs de la publication utilise une approche kNN pour obtenir des résultats identiques à Gunetti et Picardi mais avec une amélioration de 66.7% de la vitesse d'authentification.

## Introduction

L'utilisation d'un mot de passe permet de vérifier qu'un utilisateur possède l'information attendue mais ne permet pas de vérifier si l'utilisateur est légitime ou pas (il y a 20 ans on pensait que posséder le mot de passe était une preuve de légétimité, ce genre de raisonnement pourra s'appliquer dans 20 ans pour les systèmes biométriques tel que les empreintes digitales ou le visage, jusqu'où ira-t'on dans cette logique ?).

La variabilité et l'instabilité des keystroke dynamics entraîne un bottleneck technologique.

Bergadano utilise 680 caractères pour le texte d'entraînement. Il mesure le rythme de frappe des différents trigraphes et les ordonne. L'ordre des trigraphes est utilisé pour le processus d'authentification, ce qui permet de supprimer la dimension temporelle. Il appelle cette technique Degree of Disorder.

Gunetti et Picardi étendent cette idée en intégrant tous les n-graphes. FAR de 5% et FRR de 0.005%.

Ce papier propose d'utiliser une classification en kNN. Même performances que Gunetti et Picardi avec une performance améliorée de 66.7%.

## Classification par kNN

La classification est souvent utilisée comme outil de vérification dans le domaine de la biométrie. La méthode de kNN (k-Nearest Neighbours ou k plus proches voisins) est une méthode de classification simple basé sur la distance entre une nouvelle mesure et les mesures déjà obtenues. Pour classifier notre nouvelle mesure, on calcule la position moyenne entre les k voisins les plus proches de notre mesure.

CKAA : Clustering based Keystroke Authentication Algorithm.

Construction des profils utilisateurs :

* Chaque utilisateur entre plusieurs échantillons. Chaque échantillons comporte n-graphes. On fait la moyenne des différents n-graphes et on les tris.
* Un profile est constitué à partir de la moyenne des vecteurs obtenus précédemment.

Authentification : pour confirmer l'authentification d'un utilisateur, on compare l'échantillon X capturé aux regroupements et au profil A qu'il prétend être. Il faut que A soit dans le group le plus proche de X et la distance (A, X) doit être la plus proche de la moyenne de A dans ce groupe.

## Conclusion

CKAA permet d'obtenir des bons résultats en terme de FAR et de FRR tout en améliorant sensiblement la vitesse d'authentification.