# 量子平滑与错误假设 - 深度提取内容

**论文ID**: arXiv 2506.15951

**总页数**: 24

---

## 引言/概述

```

--- 第1页 ---
Quantum state smoothing when Alice assumes the
wrong type of monitoring by Bob
Areeya Chantasri 1,2, Kiarn T. Laverick 2,3,4, Howard M.
Wiseman 2
1Optical and Quantum Physics Laboratory, Department of Physics, Faculty of
Science, Mahidol University, Bangkok, 10400, Thailand
2Centre for Quantum Computation and Communication Technology (Australian
Research Council), Quantum and Advanced Technology Research Institute, Griffith
University, Yuggera Country, Brisbane, QLD 4111, Australia
3MajuLab, CNRS-UCA-SU-NUS-NTU International Joint Research Laboratory
4Centre for Quantum Technologies, National University of Singapore, 117543
Singapore, Singapore
E-mail: areeya.chn@mahidol.ac.th, dr.kiarn.laverick@gmail.com,
h.wiseman@griffith.edu.au
15 July 2025
Abstract. An open quantum system leaks information into its environment. In some
circumstances it is possible for an observer, say Alice, to recover that information, as a
classical measurement record, in a variety of different ways, using different experimental
setups. The optimal way for Alice to estimate the quantum state at time t from
the record before t is known as quantum filtering. Recently, a version of quantum
smoothing, in which Alice estimates the state at time t using her record on both sides
of t, has been developed. It requires Alice to make optimal inferences about the pre- t
record of a second observer, say Bob, who recovers whatever information Alice does
not. But for Alice to make this inference, she needs to know Bob’s setup. In this
paper we consider what happens if Alice is mistaken in her assumption about Bob’s
setup. We show that the accuracy — as measured by the Trace-Squared-Deviation,
of Alice’s estimate of the true state ( i.e., the state conditioned on her and Bob’s pre-
t records) — depends strongly on her setup, Bob’s actual setup, and the wrongly
assumed setup. Using resonance fluorescence as a model system, we show numerically
that in some cases the wrong smoothing is almost as accurate as the right smoothing,
but in other cases much less accurate, even being less accurate than Alice’s filtered
estimate. Curiously, in some of the latter cases the fidelity of Alice’s wrong estimate
with the true state is actually higher than that of her right estimate. We explain this,
and other features we observe numerically, by some simple analytical arguments.
arXiv:2506.15951v1  [quant-ph]  19 Jun 2025

--- 第2页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 2
1. Introduction
Many theoretical techniques applied to quantum systems have been borrowed from
those successfully implemented in classical regimes. However, some have posed new
puzzles, which could also lead to new discoveries. In this work, we are interested in
problems of continuously monitored systems, where unknown physical states are to be
estimated given partial information from observation. Two of the techniques in classical
signal processing are filtering [1, 2, 3] and smoothing [4, 5, 6], where noisy measurement
signals can be ‘filtered’ (causally) or ‘smoothed’ (acausally) to estimate the underlining
physical state dynamics of the system in time. The filtering technique can be readily
extended to the quantum realm [7, 8, 9, 10]. However, the extension of smoothing is less
straight-forward, because it involves estimating a state using future information. This
has led to various formalisms, including the two-state formalism [11, 12, 13] (generalized
as the past quantum state formalism [14, 15]), weak values [16] and the weak-valued
state [14, 17], smoothed psuedo-probability distributions [18, 19] and the most likely
path formalism [20, 21]. In this paper, we are concerned with another formalism, known
as quantum state smoothing [22]. (See Ref. [23] for a unified presentation and application
of many of these formalisms to an open quantum system.)
Quantum state smoothing applies to open quantum systems where information is
missing. That is, the observer (Alice) has access to only some of the information leaking
out of the system into its environment. Another observer (Bob), with access to the
missing information as well as Alice’s information, can estimate the system’s properties
better than Alice, allowing him to assign it a more pure state. Using quantum state
smoothing, Alice can do better than using quantum state filtering, in the sense that she
can assign a state that is closer to the unknown (to her, but known to Bob) state. This
is a fair comparison because both quantum state smoothing and filtering can be defined
as the task of optimally estimating the unknown state with the cost function being the
trace-square-deviation [23] or, equivalently, the relative entropy [24]. The only difference
is that quantum smoothing, like classical smoothing, uses Alice’s future record as well
as her past record.
However, because of the differences between classical and quantum mechanics,
quantum state smoothing has some differences from the classical case, even in situations
where one might assume they are the same [25]. Here, we are concerned with the fact
that, contrary to classical state smoothing, the quantum version requires Alice to know
how Bob is obtaining his information from the system’s environment. That is, Bob
has to choose a particular measurement setup to monitor the environment, and Alice
has to know what that setup is. This difference raises intriguing questions about how
the quantum state smoothing power varies with different setups of the unobserved (by
Alice) channels [26, 27]. Here, by smoothing power, we mean how much improvement
smoothing offers over filtering, in terms of the cost function. In fact, by choosing
different setups, Bob changes his ‘unraveling’ [8] of the master equation, which can
result in quantum smoothed states with quite different properties [25, 26, 28].

--- 第3页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 3
In this paper, we pose an even more dramatic question for the quantum state
smoothing formalism: what would happen if Alice made a wrong assumption about what
measurement setup Bob was using? How badly does this affect her ability to estimate
the actual unknown state? Could smoothing even become worse than filtering? Does
it depend on the characteristics of Bob’s actual unraveling in relation to the wrongly
assumed one? And does it depend on the characteristics of Alice’s unraveling in relation
to one or the other of these?
To address these questions, after detailing the quantum state smoothing formalism
in Sec. 2, we introduce in Sec. 3 the simple system we will focus upon. This is a driven
two-level atom where three measurement setups are considered: photon detection, x-
homodyne detection, and y-homodyne detection, as analyzed in Ref. [26]. In Sec. 4, we
make some broad conjectures about smoothing power for all 18 combinations of Alice’s
setup, Bob’s (actual) setup, and a (different) wrongly assumed setup for Bob. Numerical
simulations in Sec. 5 validate these conjectures, and also allow us to dig more deeply
into the questions in the preceding paragraph. We find that with a wrongly assumed
unobserved (Bob’s) setup, the smoothing power (defined using the cost function) is
sometimes roughly the same as that with the rightly assumed setup, but in other cases
significantly worse than this, or even negative. This last case indicates that the quantum
state smoothing is worse than the quantum state filtering (which is independent of Bob’s
measurement), but in this case, paradoxically, the smoothed state typically has a higher
fidelity with the unknown state than does the filtered state. We give some analytical
explanations supplemented by numerical results for these observations in Sec. 6. Finally,
we conclude in Sec. 7.
2. Quantum State Smoothing
Let us consider an open quantum system coupled to two independent baths (or
environments) under the strongest Markov assumption [29]. One of the baths is
monitored by an observer, Alice, so that a measurement record O is observed by Alice.
Here the double-headed arrow means a record over the full duration of the experiment,
the interval [ti, tf). The other bath is not monitored by Alice, but it is assumed to
yield a measurement record U by virtue of a second observer labelled Bob. That is,
U is unobserved by Alice, our primary observer. Bob may be an actual observer, or
just a stand-in for the way information is robustly present in the environment due to
decoherence [30, 31, 32, 33]. Therefore, Alice has access to only part of the classical
information about the quantum system.
It is useful to consider an observer who knows both O and U. To save introducing
a third observer with this role, we can assume that Bob knows Alice’s record and
the measurement setup used to obtain it, as well as his own. Then Bob has all the
information and, if the initial state of the system is pure, his conditioned state at any
time t≥ti, denoted by ρO,U, will also be pure. Here O and U are the records from time
ti up to time t. Thus ρO,U can be regarded as the true state of the quantum system at

--- 第4页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 4
time t, since no other observer can assign a more pure state.
Alice’s task, defined loosely for now, is to estimate the true state (Bob’s state) at
time t, using only her observed record O. This could involve making inferences about
what records Bob may have, and with what probabilities.
The most straightforward technique for Alice, without any need to know what
type of monitoring happens on Bob’s side, is to compute her estimated state from the
observed record using the quantum trajectory approach [8, 10], also called quantum state
filtering [7, 9]. The technique yields an estimated state ρO at any time t, conditioned on
(past) observed measurement results from the initial time ti up to the time t. The pure
state ρO,U introduced above is exactly this kind of filtered state, but there conditioned
on both the observed ( O) and unobserved ( U) records. Let us define a little more
formally the past observed record as O ≡{os∶s∈[ti, t)}, where os denotes the observed
meausurement outcome at time s, and similarly for U. Alice’s filtered quantum state,
ρO(t), which has also been denoted ρF(t), is mixed because it is conditioned only on
partial information. Indeed, it is defined without reference to Bob’s information U.
Nevertheless it can be related to the state conditioned on the latter [22]:
ρO(t) = ⟨ρO,U(t)⟩
U ∣O
≡∑
U
℘(U∣O)ρO,U(t). (1)
That is, it could be computed from considering all possible true statesρO,U and summing
over the unobserved record using ℘(U∣O). This last is a classical probability density
function of past unobserved records conditioned on the past observed record, which can
be obtained by classically filtering (processing in real time) the record O.
However, as shown in Refs. [22, 23], Alice can do better than quantum state filtering
by additionally using the remaining measurement results after the estimation time
O ≡{os ∶s ∈[t, tf)} (future record) to help with the state estimation. This leads
to the quantum state smoothing technique, where the filtered probability distribution
℘(U∣O) is replaced by the smoothed probability distribution℘(U∣O). The key difference
is that smoothing requires processing of the whole record O, which must necessarily be
done after the fact. In other words, the estimated state becomes
ρdU
O (t) = ⟨ρO,U(t)⟩
U ∣O
≡∑
U
℘(U∣O)ρO,U(t). (2)
This is called the smoothed quantum state, which has also been denoted ρS(t),
conditioned on the whole (past and future) observed record. We note that, to calculate
a smoothed quantum state, Alice is required to make an assumption about Bob’s
measurement setup (unobserved by Alice), so we have introduced the superscript dU
in Eq. (2) to emphasise that. The relationship between the two classical probability
distributions used in Eq. (1) and Eq. (2) is
℘(U∣O)∝℘(O∣U, O)℘(U∣O), (3)

--- 第5页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 5
which is Bayes’ theorem with the factor℘(O) omitted, leading to proportionality rather
than equality. The relation (3) is useful for numerically evaluating the smoothed
quantum state (2), which is a non-trivial procedure; for details, see Refs. [23, 24, 34].
In the above, we said that smoothing gives a better estimate than filtering, but
that is meaningless unless we define the cost function for evaluating estimates. In
fact, both the filtered and smoothed states in Eq. (1) and Eq. (2), respectively, are
optimal estimators for the expected Trace Square Deviation (TrSD) cost functions, but
conditioned on different information. The TrSD, also known as the square of the Hilbert-
Schmidt distance [35], is defined as
S[ρ, σ]= Tr[(ρ−σ)2]. (4)
As shown in Ref. [23], the filtered state can be defined as
ρO(t) = arg min
ρ∈S
⟨S[ρ, ρO,U(t)]⟩
U ∣O
, (5)
the element of the set of unit-trace positive semi-definite operators S with minimum
expected TrSD to the true state, conditioned on the past observed record. Similarly,
the smoothed state can be defined as
ρdU
O (t) = arg min
ρ∈S
⟨S[ρ, ρO,U(t)]⟩
U ∣O
, (6)
the estimator that minimizes the expected TrSD to the true state conditioned on the
past-future observed record. Assuming (as we will throughout) that the true state ρO,U
is pure, the minimal value of the expected TrSD (i.e., when using the optimal estimator),
is given by the impurity 1 −P[ρO(t)]. Here O indicates O or O, depending on whether
we are doing filtering or smoothing, and the purity is defined as usual, via
P[ρ]= Tr[ρ2]. (7)
Of course, the TrSD is only one of many quantifiers of the difference between two
quantum states. The justification for choosing it is that it is simple to use and reproduces
the standard filtered state ρO (and in particular its property of being independent of
Bob’s monitoring choice). In fact, the same filtered and smoothed states also arise from
using relative entropy in place of TrSD [24], but the TrSD is mathematically simpler. By
contrast, using negative Fidelity — with the negative sign allowing us to consider it a
cost function, to be minimized — instead of TrSD leads to optimal filtered and smoothed
states that are different. Since we have assumed pure true states, the Fidelity, as defined
originally by Jozsa [36], can be simplified to
F[ρ, σ]= Tr[ρ σ], (8)
which holds if either ρ or σ is pure. The optimal estimators by the negative Fidelity
cost function are “lustrated” versions of the standard ones [23, 24]. In this paper we
stick to the TrSD as the cost function to define the estimates, but we will also calculate
the Fidelity of these estimates, as we now discuss.

```

