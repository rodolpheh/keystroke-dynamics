# Evalutaion des systèmes biométriques

Comment sont évalués les système biométriques et comment pourra-t-on évaluer le notre.



### Indicateurs de performance

Failure To Acquire ( **FTA** ) - Échec de la capture. Dans le cas de la dynamique de frappe, il peut s’agir d’une mauvaise saisie. 

 Failure To Enroll ( **FTE** ) - Échec de l’enregistrement d’un nouvel utilisateur, principalement dû à un FTA.

### Indicateur de restrictivité

False Rejection Rate ( **FRR** ) ( moins c'est mieux )

Le FRR s’obtient en divisant le nombre de rejets lorsque l’utilisateur est légitime sur le nombre de tentatives provenant d’un utilisateur légitime.

Il indique à quel point le système est restrictif.

### Indicateur de sécurité

False Acceptance Rate ( **FAR** ) ( moins c'est mieux )

Le FAR s’obtient en divisant le nombre de confirmations lorsque l’utilisateur est un imposteur sur le nombre de tentatives provenant d’un imposteur. Il indique à quel point le système est sécurisé (plus le FAR est bas, plus le système est sécurisé).

### Indicateurs de l'usabilité

Facteur humain - l'utilisateur accepte-il d’utiliser le système

- Performances (FTA et FTE)
- Rapidité de fonctionnement 
- Facilité d’utilisation
- Sécurité
- Niveu de transparence

### Indicateurs de qualité pour un système biométrique

Fonctionnement indépendant de la **catégorie du sujet** (identique pour les femmes, pour les hommes, pour les personnes jeunes et pas pour les plus âgées, pour les peaux claires, moins pour les peaux foncées, etc.)

Impossibilité de **falsification** (ex. une photo pour un système de reconnaissance du visage)

Adaptation aux **évolutions du sujet** ( lorsque qu’il change de morphologie)

Resistance aux **différences de matériel** (clavier different, connexion internet, qualité du matériel)

Invariance selon les **environnements** (humeur de la personne, une autre période du jour en particulier)

### Standards pour l'évaluation des systèmes biométriques

Le standard ISO existe, mais est consultable seulement après l’achat.

**ISO/IEC 19795-1:2006** qui sera remplacé par  **ISO/IEC WD 19795-1** (Biometric performance testing and reporting)

### Ce qu'on doit prévoir en consequence dans notre système

Les statistiques de performance, FTA et FTE pour l’usage.

Les statistiques de la sécurité et de la restrictivité, mais qui peuvent être évalués uniquement pendant les tests quand la légitimité d’un essai est connue d’avance.

Quelque chose pour détecter si c’est bien un humain qui fait la tentative, pour empêcher la falsification ( pas sur si une telle vérification sera possible ).

Mise à jour de l’empreinte lors de le connexion légitime pour s’adapter aux changement de morphologie du sujet, comme le FaceID

Plusieurs empreintes pour la même personne provenant des environments et du materiel different

Fonctionnement le plus transparent possible pour que l’usage soit satisfaisant

#### Sources

Indicateurs FRR FAR - [https://tel.archives-ouvertes.fr/tel-01007679/document](https://tel.archives-ouvertes.fr/tel-01007679/document)

Marqueurs de qualité - [https://www.gemalto.com/france/gouv/inspiration/biometrie](https://www.gemalto.com/france/gouv/inspiration/biometrie)
