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