---

## 方法/公式

```

--- 第6页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 6
2.1. Quantities for state comparisons between valid and wrong smoothing
While the expected TrSD from the true state is the quantity that is minimized by the
standard optimal smoothed (or filtered) quantum state (depending on the information
available), there are other natural quantities that quantify the deviation from the true
state, as discussed above. In particular, it is interesting to compute for our estimates
not only the expected TrSD, but also the expected Fidelity of the estimated state with
the true state. The TrSD, as introduced in the previous section, has values between
0 (the two states are identical) and 2 (the two states are pure and orthogonal). By
contrast, the Fidelity F goes from 0 to 1, which are obtained when the two states are
orthogonal and identical, respectively. Interestingly, it has also been proven [24, 26]
that, for a given observed record, O, and an optimal estimate ρO (in the TrSD sense
defined above),
1−⟨S[ρdU
O (t), ρO,U(t)]⟩
U ∣O
= ⟨F[ρdU
O (t), ρO,U(t)]⟩
U ∣O
= P(ρdU
O (t)). (9)
That is, the expected distance of the estimated state from the true state, by either
TrSD or Fidelity measures, can be evaluated simply by computing the Purity of the
(TrSD-optimal) state ρO, whether O = O (filtering) or O = O (smoothing). In previous
work [23, 26], it has been shown that smoothed states generally give higher purities,
and hence a higher fidelity with the true states, which one would expect given that
the smoothed state uses more information (the whole observed record) than the filtered
state (past-only observed record).
However, in this paper, we are interested in the case of the sub-optimal estimates
that arise when Alice makes an erroneous assumption about Bob’s setup when
computing her smoothed estimate. To understand the features of such “wrong” or
“erroneous” smoothed quantum states, it is helpful to distinguish these cases, which
we do by using the notation dV and V for the valid setting and records, respectively,
and dW and W for the wrong case, in place of dU and U. In the first case, Alice
makes the valid assumption about Bob’s measurement setup, and thus considers the
correct possible records, leading to “right smoothing”, with ρdV
O
(t) given by Eq. (2)
with dU = dV and U = V . In the second case, Alice assumes the wrong setup, leading
to “wrong smoothing”, with ρdW
O
(t) given by Eq. (2) with dU = dW and U = W . This
is “wrong” because the true state is still determined by V , not W , meaning that none
of the equalities in Eq. (9) will hold:
P(ρdW
O ) ≠1−⟨S[ρdW
O (t), ρO,V(t)]⟩
V ∣O
≠⟨F[ρdW
O (t), ρO,V(t)]⟩
V ∣O
≠P(ρdW
O ). (10)
For the rest of the paper, the notations dU (and U) will be used only when it can be
replaced by either dV (and V) or dW (and W).
Since the expected distances between filtered or smoothed states and true states
vary from realization to realization of the observed records, O, just as the purity of
the conditioned states vary. Thus, to make quantitative comparisons of the different

--- 第7页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 7
scenarios around measurement setups and beliefs about them, we want to average over
all possible observed records as well. We denote this average, over both observed and
valid unobserved records, by E[⋅] (for total ensemble average). For the TrSD we have
E[S[ρdU
O (t), ρO,V(t)]]≡∑
O,V
℘(O, V )Tr{[ρdU
O (t)−ρO,V(t)]2}, (11)
as an average TrSD distance for the estimated state ρdU
O . Similar expressions hold for
the ensemble average fidelity F and Purity P, but we note that the latter does not
require averaging over V . In particular, we consider what would be measures of the
power of smoothing relative to filtering, as follows.
1) Smoothing Power in terms of (negative) Trace Square Deviation
RdU
S (t) =−E[S[ρdU
O (t), ρO,V(t)]]+ E[S[ρO(t), ρO,V(t)]], (12)
2) Smoothing Power in terms of Fidelity
RdU
F (t) =+E[F[ρdU
O (t), ρO,V(t)]]−E[F[ρO(t), ρO,V(t)]], (13)
3) Smoothing Power in terms of Purity
RdU
P (t) =+E[P[ρdU
O (t)]]−E[P[ρdU
O (t)]]. (14)
Note, the difference in sign for the TrSD, as also appearing in Eq. (9), is because it is
a quantity we wish to minimize, while the Fidelity and Purity are quantities we would
expect (at least na¨ ıvely) to be maximized for a good estimate. If Alice’s assumption
about Bob’s measurement setup is valid, one would expect a positive smoothing power
in all three cases. However, if Alice assumes the wrong setup, it is not obvious that
this will be so. Before calculating what does happen, we introduce our model system
(Sec. 3) and make some predictions (Sec. 4).
3. Model system: Coherently-driven qubit in vacuum bosonic baths
Let us consider the example of a coherently-driven qubit, as in Refs. [22, 23, 24, 26].
The single qubit is driven by a qubit oscillation around the x-axis of the Bloch sphere
with a frequency Ω and is coupled to two baths described by the Lindblad equation:
dρ(t) =−idt[ ˆH, ρ(t)]+ dt D[ˆco]ρ(t)+ dt D[ˆcu]ρ(t). (15)
Here Alice only observes the first channel ˆco and Bob measures the other bath ˆcu which is
hidden from Alice (unobserved channel). The Hamiltonian is ˆH = (Ω/2) ˆσx and the two
Lindblad operators describing coupling to bosonic baths are assumed to be the (qubit
fluorescence) lowering operators: ˆco,u =
√
γ/2 ˆσ−with the same decay rate γ/2 such that
both channels acquire the same amount of information.

--- 第8页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 8
Following Ref. [26], we consider three types of setup for the continuous
measurement: (a) direct photon detection (leading to a jump-like unravelling), (b)
x-quadrature homodyne detection (leading to a diffusive unravelling), and (c) y-
quadrature homodyne detection (also diffusive). We use the symbol d J for the
measurement record obtained in a time step of duration d t, with subscripts N, X, and
Y to distinguish the three different types of monitoring.
For the photon detection setup, the photon count in the infinitesimal interval is
either d JN = 1 (click) or d JN = 0 (no click). The respective operations [10, 37] (trace-
decreasing maps) are M1ρ= ˆcN ρ ˆc†
Ndt and M0ρ= M0ρM †
0, where M0 = ˆ1−i ˆHdt−1
2ˆc†
NˆcNdt.
Here ˆcN =
√
γ/2ˆσ−, which is the same as ˆco,u. The map M1 includes the unitary evolution
described by the Hamiltonian ˆH but, for the sake of a simple presentation, omits the
effect of the other channel. (Obviously when both channels are considered we do not
include the Hamiltonian evolution twice; this remark applies also to the diffusive cases
below.) Since d t is infinitesimal, the above dynamics can be described by the stochastic
master equation for quantum jumps,
dρ(t) =−i dt[ ˆH, ρ(t)]+ dJN(t)G[ˆcN]ρ(t)−dt H[1
2ˆc†
NˆcN]ρ(t), (16)
where we use [10]
G[ˆc]= ˆc ρˆc†
Tr[ˆc ρˆc†]−ρ, (17)
H[ˆc]= ˆcρ+ ρˆc†−Tr[ˆcρ+ ρˆc]ρ. (18)
Turning now to the x- and y-homodyne detections, these are homodyne detections
with local oscillator phases being Φ = 0 and Φ = π/2, respectively. In contrast to
photon detection, homodyne measurement results during an infinitesimal interval can
have any real value, denoted by d JΦ. Defining the Lindblad operators for these cases
by ˆcΦ =
√
γ/2ˆσ−e−iΦ, the associated measurement operations are MdJΦ = MdJΦρM †
dJΦ
where MdJΦ = ˆ1−i ˆHdt−1
2ˆc†
ΦˆcΦdt+ dJΦˆcΦ. This yields a diffusive unravelling for the
system state described by the stochastic master equation [10],
dρ(t) =−i dt[ ˆH, ρ(t)]+ dt D[ˆcΦ]ρ(t)+ dWΦ(t)H[ˆcΦ]ρ(t). (19)
Here d WΦ is a Wiener process related to the measurement record via d WΦ(t) =
dJΦ−Tr[(ˆcΦ+ ˆc†
Φ)ρ(t)]dt. For convenience, we denote d JX ≡dJΦ=0 and dJY ≡dJΦ=π/2,
for the results of x-homodyne and y-homodyne, respectively.
To ease our later discussion, we adopt the style of notation used in Ref. [26],
generalized to the purpose of this paper: “dO” as shorthand for the “Observed”
measurement setup or unravelling, and “dU” as shorthand for “Unobserved”
measurement setup or unravelling. That is, we use the same capital letter for the
monitoring setup as for the records themselves ( O and U) as in Sec. 2, but preceded by
a “d” and all in Roman font. Also following Sec. 2, since we will allow for Alice to make
either a valid or wrong assumption about Bob’s measurement setup, the unobserved

--- 第9页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 9
monitoring setup dU can be replaced by two options: “dV” for “Valid” (or right)
unobserved setup and “dW” for “Wrong” unobserved setup.
Each of dO, dV, and dW can be one of the three options:
dN /Leftr⫯g⊸tl⫯ne⇒jump records, d JN,
dX /Leftr⫯g⊸tl⫯ne⇒x-homodyne records, d JX,
dY /Leftr⫯g⊸tl⫯ne⇒y-homodyne records, d JY.
(20)
For the right measurement records, there are in total nine combinations, denoted by
dOdV = dNdN, dNdX, dNdY, dXdN, dXdX, dXdY, dYdN, dYdX, dYdY. However, each
of the right combination can have two types of wrongly assumed setups dW (not to be
confused with the Weiner increment dWΦ). Thus, there are additional 18 combinations
giving “wrong smoothing”.
Before turning to the smoothed state under these 27 scenarios, we note that a
wrong assumption by Alice about Bob’s monitoring setup makes no difference to the
optimal filtered state. That is because, as noted before, although the filtered state can
be defined with reference to Bob’s information U as in Eq. (1), it can also be defined
without any such reference. Thus, there are only 3 different types of filtered states,
depending on whether Alice’s setup dO equals dN, dX, or dY.
4. Conjectures based on correlations of measurement records
From previous work [22, 26], it has been shown that quantum state smoothing typically
improves the fidelity between the estimated states to the hidden true states, relative
to filtering. In particular, Ref. [26] investigated systematically the smoothing power
in terms of Purity, RP, in Eq. (14). This latter quantity is the average purity of the
smoothed state minus that of the filtered states, and so in Ref. [26] was called the average
purity recovery. [Recall that in the case of a rightly assumed setup, RP is the same as
the smoothing power in terms of Fidelity ( RF) (13) and the smoothing power in terms
of TrSD ( RS) (12), because of Eq. (9).] Notably, it was found that there was a large
variation in the smoothing power for different dOdV measurement setups (or dOdU,
to use the notation of [26], where dOdW was not considered). More interestingly, it
was shown that this variation can be explained by the variation in correlation strength
between the observed and unobserved measurement records. The greater the correlation
strength, the higher the smoothing power.
Now consider what will happen if Alice mistakenly assumes the wrong measurement
setup for Bob when she does smoothing. We propose that the correlation strength should
still have the ability to predict the smoothing power, because the correlation between two
measurement records indicates how strong the stochastic measurement backaction on
the system’s state from one measurement affects the result of the other measurement. In
the following, we propose four conjectures based on this intuition about correlation and
measurement backaction, and how it would affect the power of (even wrong) smoothing.
These conjectures were made prior to obtaining the numerical results in Sec. 5.

--- 第10页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 10
4.1. Correlations of measurement records
Following Ref. [26], we begin by considering a normalized two-time correlation function
between any two measurement records,
C2[dO, dU]≡E[dJO(t+ τ)dJU(t)]ss−E[dJO(t+ τ)]ssE[dJU(t)]ss
NONU
, (21)
where JO, JU ∈{JN, JX, JY}, with JO and JU representing the two simultaneous
measurement signals, observed and unobserved by Alice respectively (recall that we
have two output channels of equal strength in our model). The expected value E [⋅]ss
is computed over an ensemble of trajectories in the steady-state (ss) regime; that is,
in any interval where the trajectory is statistically independent of the initial and final
conditions. The normalized factors N in Eq. (21), defined so that the correlations are
all of the same magnitude and independent of d t, are N●=
√
⟨(dJ●)2⟩ss/dt; see Ref. [26]
for more details. Unlike in that paper, here we consider only this two-point correlation
function (as indicated by the subscript 2 of the C2 function in Eq. (21)), and only the
crudest classification of it, namely whether it is zero for all time differencesτ or non-zero
for some τ. Note that the two-time correlators being zero does not imply that higher
order (multi-time) correlations between the two measurement records dO and dU are
zero [26]. Nevertheless, the two-time correlation is the dominant contribution to the
power of the smoothing, as was shown numerically in Ref. [26]. Therefore, for the rest
of the paper, we will use this notation without the ‘2’ subscript: C[dO, dU]∼✗ to refer
to C2[dO, dU]= 0 and C[dO, dU]∼✓ for C2[dO, dU]≠0.
dX dY dN
dX ✓ ✗ ✗
dY ✗ ✓ ✓
dN ✗ ✓ ✓
T able 1. Summary of normalized two-time correlation functions between any two
measurement records in a binary format: ‘ ✗’ for zero correlation and ‘ ✓’ for finite
correlation. The measurement records are shown with the defined notation: dN, dX,
and dY, referring to the photon count, the x-homodyne, the y-homodyne records,
respectively.
The results for the two-time correlators among dN, dX, and dY are shown in Table 1.
In words, the Table shows that: (1) the autocorrelations are always nonzero, as expected,
(2) the cross correlation is nonzero only between dN and dY. This occurs because both
dN and dY have measurement backaction in the y-z plane of the Bloch sphere, which
is in the same plane as the Rabi evolution, while dX is the only setup that gives the
measurement backaction in the x-coordinate of the qubit [26]. This binary classification
is sufficient because, for our system, the non-zero cross correlations are comparable in
size to the autocorrelations [26].

--- 第11页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 11
4.2. Four conjectures for valid-wrong smoothing
In Table 2, we summarize our four conjectures regarding the smoothing power for
a wrongly assumed setup, based on zero and non-zero correlators of the two types:
C[dO, dV] and C[dO, dW].
C[dO, dV]∼✗ C[dO, dV]∼✓
C[dO, dW]∼✗ C1: RdW ∼RdV ∼small C3: RdW ≪RdV ∼large
C[dO, dW]∼✓ C2: RdW ∼?, RdV ∼small C4: RdW ∼RdV ∼large
T able 2. Summary of four conjectures (C1 - C4) based on the correlations between
records from Alice’s setup (dO), records from Bob’s actual setup (dV), and from a
wrongly assumed setup for Bob (dW). The symbol R stands for all types of smoothing
power defined in Section 2.1 except for the conjecture where a question mark appears
(see text). In the main text RdV and RdW are referred to as right smoothing power
and wrong smoothing power, respectively. Here “large” and “small” are relative terms.
Let us start with the first two conjectures that are in the diagonal cells of Table 2.
Conjecture 1: (Top-left of Table 2) If the observed record is correlated neither
with the unobserved record from the correct (valid) setup nor the record from the wrongly
assumed setup, i.e., C[dO, dV]∼✗ and C[dO, dW]∼✗, then the Wrong smoothing power
should be roughly the same as the Valid smoothing power and both should be small.
Cases for Conjecture 1: dOdVdW = dXdYdN, dXdNdY.
Conjecture 4: (Bottom-right of Table 2) If the observed record is correlated both
with the unobserved record from the correct (valid) setup and the record from the wrongly
assumed setup, i.e., C[dO, dV]∼✓ and C[dO, dW]∼✓ then the Wrong smoothing power
should be roughly the same as the Valid smoothing power and both are not small.
Cases for Conjecture 4: dOdVdW = dYdYdN, dNdNdY, dYdNdY, dNdYdN
In the two conjectures above, the level of correlations between the observed and
unobserved records are the same for both the correct (valid) setup (dV) and from the
wrongly assumed setup (dW). The intuition behind these conjectures is as follows. In
both case, the similar correlations between the observed record and the valid and wrong
unobserved measurement setups implies that the different unobserved measurements
have similar backaction on the system. As such, while the smoothed state will not be
identical between the correctly and incorrectly assumed setups, we expect it to be sim-
ilar. Thus, the performance in terms of smoothing power for the wrong smoothed state
should be similar to that of the valid smoothed state, which is small for the uncorrelated
case and large (in relative terms) for the correlated case.
Conjecture 2: (Bottom-left in Table 2) If the observed record is uncorrelated with

--- 第12页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 12
the correct (valid) unobserved record, i.e., C[dO, dV]∼✗, but it is correlated with the
record from the wrongly assumed setup, i.e., C[dO, dW]∼✓ then the Valid smoothing
power should be small, but the Wrong smoothing power may be strange.
Cases for Conjecture 2: dOdVdW = dXdNdX, dXdYdX, dNdXdN, dNdXdY, dY-
dXdY, dYdXdN.
In these cases, when there is near-zero correlation between the records from dO
and dV, it means that, to a first approximation [26], the unobserved measurement does
not incur any measurement backaction onto the quantum system such that Alice’s mea-
surement can detect. That is, there should be little effect from Bob’s measurement
on Alice’s observed record, and hence the right smoothing power will be small. In
this situation, if Alice assumes an incorrect measurement setup dW that gives a record
with a non-zero correlation with her observed record, it is not obvious how the wrong
smoothing power will behave, and the different measures of the power in Sec. 2.1 may
be different. Specifically, since the smoothing with the valid setup assumption is opti-
mal for the TrSD cost function (see Eq. (6)), the smoothing power, RdW
S of the wrong
smoothing must be even worse than the right smoothing, RdV
S . Thus RdW
S may even
be negative; that is, the smoothing would gives a worse estimate than filtering. How-
ever, we cannot draw the same conclusion for the other types of smoothing power, RF
and RP, and for these the wrong smoothing mayappear better than the valid smoothing.
Conjecture 3: (Top-right in Table 2) If the observed record is correlated with the
correct (valid) unobserved record, i.e., C[dO, dV]∼✓ but uncorrelated with the record
from the wrongly assumed setup, i.e., C[dO, dW]∼✗, then the Valid smoothing power
will be large but the Wrong smoothing power will be small, if not zero.
Cases for Conjecture 3: dOdVdW = dXdXdY, dXdXdN, dYdYdX, dNdNdX, dYd-
NdX, dNdYdX
The intuition for this conjecture comes from the fact that here, when Alice makes
an incorrect assumption about Bob’s measurement setup, she infers that his monitoring
will cause minimal backaction on the system. Thus Alice is effectively only taking into
consideration her own measurement backaction when performing smoothing. As such,
we can expect that this wrong smoothing will perform roughly as well as filtering. That
is, the smoothing power will be small at best, even though it is large for the valid setup.
5. Numerical investigation
In order to test our conjectures, we numerically generated qubit trajectories and
analyzed the smoothing power using different measurement setups for the observed
and unobserved channels. As discussed in Sec. 3, we are considering three types
of measurement setups: dN, dX, and dY. This leads to 9 combinations of Alice’s

--- 第13页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 13
observed and Bob’s (valid) unobserved measurement setups, dOdV, to consider. For
each combination, the valid unobserved setup (dV) can be mistakenly replaced by Alice,
in her computations of the smoothed state, by two possible wrongly assumed setups
(dW). Considering both valid and wrong smoothing, there are 27 cases in total.
For each of the 9 combinations of Alice’s observed and Bob’s (valid) unobserved
measurement setups, an ensemble of 3000 true state trajectories (ρT = ρO,V ) is generated.
Each of these trajectories comes from a pair of observed ( O) and valid unobserved ( V )
records, generated stochastically at the same time with the correct actual statistics.
For each of the observed records, we numerically compute one filtered state trajectory,
ρO, one valid smoothed state trajectory, ρdV
O
, and one wrongly-assumed smoothed state
trajectory, ρdW
O
. For the smoothed state calculations, we follow Eq. (2), where the
ensemble averages were done over 10 4 randomly-generated hypothetical unobserved
records, given the appropriate Bob measurement setups (valid in one case, wrong in
the other). We note that for the smoothed states using the valid setups, the numerical
data is replicated from Ref. [26]. We use the same parameters defined in Ref. [26], i.e.,
the decay time Tγ = 1/γ is set as the unit of time for all data plots, the qubit’s unitary
dynamics is an oscillation around the x-axis with the rate Ω = 5γ and the measurement
rate for both observed and unobserved channels is half of the total decay rate γ/2. The
total time is tf −ti = 8 Tγ. More details of the calculation and numerical techniques for
the simulation can be found in [22, 26].
5.1. Examples of individual observed trajectories
We show in Figure 1 examples of Alice’s filtered (solid blue) and smoothed (dashed red)
state trajectories and their corresponding negative Trace Square Deviation (nTrSD) and
Fidelity to the true (grey) trajectories, for two combinations: dOdVdW = dYdYdX (top
panels) and dOdVdW = dYdXdY (bottom panels). The two combinations are chosen
such that obvious differences can be seen. The panels in the first three columns, (a)-
(c) and (f)-(h), show the Bloch sphere coordinates of: true state trajectories, filtered
state trajectories, valid smoothed state trajectories, and wrongly-assumed smoothed
state trajectories. Because the observed records, dO = dY, are from the y-homodyne
measurement in both examples, the filtered and smoothed states have vanishing x-
components and finite oscillations in y- and z-coordinates. The non-zero x-component
only occurs for the true state when the unobserved record, dV = dX, is from the x-
homodyne setup (shown in panel (f)).
Interesting results are shown in the last column of Figure 1, showing the negative
TrSD and Fidelity (larger numbers mean better estimation of true states). The values
fluctuate over time, but we can still see some trends. In the case of dOdV = dYdY (top
panel), the valid smoothed state (dashed red) gives a better estimate of the true states
than the one with the wrongly assumed Bob setup dW = dX (dashed black). In this
case, the wrongly assumed smoothing still gives a better estimation quality than the
filtered state (blue). However, in the case of dOdV = dYdX with dW = dN (bottom

--- 第14页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 14
0 2 4 6 8
-1.0
-0.5
0.0
0.5
1.0
0 2 4 6 8
-1.0
-0.5
0.0
0.5
1.0
0 2 4 6 8
-1.0
-0.5
0.0
0.5
1.0
0 2 4 6 8
-1.0
-0.5
0.0
0.5
1.0
0 2 4 6 8
-1.0
-0.5
0.0
0.5
1.0
0 2 4 6 8
-1.0
-0.5
0.0
0.5
1.0
0 2 4 6 8
0.2
0.4
0.6
0.8
1.
0 2 4 6 8
0.4
0.6
0.8
1.
x-coordinate y-coordinate z-coordinate
dOdV = dYdY
dOdV = dYdX
Fidelity
nTrSD
dOdW = dYdX
dOdW = dYdN
(a) (b)
(d)
(f)
(e)
(i)
(j)
0 2 4 6 8
0.2
0.4
0.6
0.8
1.
0 2 4 6 8
0.4
0.6
0.8
1.
0 2 4 6 8
0.2
0.4
0.6
0.8
1.
0 2 4 6 8
0.4
0.6
0.8
1.
0 2 4 6 8
0.2
0.4
0.6
0.8
1.
0 2 4 6 8
0.4
0.6
0.8
1.
Time (units of ) Tγ Time (units of ) Tγ Time (units of ) Tγ Time (units of ) Tγ
(c)
(g) (h)
0 2 4 6 8
0.2
0.4
0.6
0.8
1.
0 2 4 6 8
0.4
0.6
0.8
1.
-0.4
-0.6
-0.8
-1.
-0.2
0
-0.4
-0.6
-0.8
-1.
-0.2
0
Fidelity
nTrSD
0 2 4 6 8
0.2
0.4
0.6
0.8
1.
0 2 4 6 8
0.4
0.6
0.8
1.
Figure 1. Two examples of individual (true, filtered, and smoothed) trajectories and
their corresponding nTrSD and Fidelity to true states. Panels in the first three columns,
(a)-(c) and (f)-(h), show the Bloch sphere coordinates of: true state trajectories
(light grey), filtered state trajectories (solid blue), valid smoothed state trajectories
(dashed red), and wrongly-assumed smoothed state trajectories (dashed black). The
last column shows the nTrSD and Fidelity between Alice’s estimated states (filtering,
valid smoothing, and wrong smoothing) and true states, using the same colour coding.
panel), the three curves are quite close, and often cross. This is an example of a case
where we predicted the possibility of strange results. A more systematic study is clearly
needed in this case to discern the trends.
5.2. Trace-Square-Deviation (RS) and Fidelity ( RF) smoothing powers
In this section, we analyse all 27 cases for the qubit examples numerically and determine
whether the conjectures proposed in Section 4.2 are borne out for the 9 right smoothing
cases (dU = dV) and the 18 wrong smoothing cases (dU = dW). From the smoothed
state trajectories for different Alice’s observed records, we compute their smoothing
power, both in terms of TrSD, RS, defined in Eq. (12), and in terms of fidelity, RF,
defined in Eq. (13). The smoothing power in terms of purity, RP, defined in Eq. (14),
is determined solely by the unobserved setup dU, regardless of whether it is the valid
one or the wrong one. Thus RP is as already calculated in Ref. [26], and in this work is
identical (for a sufficiently large ensemble) to RdU=dV
S or RdU=dV
F .
All the numerical results for RS are shown in Figure 2 and RF (also RP) are shown
in Figure 3. In each figure, there are 9 panels, covering all dOdU combinations, and
each panel has 3 curves, corresponding to the valid smoothed state (dU = dV, solid
coloured curves) and the two more wrong smoothed states (dU = dW ≠dV, dashed
black and grey curves). The triangle colour legend, which explains the colour given to
dOdV, should be read according to the labels and the arrow, for example, dOdV =
dXdX (green), dOdV = dYdN, dNdY (magenta), and dOdV = dNdX, dXdN (orange).
We note that the recovery data is quite noisy because of the finite sample size as well as

--- 第15页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 15
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(a)dOdV=dXdX
dOdW=dXdY
dOdW=dXdN
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(b)dOdV=dYdY
dOdW=dYdX
dOdW=dYdN
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(c)dOdV=dNdN
dOdW=dNdX
dOdW=dNdY
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(d)dOdV=dXdY
dOdW=dXdX
dOdW=dXdN
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(e)dOdV=dYdX
dOdW=dYdY
dOdW=dYdN
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(f)dOdV=dXdN
dOdW=dXdX
dOdW=dXdY
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(g)dOdV=dNdX
dOdW=dNdY
dOdW=dNdN
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(h)dOdV=dYdN
dOdW=dYdX
dOdW=dYdY
0 2 4 6 8
-0.01
0.00
0.01
0.02
0.03
0.04
(i)dOdV=dNdY
dOdW=dNdX
dOdW=dNdN
Conj. 3
Conj. 2
Conj. 2Conj. 1
Conj. 2
Conj. 3
Conj. 4
Conj. 3
Conj. 4
Conj. 3
Conj. 4
Conj. 1
Conj. 2
Conj. 3
Conj. 4
Time (units of ) TγTime (units of ) TγTime (units of ) Tγ
Figure 2. Numerical results for the negative Trace Square Deviation smoothing power
(RS), defined in Eq. (12), for all 27 cases, plotted as functions of time (units of Tγ),
where the larger numbers mean better recoveries. The data of 27 cases are separated in
9 panels based on the 9 combinations of dOdV. The colour legends are used in reading
the dO, dV, dW setups. The vertical dashed lines show the steady-state region where
the transient behaviours from the initial and final conditions are minimal. We also
mark “Conj. 1 - 4” to indicate the conjecture each curve correspond to.
the transient behaviour at the start and end of the interval. The reader can focus on the
results during the steady-state regime which is approximately τss = {t∶t∈[4.5 Tγ, 6 Tγ]},
marked by vertical dashed grey lines in the plots. We use this region to analyze all four
conjectures, sumarized in Table 2.
For Conjecture 1 in Table 2 (top left), both correlations,C[dO, dV]and C[dO, dW],
are nearly zero, meaning that the observed record is not correlated, to lowest order, with
any of the unobserved records (either righly or wrongly assumed). The prediction was
that the wrong and valid smoothing powers should both be small. The numerical results
corresponding to Conjecture 1 are the cases where dOdVdW = dXdYdN, dXdNdY,
which are shown in panels (d) and (f) of Figures 2 and 3. We see that the wrong
smoothing power (dashed black) are close to the right smoothing power (coloured
solid), and both are quite small in comparsion to the smoothing powers in other panels,

```

