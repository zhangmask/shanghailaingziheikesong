# 量子降阶滤波 - 深度提取内容

**论文ID**: arXiv 2511.07949

**总页数**: 27

---

## 引言/概述

```

--- 第1页 ---
Stabilization of Time-Varying Perturbed Quantum Systems via
Reduced Filters
Weichao Liang ∗ Daoyi Dong †
Abstract
In practical applications, quantum systems are inevitably subject to significant uncer-
tainties, including unknown initial states, imprecise physical parameters, and unmodeled
environmental noise, all of which pose major challenges to robust quantum feedback control.
This paper proposes a feedback stabilization strategy based on a reduced quantum filter
that achieves robustness against time-varying Hamiltonian perturbations and additional
dissipative effects, without requiring prior knowledge of the initial state or exact system
parameters. The proposed filter estimates only O(N) real variables corresponding to the
diagonal elements of the system density matrix in a quantum non-demolition basis in
contrast to the O(N 2) variables required by a full stochastic master equation, where N
is the Hilbert space dimension. This dimensionality reduction substantially simplifies
real-time computation and feedback implementation while preserving both convergence
and robustness guarantees. Rigorous analysis further establishes global exponential sta-
bility of the target subspace. The results provide a scalable framework for robust and
efficient measurement-based feedback control applicable to high-dimensional perturbed
open quantum systems.
1 INTRODUCTION
The theory of open quantum systems [ 11], describing systems interacting with an external
environment, has profoundly impacted quantum information science [ 31]. Such interactions
inevitably induce quantum dissipation and decoherence, leading to information loss, one
of the most critical challenges in quantum control and quantum computation. Developing
feedback control strategies to mitigate decoherence is crucial for the scalability and reliability
of quantum technologies, including quantum computing, quantum chemistry, and quantum
information processing [13, 1].
A widely adopted framework for analyzing quantum control in the presence of continuous
measurement is based on Stochastic Master Equations (SMEs) [6, 10, 3]. In this framework, an
open quantum system interacts with its environment and a probe system, where the probe sys-
tem is continuously monitored. SME-based feedback control has been a key enabler for various
quantum technologies [46], leading to significant advances in various domains [ 46]:Quantum
state protection, extending coherence lifetimes [ 45] and protecting macroscopic Schr¨ odinger cat
∗W. Liang is with the School of Automation Science and Engineering, Faculty of Electronic and
Information Engineering, Xi’an Jiaotong University, Xi’an, 710049, Shaanxi, P.R. China (e-mail:
weichao.liang@xjtu.edu.cn).
†D. Dong is with Australian Artificial Intelligence Institute, Faculty of Engineering and Information
Technology, University of Technology Sydney, Broadway, Ultimo, 2007, New South Wales, Australia,
(daoyidong@gmail.com).
1
arXiv:2511.07949v1  [math-ph]  11 Nov 2025

--- 第2页 ---
states [32];Quantum error suppression and correction, mitigating decoherence and enabling
real-time error suppression [ 27];Quantum simulation, stabilizing Bose-Einstein condensates
to improve quantum simulations of condensed matter systems [ 38];Quantum transport in
nano-structures: offering new opportunities in quantum device engineering;Quantum sensing
and metrology, increasing sensor sensitivity [ 14];Entanglement distribution, enabling robust
remote entanglement generation and stabilization, critical for quantum communication and
distributed computing [35]. Recent research has also explored its role in connecting gravity
and quantum matter in the so-called Newtonian limit [33].
Despite these successes, two major challenges remain for the practical implementation of
SME-based feedback control:
• Computational complexity of quantum filtering: Traditional full-state quantum filters
track O(N 2) parameters for an N-level quantum system, making real-time feedback
control infeasible for large quantum systems [ 43]. Several model reduction methods have
been proposed to address this challenge [ 44, 30, 15, 16, 2, 17], but their applicability
remains restricted.
• Robustness to uncertainties: Unknown initial states, detector inefficiencies, model inaccu-
racies, and time-varying parameters (e.g., coupling strengths, measurement efficiencies)
reduce the effectiveness of a control strategy. Existing robust methods often assume struc-
tured uncertainties or full-state estimation [26, 22, 23, 18], limiting practical applicability.
These issues are also closely related to non-Markovian effects [11, 5, 4].
Earlier stabilization approaches have largely relied on engineering Lindbladian dynamics [42,
29, 39, 9], focusing on deterministic dissipator design while paying less attention to measurement
back-action, i.e., the diffusion terms in the SME. Although valuable structural conditions were
derived, such methods often assume precise knowledge of the system state and parameters.
In contrast, our earlier work [ 20, 23, 22, 26] has shown that directly leveraging measurement
back-action makes it possible to design feedback laws that guarantee exponential stabilization,
while remaining robust against both unknown initial states and parameter uncertainties within
admissible ranges. This highlights a clear advantage of measurement-based feedback strategies
over purely Lindbladian designs. Specifically, in [ 21], we first introduced a reduced-filter-based
approach for stabilizing perturbed systems with time-invariant coefficients.
This work extends our prior results by developing a rigorous framework for robust feedback
stabilization of time-varying perturbed quantum systems using a reduced-order filter. This
approach addresses both the computational challenges and robustness issues that arise when
dealing with large quantum systems subject to time-varying perturbations. Our key idea is to
construct a reduced filter that tracks only O(N) real parameters, corresponding to the diagonal
entries in a Quantum Non-Demolition (QND) basis, rather than the full O(N 2)-dimensional
state. This substantially reduces computational costs and enables scalable real-time feedback
control for large quantum systems. Our main contributions are summarized as follows:
1. Reduced filter construction: We rigorously establish the existence and well-posedness
of the reduced filter and derive sufficient conditions for its systematic construction in an
intuitive manner (Theorem 4.1).
2. Robust exponential stabilization: We prove that the reduced-filter-based feedback
globally exponentially stabilizes the quantum system to the desired target subspace,
2

--- 第3页 ---
under time-varying model perturbations. Unlike prior methods, our approach elimi-
nates the need for full-state estimation or precise system parameters. Additionally, we
relax constraints on the feedback controller compared to our previous work [ 23, 26]
(Theorem 4.10).
Beyond rigorous proofs, we provide intuitive insights into the reduced filter’s construction and
the rationale behind the proposed conditions, ensuring robust stabilization.
This paper is organized as follows: In Section 2, we introduce the stochastic dynamical
model of open quantum systems under continuous-time measurements and present the control
problem. Section 3 discusses the large-time behavior of uncontrolled systems, focusing on
exponential quantum state reduction. In Section 4, we present the reduced-filter-based feedback
design and explore its robustness for stabilizing the open quantum system. Section 5 provides
a numerical example of a three-level system. Finally, Section 6 concludes the paper and
discusses future directions for research.
Notation.The imaginary unit is denoted by i. For X∈ B (H), the adjoint is X ∗,
where B(H) denotes the space of all linear operators on H, andIdenotes the identity
operator. The set of Hermitian operators is B∗(H) := {X∈ B (H) |X = X ∗}. The trace
of X∈ B (H) is Tr(X), and the Hilbert–Schmidt norm is ∥X∥ := Tr(XX ∗)1/2. For v∈ H ,
∥v∥ denotes the standard vector norm. Define L∞([0,∞ ),B (H)) := {X : [0,∞ ) → B (H) |
each entry is measurable and sup t≥0 ∥X(t)∥<∞} . The commutator of X, Y∈ B (H) is
[X, Y ] := XY−Y X . For x∈C , ℜ{x} denotes the real part. The H¨ older space of functions from
A to B is denoted C1,α(A, B) for α∈ (0, 1]. For a positive integer m, we write [m] := {1, . . . , m}.
If H = HS ⊕ HR and X∈ B (H), then in a basis adapted to this decomposition X has block
form
X=
XS XP
XQ XR

,
where XS, XR, XP and XQ are matrices representing operators from HS to HS, from HR to
HR, fromH R toH S, fromH S toH R, respectively.
2 Stochastic dynamical model
We consider an open quantum system undergoing m continuous-time homodyne or heterodyne
measurements on a N-dimensional Hilbert space H. The state of the system is associated to a
density matrix onH,
S(H) :={ρ∈ B(H)|ρ=ρ ∗ ≥0,Tr(ρ) = 1}.
Fix a filtered probability space (Ω ,F, (Ft),P ) supporting an m-dimensional Wiener process
W (t). On this space, the conditional evolution of the state given the measurement outcomes
is described by the Stochastic Master Equation (SME):
dρ(t) =Lu
γ(t, ρ(t))dt+P(t, ρ(t))dt+
mX
k=1
p
θk(t)GLk(ρ(t))dWk(t),(1)
dYk(t) =
p
θk(t)Tr((L∗
k +L k)ρ(t))dt+dW k(t),(2)
withρ(0)∈ S(H). Here,
3

--- 第4页 ---
•θ k(t) = ηk(t)γk(t) ∈ [θk, ¯θk] is a deterministic measurable function combining measure-
ment efficiency ηk(t) ∈ [ηk,¯ηk] ⊂ (0, 1] and coupling strength γk(t) ∈ [γk,¯γk] with γk > 0,
associated with thek-th probe, whereθ k =η kγk and ¯θk = ¯ηk¯γk.
•Lindblad generator is
Lu
γ(t, ρ) :=−i[H 0(t) +u tH1, ρ] +
mX
k=1
γk(t)DLk(ρ),
where DLk(ρ) := LkρL∗
k − 1
2 L∗
kLkρ− 1
2 ρL∗
kLk. Here H0(t), H1 ∈ B ∗(H) represent the free
and control Hamiltonians, and the measurement operator
p
γk(t)Lk ∈ B(H) describes
interaction with thek-th probe.
•The measurement back-action associated withk-th probe is described by
GLk(ρ) :=L kρ+ρL ∗
k −Tr((L k +L ∗
k)ρ)ρ.
•Perturbations are modeled by
P(t, ρ) :=−i[ ˜H0(t), ρ] +
¯mX
k=1
DCk(t)(ρ).
The terms H0(t), ˜H0(t) ∈L ∞([0,∞ ),B ∗(H)) and Ck(t) ∈L ∞([0,∞ ),B (H)) are deterministic.
The continuous semi-martingale Yk(t) represents measurement record of k-th probe with
quadratic variation ⟨Yk(t), Yk(t)⟩ = t. Its natural filtration F Y
t := σ{Y (s), 0 ≤s≤t} , i.e.,
the smallest σ-algebra containing all measurement outcomes up to time t, coincides with
σ{W (s), 0 ≤s≤t} by [41, Proposition 5.2.14]. The control input ut is a bounded real-valued
F Y
t -adapted process. Existence, uniqueness, and invariance of solutions to (1) within S(H)
follow arguments similar to those in [29, Section 3] and [3, Chapter 5].
We now consider a decomposition: H = H0 ⊕ · · · ⊕ H d, with orthogonal projections
Π0, . . . ,Πd onto each subspace. Impose the following assumption on the system which is called
Quantum Non-Demolition (QND) measurement :
A1:H 0(t) = diag[H0(t), . . . ,Hd(t)] withH j(t)∈L ∞([0,∞),B ∗(Hj));
Lk =Pd
j=0 lk,jΠj withl k,j ∈C.
System operators H0(t) and Lk are simultaneously block-diagonal with respect to the above
decomposition.
Forj∈ {0, . . . , d}, define
dj(ρ) :=∥ρ−Π jρΠj∥,
Br(Hj) :={ρ∈ S(H)|d j(ρ)< r},
I(H j) :={ρ∈ S(H)|Tr(Π jρ) = 1}.
Definition 2.1.The subspace Hj is called invariant almost surely if, for all ρ(0) ∈ I (Hj),
ρ(t)∈ I(H j) for allt >0 almost surely.
4

--- 第5页 ---
Definition 2.2.An invariant subspace Hj is almost surely Global Exponential Stable (GES)
if lim supt→∞
1
t log dj(ρ(t)) < 0 almost surely, for all ρ(0) ∈ S (H). The left-hand side is the
sample Lyapunov exponent.
Problem setting:We study feedback stabilization of (1) toward the target subspace H0
using a reduced filter instead of full state estimation. For consistency with earlier notation,
we identifyH S withH 0.
Throughout, we focus on perturbations that preserve the invariance of the target subspace
H0. Intuitively, it means that the perturbations do not induce transitions that drive the
state of system out of H0, and then stabilization towards this subspace remains feasible.
Following [40], we formalize this assumption as:
A2:For allt≥0, ˜H0,P (t) = 0, and∀k∈[m],C k,Q(t) = 0 andPm
k=1 C∗
k,S(t)Ck,P (t) = 0.
Here, ˜H0,P (t) denotes the coupling between the subspace H0 and its orthogonal complementLd
i=1 Hi in the perturbed Hamiltonian, while Ck,Q(t) and Ck,P (t) represent, respectively,
the off-diagonal blocks of the noise operators that connect H0 with the external subspaces.
AssumptionA2therefore guarantees that neither the Hamiltonian nor the dissipative channels
induce leakage out of H0, ensuring that the subspace is invariant under the perturbed dynamics.
3 Stochastic Evolution of States in QND basis
We first analyze the uncontrolled dynamics ( ut ≡ 0) to identify the state components that
govern large-time behavior. In the QND setting, the diagonal weights Tr(ρ(t)Πi) carry the
relevant asymptotic information; see also [8].
UnderA2, invariant sets of the perturbed SME (1) are determined by the block structure
of ˜H0(t) and{C k(t)}k∈[m]:
Case 1. There exists a non-empty subset E⊆ { 0, . . . , d} such that, for all j∈E , I(Hj)
is invariant.
Case 2. For generic ˜H0(t) ∈L ∞([0,∞ ),B ∗(H)) and Ck(t) ∈L ∞([0,∞ ),B (H)), the only
invariant sets are those inCase 1. Extra invariant subsets arise only on a measure-zero
set of nongeneric parameters (additional algebraic constraints on block entries).
If the stronger structural assumption below holds, thenCase 2occurs withE={0, . . . , d}.
A-qsr: ˜H0(t) = diag[˜H0(t), . . . , ˜Hd(t)] with ˜Hj(t)∈L ∞([0,∞),B ∗(Hj));
Ck(t) = diag[Ck,0(t), . . . , Ck,d(t)] withC k,j(t)∈L ∞([0,∞),B(H j)).
We impose the following identifiability assumption on the measurement operators:
A3:For alli̸=j, there exists at least onek∈[m] such thatR{l k,i} ̸=R{l k,j }.
Define
El := min
i̸=j
" mX
k=1
θk(R{lk,i} −R{l k,j })2
#
.
AssumptionA3ensures that different eigenstates of the measurement operators can be
distinguished through their measurement records. The following theorem establishes that, in
the absence of control input, the stochastic dynamics induced by continuous measurements
drive the quantum state exponentially toward one of the invariant subspaces.
5

```

