# Keystroke Dynamics Authentication

## Romain Giot, Mohamad El-Abed, Christophe Rosenberger

### 2014

#### [Fig. 2. Topology of keystroke dynamics families](https://hal.archives-ouvertes.fr/hal-00990373/document#page=5)

```mermaid
graph LR;
	A[Keystroke Dynamics]-->B[Dynamic authentication]
	A-->C[Static authentication]
	B-->D[Continuous authentication]
	B-->E[Random password]
	C-->F[Two classes authentication]
	C-->G[One class authentication]
```

#### [Fig. 4. Topology of keystroke dynamics sensors of the literature](https://hal.archives-ouvertes.fr/hal-00990373/document#page=9)

```mermaid
graph LR;
	A[Keystroke Dynamics Sensor]-->B[Computer]
	A-->C[Mobile]
	B-->D[PC/Laptop keyboard]
	B-->E[Microphone]
	B-->H[Numeric keyboard]
	C-->F[Touch screen]
	C-->G[Mobile keyboard]
	H-->I[Pressure sensitive]
	G-->J[All the keys]
	G-->K[Numeric keyboard]
```

#### [Fig. 5. Topology of factors which may impact the accuracy of the timer](https://hal.archives-ouvertes.fr/hal-00990373/document#page=9)

```mermaid
graph LR;
	A[Timer variations]-->B[Operating System]
	A-->C[Type]
	A-->D[Language]
	C-->E[Desktop application]
	C-->F[Mobile phone]
	C-->G[Web based application]
	D-->H[Native]
	D-->I[interpreted]
```