---

## 实验/结果

```

--- 第16页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 16
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(a)dOdV=dXdX
dOdW=dXdY
dOdW=dXdN
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(b)dOdV=dYdY
dOdW=dYdX
dOdW=dYdN
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(c)dOdV=dNdN
dOdW=dNdX
dOdW=dNdY
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(d)dOdV=dXdY
dOdW=dXdX
dOdW=dXdN
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(e)dOdV=dYdX
dOdW=dYdY
dOdW=dYdN
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(f)dOdV=dXdN
dOdW=dXdX
dOdW=dXdY
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(g)dOdV=dNdX
dOdW=dNdY
dOdW=dNdN
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(h)dOdV=dYdN
dOdW=dYdX
dOdW=dYdY
0 2 4 6 8
0.00
0.01
0.02
0.03
0.04
(i)dOdV=dNdY
dOdW=dNdX
dOdW=dNdN
Conj. 1 Conj. 1
Conj. 2 Conj. 2Conj. 2
Conj. 2
Conj. 3
Conj. 3 Conj. 3
Conj. 3 Conj. 3
Conj. 4 Conj. 4
Conj. 4 Conj. 4
Time (units of ) TγTime (units of ) TγTime (units of ) Tγ
Figure 3. Numerical results for the Fidelity smoothing power ( RF), as defined in
Eq. (13). Other details are as in Figure 2. Importantly, the Purity smoothing power
(RP), as it does not depend on whether the smoothing was valid or wrong, is exactly
the Fidelity power and the TrSD power for the valid case, i.e.,RdU
P = RdU=dV
F = RdU=dV
S
for a given dO, and can be read from the colored (not gray nor black) curves.
consistent with Conjecture 1.
For Conjecture 4 in Table 2 (bottom right), the opposite of Conjecture 1, both
correlations, C[dO, dV] and C[dO, dW], are non-zero. The prediction was that the
wrong and valid smoothing powers should both be not small. We know from Ref. [26]
that RdV
F should be relatively large for the valid smoothing, and our prediction for the
wrong smoothing is that RdW
F would be of similar size. We can also extend the prediction
to RS being relatively large in both the valid and wrong guessing cases. There are four
examples that correspond to Conjecture 4: dOdVdW = dYdYdN, dNdNdY, dYdNdY,
dNdYdN, which are shown as dashed black curves in panels (b), (c), (h), and (i). In
these panels of Figure 2, we indeed see that the RS of the wrongly assumed smoothed
state (dashed black) is approximately as large as that of the valid smoothed state (solid
coloured curves), albiet strictly lower. Also in Figure 3, the same panels, we see similar
behaviour where RF of the wrong smoothing (dashed black) is quite similar to that of
the valid smoothing (solid coloured curves).
For Conjecture 2 in Table 2 (bottom left), the observed record is uncorrelated with
the record from the valid Bob setup, C[dO, dV]∼✗, but is correlated with that from
the wrongly assumed one, C[dO, dW]∼✓. This is where we may see big differences

--- 第17页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 17
between the different types of smoothing power. For the valid smoothing, all types of
smoothing power, RdV, are equal and should be small, as per Conjecture 1. For the
wrong smoothing, the correlations suggest a large smoothing power. However, we know
that the RdW
S power must be less than RdV
S due to the optimality in Eq. 6, which means
very small or even negative. But we cannot conclude this about RF, allowing for a
‘strange’ result. This occurs for six combinations: dOdVdW = dXdYdX, dXdNdX,
dYdXdY, dYdXdN, dNdXdY, and dNdXdN. The numerical results for the first two
are shown as grey curves in panels (d) and (f) and the rest of the examples are shown
as dashed black and grey curves in panels (e) and (g), in both figures. Interestingly,
the negative values of RdW
S are obvious in these panels of Figure 2, especially in the
panels (e) and (g). These negative values of RdW
S also somewhat coincide with the
strange results of Fidelity powerRdW
F in Figure 3(e) and (g), where the wrong smoothing
power (dashed grey and black) can even be larger than the valid smoothing power (solid
colored curves). These strange behaviours that the wrong smoothing could be worse
than filtering in TrSD, i.e., RdW
S ≲0, but could be somehow better than valid smoothing
in Fidelity, i.e., RdW
F > RdV
F , will be investigated further in Section 6.
Finally, for Conjecture 3 in Table 2 (top right), the observed record is correlated
with that from the valid Bob setup, C[dO, dV]∼✓, but not correlated with that from
the wrongly assumed one C[dO, dW]∼✗ . Here one clearly expects the valid smoothing
power to always be greater than the wrong smoothing one, for both RS and RF, with
the wrongly assumed smoothing power being small. For the numerical results, there are
six examples: dOdVdW = dXdXdY, dXdXdN, dYdYdX, dNdNdX, dYdNdX, dNdYdX.
The first two are shown as dashed black and grey curves in panel (a), which are lower
in smoothing power than the right smoothing one (solid green curve). The remaining
four examples are shown as dashed grey curves in panels (b), (c), (h), and (i), which
are also smaller than the right smoothing cases (solid coloured curves). We note that
the above observations are more evident forRF, in Figure 3, than for for RS, in Figure 2.
6. Refined analytical and numerical investigation
While the numerical results broadly support the four conjectures we made based on
simple arguments, there is room both to make the arguments more rigorous and to
explain details that emerged in the numerics which the conjectures did not specify. We
begin by deriving some simple properties of quantum state smoothing power analytically.
To aid our analysis, let us write the smoothed states as
ρdU
O =ρO+ δρdU, (22)
where δρdU is traceless but need not be small. Then, from the fact that an ensemble of
smoothed states with different future records (given a fixed past record) averages to the
filtered state [27], it follows that ∑O℘(O∣O)δρdU = 0. Using this (see Appendix A), we

--- 第18页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 18
can write the Fidelity and Purity smoothing powers in terms of δρdV and δρdU as
RdU
F = E[Tr[δρdUδρdV]], (23a)
RdU
P = E[Tr[(δρdU)2]], (23b)
which apply to both dU = dV and dU = dW. For the TrSD power, we use a relationship
(see Appendix A) among the three smoothing powers to get
RdU
S = 2 RdU
F −RdU
P , (24a)
= 2 E[Tr[δρdUδρdV]]−E[Tr[(δρdU)2]]. (24b)
Given these general definitions of the smoothing power in Eqs. (23) and (24), we can
show that, for the valid smoothing, all types of smoothing power are equal:
RdV
S = RdV
F = RdV
P = E[Tr[(δρdV)2]], (25)
as has been confirmed both analytically and numerically in Refs. [22, 24, 34].
We now use the above properties and formulas for the smoothing powers to refine
our explanation and predictions for the four conjectures. Firstly, for the Purity power,
because the purity does not depend on the unknown true states, the power RP should
monotonically depend on the correlation strength between Alice’s observed and assumed
unobserved records, C[dO, dU], irrespective of whether dU = dV or dW. That is, we
conclude that
C[dO, dU]∼✗ /Leftr⫯g⊸tl⫯ne⇒RdU
P = E[Tr[(δρdU)2]]is small, (26a)
C[dO, dU]∼✓ /Leftr⫯g⊸tl⫯ne⇒RdU
P = E[Tr[(δρdU)2]]is larger. (26b)
For the valid smoothing, since all types of smoothing power are equal, Eqs. (26) are
true when replacing RdU
P with RdV. These properties consistently explain the numerical
results for Conjecture 1, 3 and 4.
We now focus solely on understanding the strange results of Conjecture 2, i.e.,
when the valid two-time correlation vanishes, C[dO, dV]∼✗, and the wrongly assumed
correlation does not, C[dO, dW] ∼✓. The numerical results were clearly shown in
Section 5.2 that the TrSD power can even be negative, i.e., RdW
S ≲0, and that the
Fidelity power for the wrong guessing can be better than the valid one, i.e., RdW
F > RdV
F .
These strange behaviours are particularly pronounced for some combinations of the
measurement setups for Conjecture 2, i.e., dOdVdW = dYdXdY, dYdXdN, dNdXdY,
dNdXdN, as shown in panels (e) and (g) of Figures 2 and Figures 3. To investigate
this, let us introduce another quantity that can be thought of as a correlation coefficient
between the state deviations δρdV and δρdW,
α≡ RdW
F√
RdW
P RdV
P
= E[Tr[δρdWδρdV]]√
E[Tr[(δρdW)2]]E[Tr[(δρdV)2]]
. (27)
Given that all smoothed states, regardless of the valid or wrong unobserved unravelling,
are calculated with the same future observed record, O, one would expect that the state

--- 第19页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 19
deviation δρdU for different types of unravelling dU should be highly correlated. That
is, we expect that α should be of order 1, or even close to 1. This intuition is borne out
by numerical simulations for all 27 cases of different dV and dW, which show that α is,
in all cases, larger than 1 /
√
2 for the great majority of the time, and often much closer
to 1 (see Figure B1 in Appendix B).
We now return to the two quantities we are particularly interested in for Conjecture
2 for wrongly assumed smoothing. These are the TrSD power and the Fidelity power
compared to the Fidelity power for the valid smoothing. These can be written in terms
of the above quantities, in Eqs. (23), (24) and (27), as follows:
RdW
S = 2 α
√
E[Tr[(δρdW)2]]E[Tr[(δρdV)2]]−E[Tr[(δρdW)2], (28)
RdW
F −RdV
F = α
√
E[Tr[(δρdW)2]]E[Tr[(δρdV)2]]−E[Tr[(δρdV)2]. (29)
Thus it follows that both counterintuitive results — the TrSD power of the wrong
smoothing being negative (Eq. 28 being negative) and the Fidelity power of the wrong
smoothing being larger than that of the valid smoothing (Eq. 29 being positive) — occur
at the same time if and only if the following is true:
E[Tr[(δρdV)2]
E[Tr[(δρdW)2]< min{α2, 1
4α2}. (30)
Since min{α2, 1/4α2}≤1/2, a necessary condition for Eq. (30) to be satisfied is for RdV
P
to be at most half the size of RdW
P , which only occurs for Conjecture 2 conditions, where
we have C[dO, dV]∼✗ and C[dO, dW]∼✓.
But we can say more. Since the correlation between the state deviation is, in
actuality, quite strong, i.e., 1/2≤α2 ≤1, then we have 1/4≤min{α2, 1/4α2}≤1/2. That
is, for our system, a sufficient condition for Eq. (30) to be satisfied, and so for both
the counter-intuitive results to occur, is that the valid Purity smoothing power to be at
most one quarter of the wrong Purity smoothing power. This is exactly where we see
the clear manifestation of the above counterintuitive phenomena in panels (e) and (g) of
Figures 2 and 3. To verify that valid Purity smoothing power is at most one quarter of
the wrong Purity smoothing power, the reader can refer to the coloured curves for RdU
P
for dU = dV or dW (which equals RdV
S in Figure 2 or RdV
F in Figure 3). For example,
comparing the cyan curve in panel (e), for RdV=dX
P , and the blue curve in panel (b), for
RdW=dY
P , the condition is satisfied to explain the counter-intuitive result of dOdW =
dYdY (the grey curve in panel (e)). Another example is to compare the orange curve
in panel (g), for RdV=dX
P , and the magenta curve in panel (i), for RdW=dY
P , the condition
is satisfied for the strange result of dOdW = dNdY (the grey curve in panel (g)).
7. Conclusion
In this paper, we have considered “perplexing” quantum state smoothing scenarios,
where an observer, Alice, who has access to only some of the information of a quantum
system of interest, attempts to estimate its true state by conditioning on both her

--- 第20页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 20
past and future records, but makes an erroneous assumption about how the missing
quantum information was recovered by a hidden observer Bob. That is, the true
states, conditioned on Alice’s records and the hidden records arising from Bob’s “valid”
measurement scheme, are different from the ones Alice guesses because she assigns a
“wrong” measurement scheme to Bob.
We have analysed the power of Alice’s smoothing, considering three different
measures: the negative Trace Square Deviation (nTrSD) from the true state, Fidelity
with the true state, and Purity. The first and second of these are actually averages
over the valid unobserved (Bob’s) record. By the power of quantum state smoothing we
mean how much it increases these measures compared to filtering, the conventional state
estimate using only past information. We evaluated these three measures for the same
state estimates (one smoothed and one filtered), which are the optimal ones according
to the nTrSD measure.
As a model system, we considered a two-level atom undergoing resonance
fluoresence, where Alice and Bob could choose from three different measurement setups
— photon detection, x-homodyne, and y-homodyne — and thus in each case Alice could
be wrong about Bob’s measurement in two different ways. Guided by the strength of the
correlations between Alice’s observed records and Bob’s records (unobserved by Alice),
we constructed conjectures for the various smoothing powers in four different regimes.
All of these conjectures were then validated through numerical simulations. The most
interesting of the four conjectures related to the situation where Alice’s record is highly
correlated with the type of record she wrongly assumes Bob has, but poorly correlated
with the actual type of record Bob has. Here we predicted the potential for “strange”
results, in a manner we now explain.
One might have guessed that Alice making a wrong assumption about the
unobserved measurement setup would result in worse estimate of the true state —
by any measure — than if she assumed the valid setup. Moreover, it might have been
intuitive that, at the worst, the wrongly assumed smoothing should perform as well as
the quantum state filtering, which uses the past-only measurement records. However,
we predicted, and verified, that these intuitive guesses are not always true. The wrongly
assumed smoothing in certain cases can result in higher average fidelity to true states
than that of the correct (valid) smoothing. In those same cases, the wrongly assumed
smoothing gives even lower average trace-square distance to true states than that of the
conventional filtering. By analytical arguments supplemented by numerical simulations,
we also found necessary conditions and sufficient conditions for these strange behaviours
to occur. We emphasise that, however strange, these behaviours are consistent with the
optimality of all valid (not wrong) estimates with respect to the nTrSD measure.
In this paper we based our conjectures about the performance of the wrongly
assumed quantum state smoothing only upon the two-time correlators of measurement
records. One could, however, extend the analysis to consider higher-order correlators
between the measurement records, in particular a three-time correlator as considered
in Ref. [26]. This would likely enable better quantitative predictions of the smoothing

--- 第21页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 21
power for different combinations of settings (observed, valid, and wrongly assumed), and
especially of when the sufficient conditions for “strange” behaviour would be met. Our
consideration of wrongly assumed measurement settings also suggests a more exotic
avenue for future work, namely that of counterfactual measurement settings. For
example, one could consider the scenario where Alice performs y-homodyne detection,
obtaining a record O, while she also knows what measurement Bob performs. Given all
of this information, Alice could consider the smoothed state she would have calculated
if she had instead performed a different measurement, say x-homodyne. Last but not
least, it could also be interesting to investigate whether anything similar to the effects
we have found occur in state smoothing for classical systems with wrong assumptions
about the process noise model.
Acknowledgments
This work was supported by the Australian Research Council via the Centre of
Excellence grant CE170100012. A.C. also acknowledges the support of the Program
Management Unit for Human Resources and Institutional Development, Research and
Innovation (Thailand) grant B39G680007.
Appendix A. Derivation for Fidelity and TrSD smoothing powers
We begin by explicitly writing the Fidelity power for an unobserved measurement setup
dU (which can be dV or dW) in the form of weighted sums,
RdU
F = E[F[ρdU
O , ρO,V]−F[ρO, ρO,V]] (A.1)
= E[Tr[ρdU
O ρO,V]−E[Tr[ρOρO,V]] (A.2)
= ∑
O,V
℘(O, V ) Tr[ρdU
O ρO,V]−∑
O,V
℘(O, V ) Tr[ρOρO,V] (A.3)
= ∑
O
℘(O)
⎡⎢⎢⎢⎢⎣
∑
V
℘(V ∣O) Tr[ρdU
O ρO,V]
⎤⎥⎥⎥⎥⎦
−E[P(ρO)] (A.4)
= ∑
O
℘(O) Tr[ρdU
O ρdV
O ]−E[P(ρO)], (A.5)
using the fidelity definition in Eq. (8). Substituting the smoothed state Eq. (22) in
Eq. (A.5) above, we get
RdU
F = ∑
O
℘(O) Tr[(ρO+ δρdU)(ρO+ δρdV)]−E[P(ρO)] (A.6)
= ∑
O
℘(O) Tr[2ρOδρdU+ δρdUδρdV] (A.7)
= E[Tr[δρdUδρdV]], (A.8)

--- 第22页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 22
where we have applied the property that an ensemble of smoothed states averages back
to a filtered state [27], i.e.,
∑
O
℘(O∣O)ρdU
O = ρO . (A.9)
which is equivalent to ∑O℘(O∣O)δρdU = 0 mentioned in the main text. Note also that
the similar derivation is applied for the Purity power:
RdU
P = E[P[ρdU
O ]−E[P[ρO]] (A.10)
= ∑
O
℘(O) Tr[(ρO+ δρdU)(ρO+ δρdU)]−E[P[ρO]] (A.11)
= ∑
O
℘(O) Tr[2δρdU ρO+(δρdU)2] (A.12)
= ∑
O
℘(O) Tr[(δρdU)2]≡E[Tr[(δρdU)2]]. (A.13)
For the TrSD power, let us first derive the relationship among the three smoothing
power. The TrSD for a conditional state ρO can be written as
S[ρO, ρO,V]= Tr[(ρO−ρO,V)2] (A.14)
= Tr[ρ2
O]−2 Tr[ρOρO,V]+ Tr[ρ2
O,V] (A.15)
= P[ρO]−2F[ρO, ρO,V]+ 1 , (A.16)
where, in the final equality, we have assumed that the state ρO,V is pure, leading to the
equality F[ρO, ρO,V]= Tr[ρOρO,V]. Importantly, this relationship holds irrespective of
the choice of ρO, being ρO, ρdV
O
or ρdW
O
. By taking an ensemble average of S[ρO, ρO,V]
and substituting RF Eq. (A.8) and RP Eq. (A.13), we get
RdU
S = 2 RdU
F −RdU
P (A.17)
= 2 E[Tr[δρdUδρdV]]−E[Tr[(δρdU)2]], (A.18)
as shown in Eq. (24) in the main text.
Appendix B. Numerical results of correlation coefficient between state
deviations
Here we show numerical results of the correlation coefficient between the state deviations
δρdV and δρdW,
α≡ RdW
F√
RdW
P RdV
P
= E[Tr[δρdWδρdV]]√
E[Tr[(δρdW)2]]E[Tr[(δρdV)2]]
, (B.1)
for all 27 cases of different dV and dW. In Figure B1, we show that α is always large
for any combination of dOdVdW, and often much closer to 1.

--- 第23页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 23
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(a)
dOdV=dXdX
dOdW=dXdY
dOdW=dXdN
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(b)
dOdV=dYdY
dOdW=dYdX
dOdW=dYdN
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(c)
dOdV=dNdN
dOdW=dNdX
dOdW=dNdY
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(d)
dOdV=dXdY
dOdW=dXdX
dOdW=dXdN
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(e)
dOdV=dYdX
dOdW=dYdY
dOdW=dYdN
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(f)
dOdV=dXdN
dOdW=dXdX
dOdW=dXdY
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(g)
dOdV=dNdX
dOdW=dNdY
dOdW=dNdN
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(h)
dOdV=dYdN
dOdW=dYdX
dOdW=dYdY
0 2 4 6 80.0
0.2
0.4
0.6
0.8
1.0
1.2
(i)
dOdV=dNdY
dOdW=dNdX
dOdW=dNdN
Time (units of ) TγTime (units of ) TγTime (units of ) Tγ
Figure B1. Numerical results for the correlation coefficient α in Eq. (27) or Eq. (B.1).
showing that it is always large for all combinations of observed and unobserved
measurement setups. Each panel includes two curves (grey and black) corresponding
to two different types of dW for each dOdV. The dOdVdW labels are replicated from
Figures 2 and 1 for convenience. The dotdashed grey and dashed black lines are the
time-average values of the fluctuating grey and black curves, respectively. The cyan
shades show the area of one standard deviation from the averages. The red lines show
α =
√
0.5 and α = 1 so we can see that the values of α2 is bound in the range [0.5, 1]for
the great majority of the time. Note that, by definition, α cannot actually be greater
than one so the time spent above 1 represents a statistical fluctuation arising from a
finite ensemble size and similar remarks probably apply to the time spent below
√
0.5.
References
[1] Speyer J L and Chung W H 2008 Stochastic processes, estimation, and control (Philadelphia:
SIAM)
[2] Jazwinski A H 1970 Stochastic processes and filtering theory (New York: Chapman and Hall)
[3] Brown R G and Hwang P Y C 2012 Introduction to random signals and applied Kalman filtering
4th ed (New York: Wiley)
[4] Einicke G A 2012 Smoothing, filtering and prediction: Estimating the past, present and future
(Rijeka Croatia: InTech)
[5] Wiener N 2013 Extrapolation, interpolation and smoothing of stationary time series: with
engineering applications (Martino Fine Book)
[6] S¨ arkk¨ a S 2013Bayesian filtering and smoothing vol 3 (Cambridge University Press)
[7] Belavkin V P 1987 Information, complexity and control in quantum physics (New York: Springer)
[8] Carmichael H J 1993 An open systems approach to quantum optics (Berlin: Springer)

--- 第24页 ---
Quantum state smoothing when Alice assumes the wrong type of monitoring by Bob 24
[9] Belavkin V P 1999 Rep. Math. Phys. 43 A405
[10] Wiseman H M and Milburn G J 2010 Quantum measurement and control (UK: Cambridge
University Press)
[11] Watanabe S 1955 Reviews of Modern Physics 27 179
[12] Watanabe S 1956 Progress of Theoretical Physics 15 523–535
[13] Aharonov Y, Bergmann P G and Lebowitz J L 1964 Physical Review 134 B1410
[14] Gammelmark S, Julsgaard B and Mølmer K 2013 Physical Review Letters 111 160401
[15] Zhang J and Mølmer K 2017 Physical Review A 96 062131
[16] Aharonov Y, Albert D Z and Vaidman L 1988 Physical Review Letters 60 1351
[17] Ohki K 2022 On recursive quantum state smoothing Proceedings of the ISCIE International
Symposium on Stochastic Systems Theory and its Applications pp 8–17
[18] Tsang M 2009 Physical Review Letters 102 250403
[19] Tsang M 2009 Physical Review A 80 033840
[20] Chantasri A, Dressel J and Jordan A N 2013 Physical Review A 88 042110
[21] Chantasri A and Jordan A N 2015 Physical Review A 92 032125
[22] Guevara I and Wiseman H 2015 Physical Review Letters 115 180407
[23] Chantasri A, Guevara I, Laverick K T and Wiseman H M 2021 Physics Reports 930 1–40
[24] Laverick K T, Guevara I and Wiseman H M 2021 Phys. Rev. A 104 032213
[25] Laverick K T, Warszawski P, Chantasri A and Wiseman H M 2023 PRX Quantum 4 040340
[26] Chantasri A, Guevara I and Wiseman H M 2019 New Journal of Physics 21 083039
[27] Laverick K T, Chantasri A and Wiseman H M 2020 Quantum Studies: Mathematics and
Foundations 8 1–14
[28] Laverick K T 2021 Phys. Rev. Res. 3 033196
[29] Li L, Hall M J and Wiseman H M 2018 Physics Reports 759 1–51
[30] Schlosshauer M 2019 Physics Reports 831 1–57
[31] Kofman A G and Kurizki G 2022 Entropy 24 106
[32] Zurek W H 2022 Entropy 24 1520
[33] Strasberg P 2023 SciPost Phys. 15 024
[34] Guevara I and Wiseman H M 2020 Physical Review A 102 052217
[35] Bengtsson I and ˙Zyczkowski K 2017 Geometry of quantum states: an introduction to quantum
entanglement (Melbourne: Cambridge university press)
[36] Jozsa R 1994 Journal of Modern Optics 41 2315–2323
[37] Kraus K, B¨ ohm A, Dollard J D and Wootters W H 1983States, effects, and operations fundamental
notions of quantum theory (Springer, Berlin)

```

---