---

## 方法/公式

```

--- 第6页 ---
Theorem 3.1(Exponential quantum state reduction).Assume that ut ≡ 0, andA1,A3and
A-qsrhold. For any ρ(0) ∈ S (H), the system (1) converges towards I(H) :=Sd
j=0 I(Hj)in
mean and almost surely with Lyapunov exponent less than or equal to −El/2. Moreover, the
probability of convergence toI(H j)isTr(Π jρ(0))forj∈ {0, . . . , d}.
Proof. Define I := {k|Tr (Πjρ0) = 0 } and SI := {ρ∈ S (H)|Tr(Πjρ) = 0 iffj∈I}. It is
straightforward to verify that SI is almost surely invariant under the dynamics of system (1).
Consider the following candidate Lyapunov function, related to the Bhattacharyya distance,
also known as classical fidelity [7, Chapter 2.5],
V(ρ) =
X
i̸=j
q
Tr(Πiρ)Tr(Πjρ)≥0,(3)
with V (ρ) = 0 if and only if ρ∈ I (H). Due to the invariance of SI, V is twice continuously
differentiable when restricted toS I. For allρ∈ S I, we have
LV(ρ) =− 1
2
X
i̸=j
q
Tr(ρΠi)Tr(ρΠj)
"X
k
θk(t)(R{lk,i} −R{l k,j })2
#
≤ −E lV(ρ)/2,(4)
where the strict positivity of El follows fromA3. Detailed derivations are provided in
Appendix B.
Applying similar stochastic Lyapunov arguments as in [ 20, Theorem 5] and [ 22, Theorem
2.5], we conclude that ρ(t) converges exponentially to I(H), both in expectation and almost
surely, with Lyapunov exponent at most −El/2. Moreover, the probability of convergence to
I(H j) is Tr(Πjρ(0)).□
In the QND regime, the measurement operators Lk commute with the system Hamiltonian
H0(t), and also perturbations ˜H0(t) and Ck(t) underA-qsr. Hence, the off-diagonal elements
of ρ(t) in the QND basis vanish asymptotically (Theorem 3.1). Thus, the diagonal vector 
Tr(ρ(t)Π0), . . . ,Tr(ρ(t)Πd)

contains the statistical information for control design. Compared
to utilizing full state information, i.e., estimating the actual state via the estimator ˆρ(t) ∈
S(H) [26], relying solely on the diagonal entries dramatically reduces complexity: the number
of estimated parameters decreases from N 2 − 1 with N = dim{H} to d + 1 degrees of
freedom subject to the normalization constraint Pd
j=0 Tr(ρ(t)Πj) = 1, i.e., only d independent
parameters, whered+ 1≤N.
4 Stabilization by the reduced filter
In this section, we explore the robustness of the state feedback stabilization strategy proposed
in [22] for system (1), subject to perturbations P(ρ) and uncertainties in the initial state ρ(0),
the free Hamiltonian H0(t), and the model parameters γk(t), ηk(t). Throughout, we assume
that the measurement operators Lk are known, while the parameters γk(t) > 0 may not be
precisely identified. This assumption can be interpreted as allowing proportional time-varying
perturbations in Lk. Importantly, this technical assumption plays a crucial role in deriving
the main result, as it emphasizes that accurate knowledge of the measurement operators is
essential for ensuring robust stability.
6

--- 第7页 ---
Due to relation (2), we rewrite system (1) as follows:
dρ(t) =Lu
γ(t, ρ(t))dt+P(t, ρ(t))dt+
mX
k=1
p
θk(t)GLk(ρ(t))
×

dYk(t)−
p
θk(t)Tr((L∗
k +L k)ρ(t))dt

,(5)
with ρ(0) ∈ S (H). From a practical perspective, the initial state, the free Hamiltonian, the
model parameters and the perturbation cannot be precisely known. Following the approach
in [26], we construct the following SME to estimate the state ρ(t) replicating the structure of
the actual system (1),
dˆρ(t) =Lu
ˆγ(t,ˆρ(t))dt+
mX
k=1
q
ˆθkGLk(ˆρ(t))

dYk(t)−
q
ˆθkTr((L∗
k +L k)ˆρ(t))dt

,(6)
where ˆρ(0) ∈ S (H), ˆH0 = diag[ˆH0, . . . , ˆHd], and ˆθk = ˆηkˆγk with ˆγk ∈ [γk,¯γk], ˆηk ∈ [ηk,¯ηk].
Unlike the true system, which may involve time-varying H0(t) and θk(t), the estimator uses
fixed values selected from prior information, reducing online computational complexity. The
feedback law is then implemented as ut = u(ˆρ(t)), requiring real-time numerical integration
of (6).
4.1 Motivation for a reduced filter
As the system dimension increases, integrating the full filter (6) in real time becomes com-
putationally demanding. This motivates the design of controllers that exploit only partial
information rather than full state estimation.
Before introducing our reduced filter for feedback control, we recall two key mechanisms
established in [25, 22, 26] to interpret the full filter:
1. The term ut[H1,ˆρ] ensures that I(H0) is the only invariant subset for the estimator.
Moreover, underA2, if ˆρ(t) approaches an undesired invariant subset such as I(Hj)
withj∈E, this term forces ˆρ(t) away from such undesired invariant subsets.
2. The diffusive term GLk(ˆρ) accounts for the measurement back-action on the system. It
ensures that ˆρ(t), starting from any initial state outside the invariant subsets, is driven
toward the target invariant subset.
In view of the control objective: stabilizing system(1) toward I(H0) equivalentlyTr(ρ(t)Π0) →
1, and the large-time behavior in Theorem 3.1, which shows that the off-diagonal blocks
Πiρ(t)Πj vanish for i̸ = j. It is natural to focus only on the diagonal entries of ρ(t) in the
QND basis. We therefore construct an Rd+1-dimensional estimator that tracks these diagonal
components. By capturing precisely the information relevant for stabilization, this reduced
estimator provides an effective input to the feedback controller while avoiding the complexity
of full state estimation via ˆρ(t).
Since the measurement operators ( Lk)k∈[m] are diagonal in the QND basis, their contribu-
tion to the measurement back-action can be simplified to:
Tr(GLk(ρ)Πn) = 2Tr(ρΠn)
 
R{lk,n} −Pd
j=0 R{lk,j }Tr(ρΠj)

.(7)
7

--- 第8页 ---
Motivated by this structure, and by the analysis in Section 3, we introduce a reduced-order
estimator whose state ˆq(t) ∈R d+1 tracks the diagonal components Tr(ρ(t)Πn) based on the
measurement output F Y
t . Inspired by [12, 22], we propose the following autonomous Stochastic
Differential Equation (SDE):
dˆqn(t) =ut
dX
j=0
Γn,j ˆqj(t)dt+ 2ˆqn(t)
mX
k=1
q
ˆθkΦk
n(ˆq(t))

dYk(t)−2
q
ˆθkΛk(ˆq(t))dt

,(8)
where
Φk
n(ˆq) :=R{lk,n} −Λ k(ˆq),with Λ k(ˆq) :=Pd
j=0 R{lk,j }ˆqj,
and ˆqn = e∗
nˆq, and {e0, . . . , ed} forms an orthonormal basis of Rd+1. ut := u(ˆq(t)) represents
the feedback controller.
Moreover, we assume that the matrix Γ∈R (d+1)×(d+1) satisfies the following condition:
C1: Pd
i=0 Γi,j = 0 for all j∈ { 0, . . . , d}, Γ j,j < 0 for all j∈ { 0, . . . , d}, and Γ i,j ≥ 0 for all
i̸=j∈ {0, . . . , d}.
We observe that the second and third terms on the right-hand side of (8) effectively reproduce
the measurement back-action, as they structurally resemble the second summand in (5) when
considering the diagonal elements in (7). The first term, ut
Pd
j=0 Γn,j ˆqj, under ConditionC1,
serves to replicate the effect of ut[H1,ˆρ]. RegardingC1, the constraint Pd
i=0 Γi,j = 0 ensures
thatP
n ˆqn = 1, while the remaining conditions guarantee the positivity of ˆqn ≥0, ensuring
ˆq∈ ¯Od+1 :=
n
ˆq∈[0,1] d+1

Pd
n=0 ˆqn = 1
o
.
Thus, ˆqis a valid candidate probability vector approximating the diagonal of ˆρin the QND
basis.
4.2 Stochastic model for the reduced filter
Based on (2), we rewrite (8) as the following Wiener process-driven SDE forn∈ {0, . . . , d},
dˆqn(t) =ut
dX
j=0
Γn,j ˆqj(t)dt+ 2ˆqn(t)
mX
k=1
q
ˆθkΦk
n(ˆq(t))
 
dWk(t) +T k(t, ρ(t),ˆq(t))dt

,(9)
where
Tk(t, ρ,ˆq) :=
p
θk(t)Tr((Lk +L ∗
k)ρ)−2
q
ˆθkΛk(ˆq),
and ρ(t) is the solution to SME (1) with ut := u(ˆq(t)) as the feedback controller, which satisfies
the following assumption:
A4:u∈ C 1,α( ¯Od+1,R +) with α∈ (0, 1], u(e0) = 0 and u(en) > 0 for all n > 0, where {en}d
n=0
is the orthonormal basis ofR d+1.
Define
Od+1 :={ˆq∈(0,1) d+1 |Pd
n=0 ˆqn = 1}.
Before analyzing the stability properties of the system, it is essential to ensure that the coupled
system (1)–(9) is well-posed and that the reduced state remains within the probability simplex
Od+1 for all time. The next theorem provides these well-posedness and invariance properties.
8

--- 第9页 ---
Theorem 4.1.SupposeA4andC1hold. Then, for all( ρ(0),ˆq(0)) ∈ S (H) × Od+1, the
coupled system (1)–(9) has a unique global solution( ρ(t),ˆq(t)) ∈ S (H) × Od+1 for all t≥ 0
almost surely.
Proof. First, suppose that ut is a real, bounded positive process adapted to F Y
t . Existence,
uniqueness, and invariance of the solution ρ(t) in S(H) for (1) follow directly from [29, Section
3] or [3, Chapter 5].
Denote the explosion time from the initial state ˆq(0) by τe(ˆq(0), ω) : Rd+1 × Ω → [0,∞ ].
Since the coefficients of (9) are locally Lipschitz, by [ 28, Theorem 5.2.8], the SDE (9) admits
a unique local strong solution on [0, τ e) almost surely.
Summing (9) overn∈ {0, . . . , d}yields
d
dX
n=0
ˆqn(t) =ut
dX
n=0
dX
j=0
Γn,j ˆqj(t)dt
+ 2
mX
k=1
q
ˆθkΛk(ˆq(t))
 
1−
dX
n=0
ˆqn(t)
!
 
dWk(t) +T k(t, ρ(t),ˆq(t))dt

.
Since the coefficients of the above equation are locally Lipschitz continuous, for any given
initial state ˆq(0) ∈ O d+1, there is a unique local solution on t∈ [0, τe). According to the
conditionC1, Pd
n=0 Γn,j = 0. It follows Pd
n=0 ˆqn(t) = 1 when ˆq(0) ∈ O d+1 for all t∈ [0, τe)
almost surely. It implies that, for all ˆq(0)∈ O d+1,Pd
n=0 ˆqn(t) = 1 till the explosion time.
For all ˆq(0) ∈ O d+1, choose k0 ≥ 0 sufficiently large so that ˆqn(0) > 1/k0 for all n∈
{0, . . . , d}. For each integerk≥k 0, define two stopping times
τk := inf{t∈[0, τ e)|ˆqn(t)≤1/kfor somen},
σk := inf{t∈[0, τ e)|ˆqn(t)/∈(1/k, k) for somen}.
Clearly, σk ≤τ k and σk →τ e as k→ ∞ . Because Pd
n=0 ˆqn(t) = 1 holds almost surely for all
t < τ e, it follows thatτ k =σ k almost surely
Consider the function
V(ˆq) =Pd
n=0 log ˆq−1
n ∈ C 2(Od+1,R +),
whose infinitesimal generator is given by
LV(ˆρ) =−u tA(ˆq) +B(t, ρ,ˆq),
where
A(ˆq) :=
dX
n=0
1
ˆqn
dX
j=0
Γn,j ˆqj,
B(t, ρ,ˆq) := 2
X
n,k
q
ˆθkΦk
n(ˆq)
q
ˆθkΦk
n(ˆq)−Tk(t, ρ,ˆq)

.
Due to compactness of S(H) × ¯Od+1, there exists a finite c1 > 0 such that B(t, ρ,ˆq) ≤c 1 for
all (t, ρ,ˆq)∈R + × S(H)× ¯Od+1. Define
¯Ok
d+1 :={ˆq∈R d+1|ˆqn ≥1/kforn∈ {0, . . . , d},s.t. Pd
n=0 ˆqn = 1} ⊂ O d+1.
9

--- 第10页 ---
For all ˆq∈ ¯Ok
d+1, due to the compactness and continuity, there exists c2 > 0 such that
−A(ˆq)≤c2V(ˆq) andc 1 ≤c 2V(ˆq). Sinceu t is positive and bounded, it follows that
LV(ˆq)≤c 3V(ˆq),∀ˆq∈ ¯Ok
d+1,
for some constantc 3 >0.
For ˆq∈ Od+1 \ ¯Ok
d+1, at least one ˆqi approaches zero. We rewrite
A(ˆq) =
dX
n=0
Γn,n +
dX
n=0
1
ˆqn
X
n̸=j
Γn,j ˆqj,
with Γn,n <0 and Γ n,j ≥0 forn̸=j.
Suppose ˆqn approaches zero. There are three possible cases:
1. IfP
n̸=j Γn,j ˆqj converges to a finite positive constant, then 1
ˆqn
P
n̸=j Γn,j ˆqj diverges to
infinity.
2. IfP
n̸=j Γn,j ˆqj converges to zero slower than ˆqn, then 1
ˆqn
P
n̸=j Γn,j ˆqj diverges to infinity.
3. IfP
n̸=j Γn,j ˆqj converges to zero at the same or faster rate than ˆqn, then 1
ˆqn
P
n̸=j Γn,j ˆqj
converges to a finite constant.
Hence, −A(ˆq) either diverges negatively or remains bounded by a finite positive constant.
Note that, in these cases, V (ˆρ) approaches infinity. Thus, there exists a finite constant c4 > 0
such thatLV(ˆq)≤c 3V(ˆq) for all ˆq∈ Od+1 \ ¯Ok
d+1. Therefore, there existsc >0 such that
LV(ˆq)≤cV(ˆq),∀ˆq∈ O d+1.
Next, we show τe = ∞ almost surely by contradiction inspired by analogous result
established in [28, Lemma 4.3.2]. Assume P(τe <∞ ) > 0, and then there is T > 0 sufficient
large such that P(τe ≤T ) > 0. Given that LV (ˆq) ≤cV (ˆq) for all ˆq∈ O d+1, define
f(ˆq, t) =e−ctV(ˆq), whose infinitesimal generator is given by
Lf(ˆq, t) =e −ct(−cV(ˆq) +LV(ˆq))≤0,
for all ˆq∈ Od+1. Since ˆq(0) ∈ ¯Ok0
d+1 ⊂ ¯Ok
d+1, we have ˆq(T∧τ k) ∈ ¯Ok
d+1 ⊂ O d+1. By Itˆ o
formula, we obtain
E
 
f(ˆq(T∧τ k), T∧τ k)

=V(ˆq(0)) +E
Z T∧τ k
0
Lf(ˆq(s), s)ds

≤V(ˆq(0)).
Conditioned on the event{τ e ≤T}, we deduce
f(ˆq(T∧τ k), T∧τ k) =f(ˆq(τk), τk) =e −c(T∧τ k)V(ˆq(τk))≥e −cT V(ˆq(τk))≥e −cT logk.
It implies
E
 
e−cT logk1 {τe≤T}

≤E
 
f(ˆq(T∧τ k), T∧τ k)1{τe≤T}

≤E
 
f(ˆq(T∧τ k), T∧τ k)

≤V(ˆq(0)).
Consequently,
P(τe ≤T)≤e cT V(ˆq(0))
logk .
10

--- 第11页 ---
Letting k→ ∞ , we have P(τe ≤T ) = 0, which contradicts the assumption. Thus, we conclude
that τe = ∞ almost surely in the case where ut is a real, bounded, and positive process
adapted toF Y
t .
Now, consider the case where ut = u(ˆq) with u∈ C 1,α( ¯Od+1,R +). Due to the compactness
of S(H) × ¯Od+1, we can find an open set E ∈ B (H) ×R d+1 such that S(H) × ¯Od+1 ⊂ E .
Let X (ρ,ˆq) : B(H) ×R d+1 → [0, 1] be a smooth function with compact support such that
X (ρ,ˆq) = 1 for ( ρ,ˆq) ∈ E . Additionally, define U∈ C 1,α(Rd+1,R +) such that U(ˆq) = u(ˆq) for
all ˆq∈ ¯Od+1. Then, the following coupled equations
dϱ(t) =X(ϱ(t), ˆq(t))
"
LU
γ (ϱ(t))dt+P(ρ(t))dt
mX
k=1
p
θk(t)GLk(ρ(t))dWk(t)
#
,
dˆqn(t) =X(ϱ(t), ˆq(t))
"
U(ˆq(t))
dX
j=0
Γn,jˆqj(t)dt+ 2 ˆqn(t)
mX
k=1
q
ˆθkΦk
n(ˆqn(t))
×
 
dWk(t) +T k(t, ϱ(t),ˆq(t))dt

#
,
have global Lipschitz coefficients, ensuring a unique strong solution with almost surely con-
tinuous adapted paths [ 34]. Since X has compact support, ( ϱ(t), ˆq(t)) is bounded, making
U(ˆq(t)) an almost surely continuous, real bounded adapted process. Now, consider the coupled
system (1)–(9) with ut = U(ˆq(t)) and ( ρ(0),ˆq(0)) = ( ϱ(0), ˆq(0)) ∈ S (H) × Od+1. As both
solutions (ρ(t),ˆq(t)) and ( ϱ(t), ˆq(t)) have a unique solution, the solutions must coincide up to
the first exit time from E. Moreover, ( ρ(t),ˆq(t)) remains in S(H) × Od+1 for all t≥ 0 almost
surely, and thus (ϱ(t), ˆq(t)) will never exit from S(H) × Od+1. Hence, ( ρ(t),ˆq(t)) = (ϱ(t), ˆq(t))
for allt≥0 almost surely. The proof is complete.□
4.3 Feedback stabilization to target subspaces
We adapt methods from [ 22, 26] to ensure robust GES of I(H0) for the system (1). This
stabilization is achieved without requiring knowledge of the initial state or precise values of
the free Hamiltonian H0(t) and the model parameters {γk(t)}m
k=1 and {ηk(t)}m
k=1, and remains
effective in the presence of perturbationsP(ρ) satisfyingA2.
We systematically analyze the behavior of the coupled system (1)–(9). The key aspects of
our analysis include:
1. Instability of undesired sets.Based on the structure of perturbations discussed in
Section 3, we identify card(E) undesired invariant subsets I(Hn) ×e 0. Under assump-
tionsA2andA4, these subsets persist despite the feedback controller. Inspired by
Khas’minskii’s recurrence conditions [ 19, Theorem 3.9], we establish instability of these
non-desired subsets (Lemma 4.5).
2. Recurrence.Utilizing the support theorem [ 37], we demonstrate that the trajectory
(ρ(t),ˆq(t)) of the coupled system almost surely enters any neighborhood of the target
subsetI(H 0)×e 0 in finite time (Proposition 4.8).
3. Exponential stability.Inspired by Theorem 3.1, we use local Lyapunov methods to prove
stability in probability. Combined with the recurrence property and the strong Markov
11

--- 第12页 ---
property of ( ρ(t),ˆq(t)), local stability in probability implies almost sure asymptotic
stability of the subset I(H0) ×e 0 ([20, Theorem 6.3]). Finally, we employ Lyapunov
techniques to estimate the sample Lyapunov exponent explicitly (Theorem 4.10).
Define, for allk∈[m],
¯ck :=R{l k,0} −min n∈[d] R{lk,n},
ck :=R{l k,0} −max n∈[d] R{lk,n}.
Impose the following assumption on measurement operators:
A5:For eachk∈[m], ¯ck ≤0 orc k ≥0.
This assumption is essential for establishing the instability of undesired invariant subsets, the
recurrence property, and for estimating the Lyapunov exponent. Note that underA3, the
case where ¯ck = 0 orc k = 0 for allk∈[m] is excluded.
4.3.1 Instability of undesired invariant subsets
Here, we provide Lyapunov-type sufficient conditions ensuring the instability of an invariant
subspace of the coupled system (1)–(9), assuming the perturbation structure satisfiesCase 2.
Additionally, we estimate the average escape time of trajectories from a neighborhood of such
invariant subspaces.
The control Hamiltonian H1 determines how the feedback input ut can induce transitions
between invariant subspaces. If H1 fails to couple certain eigenspaces, the associated subspace
I(Hn) may remain invariant regardless of the applied control. To formalize this requirement,
we adopt a Hautus-type controllability condition [ 36, Chapter 3.3] ensuring that H1 connects
all relevant eigenspaces. Let Eλ(X) be the eigenspace of X corresponding to the eigenvalue λ.
A6:For eachj∈[d], and for all eigenvalueλof Π jH1Πj,
T
i̸=j Ker{ΠiH1Πj} ∩E λ(ΠjH1Πj) ={0}.
The following lemma provides a necessary and sufficient condition ensuring that H1 acts
non-trivially on eachI(H n).
Lemma 4.2.Under AssumptionA1, the necessary and sufficient condition of[ H1, ρ] ̸= 0for
allρ∈ I(H n)and alln∈[d]is AssumptionA6.
Proof. Fix n∈ [d] and let ρ∈ I (Hn), then ρ = Πnρ = ρΠn = ΠnρΠn. [ H1, ρ] = 0 is equivalent
to Πk[H1, ρ]Πk = Πi[H1, ρ]Πj = 0 for allkandi̸=j. We first focus on the diagonal part,
Πk[H1, ρ]Πk = [ΠnH1Πn, ρ] = 0,∀k∈ {0, . . . , d}.
Then, ρ admits the decomposition ρ =P
λ PλρPλ, where Pλ is the eigenprojection of Π nH1Πn
corresponds to the eigenvalueλ. Next, we have
Πi[H1, ρ]Πj = 0,∀i̸=j⇔Π iH1Πnρ= 0,∀i̸=n.
Thus, for all ρ∈ I (Hn), [H1, ρ] ̸= 0 if and only if T
i̸=n Ker{ΠiH1Πn} ∩E λ(ΠnH1Πn) = {0},
for allλ. The lemma then follows for arbitraryn∈[d].□
The following corollary provides a simple algebraic condition ensuring thatA6holds.
12

--- 第13页 ---
Corollary 4.3.For all i̸ = n∈ { 0, . . . , d}, the block matrix ofΠ iH1Πn from Hn to Hi is
injective, thenA6is satisfied.
Next, to quantify the effect of time-varying measurement perturbations, we introduce the
normalized parameter
χk(t) := (θk(t)/ˆθk)1/2 ∈[χ k,¯χk]
where χk = (θk/ˆθk)1/2 and ¯χk = (¯θk/ˆθk)1/2 for all k∈ [m], and impose the following condition:
C2:For allk∈[m],
2¯χk −1<min
n∈[d]
 R{lk,0}
R{lk,n}
R{lk,n} ̸= 0

if ¯ck ≤0,
while
2χk −1>max
n∈[d]
 R{lk,0}
R{lk,n}
R{lk,n} ̸= 0

ifc k ≥0.
Define
Rk,n(t) :=
 
R{lk,n} −R{l k,0}
 
(2χk(t)−1)R{l k,n} −R{l k,0}

.
The next lemma ensures that, under the above conditions, the weighted sum of these terms
remains strictly positive, which is crucial for establishing instability.
Lemma 4.4.IfA3,A5andC2are satisfied, then for all χk(t) ∈ [χk,¯χk],Pm
k=1 ˆθkRk,n(t) >
0.
Proof.Fixn∈[d].
•If ¯ck ≤0 andℜ{l k,n} ̸= 0, then byC2,
2χk(t)−1≤2¯χ k −1<ℜ{l k,0}/ℜ{lk,n},
which together with ℜ{lk,n} ≥ ℜ{l k,0} impliesR k,n(t) ≥ 0, with equality if and only if
ℜ{lk,n}=ℜ{l k,0}.
• If ck ≥ 0 and ℜ{lk,n} ̸= 0, a symmetric argument showsR k,n(t) ≥ 0, again with equality
if and only ifℜ{l k,n}=ℜ{l k,0}.
•Ifℜ{l k,n}= 0, thenR k,n(t) =ℜ{l k,0}2 ≥0,with equality if and only ifℜ{l k,0}= 0.
Therefore, in all casesR k,n(t) ≥ 0, and under assumptionsA3andA5, strict positivity of
the weighted sum follows: Pm
k=1 ˆθk Rk,n(t)>0.□
Define
d0(ˆq) :=∥ˆq−e0∥,
Br(e0) :={ˆq∈ ¯Od+1|d 0(ˆq)< r}.
The following lemma establishes that each non-target invariant subspace is locally unstable,
i.e., trajectories initialized sufficiently close to such subspaces will almost surely leave their
neighborhood in finite time.
13

--- 第14页 ---
Lemma 4.5.SupposeA3,A4,A5andC1andC2hold. In addition, assume there
exists a non-empty subset E⊂ [d]such that I(Hn)for all n∈E are invariant for the
perturbed system (1) when ut ≡ 0. Then, almost all ˜H(t) ∈L ∞([0,∞ ),B ∗(H))and Ck(t) ∈
L∞([0,∞ ),B (H)), there exists λ > 0such that for all( ρ(0),ˆq(0)) ∈ Bλ(Hn) ×B λ(e0) ∩ Od+1
with n∈E , the trajectory( ρ(t),ˆq(t))of the coupled system (1)–(9) exits fromB λ(Hn) ×B λ(e0)
in finite time almost surely.
Proof. Consider the functionV n(ˆq) = log ˆq−1
n ∈ C 2(Od+1,R +). Its infinitesimal generator is
given by
LV n(ˆq) =−u(ˆq)An(ˆq) +Bn(ρ,ˆq),
where
An(ˆq) := 1
ˆqn
dX
j=0
Γn,j ˆqj,
Bn(t, ρ,ˆq) := 2
mX
k=1
q
ˆθkΦk
n(ˆq)
q
ˆθkΦk
n(ˆq)−Tk(t, ρ,ˆq)

.
UnderC1andA4, we deduce that, for all ˆq∈ O d+1,
u(ˆq)An(ˆq) =u(ˆq)
 
Γn,n +P
n̸=j Γn,j
ˆqj
ˆqn

≥u(ˆq)Γn,n ≥0.
Moreover, according to Lemma 4.4, we have
lim
(ρ,ˆq)→I(Hn)×e0
Bn(t, ρ,ˆq) =−2
mX
k=1
ˆθkRk,n(t)<0.
It implies
lim sup
(ρ,ˆq)→I(Hn)×e0
LV n(ˆq)≤lim
(ρ,ˆq)→I(Hn)×e0
Bn(ρ,ˆq)<0.
Therefore, there existδ, λ >0 such that
LV(ˆq)≤ −δ,∀(ρ,ˆq)∈B λ(Hn)×B λ(e0)∩ O d+1.
Define τλ as the first exiting time fromBλ(Hn)×Bλ(e0). According to Theorem 4.1, ˆq(t) ∈ O d+1
for all t≥ 0 almost surely. Applying the Itˆ o formula onV(ˆq(t)), we obtain E(τλ) ≤ V(ˆq(0))/δ <
∞. Then, we conclude the proof by applying the Markov inequality.□
4.3.2 Recurrence property
We now provide sufficient conditions ensuring that trajectories of the coupled system (1)–(9)
are recurrent in neighborhoods of the desired invariant subset. The recurrence analysis relies
on the support theorem [37], which characterizes the reachable sets of SDEs through associated
deterministic control systems. Consider the deterministic control system associated with the
Stratonovich form [34] of (1)–(9), forn∈ {0, . . . , d},
˙ρv(t) = ˜Lu
γ,η(t, ρv(t)) +P(t, ρ v(t))
mX
k=1
p
θk(t)GLk(ρv(t))Vk(t),(10)
˙ˆqv,n(t) =f u
n(ˆqv(t)) + ∆n(ˆqv(t)) + 2ˆqv,n(t)
mX
k=1
q
ˆθkΦk
n(ˆqv(t))Vk(t),(11)
14

--- 第15页 ---
whereρ v(0) =ρ(0), ˆqv(0) = ˆq(0), and
Vk(t) :=v k(t) +
p
θk(t)Tr((Lk +L ∗
k)ρv(t)),
wherev k(t)∈ Vis the bounded control input. Here
˜Lu
γ,η(t, ρ) :=−i[H 0(t) +uH 1, ρ] +Pm
k=1
γk(t)
2
 
2(1−η k(t))LkρL∗
k −(L ∗
kLk +η k(t)L2
k)ρ
−ρ(L ∗
kLk +η k(t)L∗
k
2) +η k(t)Tr((Lk +L ∗
k)2ρ)ρ

,
fu
n(ˆq) =uPd
j=0 Γn,j ˆqj −4ˆqn
Pm
k=1
q
ˆθkΦk
n(ˆq)Λk(ˆq),
∆n(ˆq) = 2ˆqn
P
k ˆθk[P
j ˆqjR{lk,j }Φk
j (ˆq)−(Φk
n(ˆq))2].
The invariance of S(H) × Od+1 for the deterministic system (10)–(11) follows directly from
the support theorem.
We now introduce a Kalman-type controllability assumption on the control Hamiltonian H1
to guarantee sufficient coupling between the target subspace H0 and its orthogonal complementLd
i=1 Hi. This ensures that the set
I0 :={S(H)|Tr(ρΠ 0) = 0}
which contains all potential invariant subsets of the dynamics inCase 2, i.e., I(Hn) with
n∈E , is non-invariant under the evolution. Establishing the non-invariance of I0 is essential
for stabilization. Let Π ⊥
0 :=I − Π0 denote the orthogonal projector onto Ld
i=1 Hi. Consider
the block operators of the control Hamiltonian H1,R fromLd
i=1 Hi toLd
i=1 Hi and H1,Q from
H0 toLd
i=1 Hi. We impose the following assumption:
A7:There exists an∈Z + such that
rank{[I, H1,R, . . . , Hn
1,R]H1,Q} ≥N−1−dim{H 0}.
The next lemma shows that, under the required assumptions, the control Hamiltonian H1
guarantees the immediate exit of trajectories fromI 0.
Lemma 4.6.Suppose thatA1,A2,A4,A6andA7holds, then for all ρ(0) ∈ I 0, the
trajectoryρ v(t)to the system(10)exitsI 0 immediately.
Proof. UnderA4, we suppose that ut = u(ˆqv(t)) > 0 for all t≥t 0. If the lemma false, then
there exists aδ >0 arbitrarily small such thatρ v(t)∈ I 0 for allt∈[t 0, t0 +δ]. Hence,
Π0ρv(t)Π0 =ρ v(t)Π0 = Π0ρv(t) = 0.
ByA1andA2, for allk∈[m], we have,
[Lk,Π 0] = [H0(t),Π 0] = [ ˜H0(t),Π 0] = 0,∀t≥0.
It implies that, for allt∈[t 0, t0 +δ],
Π0 ˙ρv(t)Π0 =
¯mX
k=1
Π0Ck(t)ρv(t)Ck(t)∗Π0 ≥0.
15

```

