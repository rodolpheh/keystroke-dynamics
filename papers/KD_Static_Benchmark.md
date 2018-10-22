#A Review on the Public Benchmark Databases for Static Keystroke Dynamics
##Keystroke Dynamics System in a static case

A keystroke dynamics system is composed of two main modules :

- **The Enrollment** : This phase, consists in a recording of the biometrics signature of an user. In this step, the string used for the test could be a password or a text (short if possible), but already pre-defined, in order to copy it. The user types the same password several times, in order to acquire multiple samples. Those samples are used in order to create a biometric reference of the user, with the goal to identify him.    
For each input, a sequance of timing and typing information are recorded. Those records will help to know the keystroke dynamics caracteristics of the user.

- **The Verification Module**

##Comparative values between studied databases
|       Categories       | GREYC |WEBGREYC|DSN2009|BIOCHAVES|GREYC-NISLAB|
|:----------------------:|:-----:|:------:|:-----:|:-------:|:----------:|
|    Numbers of Users    |  133  |  118   |  51   |   30    |    110     |
|Duration bewteen Samples|1 week | 1 week | 1 day |    ?    |     ?      |
|   Number of Sessions   |   5   |   47   |   8   |    ?    |     ?      |
|   Number of Keyboard   |   2   |   1    |   1   |    1    |     1      |
|    Number of Samples   |12/ses | 1/sess |50/ses |   300   |    6600    |


|       Categories       |       Mean       |
|:----------------------:|:----------------:|
|    Numbers of Users    |        88        |
|Duration bewteen Samples|      1 week      |
|   Number of Sessions   |        20        |
|   Number of Keyboard   |    1 keyboard    |
|    Number of Samples   | near 23/sessions |

##Points pouvant impacter les performances d'authentification (Variances entre base de données)

- Durée d'acquisition de la base : Meilleurs résultats sur des courtes periodes, mais non réalistes
- Autorisation ou non, des fautes de frappes : Souvent non autorisé de se tromper. Pour corriger : besoin d'un grand nombre de frappe du mot erroné, sous la bonne forme afin d'entrer l'habitude de frappe du mot.
- Calme de l'endroit : Meilleures perf dans un endroit calme
- Controle de l'acquisition par un opérateur : Histoire de confiance : assurance du respect de régles.
- Mot de passe de test unique pour tous les users : Moins couteux en temps pour une acquisition et plus complexe à mettre en oeuvre. Apprentissage plus rapide de la frappe du password par les users
- OS utilisé : influence sur la précision dans les temps de captures.
- Type de clavier utilisé : Certains types de clavier ont un impact sur les performances, principalement dues à la position des doigts 
- FTAR (Failure to Acquire Rate) : FTAR elevé = FRR (False Rejection Rate) qui augmente. Peut etre un indicateur de la complexité d'un mot de passe.
- Précision du chronométre
- Types d'informations capturées

##Critères de filtres de populations

- Sexe Feminin/Masculin
- Maitrise du clavier
- Droitier/Gaucher
- Age de la personne
- Nombre d'individus impliqués dans l'etude
- Nombre de sessions durant l'etude.
- Nombre d'echantillons par utilisateur

##Critères de selection des mots de passes

- Mot de passe imposés contre mot de passe
- Complexité du mot de passe
- Entropie du mot de passe
- Complexité dans la manière de taper des mots de passes

## Performance d'une base de données
### Respect des propriétés biometriques

Il y a eu des indicateurs présentés afin de verifier la performance de reconnaissance et la qualité des echantillons

- **Unicité :** Il est basé sur la distance des échantillons d'imposteurs par rapport à
les inscriptions (le plus haut est le mieux).

>![Uniqueness formul](src/Uniqueness.png)

- **Incohérence :** Elle est basée sur la similarité entre les échantillons de requête et ceux enregistrés et dépend de la concentration et de la dextérité de l'utilisateur.
(bas est mieux).

>![Inconsistency formul](src/Inconsistency.png)

- **Discriminalité :** Elle est basée sur la distance entre l'échantillon d'imposteur le plus proche de la moyenne des échantillons authentiques et l'autre échantillon authentique (plus cet échantillon est élevé).

>![Discriminality formul](src/Discriminality.png)