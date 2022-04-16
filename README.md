# Optimal generation of Gottesman-Kitaev-Preskill states
Gottesman-Kitaev-Preskill (GKP) states are hard to generate, and most of the schemes proposed
in the literature require post-selection, which makes them highly probabilistic. Using the Python
library Strawberry Fields, we have benchmarked the breeding protocol proposed by Vasconcelos
et al, which could potentially be implemented without post-selection via a phase estimation
algorithm. This scheme uses catstates to generate GKP states. We compare this protocol with
Gaussian boson sampling (GBS), and we present an estimate of the circuit parameters which would
produce a fault-tolerant GKP state: number of iterations n = 7, and a catstate amplitude a = 21 ±
6. Three different optimization algorithms were used in the process of obtaining these parameters,
and Bayesian optimization was found to be the most efficient one. Even though our findings indicate
that the probability of success of breeding is higher than the one of GBS, the circuit parameters
which we obtained are still far beyond current experimental capabilities. This investigation also
raises the question of whether generating “simple” non-Gaussian states to produce more complex
non-Gaussian states provides with a higher probability of success and a better scaling to the fault
tolerant regime than directly converting Gaussian resources into arbitrary non-Gaussian resources.