---

## 实验/结果

```

--- 第18页 ---
and define
Ak :=l 2
k min
n
χ2
k,1
o
,
Bk := 2¯lk|ℜ{lk,0}|max
n
1−χ k,¯χk −1
o
.
We impose the following condition to guarantee local stability in probability of the target
subspace:
C3:If|ℜ{l k,0}|= 0, thenl k >0. Otherwise,A k >B k for allk∈[m].
By a straightforward calculation, we have the following lemma.
Lemma 4.9.Under conditionC3, for allχ k(t)∈[χ k,¯χk], we have
l2
k min{χk(t)2,1} −2 ¯lk|(χk(t)−1)ℜ{l k,0}|>A k −B k >0.
Define the coefficient
Cχ,¯χ:=P
k ˆθk(2Ak −B k)2/2Ak,
which is used to estimate the Lyapunov exponent. Building on the previous stability and
recurrence results, the following theorem presents the main result of this paper, under mild
regularity and coupling conditions, the target subspace is globally exponentially stable almost
surely.
Theorem 4.10.Suppose ¯ηk < 1for all k∈ [n], conditionsC1-C3and assumptionsA1-A7
hold. Then, for all ρ(0) ∈ S (H), the target subspace H0 is almost sure GES for the perturbed
system(1), for almost all ˜H(t)∈L ∞([0,∞),B ∗(H))andC k(t)∈L ∞([0,∞),B(H)), with the
sample Lyapunov exponent less than or equal to−C χ,¯χ/2.
Proof.Define the auxiliary function
V0(ρ,ˆq) = 1−Tr(ρΠ0) + 1−ˆq0,
and consider the candidate Lyapunov function
V(ρ,ˆq) =V 0(ρ,ˆq)x ≥0, x∈(0,1),
where the equality holds if and only if ( ρ,ˆq) ∈ I (H0) ×e 0. By Theorem 4.1, if the initial
condition satisfies ˆq0(0) < 1, then ˆq0(t) < 1 for all t≥ 0 almost surely. Consequently,
V(ρ(t),ˆq(t))>0 almost surely.
We first establish the local stability in probability of the target subspace H0. That is, for
everyε∈(0,1) and for everyr >0, there existsδ=δ(ε, r)>0 such that,
P
 
V(ρ(t),ˆq(t))< rfort≥0

≥1−ε,
wheneverV(ρ(0),ˆq(0))< δ.
The infinitesimal generator ofV(ρ,ˆq) is given by
LV(ρ,ˆq) =xV(ρ,ˆq)
F(t, ρ,ˆq)
V0(ρ,ˆq) − 2(1−x) P
k Gk(t, ρ,ˆq)
V0(ρ,ˆq)2

,
18

--- 第19页 ---
where
F(t, ρ,ˆq) =u(ˆq)
P
j Γ0,j ˆqj −iTr([H 1, ρ]Π0)

+ 2ˆq0
P
k Φk
0(ˆq)Tk(t, ρ,ˆq),
Gk(t, ρ,ˆq) =ˆθk

χk(t)Ψk
0(ρ)Tr(ρΠ0) + Φk
0(ˆq)ˆq0
2.
Sinceu(ˆq)∈ C 1,α withα∈(0,1),
|u(ˆq)| ≤c|1−ˆq0|1+α ≤cV 1+α
0
for somec >0. Moreover,
|Φk
0(ˆq)|=
ℜ{lk,0}Pd
j=0 ˆqj −Pd
n=0 ℜ{lk,n}ˆqn

=
Pd
n=0(ℜ{lk,0} − ℜ{lk,n})ˆqn}

≤ ¯lk(1−ˆq0)≤ ¯lkV0(ρ,ˆq).
Therefore, due to the compactness ofS(H) and ¯Od+1,
F(t, ρ,ˆq)
V0(ρ,ˆq) ≤ |u(ˆq)|
V0(ρ,ˆq)
P
j Γ0,j ˆqj −iTr([H 1, ρ]Π0)
 +
2ˆq0
P
k |Φk
0(ˆq)||Tk(t, ρ,ˆq)|
V0(ρ,ˆq)
≤cV0(ρ,ˆq)α + 2ˆq0
P
k¯lk|Tk(t, ρ,ˆq)|,
for somec >0. Together with the relation (12)–(13), we have
Pm
k=1 Gk(t, ρ,ˆq)
V0(ρ,ˆq)2 ≥
mX
k=1
ˆθkl2
k min

χk(t)2Tr(ρΠ0)2,ˆq2
0
	
.
Putting the estimates together,
LV(ρ,ˆq)≤ −V(ρ,ˆq)C x(t, ρ,ˆq),
where
Cx(t, ρ,ˆq) =2x(1−x)
X
k
ˆθkl2
k min{χk(t)2Tr(ρΠ0)2,ˆq2
0} −cxV 0(ρ,ˆq)α + 2xˆq0
X
k
¯lk|Tk(t, ρ,ˆq)|.
By continuity arguments and Lemma 4.9, there existsx∈(0,1) such that
lim
(ρ,ˆq)→I(H0)×e0
Cx(t, ρ,ˆq) =2x
X
k
ˆθk
h
(1−x)l 2
k min{χk(t)2,1} −2 ¯lk|(χk(t)−1)ℜ{l k,0}|
i
≥Cx >0,
where
Cx = 2xP
k ˆθk[(1−x)A k −B k].
Consequently,
lim sup
(ρ,ˆq)→I(H0)×e0
LV(ρ,ˆq)
V(ρ,ˆq) ≤lim
(ρ,ˆq)→I(H0)×e0
−Cx(t, ρ,ˆq) =−Cx <0.
19

--- 第20页 ---
Due to the continuity ofC x(t, ρ,ˆq), there exists aλ >0 such that
LV(ρ,ˆq)≤0,∀(ρ,ˆq)∈B λ(H0)×B λ(e0),
and by applying the similar arguments as in [20, Theorem 6.3], then local stability in probability
is ensured.
Next, according to Proposition 4.8, for almost all ˜H(t) ∈L ∞([0,∞ ),B ∗(H)) and Ck(t) ∈
L∞([0,∞ ),B (H)), the coupled system is almost surely recurrent. That is, for any initial
condition ( ρ(0),ˆq(0)) ∈ S (H) × O d+1, the trajectory ( ρ(t),ˆq(t)) almost surely enters any
neighborhood ofI(H 0)×e 0 in finite time.
Combining the above two properties,local stability in probabilityandalmost sure recurrence,
one can invoke the Strong Markov property to establish the almost sure convergence of
V (ρ(t),ˆq(t)) to zero (see [20, Theorem 6.3] for a detailed argument; see also [19, Theorem 5.5.7]).
Indeed, since the process ( ρ(t),ˆq(t)) almost surely returns infinitely often to any neighborhood
of I(H0) ×e 0, and due to local stability in probability, it remains in such neighborhoods with
non-zero probability, the probability that the trajectory leaves these neighborhoods infinitely
many times is zero. Consequently, V (ρ(t),ˆq(t)) converges to zero almost surely. Therefore, the
target subspaceH 0 is almost surely asymptotically stable for all (ρ(0),ˆq(0))∈ S(H)× O d+1.
Finally, we derive the almost sure global exponential stability and provide an estimation
of the sample Lyapunov exponent. Observe that
lim inf
(ρ,ˆq)→I(H0)×e0
nX
k=1
ˆθk
"
Tr
 
∇ρV(ρ,ˆq)χk(t)GLk(ρ)
V(ρ,ˆq)
!
+ ∇ˆqV(ρ,ˆq)⊤Φk(ˆq)
V(σ,ˆσ)
#2
≥4x
X
k
ˆθkl2
k min

χk(t)2,1
	
≥2K x,
whereΦ k(ˆq) = 2[ˆq0Φk
0(ˆq)· · ·ˆqdΦk
d(ˆq)]⊤ and∇ ρV(ρ,ˆq) is the Fr´ echet gradient, and
Kx = 2xP
k ˆθkl2
k min

χ2
k,1
	
.
Therefore, by using arguments as in the proof of [20, Theorem 6.3] again, we obtain
lim sup
t→∞
1
t logV(ρ(t),ˆq(t))≤ −max
x∈(0,1)
{Cx +K x}=−C χ,¯χ<0, a.s.
Moreover, since
 
d0(ρ)
2 ≤cV(ρ,ˆq) for some positive constantc, it follows that
lim sup
t→∞
1
t logd 0(ρ(t))≤ −C χ,¯χ/2<0, a.s.
This completes the proof.□
Remark 4.11.In Theorem 4.10 we assumed that the feedback controller satisfies u∈ C 1,α.
However, the proof shows that global exponential stability also holds under the condition that
u∈ C 1 andu(ˆq) = 0 for all ˆq∈B δ(e0), whereδ >0 is arbitrarily small.
As an example of application of the previous results, we consider the following feedback
law. Define
u(ˆq) =a
 
1−ˆq
b,(14)
witha >0 andb >1. Therefore,A4holds true.
20

--- 第21页 ---
5 Numerical example: Three-level systems
We consider a three-level system undergoing one-channel homodyne detection along the z-axis,
with target state diag(1,0,0). The system operators are specified as follows:
H0(t) =ω(t)J z, L=J z = diag(1,0,−1),
and
H1 =
√
2
2


0−i0
i0−i
0i0

 ,
with perturbations, for allk∈[ ¯m],
˜H0(t) =


∗0 0
0∗ ∗
0∗ ∗

, Ck(t)∈





0∗ ∗
0∗ ∗
0∗ ∗

 ,


∗0 0
0∗ ∗
0∗ ∗




 ,
where partial information about the perturbation is available, i.e., ˜H0(t) and {Ck(t)}k∈[ ¯m]
satisfy the above assumption, which can be verified using operator identification techniques.
The free Hamiltonian frequency is chosen to be sinusoidally modulated,
ω(t) = 1.5

1 + 0.2 sin2πt
T

.
Its time dependence reflects slow oscillations of the external magnetic field caused by line-
frequency interference or deliberately applied AC modulation.
The key physical parameters are assumed to be time-varying. The effective coupling
strengthγ(t) and the measurement efficiencyη(t) are chosen as
γ(t) =γ 0

1 + 0.2 sin2πt
T

, η(t) =η 0

1 + 0.1 trit
T

,
where tri(·) is a symmetric triangle wave with range [ −1, 1]. Thus, θ(t) = η(t)γ(t) ∈ [θ, ¯θ]
where θ = 0.72η0γ0 and ¯θ = 1.32η0γ0, reflecting atomic position-field coupling changes (sine)
and slow efficiency drift (triangle).
In addition, environmental noise is modeled by Lindblad operators of the form
C1(t) =
q
γϕ(t)J z, γ ϕ(t) = 1.5

1 + 0.2 cos2πt
T

,
describing dephasing with periodic fluctuation due to background magnetic field or laser phase
noise, and
C2(t) =
q
γ↓(t)


0 0 0
0 0 1
0 0 0

 , γ ↓(t) = 1.5

1 + 0.1 t
T

,
which models selective pumping from diag(0, 0, 1) to diag(0, 1, 0) caused by polarization-
dependent spontaneous emission or auxiliary fields. The time-varying perturbation matrices
can be specified as
˜H0(t)=


0.2 0 0
0 0.1 0.5 + 0.2 sin(2πt/T)
0 0.5 + 0.2 sin(2πt/T) 0.4

.
21

--- 第22页 ---
Figure 1:Three-level system under slow modulation ( T = 100τ). Left: no feedback ( u≡ 0). Right:
reduced-filter feedback u(ˆq). Initial conditions: ρ(0) = diag(0, 0, 1), ˆq(0) = [1, 1, 1]⊤/3. Black curve:
mean over 100 realizations.
The diagonal terms represent static level shifts, while the constant off-diagonal coupling
0.5 models a systematic coherent perturbation between diag(0, 0, 1) and diag(0, 1, 0). The
additional sinusoidal modulation 0 .2 sin(2πt/T ) accounts for bounded time-varying effects
such as line-frequency magnetic-field noise or parametric drift in the driving field.
The Hilbert space decomposes into three one-dimensional subspaces, with the target state
chosen as diag(1, 0, 0). Under this setting, assumptionsA1–A3,A5–A7and conditionC2
are satisfied. We compute c = 1, l = 1 and ¯l = 2. The physical parameters are set as η0 = 0.4,
γ0 = 1.6 yieldingθ = 0.4608 and ¯θ= 0.8448, choosing ˆη= 0.5 and ˆγ= 1.2 makingC3hold.
Let τ := 1/(η0γ0) denote the characteristic measurement time scale. To evaluate robustness,
we consider both slow and fast deterministic modulations: T = 100τ to emulate quasi-static
drifts, andT= 2τto impose rapidly varying perturbations on the reduced filter.
We implement (9) with
Γ =


−1 1 0
1−2 1
0 1−1

 ,
which satisfiesC1. and feedback of the form (14) with a = 4, b = 2 satisfyingA4. Figures 1–2
showd 0(ρ(t)) over 100 trajectories under slow/fast modulation, with and without feedback.
Exponential convergence is observed despite time-varying parameters, in agreement with the
predicted sample Lyapunov exponent−C χ,¯χ/2≈ −0.1218,supporting Theorem 4.10.
6 CONCLUSIONS AND FUTURE WORKS
We studied robust feedback stabilization of perturbed quantum systems under QND measure-
ments using a reduced quantum filter. The proposed method ensures stabilization toward
a target subspace when the free Hamiltonian, coupling strengths, measurement efficiencies,
and perturbations are time-varying, by estimating only the diagonal elements of the system
state in the non-demolition basis. Our analysis highlights invariance-preserving perturbations
and the critical role of accurately known measurement operators in ensuring effectiveness.
Future work will extend these results to broader classes of perturbations and more general
measurement settings, further advancing scalable and robust quantum feedback control.
22

--- 第23页 ---
Figure 2:Three-level system under fast modulation ( T = 2τ). Left: no feedback ( u≡ 0). Right:
reduced-filter feedback u(ˆq). Initial conditions: ρ(0) = diag(0, 0, 1), ˆq(0) = [1, 1, 1]⊤/3. Black curve:
mean over 100 realizations.
Appendices
A Invariant properties of quantum trajectories
This appendix states several auxiliary results used in the proofs of instability and recurrence.
These lemmas concern the invariance properties of the stochastic dynamics and are analogous
to those established in [20, Section 4] and [24, Lemma 7] for SME (1).
The first lemma is a direct analogue of [20, Section 4], its proof is therefore omitted.
Lemma A.1.Assume thatA4holds. The rank ofρ(t)is almost surely non-decreasing.
LetI P :={ρ∈ S(H)|Tr(ρ 2) = 1}denote the set of pure states.
Lemma A.2.Assume thatA4andA6are satisfied. In addition, suppose that there exists
a k∈ [m]such that ¯ηk < 1. Then, for all initial state ρ(0) ∈ I P \ I(H0), ρ(t)is mixed (i.e.,
Tr
 
ρ(t)2
<1) for allt >0almost surely.
Proof. For all ρ∈ I P , we have ρ2 = ρ and Tr(ρAρB) = Tr(ρA)Tr(ρB) with A, B∈ B (H). By
Itˆ o formula, we getdTr(ρ(t)2) = A(t, ρ(t))dt +P
k Bk(t, ρ(t))dWk(t). By a straightforward
calculation, it follows that, for allρ∈ I P ,B k(t, ρ) = 0 for allk, and
A(t, ρ) =−2
mX
k=1
γk(t)
 
1−η k(t)

Tr(L∗
kLkρ)−Tr(L ∗
kρ)Tr(Lkρ)

−2
¯mX
k=1

Tr
 
C∗
k(t)Ck(t)ρ

−Tr
 
C∗
k(t)ρ

Tr
 
Ck(t)ρ

By Cauchy-Schwarz inequality, we have
Tr(L∗
kLkρ)≥Tr(L ∗
kρ)Tr(Lkρ),
Tr
 
C∗
k(t)Ck(t)ρ

≥Tr
 
C∗
k(t)ρ

Tr
 
Ck(t)ρ

,
23

--- 第24页 ---
where the equalities hold if and only if ρ∈ Sd
i=0 I(Hi). By Lemma 4.2, the trajectory exitsSd
i=1 I(Hi) immediately. Then, the state becomes mixed immediately and remains mixed
afterwards almost surely due to Lemma A.1. The proof is complete.□
B Proof of Inequality(4)
Computing the infinitesimal generator LV (ρ) via Itˆ o formula provides a more direct and
compact approach than differentiating the Lyapunov function (3) explicitly, especially since
the quantum stateρis a complex matrix.
Under assumptionsA1andA-qsr, and for u = 0, the cyclic property of the trace implies
that, for anyi∈ {0, . . . , d},
dTr(ρ(t)Πi) =
mX
k=1
p
θk(t)
 
Tr(ρ(t)LkΠi) + Tr(ρ(t)L∗
kΠi)−Tr(L kρ(t) +ρ(t)L ∗
k)Tr(ρ(t)Πi)

dWk(t)
=
mX
k=1
p
θk(t)Zk,i(ρ(t))Tr(ρ(t)Πi)dWk(t),
whereZ k,i(ρ) := 2ℜ{lk,i} −Tr(L kρ+ρL ∗
k). By Itˆ o product rule, we have
dTr(ρ(t)Πi)Tr(ρ(t)Πj) =Tr(ρ(t)Πi)Tr(ρ(t)Πj)
mX
k=1
h
θk(t)Zk,i(ρ(t))Zk,j(ρ(t))dt
+
p
θk(t)
 
Zk,i(ρ(t)) +Z k,j(ρ(t))

dWk(t)
i
.
Due to the invariance of SI, V is twice continuously differentiable when restricted to SI.
Applying Itˆ o formula to
p
Tr(ρ(t)Πi)Tr(ρ(t)Πj) and collecting the drift terms yields the
following infinitesimal generator,
L
q
Tr(ρ(t)Πi)Tr(ρ(t)Πj)
=− 1
8
q
Tr(ρΠi)Tr(ρΠj)
mX
k=1
θk(t)
 
Zk,i(ρ)− Z k,j(ρ)
2
=− 1
2
q
Tr(ρΠi)Tr(ρΠj)
mX
k=1
θk(t)
 
ℜ{lk,i} − ℜ{lk,j }
2
≤ − El
2
q
Tr(ρΠi)Tr(ρΠj).
Therefore, we conclude
LV(ρ)≤ − El
2 V(ρ).
References
[1] Claudio Altafini and Francesco Ticozzi. Modeling and control of quantum systems: An
introduction.IEEE Transactions on Automatic Control, 57(8):1898–1917, 2012.
24

--- 第25页 ---
[2] Nina H Amini, Paolo Mason, and Ibrahim Ramadan. Feedback stabilization via a quantum
projection filter.SIAM Journal on Control and Optimization, 63(1):S128–S147, 2025.
[3] A. Barchielli and M. Gregoratti.Quantum Trajectories and Measurements in Continuous
Time: The Diffusive Case. Springer, 2009.
[4] Alberto Barchielli. Markovian dynamics for a quantum/classical system and quantum
trajectories.Journal of Physics A: Mathematical and Theoretical, 57(31):315301, 2024.
[5] Alberto Barchielli and Matteo Gregoratti. Quantum measurements in continuous time,
non-Markovian evolutions and feedback.Philosophical Transactions of the Royal Society
A: Mathematical, Physical and Engineering Sciences, 370(1979):5364–5385, 2012.
[6] V. P. Belavkin. Nondemolition measurements, nonlinear filtering and dynamic program-
ming of quantum stochastic processes. InModeling and Control of Systems, pages 245–265.
Springer, 1989.
[7] I. Bengtsson and K. ˙Zyczkowski.Geometry of quantum states: an introduction to quantum
entanglement. Cambridge University Press, 2017.
[8] T. Benoist and C. Pellegrini. Large time behavior and convergence rate for quantum filters
under standard non demolition conditions.Communications in Mathematical Physics,
331(2):703–723, 2014.
[9] T. Benoist, C. Pellegrini, and F. Ticozzi. Exponential stability of subspaces for quantum
stochastic master equations. InAnnales Henri Poincar´ e, volume 18, pages 2045–2074,
2017.
[10] L. Bouten, R. van Handel, and M. James. An introduction to quantum filtering.SIAM
Journal on Control and Optimization, 46(6):2199–2241, 2007.
[11] H.P. Breuer and F. Petruccione.The theory of open quantum systems. Oxford University
Press, 2002.
[12] Gerardo Cardona, Alain Sarlette, and Pierre Rouchon. Exponential stabilization of quan-
tum systems under continuous non-demolition measurements.Automatica, 112:108719,
2020.
[13] D. Dong and I. R. Petersen. Quantum control theory and applications: a survey.IET
control theory & applications, 4(12):2651–2671, 2010.
[14] Alessio Fallani, Matteo AC Rossi, Dario Tamascelli, and Marco G Genoni. Learning
feedback control strategies for quantum metrology.PRX Quantum, 3(2):020310, 2022.
[15] Qing Gao, Daoyi Dong, Ian R Petersen, and Steven X Ding. Design of a quantum
projection filter.IEEE Transactions on Automatic Control, 65(8):3693–3700, 2019.
[16] Qing Gao, Guofeng Zhang, and Ian R Petersen. An improved quantum projection filter.
Automatica, 112:108716, 2020.
[17] Tommaso Grigoletto, Cl´ ement Pellegrini, and Francesco Ticozzi. Quantum model re-
duction for continuous-time quantum filters. InAnnales Henri Poincar´ e, pages 1–53.
Springer, 2025.
25

--- 第26页 ---
[18] Manuel Guatto, Gian Antonio Susto, and Francesco Ticozzi. Improving robustness of
quantum feedback control with reinforcement learning.Physical Review A, 110(1):012605,
2024.
[19] R. Khasminskii.Stochastic Stability of Differential Equations, volume 66. Springer, 2011.
[20] W. Liang, N. H. Amini, and P Mason. On exponential stabilization of N-level quantum
angular momentum systems.SIAM Journal on Control and Optimization, 57(6):3939–
3960, 2019.
[21] Weichao Liang. Feedback stabilization of perturbed quantum systems via reduced filters.
InIEEE International Conference on Quantum Control, Computing and Learning, pages
173–178, 2025.
[22] Weichao Liang and Nina H Amini. Model robustness for feedback stabilization of open
quantum systems.Automatica, 163:111590, 2024.
[23] Weichao Liang and Nina H Amini. Model robustness for feedback stabilization of open
quantum systems.Automatica, 163:111590, 2024.
[24] Weichao Liang, Nina H Amini, and Paolo Mason. Feedback exponential stabilization of
GHZ states of multiqubit systems.IEEE Transactions on Automatic Control, 67(6):2918–
2929, 2021.
[25] Weichao Liang, Nina H Amini, and Paolo Mason. Robust feedback stabilization of N-level
quantum spin systems.SIAM Journal on Control and Optimization, 59(1):669–692, 2021.
[26] Weichao Liang, Kentaro Ohki, and Francesco Ticozzi. Exploring the robustness of
stabilizing controls for stochastic quantum evolutions.SIAM Journal on Control and
Optimization, pages S148–S174, 2025.
[27] Hideo Mabuchi. Continuous quantum error correction as classical hybrid control.New
Journal of Physics, 11(10):105044, 2009.
[28] Xuerong Mao.Stochastic Differential Equations and Applications. Woodhead Publishing,
2 edition, 2007.
[29] M. Mirrahimi and R. van Handel. Stabilizing feedback controls for quantum systems.
SIAM Journal on Control and Optimization, 46(2):445–467, 2007.
[30] Anne EB Nielsen, Asa S Hopkins, and Hideo Mabuchi. Quantum filter reduction for
measurement-feedback control via unsupervised manifold learning.New Journal of
Physics, 11(10):105043, 2009.
[31] M. A. Nielsen and I. L. Chuang.Quantum Computation and Quantum Information.
Cambridge University Press, 2010.
[32] Nissim Ofek, Andrei Petrenko, Reinier Heeres, Philip Reinhold, Zaki Leghtas, Brian
Vlastakis, Yehan Liu, Luigi Frunzio, et al. Extending the lifetime of a quantum bit with
error correction in superconducting circuits.Nature, 536(7617):441–445, 2016.
[33] Jonathan Oppenheim and Zachary Weller-Davies. The constraints of post-quantum
classical gravity.Journal of High Energy Physics, 2022(2):1–39, 2022.
26

--- 第27页 ---
[34] P. E. Protter.Stochastic Integration and Differential Equations. Springer, 2004.
[35] D Riste, M Dukalski, CA Watson, G De Lange, MJ Tiggelman, Ya M Blanter, Konrad W
Lehnert, RN Schouten, and L DiCarlo. Deterministic entanglement of superconducting
qubits by parity measurement and feedback.Nature, 502(7471):350–354, 2013.
[36] E. D. Sontag.Mathematical control theory: Deterministic Finite Dimensional Systems,
volume 6. Springer, 1998.
[37] D. W. Stroock and S. R. Varadhan. On the support of diffusion processes with applica-
tions to the strong maximum principle. InProceedings of the Berkeley Symposium on
Mathematical Statistics and Probability, volume 1, pages 333–359, 1972.
[38] SS Szigeti, MR Hush, ARR Carvalho, and JJ Hope. Continuous measurement feedback
control of a bose-einstein condensate using phase-contrast imaging.Physical Review
A—Atomic, Molecular, and Optical Physics, 80(1):013614, 2009.
[39] F. Ticozzi, K. Nishio, and C. Altafini. Stabilization of stochastic quantum dynamics via
open-and closed-loop control.IEEE Transactions on Automatic Control, 58(1):74–85,
2012.
[40] F. Ticozzi and L. Viola. Quantum Markovian subsystems: invariance, attractivity, and
control.IEEE Transactions on Automatic Control, 53(9):2048–2063, 2008.
[41] R. van Handel.Filtering, stability, and robustness. PhD thesis, California Institute of
Technology, 2007.
[42] R. van Handel, J. K Stockton, and H. Mabuchi. Feedback control of quantum state
reduction.IEEE Transactions on Automatic Control, 50(6):768–780, 2005.
[43] R. van Handel, J. K. Stockton, and H. Mabuchi. Modelling and feedback control design
for quantum state preparation.Journal of Optics B: Quantum and Semiclassical Optics,
7(10):S179, 2005.
[44] Ramon van Handel and Hideo Mabuchi. Quantum projection filter for a highly nonlinear
model in cavity QED.Journal of Optics B: Quantum and Semiclassical Optics, 7(10):S226,
2005.
[45] R Vijay, Chris Macklin, DH Slichter, SJ Weber, KW Murch, Ravi Naik, Alexander N
Korotkov, and Irfan Siddiqi. Stabilizing rabi oscillations in a superconducting qubit using
quantum feedback.Nature, 490(7418):77–80, 2012.
[46] Jing Zhang, Yu-xi Liu, Re-Bing Wu, Kurt Jacobs, and Franco Nori. Quantum feedback:
theory, experiments, and applications.Physics Reports, 679:1–60, 2017.
27

```

---

