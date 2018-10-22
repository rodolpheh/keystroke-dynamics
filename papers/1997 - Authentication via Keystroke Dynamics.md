#Authentication via Keystroke Dynamics
###1997

Fabian Monrose - New York University  
Aviel Rubin - Bell Communications Research

[Consulter la publication](https://drive.google.com/open?id=1SOglRMStJuOhKo45ugviCsUtdOXROKlA)

##1. Contexte

En 1997, Windows95 est installé sur la plupart des ordinateurs personnels. Intel sort le processeur Pentium II avec une horloge allant jusqu’à 300 MHz.

Cette même année sortent GTA et Internet Explorer 4.0. Les ordinateurs sont là depuis assez longtemps, mais leur application commence à changer grâce à l’internet

Au moment de la publication de cet article il n’existe ni Google (1998) ni Wikipédia (2001). 

##2. Introduction


L’auteur mentionne que les possibilités que donne internet semblent illimitées. Il en tire tout de même que des nouveaux dangers apparaissent. Les mesures de sécurité courantes ne sont plus adéquates. En résultat, de nouvelles méthodes d’authentification sont fortement demandés.

Selon l’auteur, le Keystroke Dynamics est une solution pour plusieurs raisons :  
 - Les résultats des observations montrent des similitudes neuro-psychologiques entre le Keystroke Dynamics et les signatures écrites.  
- La transparence à l’utilisateur.  
- Le fait que les utilisateurs utilisent déjà un clavier.  
- Le bas coût de mise en place d’une telle solution contrairement aux méthode biométriques.  

L’auteur mentionne aussi que des travaux sporadiques ont déjà été menés sur le sujet.

##3. Methode experimentale

Les données ont été collectées sur une période de 7 semaines, les sujets utilisaient chacun leurs propres machines. Les sujets n’étaient pas spécialisés dans la dactylographie mais étaient tous familiers avec les ordinateurs. Les résultats étaient envoyé par mail aux chercheurs. Environ 60% des participants avaient conscience du but de l’expérience.

Pour la reconnaissance des profils les auteurs ont utilisé:  
- La mesure euclidienne des distances entre des vecteurs N-dimensionnels   
- Des probabilités non pondérées   
- Des probabilités pondérées   

##4. Résultat

L’analyse des probabilités pondérés, comme méthode la plus efficace dans cette étude, donne une fiabilité de 90%. Les auteurs supposent que des meilleurs résultats peuvent être atteints dans des environments plus contrôlés, comme les connexions sur les serveurs Kerberos.

##5. Conclusion vis à vis notre travail

Le Keystroke Dynamics n’est pas une technologie nouvelle. Les recherches sur le sujet ont commencés dans les années 80 du XX ème siècle.   
La méthode de calcul de probabilités pondérés peut rapporter une bonne fiabilité sur des groupes de personnes limités.

##6. Problématique

La méthode utilisée ne prends pas en compte le rejet des profils non presents dans la base de données. C’est à dire, que l’algorithme peut authentifier ou rejeter uniquement les personnes ayant déjà déposé un échantillon.   

**Pb**: Rendre l’algorithme capable de prendre l’échantillon à la volée.

