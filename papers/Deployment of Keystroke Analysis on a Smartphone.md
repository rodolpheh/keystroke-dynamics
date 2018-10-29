# Deployment of Keystroke Analysis on a Smartphone

A. Buchoux
University of Plymouth

N.L. Clarke
Edith Cowan University

2008

## Spoiler alert

Pour une bonne balance entre la performance et l'efficacité, les classificateurs statistiques sont les plus intéressants. Attention, ce document a été écrit en 2008, les performances ont grandement évoluées depuis. L'efficacité des méthodes mises en places dans le document restent valables, même d'après les standards d'aujourd'hui.

## Introduction

Les auteurs partent du postulat qu'avec le développement de la technologie du mobile, celui-ci est devenu un point d'entrée vers des données sensibles (personnellement et financièrement). À cet effet, ils prévoient une augmentation de la complexité des systèmes d'authentification pour mobiles afin de répondre à un risque de plus en plus grand.

Il existe, selon Wood, trois approches à l'authentification : 

* Utiliser ce que l'utilisateur sait
* Utiliser ce que l'utilisateur a
* Utiliser ce que l'utilisateur est

Cette dernière approche est la biométrie.

Selon les auteurs, une meilleure approche de la sécurité serait une sécurité multi-factorielle. Dans ce document, l'approche utilisée sera une approche bi-factorielle, utilisant un mot de passe et les données de frappe au clavier. Cette approche sera implémentée sur un téléphone portable.

## Revue de la littérature

Les auteurs font une revue de la littérature autour des keystroke dynamics et liste les scores de FAR et FRR obtenus en fonction de la technique de classification, des données mesurées, du nombre de sujet et de la méthode utilisée (statique ou dynamique). La revue de ces documents leur permet de conclure qu'il est conseillé d'utiliser les données de latence et de hold-time des touches, sauf pour les mobiles, pour lesquels seul la latence importe (Karatzouni et al. (2007)).

## Méthodologie

Le matériel utilisé est, en termes de performances et d'après les standards actuels, plutôt faible. Nous n'allons donc pas décrire l'ensemble de la méthodologie qui concerne surtout le matériel et le logiciel utilisé. Nous retiendrons que les classificateurs utilisés sont des algorithmes basés sur la distance Euclidienne, la distance de Mahalanobis et un réseau de neurones de type Feed-Forward Multi-Layered Perceptron (autrement dit, le type de réseau de neurones le plus basique et le plus courant).

L'expérience commence par la prise de 20 mesures par utilisateur, pour les données d'entraînement, et de 10 mesures supplémentaires pour les données de test.

## Résultats

Les auteurs observent un rapport de 10 entre les temps d'enregistrements des différents algorithmes (2 secondes pour la distance de Mahalanobis contre 210 secondes pour un réseau de neurones simples). Le temps de vérification est quasi-instantané avec les distances Euclidienne et de Mahalanobis. Les FAR et FRR sont biens meilleurs lorsqu'on utilise tout le clavier alphanumérique plutôt que juste le clavier numérique. La différence entre les méthodes par distance Euclidienne et distance de Mahalanobis n'est pas assez significative pour en tirer une conclusion. Pour des raisons de performances, le réseau de neurones n'a pas été évalué.

## Conclusion

Les auteurs concluent qu'il est possible d'implémenter une authentification combinant mot de passe et frappe au clavier, à condition d'utilise tous les caractères (pas d'approche par code PIN). Aujourd'hui, les performances des téléphones pourraient permettre de refaire l'étude et de la compléter avec des résultats sur l'utilisation d'un réseau de neurones.