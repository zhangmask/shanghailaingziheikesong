# 量子态轨迹估计 - 深度提取内容

**论文ID**: arXiv 2510.16754

**总页数**: 28

---

## 引言/概述

```

--- 第1页 ---
Post-processed estimation of quantum state trajectories
Soroush Khademi ,1,∗ Jesse J. Slim ,1 Kiarn T. Laverick ,2, 3, 4 Jin Chang ,5 Jingkun
Guo ,5 Simon Gr¨ oblacher,5 Howard M. Wiseman ,2 and Warwick P. Bowen 1, 6,†
1Australian Research Council Centre of Excellence for Engineered Quantum Systems,
School of Mathematics and Physics, The University of Queensland, St Lucia, Queensland 4072, Australia
2Centre for Quantum Dynamics, and Australian Research Council Centre
of Excellence for Quantum Computation and Communication Technology,
Griffith University, Yuggera Country, Brisbane, Queensland 4111, Australia
3MajuLab, CNRS-UCA-SU-NUS-NTU International Joint Research Laboratory
4Centre for Quantum Technologies, National University of Singapore, 117543, Singapore
5Kavli Institute of Nanoscience, Department of Quantum Nanoscience,
Delft University of Technology, 2628CJ Delft, The Netherlands
6Australian Research Council Centre of Excellence in Quantum Biotechnology,
School of Mathematics and Physics, The University of Queensland, St Lucia, Queensland 4072, Australia
Weak quantum measurements enable real-time tracking and control of dynamical quantum sys-
tems, producing quantum trajectories — evolutions of the quantum state of the system conditioned
on measurement outcomes. For classical systems, the accuracy of trajectories can be improved by
incorporating future information, a procedure known as smoothing. Here we apply this concept
to quantum systems, generalising a formalism of quantum state smoothing for an observer mon-
itoring a quantum system exposed to environmental decoherence, a scenario important for many
quantum information protocols. This allows future data to be incorporated when reconstructing the
trajectories of quantum states. We experimentally demonstrate that smoothing improves accuracy
using a continuously measured nanomechanical resonator, showing that the method compensates for
both gaps in the measurement record and inaccessible environments. We further observe a key pre-
dicted departure from classical smoothing: quantum noise renders the trajectories nondifferentiable.
These results establish that future information can enhance quantum trajectory reconstruction, with
potential applications across quantum sensing, control, and error correction.
The continuous observation of dynamical systems plays
a central role in physics and engineering [1–4]. In quan-
tum technologies, it provides important capabilities for
sensing [5, 6], tracking and control [7–10], error correc-
tion [11, 12], and allows the preparation of non-classical
states as resources [9, 13, 14]. By filtering the measure-
ment outcomes up to the present time, it is possible to
produce real-time estimates of the trajectory of the sys-
tem. Measurement outcomes can also bepost-processed
using both past and future data. This procedure is known
assmoothing[15] and allows more accurate reconstruc-
tion of trajectories.
Even though the controlled evolution of quantum
states is fundamental to quantum technologies, smooth-
ing has not yet been applied to improve quantum state
trajectories themselves. It has been applied to generate
trajectories of quantum weak-values [16, 17]. However,
their physical significance is disputed since they can ex-
hibit negative probabilities and values that lie outside the
eigenvalue spectrum [18–20]. Beyond smoothing, future
data has also been used to improve predictions of the out-
comes of intermediate single-shot measurements [21–23],
and to retrospectively verify filtered trajectories [24–27],
but these approaches do not improve understanding of
the evolution of the quantum system itself.
∗ s.khademi@uq.edu.au
† w.bowen@uq.edu.au
In this work, we demonstrate smoothing of quantum
state trajectories using and generalising the quantum
state smoothing formalism of Ref. [28]. We apply the
formalism to the case of a single observer monitoring an
open quantum system interacting with its environment,
where some of the information in the environment is in-
accessible. We also generalise the theory by consider-
ing inaccessible information from before the observation
began. We then implement quantum smoothing experi-
mentally using a mechanical resonator. The resonator is
subject to continuous monitoring which introduces signif-
icant quantum backaction. We show that smoothing en-
ables more accurate quantum trajectories of the system’s
dynamics, both during the transient regime after moni-
toring begins (Sec. I) and relative to the trajectories that
would be obtained with full access to the environment
(Sec. II). Further, we confirm a key prediction of quan-
tum state smoothing (Sec. III): while classical smoothing
typically results in differentiable trajectories (hence the
name), the stochasticity of quantum noise cannot, in gen-
eral, be entirely eradicted, resulting in the formal non-
differentiability of smoothed quantum trajectories [29].
The ability to more accurately infer the time evolution
of a quantum system using future measurements could
advance continuous quantum sensing, control, and er-
ror correction protocols that incorporate post-processing
stages [11, 12]. It could also provide insight into founda-
tional questions such as the nature of quantum state tra-
jectories [30], conditional entropy production [31], quan-
tum clocks [32], quantum decoherence [33], and time
arXiv:2510.16754v2  [quant-ph]  27 Oct 2025

--- 第2页 ---
2
symmetry in quantum mechanics [34].
I. QUANTUM TRAJECTORIES OF THE
LONG-TIME-LIMIT FILTERED STATE
The time evolution of a quantum system under contin-
uous weak measurement is described in real time by the
filtered state trajectoryρ F(t). The accuracy of this tra-
jectory is constrained by the finite duration of the past
measurement record, especially in the transient period
shortly after onset of monitoring. Here, we aim to re-
construct more accurate trajectories, closer to the ideal
long-time-limit (LTL) filtered stateρ LTL
F (t) that would
be obtained if the measurement record extended far into
the distant past.
ρF(t) is the optimal real-time estimate ofρ LTL
F (t)
(Methods II). As such, the estimate can only be im-
proved, and valuable early-time information recovered,
by employing future information and post-processing. To
do so, we adapt the quantum state smoothing formalism
originally developed for a different scenario — where two
observers, Alice and Bob, simultaneously measure dis-
tinct baths interacting with the quantum system [28, 35]
— and tested very recently in that context [36]. We re-
formulate the problem to a sequential scenario so it can
be applied to estimate the trajectory of the LTL filtered
state. Specifically, the two observers measure the same
bath in the same way, with Bob monitoring from the
distant past until timet= 0 and Alice fromt= 0 on-
wards, while Bob retains access to Alice’s record. The
task is for Alice to optimally estimate, using only her
own record, Bob’s inference,ρ LTL
F (t), of the system’s
quantum state. Here, the optimal estimate is theρ C
that minimizes the squared Hilbert-Schmidt distance,
∆2
HS[ρLTL
F , ρC] = Tr[(ρLTL
F −ρ C)2]. The relative entropy
— another measure of distinguishability between quan-
tum states — gives the same optimum [37].
The above idea can be applied to general quantum sys-
tems (Methods II), but for our experiment we can use
the formalism of linear-Gaussian quantum (LGQ) sys-
tems [38]. A LGQ system is characterised by the first
and second moments of its phase-space operators. Here
we generalise the derivation in Ref. [39] to obtain the
equations for these moments for our smoothed estimate
of the LTL filtered state:
⟨ˆx⟩S(t) =
 
VS(t)−V ss
F
 
VF(t)−V ss
F
−1
⟨ˆx⟩F(t)
+
 
VR(t) +V ss
F
−1
⟨ˆx⟩R(t)

,
VS(t) =
 
VF(t)−V ss
F
−1
+
 
VR(t) +V ss
F
−1
−1
+V ss
F .
(1)
Here, the vector ˆx= (ˆq 1,ˆp1, ...,ˆqN ,ˆpN)T contains the
canonical operators for position ˆq j and momentum ˆpj
of theNsystem modes, while⟨ ˆx⟩C andV C are the
mean and covariance matrix of Gaussian Wigner func-
tions inferred from the measurement record, with sub-
script C specifying types of conditioning: F for filtered
state (inferred from past measurement data); R for retro-
filtered effect operator (inferred from future data); and
S for smoothed quantum state (inferred from the whole
record). Equations for the filtered and retrofiltered mo-
ments, derived from the system’s stochastic master equa-
tion [39], are provided in Methods I. Finally,V ss
F is
the deterministic covariance matrix of the LTL filtered
state, which equalsV F(t) in the steady state (t→ ∞).
Eq. (1) indicates that the smoothed trajectory converges
asymptotically to the filtered trajectory after the tran-
sient phase, i.e., onceV F(t)→V ss
F .
Strong optical monitoring of a nanomechanical
resonator
The benefits of quantum state smoothing are most pro-
nounced when a substantial fraction of the information
leaking from the system into its environment is collected,
so that its time evolution can be inferred with near-
ground-state resolution. Notably, in such cases, there
is significant back-action associated with the bath un-
der observation itself. Cavity optomechanical systems —
where an optical probe enables quantum-limited readout
of mechanical motion — offer an important platform for
achieving this regime [25, 40–42]. Moreover, tracking the
trajectory of a macroscopic resonator underpins appli-
cations in quantum control [43], gravitational wave and
dark matter detection [13, 44, 45], and proposed tests of
quantum gravity [46].
To validate our approach and demonstrate the util-
ity of quantum state smoothing in experiment, we
track the quantum trajectory of the fundamental out-
of-plane resonance of the on-chip mechanical structure
shown in FIG. 1, which has a frequency of Ω/2π=
1.04 MHz. We monitor this resonance via dispersive
coupling to a telecom-wavelength photonic crystal cavity
with linewidthκ/2π= 11.5 GHz (Methods V A). The
combined optomechanical system is well inside the fast-
cavity limit, so that the cavity dynamics can be adiabati-
cally eliminated. Consequently, the mechanical displace-
ment is directly imprinted on the phase of a resonant
laser probe reflected off the cavity [42], which we detect
with efficiencyηusing shot-noise-limited homodyne mea-
surement (Methods IV A).
As illustrated in FIG. 1a, the cavity mediates an inter-
action between the resonator and an optical bath. The
rate at which information leaks into the optical bath is
given byγ opt = 4¯ncavg2
0/κ, whereg 0 is the single-photon
optomechanical coupling rate and ¯ncav the mean cavity
photon number [14, 42]. At the same time, information
leaks into the resonator’s mechanical thermal bath at a
rateγ th. In the limit that the resonator temperature
T≫ℏΩ/k B, relevant to our experiments, this is approx-

--- 第3页 ---
3
FIG. 1.Post-processed quantum trajectories in experiment. a,A high-quality mechanical resonator, formed by the
out-of-plane mode of a hierarchical arrangement of stressed silicon nitride strings, is in contact with a cryogenic thermal bath.
It is also in contact with an optical bath, via a photonic crystal cavity coupled with rateg. A fractionη(yellow) of the optical
bath is observed, and the acquired photocurrent is processed to reconstruct the resonator’s quantum trajectory. Trajectories
obtained from real-time (blue) and post-processed (red) analysis of a sample measurement record diffuse in the rotating phase
space spanned by mechanical quadraturesX 1,2. Their means start at distant points (crosses), while their final values coincide.
At intermediate timet, variances of the inferred Gaussian quantum states are indicated (circles), illustrating that the post-
processed stateρ S(t) is purer, with smaller variance, than the real-time filtered stateρ F(t).b,Optical image of the large
optomechanical device, with vertically stacked optical cavity and tapered waveguide for fibre coupling. A scanning electron
micrograph (inset) shows the cavity’s and waveguide mirror’s photonic crystal design.
imated asγ th ≈Γn th [40], where Γ is the resonator’s
energy decay rate andn th ≈k BT /(ℏΩ) its thermal oc-
cupancy. With these bath interactions and the homo-
dyne measurement, the resonator constitutes a single-
mode linear Gaussian system.
As only the detected part of the optical bath can be
accessed, to effectively monitor the system one must max-
imize both the optical detection efficiencyηand the ra-
tioγ opt/γth =C/n th, whereC= 4¯n cavg2
0/(κΓ) is the
optomechanical cooperativity. Our optomechanical de-
vice is carefully engineered to do this [47, 48]. Acoustic
clamping losses are minimized by the resonator’s hierar-
chical fractal structure [49], resulting in an exceedingly
low decay rate of Γ/2π= 11.5 mHz at cryogenic temper-
atures (Methods V B). Simultaneously, vertical integra-
tion of the optical cavity allows for a large single-photon
optomechanical coupling rate ofg 0/2π= 159 kHz (Meth-
ods V C). Details on device structure and fabrication are
discussed in Ref. [47].
The device is placed in a dilution refrigerator to re-
ducen th. We drive the cavity to a mean photon number
of ¯ncav = 41.4 (C= 3.16×10 4), limited by higher fre-
quency mechanical resonances that introduce coloured
noise at larger ¯ncav. Optical absorption raises resonator
temperature toT= 12.1 K (Methods V E), so that
nth = 2.45×10 5 andC/n th =γ opt/γth ≈0.13 – indi-
cating that an appreciable fraction of information enters
the optical bath.
At the mean cavity photon number used, we find that
the mechanical resonator intermittently switches to a
self-oscillating regime. We suppress this instability by
applying weak, phase-tuned, band-limited optical feed-
back (Methods IV D) , which is effectively Markovian and
increases the effective mechanical decay rate to Γfb/2π=
85 Hz. While the feedback could, in principle, be mod-
elled explicitly within the system dynamics, in our case
it suffices to replace Γ→Γ fb andn th →n th ×Γ/Γ fb in
analysis (Methods VI C). This leaves the ratioγ opt/γth,
unchanged.
To maximiseη, the cavity is first evanescently coupled
to an on-chip waveguide with efficiencyη esc = 0.82. The
waveguide’s shape is engineered to maximize transfer to a
complementarily tapered optical fibre. After cool-down,
we carefully optimize the fibre–waveguide alignment in-
side the dilution refrigerator to achieve a notably high
transfer efficiency ofη wf = 0.77 (Methods IV B). Mini-
mizing inefficiencies in the optical fibre path and employ-
ing high-efficiency, low-noise photodiodes, we achieve a
total efficiency ofη= 0.38, verified independently using
a new method that exploits the mechanical instability
(Methods V G). Together with our high ratio of optical
to thermal bath coupling, this allows us to track the res-
onator’s evolution in real-time with a resolution about
4.7 times higher than its zero point motion, indicating
that quantum backaction will play a significant role in the
system dynamics. Validating this, we demonstrate pon-
deromotive squeezing of light by quantum backaction [42]
(Methods V E).

--- 第4页 ---
4
Experimental estimation of the long-time-limit
filtered state
To determine the resonator’s filtered and smoothed
trajectories (ρ F andρ S), and statistically compare them
with its LTL filtered trajectory (ρ LTL
F ), we monitor the
nanomechanical resonator for several seconds and record
the homodyne photocurrent. The photocurrent is nor-
malized to the shot noise level and demodulated at me-
chanical frequency Ω. This neglects the fast-oscillating
dynamics of the resonator while retaining the effective
interaction-frame dynamics [50]. The demodulation pro-
duces two measurement currents corresponding to het-
erodyne detection of the resonator’s quadratures, ˆX1 =
cos(Ωt) ˆq−sin(Ωt) ˆpandˆX2 = sin(Ωt) ˆq+cos(Ωt) ˆp, where
the mechanical position ˆqand momentum ˆpare normal-
ized to have ground-state variance of one. We divide
these quadrature currents into 16,653 750-µs-long mea-
surement records.
The measurement records are processed using the
filtering and retrofiltering equations given in Methods
(Eqs. (47) and (50)) to obtain trajectories of the mean
values⟨ ˆXj⟩F and⟨ ˆXj⟩R, wherej∈ {1,2}. The tra-
jectories of the covariances,V F andV R, are deter-
ministic and set by the experimental parameters Γ,C,
nth, andη(Eqs. (45) and (48)). Together,⟨ ˆXj⟩F and
VF provide the filtered quantum state trajectory. The
smoothed quantum state trajectory is obtained by intro-
ducing ˆx= ( ˆX1, ˆX2)T with the moments calculated by
filtering and retrofiltering into Eq. (1). Finally, the LTL
filtered trajectory is determined similar to the filtered
trajectory, but with the filtering interval extended over
the three preceding records. This ensures that the filter-
ing covariance matrix converges toV ss
F , as the transient
phase lasts for about half a record.
The outputs of the analysis are shown in FIG. 2. The
schematic in FIG. 2asummarizes the two estimation pro-
tocols and their target,ρ LTL
F (t). Filtering uses the record
data from time zero until the present timet. Smoothing
uses the entire record, combining filtering of past data
(between zero andt) with retrofiltering of future data
(betweentand 750µs). FIGs. 2b–ecompare the trajec-
tories, each defined by the mean values⟨ ˆX1⟩and⟨ ˆX2⟩
(for brevity, only⟨ ˆX2⟩is shown;⟨ ˆX1⟩is presented in Sup-
plementary S1), together with a single parametervthat
fully specifies the covariance matrix (V=vI, withIthe
2×2 identity matrix). This single-parameter description
ofVis possible due to the dynamical symmetry of ˆX1
and ˆX2 when Ω≫γ opt, γth [50].
FIG. 2bshows⟨ ˆX2⟩for a sample measurement record.
For filtering (blue), it starts at zero — the uncondi-
tional mean — well separated from the LTL target
value (dashed black). For smoothing (solid red), it be-
gins closer to the target, as smoothing incorporates fu-
ture data. The two estimates converge in the second
half of the record interval. To statistically assess the
accuracy of these estimates, we calculate the distance
δC(t) =⟨ ˆXj⟩LTL
F (t)− ⟨ ˆXj⟩C(t) for filtering (C = F) and
smoothing (C = S) across the ensemble of records. The
standard deviation ofδ C is shown in FIG. 2c. Att= 0, it
is smaller for smoothing (red) than for filtering (blue) by
a factor of three, and it remains smaller throughout the
transient phase, demonstrating the advantage of smooth-
ing.
FIG. 2dshows the deterministic conditional variances.
In the transient phase,v S (solid red) is smaller thanv F
(blue), indicating that the smoothed state is purer than
the filtered state as purity is given by 1/
p
det[VC] =
1/vC [51]. Specifically, the smoothed state is about six
times purer att= 0. While these variances cannot
be directly measured — a set of projective measure-
ments evaluatingv F would disturb the resonator’s dy-
namics — they are involved in the inference of⟨ ˆXj⟩C
(Methods VI B) and are thus linked to the experimen-
tal mean-value traces. Provided the system is accurately
modelled and characterised, and the measurement data
properly analysed,v C(t) equals the variance difference
σ2
uncon −Var ens[⟨ ˆXj⟩C(t)], whereσ 2
uncon is the uncondi-
tional variance and the last term is evaluated over a suf-
ficiently large ensemble of measurement records (Supple-
mentary S3). We test this inference consistency by calcu-
lating the variance difference from the collected ensemble
(solid red diamonds and blue squares in FIG. 2d). The
close agreement withv C(t) confirms the reliability of our
analysis.
Finally, the accuracy of the estimator state trajectories
is assessed by calculating the ensemble-averaged squared
Hilbert–Schmidt distance. The data points in FIG. 2e
show the experimentally measured values, in close agree-
ment with the theoretical curves. Att= 0, the measured
value for smoothing (solid red diamond) is roughly two-
thirds of that for filtering (blue square), and it remains
smaller for smoothing throughout the transient phase.
The smoothed state is thus demonstrated to be closer to
the target than the filtered state, yielding a more accu-
rate trajectory for the resonator.
II. QUANTUM TRAJECTORIES OF THE
“TRUE” STATE
Because all real quantum systems interact with baths
that are not measured, the LTL filtered state is never
pure in practice. Were one able to measure the unob-
served baths, or access the outputs of naturally occur-
ring measurements on them, one could produce a more
accurate trajectory of the system’s evolution. We refer to
the system’s state, conditioned on measurements on all
baths far into the past, as the “true” stateρ T(t). Ideally,
this state is pure and evolves according to a stochastic
Schr¨ odinger equation. The trajectory of the true state,
as the best possible description of the system’s evolution,
is our next estimation target.
As with the LTL filtered state, the optimal real-
time estimate ofρ T(t) is given by the system’s filtered

--- 第5页 ---
5
FIG. 2.Inferred trajectories of the mechanical res-
onator. a,Conceptual illustration of the inference process.
Each bar represents all the baths as a whole that continu-
ously interacts with the resonator. The yellow portions in-
dicate the extent to which this combined bath is measured
over time, with the outputs used to infer a quantum state
for the resonator at record timet(dashed line). Estimator
states are inferred from the actual measurement record — ei-
ther from 0 tot(filtered state) or from 0 to the record end
T(smoothed state) — whereas target trajectories assume ac-
cess to a long-time-limit (LTL) measurement history and to all
baths (“true”). As illustrated in phase space (right), both tar-
get trajectories share a single real-time estimator (ρ F, blue)
but differ in their optimal post-processed estimators (ρ S’s,
red). The filtered stateρ F also provides the optimal estimate
of the fictitious true value (cross) of the resonator’s classi-
cal counterpart, which has its own post-processed estimator
(green).b-e,Comparing the estimation protocols. Insets
on the right indicate the quantity plotted in each panel, as
computed from estimator (orange) and target (black) states.
b,Stochastic traces of the quadrature mean⟨ ˆX2⟩(t) for a
sample measurement record.c,Standard deviation of dis-
tanceδ C(t) =⟨ ˆXj⟩LTL
F (t)− ⟨ ˆXj⟩C(t), j= 1,2 between the
LTL target and its estimators (C = F, S) or the classical
smoother (C = cS), normalised to the unconditional state
sizeσ uncon. Statistics derived from an ensemble of 16,653
records (data points) correspond well to theory (lines). Inset
histogram shows the distributions ofδ C(0) across the ensem-
ble.d,Deterministic variancesv C of the estimator states,
of the classical smoother and of the LTL target. Estima-
tors’ variances agree well with the corresponding value of
σ2
uncon −Var ens[⟨ ˆXj⟩C(t)], calculated across the ensemble of
records (data points, Supplementary S3 and S4).e,Distin-
guishability of the estimator states from their corresponding
targets, and of the classical smoother from both quantum
targets. The measure is the estimation cost function, given
by the ensemble-averaged Hilbert-Schmidt distance squared,
∆2
HS[ρ target(t), ρ C(t)] = Tr[(ρ target(t)−ρ C(t))2]. Theory
(lines) and experimental values (data points) are shown.
state [28]. However, as we show below, a better estimate
can be obtained using future data. In previous studies of
the quantum state smoothing formalism, Bob and Alice
measure their respective baths from timet= 0 assuming
the same initial state [28, 29, 37, 39, 52, 53], with most
taking that to be a pure state. Here we generalize this to
an impure initial state for Alice by imagining that Bob
monitors all baths from the distant past untilt= 0, at
which point he hands one bath (or part of a bath) to
Alice, who begins measuring it while Bob continues ob-
serving the remaining baths as well as having access to
Alice’s record. For a Gaussian true state, the smoothed
estimate is characterised by Eq. (1), withV ss
F replaced
by the deterministic covariance matrix of the true state
(that is, Bob’s state),V ss
T.
The set of possible true states conditioned, in part,
on naturally occurring measurements (on the unobserved
baths) depends on the types of interactions between the

```

---

## 方法/公式

```

--- 第6页 ---
6
unobserved baths and the larger environment which acts
as a measurement apparatus for those baths. Since these
interactions are generally unknown, this set is also not
known in general. However, in our case, there is a unique
“unravelling” (type of measurement) which satisfies the
following desiderata for naturalness: (i) the resulting
stochastic master equation of the system should be in-
variant under transformations that preserve the master
equation (see Methods III and Refs. [54, 55]); and (ii)
the measurement should be Markovian, just as the baths
are. Under these criteria, the natural unravelling of the
resonator’s symmetric master equation is unique and cor-
responds to heterodyne detection [56]. This unravelling
on the unobserved baths of course matches with the un-
ravelling on the observed bath, which is another reason it
is natural for our system. Considering the total unravel-
ling, the true state of the system is a stochastic coherent
state (that is, the ground state with a stochastic phase-
space displacement) (Methods VII).
Experimental “true” state estimation
We now estimate the resonator’s true trajectory
(FIG. 2a). Its real-time estimate is the filtered trajec-
tory already characterized by⟨ ˆXj⟩F andv F. Its post-
processed estimate is given by Eq. (1), with allV ss
F terms
replaced byV ss
T =I, the covariance matrix of a displaced
ground state, and ˆx= ( ˆX1, ˆX2)T, considering the previ-
ously calculated values of⟨ ˆXj⟩F,⟨ ˆXj⟩R,v F andv R. The
results are shown in FIG. 2. Until the very end of the
measurement record, the smoothed estimate differs from
both the filtered estimate and from the smoothed esti-
mate of the LTL filtered trajectory. For example, the
red dashed line in FIG. 2bshows the markedly different
value of⟨ ˆX2⟩S for the sample record. As the smoothing
here targets the true state rather than the LTL filtered
state, some dynamics uncorrelated with the LTL state
(dashed black) are evident.
The variance of the smoothed quantum statev S is
shown by the red dashed curve in FIG. 2d. It begins
below the filtering variancev F (blue curve) att= 0 and
remains lower as both gradually decrease until they reach
their steady-state values. Near the end of the record,
where less future data is available for smoothing,v S be-
gins to increase towardsv F. Asv S is smaller thanv F, the
smoothed state is purer than the filtered state. Similar to
LTL estimation, there is a purity gain in the initial tran-
sient phase, exceeding an order of magnitude att= 0.
In contrast to LTL estimation, the purity gain persists
into the steady state, where bothv S andv F have steady
values, leaving the smoothed state 43% purer. The con-
sistency of the inference of this smoothed state is tested
by calculatingσ 2
uncon −Var ens[⟨ ˆXj⟩S(t)] (hollow red di-
amonds in FIG. 2d), which matchesv S(t) as predicted
analytically (Supplementary S3).
The dashed curves in FIG. 2eshow the average value of
the estimation cost function ∆2
HS[ρT, ρC] = Tr[(ρT−ρC)2]
— red dashed for C = S and blue dashed for C = F.
Throughout the entire record, the smoothed quantum
state better estimates the target and thus its trajec-
tory captures the resonator’s evolution more accurately.
These curves are not accompanied by experimental data
because the mean values of the pure true state are inac-
cessible to our experiment; obtaining them would require
access to the unobserved baths or to the information leak-
ing from them into the rest of the environment.
Therefore, as a final experiment to demonstrate the
performance of our true-state estimators, we add white
noise to the homodyne photocurrent. This effectively cre-
ates an additional unobserved bath whose measurement
outcomes are already incorporated into the resonator’s
LTL filtered stateρ LTL
F . The LTL trajectory thus serves
as a true-state target for the noise-added data, being
partly conditioned on an unobserved bath (FIG. 3a).
This enables direct experimental validation of our true-
state estimation techniques.
The noise-added photocurrent is analysed in a similar
manner to previous experiments (Methods VI D). The
noise-added smoothed mean values typically track the
LTL filtered state more closely than the noise-added fil-
tered values (FIG. 3b), and the smoothing variance is
smaller than the filtering variance (FIG. 3c). To quan-
tify the performance of these noise-added state trajecto-
ries in estimating their target, we calculate their squared
Hilbert–Schmidt distance to the LTL filtered state, aver-
aged over all available records. As shown in FIG. 3d, it is
23% smaller for smoothing (red) than for filtering (blue)
at the record start (t= 0) and 13% smaller in the steady
state (t≈500µs). This result validates the advantage
of smoothing for estimating a true state. Significantly,
it demonstrates that post-processing can partially com-
pensate for noise-induced degradation in the accuracy of
quantum trajectories. Since the effect of increasing white
electronic noise is quantitatively equivalent to reducing
optical detection efficiency — in our case loweringηfrom
0.38 to 0.10 (Methods VI D) — it further indicates that
post-processing can mitigate any bath measurement in-
efficiency.
III. CONTRASTING QUANTUM AND
CLASSICAL SMOOTHING
The filtering equations that apply to linear-Gaussian
quantum systems are the same as those of classical dy-
namical systems, as the measured observables of the bath
commute with the past Heisenberg-picture observables
of the system [2]. However, they do not commute with
the future observables, and thus quantum state smooth-
ing cannot be regarded as a direct extension of classical
smoothing [28]. This leads to characteristic differences.
One key difference is that the quantum-smoothed mean
values are predicted to generally exhibit stochastic char-
acter (with special exceptions identified in Ref. [29]). By
contrast, classical smoothing yields mean value traces

--- 第7页 ---
7
FIG. 3.Trajectories after noise injection. a,Concep-
tual illustration. The yellow portions of each bar denote
the measured bath fraction used to infer a quantum state
for the resonator at record timet(dashed line). The gray
shading indicates an artificial reduction of the detection ef-
ficiencyη, implemented by adding white noise to the pho-
tocurrent. This noisier current is used to estimate the tra-
jectory of the primary LTL filtered state, a target effectively
conditioned on a partially unobserved bath (similar to the
“true” target in FIG. 2). The filtered estimate (blue) relies
on real-time data, whereas the smoothed estimate (red) incor-
porates the entire data record in post-processing. As shown
in phase space (right), the filtered state also yields the op-
timal estimate of the fictitious true value (cross) of the res-
onator’s classical counterpart, which has its own smoothed
estimator (green).b-d,Estimation analysis. The right in-
sets show the quantity plotted, obtained from estimator (or-
ange) and target (black) states.b,Stochastic quadrature
means⟨ ˆX2⟩LTL
F (t) and⟨ ˆX2⟩η↓
C (t), with C = F (filtering), S
(smoothing) or cS (classical smoothing), shown for a sam-
ple measurement record.c,Deterministic variances of the
target, estimator states, and classical smoother. The values
ofv η↓
C agree well withσ 2
uncon −Var ens[⟨ ˆXj⟩η↓
C (t)] computed
over an ensemble of 12,489 records (data points, Supplemen-
tary S3 and S4). The similarity in variance between the tar-
get and classical smoother is coincidental.d,Comparison
of the estimator states and the classical smoother with the
target. The data points represent the ensemble average of
the Hilbert–Schmidt distance squared, ∆2
HS[ρLTL
F (t), ρη↓
C (t)] =
Tr[(ρLTL
F (t)−ρ η↓
C (t))2]. Theoretical predictions are shown as
lines.
that are — as the name suggests — smooth, with a first
derivative that is continuous in time (except in the pres-
ence of correlated measurement and process noise [29]).
To validate these theoretical predictions, we apply the
classical smoothing equations, given by Eq. (1) with
allV ss
F terms replaced by0[57], to our measurement
records. As the feedback-induced correlation is negligi-
ble, the trajectories of the classical mean values are in-
deed smooth, with no abrupt changes in the time deriva-
tive (green lines in FIGs. 2band 3b). The stochastic
behaviour of the quantum traces should, in principle,
manifest as sharp features with an ill-defined time deriva-
tive. While the finite acquisition speed of any real exper-
iment prevents such sharp features from being directly
observed, signatures of the stochastic behavior are evi-
dent in our experiment as enhanced fluctuations of the
mean values, i.e., faster changes in the time derivative of
all red curves in FIGs. 2band 3b.
To compare the fluctuations quantitatively, we com-
pute the autocorrelation of the time derivative of the
mean values, or “quadrature velocities”. The autocor-
relation functions for the noise-injection experiment are
shown in FIG. 4. As expected, the quadrature veloc-
ities for classical smoothing exhibit sustained correla-
tions, with a 115-µs decorrelation time. By contrast,
both quantum smoothing and filtering show rapid decor-
relation, about 21 times faster than classical smoothing
and consistent with the experimentally acquired noise.
Thus, our experiment verifies one of the key expected
differences between classical and quantum smoothing.
A second key distinction is that the classical smoothing
equations — when applied to a quantum system — can
produce unphysical quantum states. In fact, the classi-
cal smoothing variance can fall below the minimum value

--- 第8页 ---
8
FIG. 4.Fluctuations of the mean value traces.The
quadrature “velocity” (d⟨ ˆXj⟩η↓
C /dt) autocorrelation function
(VACF) for filtering (blue), quantum state smoothing (red)
and classical smoothing (green). Its decay, indicated by the
dashed line, is markedly slower for classical smoothing. The
function is first averaged overjand across the ensemble of
measurement records in the noise-injection experiment, and
then normalized to its maximum value.
set by the Heisenberg uncertainty principle (see Discus-
sion and Ref. [58]). Our experiments show precursors
of this apparent violation of the uncertainty principle in
FIGs. 2dand 3cwhere the classical smoothing variances
(green curves) are consistently smaller than both quan-
tum smoothing and filtering. Additionally, the classical
mean values (green lines in FIGs. 2band 3b) — while
giving theweak valuesof the quadratures [58, 59] — are
not optimal estimates of the mean values of the target
states. For example, the green circles in FIG. 2cshow
the statistical deviation of the mean values when target-
ing the LTL filtered state, demonstrating their inferior
accuracy compared to quantum state smoothing. Finally,
the larger squared Hilbert-Schmidt distances for classical
smoothing (green curves in FIGs. 2dand 3e) confirm that
the trajectories produced by the classical equations are
more distinguishable from the targets than the quantum
smoothed trajectories. These experimental findings high-
light the fundamental inadequacy of classical smoothing
for reconstructing quantum state trajectories.
IV. DISCUSSION
Our demonstration that future information allows
more accurate quantum state trajectories could enable
a range of new applications in quantum sensing, commu-
nication and computation [6, 7, 10–12]. For instance, in
quantum sensing, it may allow improved precision. We
validate this, in spirit, in the noise-injection experiment,
where future information is used to mitigate noise, im-
proving the precision with which the quadrature mean
values are known. In quantum error correction, it may
benefit protocols that employ post-processing [11, 12].
These protocols must store information, presenting re-
source constraints for large-scale quantum computers.
Here, trading off some stored past data for future data
may allow a net reduction in the stored information for
post-processing with a desired level of accuracy.
Our approach is particularly relevant to protocols that
exploit the transient conditional dynamics of quantum
systems shortly after monitoring begins. For example,
continuous weak measurements are widely used to gen-
erate non-classical states of quantum systems [9, 13, 14].
Employing future information could allow useful states
to be produced earlier in the transient phase and im-
prove the fidelity of the final states that are generated.
Similar transient-phase physics has been shown to play
an important role in studies of conditional entropy pro-
duction under weak continuous measurement [31]. Since
quantum smoothing yields purer quantum states, access
to future information would appear to modify the rate of
entropy production, offering a new perspective on these
studies.
As discussed earlier, while our formalism allows im-
proved estimation of the true state of quantum systems
that are interacting with an environment, there is usually
an ambiguity about the type of the true state. This raises
interesting philosophical and practical questions about
decoherence in quantum mechanics. In particular, differ-
ent assumptions about the nature of the unobserved envi-
ronment lead to different sets of possible true states, even
when the observed measurement record is identical. For
instance, while an environment that performed position
detection would drive the resonator towards a coherent
true state [42], phonon-number resolving measurements
would instead drive it towards a Fock state [60, 61]. This
highlights that, when adapted to the case of a single ob-
server, quantum state smoothing is not necessarily a re-
construction of objective reality but rather a conditional
description that depends on the physical model of the
interactions between system, bath and environment.
Our work also highlights the incompatibility of classi-
cal smoothing with quantum state trajectories, in partic-
ular by showing precursors of the apparent violation of
the Heisenberg uncertainty principle by classical smooth-
ing. As derived in Supplementary S5, such a violation
would requireη >0.25 andC/n th >1/(4η−1). Our
experiment satisfies the first condition (η= 0.38) but
not the second, the latter being limited by the maximum
optical power that can be used before mode competition
degrades performance [62].
ACKNOWLEDGEMENTS
We thank A. C. Doherty, W. W. Wasserman, A. G.
White, I. Marinkovi´ c, G. I. Harris and J. S. Ben-
nett for useful discussions. This research was sup-
ported primarily by the Australian Research Council
Centre of Excellence for Engineered Quantum Systems
(EQUS, CE170100009). It was also supported by the Air
Force Office of Scientific Research under award number
FA9550-20-1-039, and the Australian Research Council
Centre of Excellence CE170100012 (Centre for Quantum
Computation and Communication Technology). K.T.L.

--- 第9页 ---
9
acknowledges the Plan France 2030 through the project
NISQ2LSQ (Grant ANR-22-PETQ-0006) and the project
OQuLus (Grant ANR-22-PETQ-0013).
AUTHOR CONTRIBUTIONS
S.K. conceived the concepts of LTL filtered state estima-
tion and the noise-injection experiment. H.M.W., S.K.
and K.T.L., with input from W.P.B., developed the ideas
of natural measurements and estimation of a pure state.
K.T.L., H.M.W. and S.K. carried out the novel theoret-
ical derivations. S.K. applied the framework to the ex-
periment. S.K. and J.J.S., with input from W.P.B., built
the setup, characterised the optomechanical device and
devised the experimental protocols. The device was fab-
ricated by J.C., J.G. and S.G. Final data was collected
by S.K. Data analysis was carried out by S.K., with ad-
ditional input from K.T.L., W.P.B., J.J.S. and H.M.W.
Figures were prepared by S.K., J.J.S. and W.P.B., with
contributions from J.C., J.G. and S.G. The manuscript
was written by S.K., W.P.B., J.J.S., K.T.L. and H.M.W.
with feedback from all authors. W.P.B. and H.M.W. su-
pervised the project.
COMPETING INTERESTS
The authors declare no competing interests.
[1] R. F. Stengel,Optimal control and estimation(Courier
Corporation, 1994).
[2] H. M. Wiseman and G. J. Milburn,Quantum measure-
ment and control(Cambridge University Press, 2010).
[3] D. Dong and I. R. Petersen, Annu. Rev. Control54, 243
(2022).
[4] H. Carmichael,An Open Systems Approach to Quantum
Optics(Springer, 1993).
[5] R. Jim´ enez-Mart´ ınez, J. Ko lody´ nski, C. Troullinou, V. G.
Lucivero, J. Kong, and M. W. Mitchell, Phys. Rev. Lett.
120, 040503 (2018).
[6] J. Duan, Z. Hu, X. Lu, L. Xiao, S. Jia, K. Mølmer, and
Y. Xiao, Nat. Phys.21, 909 (2025).
[7] C. Sayrin, I. Dotsenko, X. Zhou, B. Peaudecerf,
T. Rybarczyk, S. Gleyzes, P. Rouchon, M. Mirrahimi,
H. Amini, M. Brune, J.-M. Raimond, and S. Haroche,
Nature477, 73 (2011).
[8] W. Wieczorek, S. G. Hofer, J. Hoelscher-Obermaier,
R. Riedinger, K. Hammerer, and M. Aspelmeyer, Phys.
Rev. Lett.114, 223601 (2015).
[9] R. A. Thomas, M. Parniak, C. Østfeldt, C. B. Møller,
C. Bærentsen, Y. Tsaturyan, A. Schliesser, J. Appel,
E. Zeuthen, and E. S. Polzik, Nat. Phys.17, 228 (2021).
[10] L. Magrini, P. Rosenzweig, C. Bach, A. Deutschmann-
Olek, S. G. Hofer, S. Hong, N. Kiesel, A. Kugi, and
M. Aspelmeyer, Nature595, 373 (2021).
[11] I. Convy, H. Liao, S. Zhang, S. Patel, W. P. Livingston,
H. N. Nguyen, I. Siddiqi, and K. B. Whaley, New J. Phys.
24, 063019 (2022).
[12] W. P. Livingston, M. S. Blok, E. Flurin, J. Dressel, A. N.
Jordan, and I. Siddiqi, Nat. Commun.13, 2307 (2022).
[13] H. M¨ uller-Ebhardt, H. Rehbein, R. Schnabel, K. Danz-
mann, and Y. Chen, Phys. Rev. Lett.100, 013601 (2008).
[14] C. Meng, G. A. Brawley, J. S. Bennett, M. R. Vanner,
and W. P. Bowen, Phys. Rev. Lett.125, 043604 (2020).
[15] H. L. Weinert,Fixed Interval Smoothing for State Space
Models(Kluwer Academic, New York, 2001).
[16] S. Kocsis, B. Braverman, S. Ravets, M. J. Stevens, R. P.
Mirin, L. K. Shalm, and A. M. Steinberg, Science332,
1170 (2011).
[17] K. Y. Bliokh, A. Y. Bekshaev, A. G. Kofman, and
F. Nori, New J. Phys.15, 073022 (2013).
[18] Y. Aharonov, D. Z. Albert, and L. Vaidman, Phys. Rev.
Lett.60, 1351 (1988).
[19] A. J. Leggett, Phys. Rev. Lett.62, 2325 (1989).
[20] C. Ferrie and J. Combes, Phys. Rev. Lett.113, 120404
(2014).
[21] S. Gammelmark, B. Julsgaard, and K. Mølmer, Phys.
Rev. Lett.111, 160401 (2013).
[22] T. Rybarczyk, B. Peaudecerf, M. Penasa, S. Gerlich,
B. Julsgaard, K. Mølmer, S. Gleyzes, M. Brune, J. M.
Raimond, S. Haroche,et al., Phys. Rev. A91, 062116
(2015).
[23] D. Tan, S. J. Weber, I. Siddiqi, K. Mølmer, and K. W.
Murch, Phys. Rev. Lett.114, 090403 (2015).
[24] H. Miao, S. Danilishin, H. M¨ uller-Ebhardt, H. Rehbein,
K. Somiya, and Y. Chen, Phys. Rev. A81, 012114 (2010).
[25] M. Rossi, D. Mason, J. Chen, and A. Schliesser, Phys.
Rev. Lett.123, 163601 (2019).
[26] C. Meng, G. A. Brawley, S. Khademi, E. M. Bridge,
J. S. Bennett, and W. P. Bowen, Sci. Adv.8, eabm7585
(2022).
[27] J. Lammers and K. Hammerer, Front. Quantum Sci.
Technol.2, 1294905 (2024).
[28] I. Guevara and H. Wiseman, Phys. Rev. Lett.115,
180407 (2015).
[29] K. T. Laverick, Phys. Rev. Res.3, 033196 (2021).
[30] H. M. Wiseman, J. Opt. B: Quantum Semiclass. Opt.8,
205 (1996).
[31] M. Rossi, L. Mancino, G. T. Landi, M. Paternostro,
A. Schliesser, and A. Belenchia, Phys. Rev. Lett.125,
080601 (2020).
[32] X. He, P. Pakkiam, A. A. Gangat, M. J. Kewming, G. J.
Milburn, and A. Fedorov, Phys. Rev. Appl.20, 034038
(2023).
[33] H. M. Wiseman and J. A. Vaccaro, Phys. Rev. Lett.87,
240402 (2001).
[34] Y. Aharonov, P. G. Bergmann, and J. L. Lebowitz, Phys.
Rev.134, B1410 (1964).
[35] A. Chantasri, I. Guevara, and H. M. Wiseman, New J.
Phys.21, 083039 (2019).
[36] S. Yokoyama, K. T. Laverick, D. McManus,
Q. Yu, A. Chantasri, W. Asavanant, D. Dong,
H. M. Wiseman, and H. Yonezawa, arXiv preprint
10.48550/arXiv.2509.04754 (2025).

--- 第10页 ---
10
[37] K. T. Laverick, I. Guevara, and H. M. Wiseman, Phys.
Rev. A104, 032213 (2021).
[38] K. T. Laverick, A. Chantasri, and H. M. Wiseman, Phys.
Rev. Lett.122, 190402 (2019).
[39] K. T. Laverick, A. Chantasri, and H. M. Wiseman, Phys.
Rev. A103, 012213 (2021).
[40] M. Aspelmeyer, T. J. Kippenberg, and F. Marquardt,
Rev. Mod. Phys.86, 1391 (2014).
[41] D. Mason, J. Chen, M. Rossi, Y. Tsaturyan, and
A. Schliesser, Nat. Phys.15, 745 (2019).
[42] W. P. Bowen and G. J. Milburn,Quantum optomechanics
(CRC press, 2015).
[43] J. Guo, R. Norte, and S. Gr¨ oblacher, Phys. Rev. Lett.
123, 223602 (2019).
[44] M. Hirschel, V. Vadakkumbatt, N. P. Baker, F. M.
Schweizer, J. C. Sankey, S. Singh, and J. P. Davis, Phys.
Rev. D109, 095011 (2024).
[45] C. G. Baker, W. P. Bowen, P. Cox, M. J. Dolan, M. Gory-
achev, and G. Harris, Phys. Rev. D110, 043005 (2024).
[46] P. Girdhar and A. C. Doherty, New J. Phys.22, 093073
(2020).
[47] J. Guo and S. Gr¨ oblacher, Light Sci. Appl.11, 282
(2022).
[48] J. Guo, J. Chang, X. Yao, and S. Gr¨ oblacher, Nat. Com-
mun.14, 4721 (2023).
[49] S. A. Fedorov, A. Beccari, N. J. Engelsen, and T. J. Kip-
penberg, Phys. Rev. Lett.124, 025502 (2020).
[50] A. C. Doherty, A. Szorkovszky, G. I. Harris, and W. P.
Bowen, Phil. Trans. R. Soc. A.370, 5338 (2012).
[51] A. Serafini,Quantum continuous variables: a primer of
theoretical methods(CRC press, 2017).
[52] I. Guevara and H. M. Wiseman, Phys. Rev. A102,
052217 (2020).
[53] A. Chantasri, I. Guevara, K. T. Laverick, and H. M.
Wiseman, Phys. Rep.930, 1 (2021).
[54] N. Gisin and I. C. Percival, J. Phys. A Math. Gen.25,
5677 (1992).
[55] N. Gisin and I. C. Percival, Phys. Lett. A167, 315 (1992).
[56] H. M. Wiseman and L. Di´ osi, Chem. Phys.268, 91
(2001), erratumibid.271, 227 (2001).
[57] D. Fraser and J. Potter, IEEE Trans. Automat. Contr.
14, 387 (1969).
[58] K. T. Laverick, A. Chantasri, and H. M. Wiseman, Phys.
Rev. A112, 022411 (2025).
[59] M. Tsang, Phys. Rev. A80, 033840 (2009).
[60] G. A. Brawley, M. R. Vanner, P. E. Larsen, S. Schmid,
A. Boisen, and W. P. Bowen, Nat. Commun.7, 10988
(2016).
[61] S. Deleglise, I. Dotsenko, C. Sayrin, J. Bernu, M. Brune,
J.-M. Raimond, and S. Haroche, Nature455, 510 (2008).
[62] S. Khademi,Optomechanical monitoring of quantum
Brownian motion and the challenge of Heisenberg, Ph.D.
thesis, The University of Queensland (2024).
[63] A. C. Doherty and K. Jacobs, Phys. Rev. A60, 2700
(1999).
[64] R. E. Kalman and R. S. Bucy, J. Basic Eng.83, 95 (1961).
[65] J. Zhang and K. Mølmer, Phys. Rev. A96, 062131
(2017).
[66] K. T. Laverick, P. Warszawski, A. Chantasri, and H. M.
Wiseman, PRX Quantum4, 040340 (2023).
[67] V. P. Belavkin,Information, complexity and control in
quantum physics, edited by A. Blaquiere, S. Dinar, and
G. Lochak (Springer, New York, 1987).
[68] V. P. Belavkin, Commun. Math. Phys.146, 611 (1992).
[69] T. G. Tiecke, K. P. Nayak, J. D. Thompson, T. Peyronel,
N. P. de Leon, V. Vuleti´ c, and M. D. Lukin, Optica2, 70
(2015).
[70] J. Guo,Bringing Classical Mechanical Resonators to-
wards the Quantum Regime, Ph.D. thesis, Delft Univer-
sity of Technology (2021).
[71] K. Usami, A. Naesby, T. Bagci, B. Melholt Nielsen,
J. Liu, S. Stobbe, P. Lodahl, and E. S. Polzik, Nat. Phys.
8, 168 (2012).
[72] B. D. Hauer, T. J. Clark, P. H. Kim, C. Doolin, and J. P.
Davis, Phys. Rev. A99, 053803 (2019).
[73] H. Ftouni, C. Blanc, D. Tainoff, A. D. Fefferman, M. De-
foort, K. J. Lulla, J. Richard, E. Collin, and O. Bourgeois,
Phys. Rev. B92, 125439 (2015).
[74] R. Leijssen, G. R. La Gala, L. Freisem, J. T. Muhonen,
and E. Verhagen, Nat. Commun.8, 16024 (2017).
[75] M. S. Grewal and A. P. Andrews, Optimal smoothers,
inKalman Filtering(John Wiley & Sons, Ltd, 2014)
Chap. 6, pp. 239–279.
[76] G. V. Bayley and J. M. Hammersley, J. R. Stat. Soc.
Suppl.8, 184 (1946).
METHODS
I. FILTERING AND RETROFILTERING IN
LINEAR GAUSSIAN QUANTUM SYSTEMS
The problem of quantum filtering, retrofiltering and
smoothing applies to Markovian open quantum systems,
where the quantum state of the system is described by a
Lindblad master equation
ℏ d
dt ρ=−i[ ˆH, ρ] +D[ ˆc]ρ ,(2)
where ˆHis the system Hamiltonian and ˆcis a vector of
Lindblad operators. A linear Gaussian quantum (LGQ)
system is an openN-mode bosonic system, with canoni-
cal position and momentum operators for thenth mode
ˆqn and ˆpn, satisfying the canonical commutation relations
[ˆqk,ˆpℓ] =iℏδ k,ℓ. In the Heisenberg picture, the opera-
tors evolve dynamically according to the linear Langevin
equation [2, 63],
dˆx(t) =A ˆx(t)dt+Ed ˆvp(t),(3)
where ˆx= (ˆq1,ˆp1, ...,ˆqN ,ˆpN)⊤. d ˆvp(t) is a set of external
operators that influence the evolution due to interactions
with a quantum environment (i.e., quantum noise), sat-
isfying
⟨dˆvp(t)⟩= 0,and⟨dv ⊤
p (t)dvp(t′)⟩=Iδ(t−t ′)dt2 ,
(4)
whereIthe identity matrix. The particular drift matrix
Aand the matrixEdepend on the system Hamiltonian
and Lindblad operators [2], and can in general be time-
dependent without affecting any of the following. We will
assume throughout that these are time-independent (as
they are in our experiment). These systems arise when
ˆHis at most quadratic and ˆcis linear in the canonical

--- 第11页 ---
11
operators,e.g., ˆH= ˆx⊤Gˆxand ˆc=B ˆx, whereGis
Hermitian.
As for the “Gaussian” part, these dynamics are unique
in that they preserve Gaussian states, meaning that if the
system is initially in a Gaussian state (e.g., a coherent or
thermal state), it will remain Gaussian over its entire evo-
lution. This is extremely useful since Gaussian quantum
states are completely described, in terms of their Wigner
function, by the mean⟨ ˆx⟩and the (symmetrized) covari-
ance matrixV ij = 1
2 ⟨ˆxiˆxj + ˆxj ˆxi⟩ − ⟨ˆxi⟩⟨ˆxj⟩. It is easy
to show [2] that the mean and covariance matrix evolve
according to
d⟨ˆx⟩(t) =A⟨ ˆx⟩(t)dt ,(5)
d
dtV=AV+V FA⊤ +D,(6)
whereD=EE ⊤.
Currently, the LGQ systems we have been describing
have not involved any measurements acting on the exter-
nal environment to refine the description of the quantum
system. In particular, as mentioned in the main text,
we consider a continuous-in-time measurement of the en-
vironment, or some fraction thereof. In order for the
system to remain a LGQ system, it must be that the
conditionaldynamics are linear and preserve Gaussian
states. This is the case [63] if and only if the operator
describing the measurement is linear in ˆx, i.e.,
ˆy(t)dt=C ˆx(t)dt+ d ˆvm(t),(7)
where dˆvm are noise operators affecting the measurement
outcome, satisfying similar conditions to Eq. (4). Note,
in general, dˆvm(t) may be correlated with d ˆvp(t), giving
⟨Ed ˆvp(dˆvm)⊤⟩=Γdt. We will assume, as was the case
withAandE, that the measurement matrixCis time
independent. Conditioning (equiv.Filtering) the system
on each measurement outcomey t from the initial timet 0
until the timet, causes the mean and covariance matrix
to evolve according to [2, 63]
d⟨ˆx⟩F(t) =A⟨ ˆx⟩F(t)dt+K +[VF(t)]dwF(t),(8)
d
dtVF =AV F +V FA⊤ +D− K +[VF]K +[VF]⊤ .(9)
Here, the “kick” matrixK ±[V] =VC ⊤ ±Γ ⊤ and the
(filtered) vector of innovations is dw F(t) =y(t)dt−
C⟨ˆx⟩F(t)dt, with statistics identical to that of an in-
finitesimal Weiner increment [2]. Note, these equations
are identical to the classical Kalman-Bucy filtering equa-
tions [64].
To describe the probability of the measurement out-
comes that occurred fromtuntil the final timeT, one
generally introduces a positive-valued operator measure
(POVM) element ˆER(t), more commonly called the retro-
filtered effect. This operator encodes the probability of
the measurement record − →O t :={y(τ) :τ∈[t,T]}oc-
curring for any given state viap( − →O;t|ρ) = Tr[ ˆER(t)ρ].
Note, the “past” measurement record is denoted by
← −O t :={y(τ) :τ∈[t 0, t)}and the “past-future” record
by ← →O:={y(τ) :τ∈[t 0,T]}. In the LGQ regime, the
(normalized) retrofiltered effect is also a Gaussian state,
with mean and covariance described by [65]
−d⟨ ˆx⟩R(t) =−A⟨ ˆx⟩R(t) dt+K −[VR(t)]dwR(t),(10)
− d
dtVR =−AV R −V RA⊤ +D− K −[VR]K −[VR]⊤ .
(11)
Note, some care must be taken with the final conditions
in this equation, sinceV R(T) =∞and the mean is
strictly undefined. See Ref. [29] for the details on how
to deal with this. It should also be noted that these
are backward-evolving equations, where−d⟨ ˆx⟩R(t) =
⟨ˆx⟩R(t−dt)− ⟨ ˆx⟩R(t) and similarly for−dV R.
Naively applying classical smoothing to the Wigner
functions [58], one obtains the classically smoothed
Wigner function with mean and covariance
⟨ˆx⟩cS =V cS

V−1
F ⟨ˆx⟩F +V −1
R ⟨ˆx⟩R

,(12)
VcS =

V−1
F +V −1
R
−1
.(13)
In general, these do not correspond to a physical state,
with the covariance matrix violating the Sch¨ odinger-
Heisenberg uncertainty principle [38]
V+ iℏ
2 Σ≥0,(14)
where Σ =
 0 1
−1 0

. Note, in our optomechanical system,
the ground state has been normalized such that its co-
variance isV=I(equiv.choosing units such thatℏ= 2).
Furthermore, since all covariance matrices are diagonal,
i.e.,V=vI, Eq. (14) reduces tov≥1.
II. ADAPTING THE QUANTUM STATE
SMOOTHING FORMALISM
For a general quantum system, whether LGQ or not,
the smoothed quantum state of Guevara and Wiseman
[28, 66] is defined as
ρS(t) =
X
ρT
p(ρT;t| ← →O)ρ T(t),(15)
where the true quantum stateρ T was defined by intro-
ducing a secondary observer, Bob, who performed a con-
tinuous in time measurement on any part of the environ-
ment (or some subset thereof) that the observer’s, Al-
ice’s, measurement missed (either due to only observing
a portion of the environment or detector inefficiencies).
The true quantum state is obtained by conditioning on
both the past measurement record of Alice, ← −O t and Bob,← −U t. Note, this particular form of the smoothed quan-
tum state does not explicitly appear in Ref. [28], but
instead performs an equivalent average over Bob’s past

--- 第12页 ---
12
measurement records ← −U t. This smoothed quantum state
has since been shown to be an optimal Bayesian estima-
tor of the true quantum state [37, 53] in terms of min-
imizing the trace-squared deviation (also known as the
squared Hilbert-Schmidt distance) from the true state,
among others. However, as shown in Ref. [66], this op-
timality is entirely independent of how one defines the
true state. So long as one has some “target” state that
one is trying to estimate from a set of possible statesT,
the optimal (in a Bayesian sense) smoothed estimate is
given by
ρtar
S (t) =
X
ρtar∈T
p(ρtar;t| ← →O)ρ tar(t),(16)
where the superscript is to emphasize that this is the
smoothed estimate of a particular target state. Note,
depending on the particular set of target states chosen,
it may be the case that the optimal real-time estimate,
i.e.,P
ρtar p(ρtar;t| ← −O t)ρtar(t), may not equal the filtered
quantum state that one obtains from conventional quan-
tum filtering theory [67, 68]. In the case of true state esti-
mation [28] and the LTL filtered state estimation (which
will be elaborated shortly), this is not the case and the
optimal real-time estimate and the conventional filtered
state coincide.
We exploit the generality of Eq. (16) to adapt quan-
tum state smoothing to our experimental setting. In the
case of our first experiment, the target state to estimate
is the LTL filtered state. That is, let us consider the sce-
nario where our system of interest has been monitored
for a long-time prior to timet 0 by a single observer — in
the main text, we sett 0 = 0. For ease of discussion and
comparison to the standard formulation of quantum state
smoothing, we will refer to this observer as Bob. At time
t0 Bob stops his measurement, having obtained a mea-
surement record ← −U t0 :={y(τ) :τ∈[τ 0, t0), τ 0 ≪t 0},
and another observer, Alice, starts to measure the sys-
tem until some final timeT. Note, Alice and Bob do
not necessarily need to perform the same measurement
on the same portion of the environment, as is the case
in our experiment, nor do they need to be physically dis-
tinct observers. However, it is necessary that (i) Alice
knows Bob’s measurement choice as well as what por-
tion of the environment he is measuring and (ii) she
is oblivious to ← −U t0. With this knowledge, Alice knows
that there exists a better description of the quantum
system than what she can obtain with just her record← −O t ={y(τ) :τ∈[t 0, t)}, i.e., the filtered quantum state
obtained by making use of ← −U t0 ∪ ← −O t. However, since Al-
ice does not know ← −U t0, the LTL filtered state could be
any state in the setT={ρ ← −U t0 ∪← −O t
,∀ ← −U t0 }. With the tar-
get state defined, one can use similar techniques to those
used for the standard quantum state smoothing theory
[52] to computeρ LTL
S (t).
All that remains is to determine Alice’s initial condi-
tion for her filtered state in the LTL case. Since we are
dealing with quantum unravellings of a Lindblad master
equation, averaging over ← −U t0 (or equivalently averaging
overρ LTL(t)) given ← −O t fort > t 0, one obtains Alice’s
filtered state. Performing this average att=t 0, where← −O t0 =∅, one instead obtains the unconditioned state.
Sinceτ 0 ≪t 0, att 0, Alice’s best knowledge of the initial
state of the system is the solution to the Lindblad master
equation.
A. Quantum Smoothing for LGQ systems
The major novelty of this section is that we derive
the quantum state smoothing equations in the LTL fil-
tered state estimation for general linear Gaussian quan-
tum systems. The derivation here largely follows that of
the standard quantum state smoothing theory (i.e., true
state estimation) in Ref. [38]. For completeness, we will
present the theory more generally for the Gaussian tar-
get state, described by mean⟨ ˆx⟩tar and covariance matrix
Vtar, being either the LTL filtered state or true state so
that the reader understands the formulae for the two pri-
mary estimator we consider in this paper. Let us begin
by defining the Wigner function [2],
Wρ(x) = (2π)−N
Z
b∈R2N
d2NbTr[ρe ib⊤(ˆx−x)].(17)
Computing the Wigner function ofρ tar
S using Eq. (16)
and noting the linearity of (17), we have that
W tar
S (x;t) =
X
ρtar∈T
p(ρtar;t| ← →O)W tar(x;t).(18)
Using Bayes’ theorem, we havep(ρ tar;t| ← →O)∝
p(− →O t|ρtar, ← −O t)p(ρtar|← −O t) =p( − →O t|ρtar)p(ρtar|← −O t), with
the equality resulting from the Markovianity of the sys-
tem. Note, for simplicity of notation, we have omit-
ted explicit dependencies on the timetin the proba-
bility distributions since it is clear by the record which
time it is. By definition of the retrofiltered effect, we
knowp( − →O t|ρtar) = Tr[ ˆER(t)ρtar]. Using the identity
Tr[ρσ]∝
R
dxWρ(x)Wσ(x) and assuming an LGQ sys-
tem, we have
p(− →O t|ρtar) =g(⟨ ˆx⟩tar;⟨ ˆx⟩R,V R +V tar).(19)
All that remains is to compute the probability
p(ρtar|← −O t)≡p(⟨ ˆx⟩tar|← −O t), where the equivalence comes
from the fact that, since the covariance is deterministic,
the possible targets states are parametrized by solely by
their mean⟨ ˆx⟩tar. Since this has already been done ex-
plicitly for the true state case in Refs. [29, 38], we will
focus only on the LTL case here and quote the results for
the true state case. The mean and covariance of the LTL

--- 第13页 ---
13
state satisfy
d⟨ˆx⟩LTL(t) =A⟨ ˆx⟩LTL(t)dt+K +[VLTL]dwLTL(t),
(20)
d
dtVLTL =AV LTL +V LTLA⊤ +D
− K+[VLTL]K +[VLTL]⊤ .(21)
Importantly, we notice that Eq. (20) is a classical lin-
ear Langevin equation with a classical linear measure-
ment recordy(t)dt=C⟨ ˆx⟩LTL(t)dt+dw LTL(t). As such,
we can apply classical filtering [64] to determine that
p(⟨ˆx⟩LTL|← −O t) =g(⟨ ˆx⟩LTL;⟨ ◦x⟩F, ◦VF), where the mean
⟨◦x⟩F and covariance ◦VF :=⟨(⟨ ˆx⟩⊤
LTL⟨ˆx⟩LTL − ⟨ˆx⟩⊤
F ⟨ˆx⟩F)⟩
satisfy
d⟨ˆx⟩F(t) =A⟨ ˆx⟩F(t)dt+ ◦K+[ ◦VF(t)]dwF(t),(22)
d
dt
◦VF =A ◦VF + ◦VFA⊤+
K+[VLTL]⊤K+[VLTL]− ◦K+[ ◦VF] ◦K+[ ◦VF]⊤ ,
(23)
where ◦K+[ ◦VF] = ◦VFC⊤+K+[VLTL]⊤. It is easy to show,
using Eqs. (8), (9), (20) and (21), that ◦VF =V F −V LTL
and ◦xF =⟨ ˆx⟩F. In the case of true state filtering, the
argument follows similarly [38], with the true mean and
covariance satisfying
d⟨ˆx⟩T(t) =A⟨ ˆx⟩T(t)dt+K +
O[VT]dwO(t)
+K +
U[VT]dwU(t),(24)
d
dtVT =AV T +V TA⊤ +D
− K+
O[VT]K +
O[VT]⊤ − K+
U[VT]K +
U[VT]⊤ .(25)
where Alice’s (Bob’s) measurement outcome isyO(U) dt=
CO(U) ⟨ˆx⟩T + dw O(U) (t), and the distribution is
p(⟨ˆx⟩T|← −O t) =g(⟨ ˆx⟩tar;⟨ ˆx⟩F,V F −V T).
Finally, we can obtain
p(⟨ˆx⟩tar|← →O)∝p( − →O t|ρtar)p(ρtar|← −O t)
=g(⟨ ˆx⟩tar;⟨ ˆx⟩S, ◦VS),
(26)
where
⟨ˆx⟩S = ◦VS

(VF −V tar)−1⟨ˆx⟩F + (VR +V tar)−1⟨ˆx⟩R

,
(27)
◦V−1
S = (VF −V tar)−1 + (VR +V tar)−1 ,(28)
with ◦VS :=⟨(⟨ ˆx⟩⊤
tar⟨ˆx⟩tar − ⟨ˆx⟩⊤
S ⟨ˆx⟩S)⟩. This leaves us
with
W tar
S (x)∝
Z
d⟨ˆx⟩targ(⟨ˆx⟩tar;⟨ ˆx⟩S, ◦VS)g(x;⟨ ˆx⟩tar,V tar)
=g(x;⟨ ˆx⟩S, ◦VS +V tar).
(29)
Thus, the mean and the covariance of the smoothed quan-
tum state are
⟨ˆx⟩S = (VS −V tar)

(VF −V tar)−1⟨ˆx⟩F
+(VR +V tar)−1⟨ˆx⟩R

,(30)
VS =

(VF −V tar)−1 + (VR +V tar)−1−1
+V tar .
(31)
In the particular LTL case that we are considering,
Bob has been performing the same measurement that Al-
ice performs for a long time prior to Alice beginning her
measurement. This means that the evolution of the LTL
target’s covariance, Eq. (21), will be identical to that of
Alice’s filtered state, Eq. (9), and will have reached its
steady-state value byt 0. Thus, we takeV LTL(t) =V ss
F .
In the case of true state smoothing, prior to Alice be-
ginning her measurement, the environment is completely
unobserved, and is thus perfectly monitored by Bob (the
environment). This means, since by our assumption on
the natural type of measurement unravelling for the en-
vironment (see Sec. III) limits the measurement to a het-
erodyne measurement and the system is left unobserved
for a long-time prior to Alice beginning her measurement,
the true state att 0 will be the steady state solution of
Eq. (25) whereC O =Γ O = 0 andC U andΓ U corre-
sponding to a perfect heterodyne measurement. For our
system, this gives the initial condition for the true co-
varianceV(t 0) =v GSI, wherev GS is the ground state
variance.
III. THE DESIDERATA FOR A NATURALLY
OCCURRING UNRAVELLING
In order to perform true state smoothing, we make an
assumption on how the environment would have natu-
rally measured the unobserved baths. In particular, we
consider two desiderata for such measurements.
First, the resulting master equation should be invari-
ant under the same transformations that leave the sys-
tem’s master equation invariant, as these are the natural
symmetries the system and environment have. Master
equation (2) is invariant under the following transforma-
tions [2]:
ˆc→U ˆc(32)
and
ˆc→ ˆc+a, ˆH→ ˆH− i
2(a†ˆc−c †a),(33)
whereUis an arbitrary unitary matrix andais a vec-
tor of arbitrary complex numbers (a † is its complex-
conjugate transpose).
The second desideratum is that the measurement per-
formed by the larger environment should be Markovian,
i.e., it should be non-adaptive. This is reasonable due
to the validity of the Born–Markov approximation — an

--- 第14页 ---
14
adaptive measurement would require the environment to
have a memory to store (at minimum) the last measure-
ment outcome.
Invariance under (33) limits the Markovian measure-
ment to “dyne”-type measurements [2]. Invariance un-
der (32) further limits this measurement to be phase-
insensitive in regard to the particular Lindblad opera-
tor being detected. Heterodyne unravelling is then the
unique natural one for our experimental system consid-
ering the form of its Lindblad master equation (given by
Eq. (41) in the limitη→0).
IV. EXPERIMENTAL SETUP
To minimise thermal fluctuations, the optomechanical
device is placed in a dilution refrigerator (Bluefors BF-
LD). While our experiments were performed with a sam-
ple stage temperature of 3.5 K, operating in a dilution
refrigerator will allow us to attain stage temperatures
down to 20 mK in the future. In the following sections,
we explain the experimental setup employed to charac-
terise, stabilise and monitor our optomechanical device.
A. Shot-noise-limited Homodyne measurement
After pumping the optomechanical cavity with an
on-resonance, narrow-linewidth, tunable laser (Santec
TSL-770), the back-reflected light is measured using
a fibre-based homodyne interferometer (Extended Data
FIG. 1a). Because the mechanical displacement is im-
printed on the phase quadrature [42], we lock to this
quadrature by feeding the low-frequency component of
the balanced detector (Femto HBPR-100M-60K-IN-FC)
output into an analogue servo controller (New Focus
LB1005). The proportional–integral servo generates a
control signal that, after amplification by a high-voltage
amplifier (PiezoDrive PX200), drives a fibre stretcher
(PiezoDrive FS) placed in the local oscillator arm of
the interferometer. To be shot-noise-limited, the optical
power at the end of this arm is about 10 4 times higher
than that at the end of the signal arm, and the laser
phase noise is suppressed by matching the optical path
lengths of the two arms to within a few centimetres.
B. Efficient optical coupling
To attain highη, we require an efficient interface be-
tween the cavity and the fibre-based interferometer. This
is provided by a short on-chip silicon nitride waveguide
that evanescently couples to the cavity with high effi-
ciency (ηesc = 82%, section V A) and ends on one side in
a photonic crystal mirror and, on the other, in a tapered
section. From the waveguide taper, light is transferred
adiabatically into a conically tapered single-mode fibre
that is brought into contact.
Maximising waveguide–fibre transfer efficiencyη wf re-
quires the fibre tip to have the appropriate tapering pro-
file. Inspired by Ref. [69], we fabricate this using a home-
built heat-and-pull setup (based on a hydrogen torch)
and an off-the-shelf solenoid (RS Components 177-0146,
for fast pulling) [62]. Maximisingη wf also requires a pre-
cise positional and angular alignment. This is challeng-
ing in a dilution refrigerator: Room-temperature pre-
alignment is lost to thermal contraction on cool-down,
while our in-situ cold alignment is hindered by limited vi-
sual access through five layers of heat shielding. To over-
come this challenge, the device alignment (and mount-
ing) is first facilitated by a custom holding structure
(Extended Data FIG. 1b). The tapered fibre is fixed
with a grooved, angle-adjustable clamp, while the chip,
containing several optomechanical devices, is mounted
upside-down on a gold-plated, oxygen-free copper holder
attached to a three-axis cryo-compatible piezo positioner
stage (Attocube ANPx or ANPz). To enhance thermal-
isation, a thermal anchor (Attocube ATC100) is sand-
wiched between holder and stage, and linked to the base
plate by a copper strip. A resistive thermometer (Lake
Shore) monitors holder temperature. The cold align-
ment is then performed using a long-working-distance
zoom microscope with a separate white-light illumination
source, both sitting outside the fridge. To suppress re-
flections from the five refrigerator windows, both micro-
scope and illuminating beam are slightly tilted towards
the chip. With all these measures in place, we achieve
ηwf = 77% (including losses in the 8-m cryostat fibre
and splices) — a notably high efficiency for a movable
in-fridge optical fibre-chip interface.
C. Vibration-reduced refrigeration
In normal operation, the refrigerator pulse tube, pro-
viding cooling power, induces substantial vibrations that
modulate waveguide–fibre coupling, optical path length,
and signal-arm polarisation. We therefore run the experi-
ment with the pulse tube off, cooling instead via a helium
“battery” mounted on the 4-K flange: a pre-charged ves-
sel of liquid helium whose evaporation sustains low tem-
perature for about three hours. As the helium battery
cools only the 4-K flange and other cryostat flanges grad-
ually heat up during the run, the probe fibre (which is
mounted on all flanges) can make a polarisation change
which we regularly check and compensate.
D. Stabilising feedback
For input optical powersP in >60 nW (injected into
the long fibre going to the cryostat), we observe inter-
mittent instability of the optomechanical device, char-
acterised by high-amplitude self-oscillations (Extended
Data FIG. 6a). Similar behaviour has been previ-
ously reported in these ultra-coherent optomechanical

--- 第15页 ---
15
pos. z
pos. x
pos. y thermal
anchor
chip holder
thermometer
fibre
holder
ba
IM 1
IM 2
ϕ
oscillo
SA
clockclock
Red Pitaya
ϕ
FG
trigger
trigger
feedback
measurement
P I
Extended Data FIG. 1.Experimental setup. a,Control and measurement circuitry. IM, intensity modulator (electro-optic).
FG, function generator. SA, spectrum analyzer. oscillo, oscilloscope. PI, proportional–integral controller. Theϕ-labelled green
box indicates a fibre stretcher. An on-resonance laser beam (red) interacts with the optomechanical device located inside a
dilution refrigerator. The mechanical displacement is imprinted on the phase quadrature of the back-reflected beam, allowing
the resonator’s motion to be monitored via homodyne detection. The measurement data is recorded by the oscilloscope. To
stabilise the device, weak feedback is applied using a detuned laser (orange) and IM 2. IM 1 and the SA are used only for
characterisation.b,Holding structure. The chip, with the optomechanical device fabricated on top, is placed upside-down
in a holder and mounted onto a stack of three piezo-positioners (pos. x, y, z) to provide three-axis motorised control. The
tapered fibre is fixed into place with adjustable angle to optimise alignment. A thermal anchor is sandwiched between chip
holder and positioning stack, while a thermometer provides temperature readings. The full structure is placed on the bottom
of the dilution refrigerator, over a series of windows that allow optical access for alignment.
resonators [70] and attributed to coherent feedback from
stray back-reflections. Alternatively, large fluctuations
could result in nonlinear cavity dynamics that induce ef-
fective amplification [40].
A minimal amount of measurement-based feedback,
which reduces amplitude and broadens linewidth, sta-
bilises the resonator. It is implemented optically by
modulating a weak, slightly red-detuned laser (Santec
TSL-550). We verify that the feedback and measure-
ment lasers beat only at frequencies larger than 1 GHz,
beyond the resonator’s response. This feedback laser is
kept off during most characterisation.
The real-time electronic feedback signal is generated
from the photocurrent by a digital signal processor (Red
Pitaya STEMlab 125-14 LN). This processor implements
two band-pass filters with tuneable gain and phase shift.
One filter is centered at Ω/2π(with a 3-dB bandwidth of
9.7 kHz) and adjusted to stabilise the mechanical mode
of our interest (section V D). The other filter is set to cool
a higher-order mode that starts to lase once the funda-
mental mode is under control. The generated signal is
then further amplified and used to drive an electro-optic
amplitude modulator (Oclaro AM1). As the dynamical
range of the feedback setup is limited, it is only effective
when engaged in the non-lasing state of the device. To
ensure this, we monitor the photocurrent on the setup
oscilloscope before turning on the feedback.
V. CHARACTERISATION
We here explain the methods used to characterise the
system.
A. Optical cavity
To characterise the optical cavity, we inject a low power
(Pin = 20 nW) from the measurement laser (feedback
laser off), step the laser frequencyω L/2πacross the cav-
ity response (with resonance frequencyω c/2πand decay
rateκ) and measure the average intensity of the back-
reflected light (Extended Data FIG. 2a). Considering
the field reflection ratio
R= (1−2η esc) + 2i∆/κ
1 + 2i∆/κ (34)
with ∆ =ω c −ω L, we fit|R| 2 to the measured inten-
sity response and findω c/2π= 194.898 THz,κ/2π=
11.50 GHz and (1−2η esc)2 = 0.40.
To determine the sign inηesc = (1±
√
0.40)/2 (overcou-
pling or undercoupling of the cavity to the waveguide),
we perform a test using the homodyne interferometer.
While the laser wavelength is swept very quickly, across
a 4-nm interval, we record the DC output of the balanced
detector (without locking on any homodyne phase). The
interferometer then measures Re[Rexp (iω LL/c)] where
Lis the optical path difference between the two arms
andcis the speed of light in vacuum. WhileLis almost
constant during a single sweep, it has random changes
each time that we do the measurement. We repeat this
measurement until we find exp (iωLL/c)≈1 atω L =ω c,
so the measurement output at this frequency approxi-
mates Re[R] for ∆ = 0. As shown in Extended Data
FIG. 2b, this output is negative, indicating that the cav-
ity is overcoupled andηesc = (1+
√
0.40)/2. In this figure,
the 1.2-nm fringe spacing indicates that the optical path
lengths of the two arms are different by about 2 mm.

```

---

## 实验/结果

```

--- 第19页 ---
19
efficiency element value
cavity–waveguide coupling (ηesc) 81.8%
waveguide–fibre coupling (ηwf, in the dilution fridge) 76.7%
interferometer components’ transmission 83.2%
interference visibility 99%
photodetector quantum efficiency 76%
electronic noise suppression 96.7%
total efficiency (η) 38%
Extended Data TABLE I.Contributions to optical de-
tection inefficiency.
Data FIG. 5), we get 160.59 kHz forg 0/2πand 12.19 K
forT, in good agreement with previous results.
F. Optical detection efficiency
In Extended Data TABLE I, we quantify the various
inefficiencies encountered by the probe field on its way
from the optical cavity to the final phase detection.
G. Estimating optical detection efficiency from
non-linear transduction
To obtain an independent estimate of the total effi-
ciencyη, we developed a new method based on the non-
linear transduction of high-amplitude mechanical motion
by the optical cavity [74]. In our experiment, we can
readily access this regime by turning the feedback off and
waiting for instability to occur. Extended Data FIG. 6c
shows a time trace of a photocurrent obtained under such
conditions.
In this method, we use the extreme values of the
phase quadrature component of the reflectivity Im[R] =
ηescκ∆/(∆2 +κ 2/4) (Extended Data FIG. 6b) as a refer-
ence level. These extrema are located at ∆ =±κ/2,
where Im[R] =±η esc, and occur in Extended Data
FIG. 6cas the mechanically-shifted instantaneous de-
tuning ∆ =g 0Qexplores a large fraction of the cavity
response. Here,Qis the mechanical displacement nor-
malized to its zero point fluctuations.
We proceed by switching to a semi-classical picture and
writing the detected phase quadrature as
ˆYdet = ˆYv + √ηκY ,(36)
the sum of a quantum vacuum field ˆYv and a classical
field, where
Y= 2 √ηescκIm[χ a]×α in (37)
is the mean phase quadrature of the driven intra-cavity
field. Here, we consider the cavity susceptibilityχ a =
(κ/2−i∆) −1 and the coherent amplitudeα in of the field
coupling in (from the waveguide, with efficiencyη esc).
We takeα in real.
/uni00000013/uni00000018/uni00000014/uni00000013/uni00000014/uni00000018/uni00000015/uni00000013/uni00000015/uni00000018
/uni00000037/uni0000004c/uni00000050/uni00000048/uni00000003/uni0000000b/uni00000056/uni0000000c
/uni00000013/uni00000011/uni00000014
/uni00000013/uni00000011/uni00000013
/uni00000013/uni00000011/uni00000014
/uni00000033/uni0000004b/uni00000052/uni00000057/uni00000052/uni00000046/uni00000058/uni00000055/uni00000055/uni00000048/uni00000051/uni00000057/uni00000003i(t)/uni00000003/uni0000000b/uni00000039/uni0000000c
/uni00000014
/uni00000013/uni00000014
/uni00000027/uni00000048/uni00000057/uni00000058/uni00000051/uni0000004c/uni00000051/uni0000004a/uni00000003/
/uni00000014
/uni00000013
/uni00000014
/uni00000033/uni0000004b/uni00000044/uni00000056/uni00000048/uni00000003/uni00000054/uni00000058/uni00000044/uni00000047/uni00000055/uni00000044/uni00000057/uni00000058/uni00000055/uni00000048
Y/Ymax
/uni00000013/uni00000015/uni00000017/uni00000019
/uni00000037/uni0000004c/uni00000050/uni00000048/uni00000003t/uni00000003/uni0000000b/uni00000056/uni0000000c
/uni00000013/uni00000011/uni00000015
/uni00000013/uni00000011/uni00000014
/uni00000013/uni00000011/uni00000013
/uni00000013/uni00000011/uni00000014
/uni00000013/uni00000011/uni00000015
/uni00000033/uni0000004b/uni00000052/uni00000057/uni00000052/uni00000046/uni00000058/uni00000055/uni00000055/uni00000048/uni00000051/uni00000057/uni00000003i(t)/uni00000003/uni0000000b/uni00000039/uni0000000c
/uni00000044
/uni00000045 /uni00000046
Extended Data FIG. 6.Non-linear transduction of high-
amplitude oscillations. a,Intervals of intermittent insta-
bility (grey) in the mechanical amplitude are observed for
higher input powers, when the feedback laser is off. These
intervals get longer and more frequent with increasing laser
power.b,Phase quadratureYof the mean intra-cavity field
as a function of detuning ∆ (blue). Extreme values±Y max
are indicated (dashed lines) and occur at ∆ =±κ/2. For
small detunings|∆| ≪κ, the linear approximation (red) is
typically used.c,High-amplitude self-oscillations of the res-
onator explore detunings beyond|∆|> κ/2. The extreme
values in the photocurrent (dashed lines) then correspond to
±Ymax and can be used for calibration.
Next, we expressα in =
p
¯ncavκ/(4ηesc) in terms of the
cavity photon number ¯ncav attained on resonance (∆ =
0), and get
Y= √¯ncav ×Im[κχ a] = √¯ncav × κ∆
∆2 +κ 2/4 ,(38)
where we note that Im[κχ a] = Im[R]/η esc. As the
instantaneous ∆ is swept across the cavity resonance
by mechanical motion,Yattains a maximum value of
Ymax = √¯ncav at ∆ =κ/2, and−Y max at ∆ =−κ/2.
The homodyne detector produces a photocurrent i =
s ˆYdet proportional to the detected phase quadrature. The
maximum photocurrent imax, as shown in Extended Data
FIG. 6c, is obtained whenY=Y max and given by
imax =s √ηκ Ymax =s √ηκ¯ncav .(39)
Ifη,κand ¯n cav are all known, we can useY max as a ref-
erence to find the detector sensitivitys= i max/√ηκ¯ncav.
If, however,ηis not known, we can determine it by
comparing imax to the shot-noise spectral densityS SN
ii (ω)
of the photocurrent measured when the cavity is not
driven, i.e., whenY= 0 and ˆYdet = ˆYv. We then find
SSN
ii (ω) =s 2S ˆYv ˆYv
(ω) = i2
max
ηκ¯ncav
(40)

--- 第20页 ---
20
whereS ˆYv ˆYv
(ω) = 1 for the optical vacuum field ˆYv. To
work outηfrom Eq. (40),κneeds to be entered as an
angular frequency andS SN
ii (ω) calculated as a double-
sided spectrum. Note that to determine ¯ncav, we still use
ηesc andη wf, which can be estimated independently and
accurately.
In our experiment, we find i max = 0.200 V for ¯ncav =
41.4, and a noise spectral densityS SN
ii (ω) = 3.53×
10−14 V2/Hz around the mechanical resonance Ω. Hence,
from Eq. (40) we find a value of 37.8% forη, in good
agreement with the previous result.
VI. DATA ACQUISITION AND ANALYSIS
Time traces of the photocurrent are recorded on a low-
noise oscilloscope (Tektronix MSO64). The oscilloscope
produces digital samples at a rate of 5 MHz with 12-bit
vertical resolution (acquisition mode Sample). The oscil-
loscope’s maximum record length is 6.25×10 7 samples.
To prevent aliasing, an analogue filter is placed before
the oscilloscope input.
A. Preparing the measurement records
The recorded data is normalised to the shot noise level
and then demodulated at frequency Ω/2π. The demodu-
lation low-pass filter is a causal Butterworth filter, with
56.5 kHz 3-dB bandwidth and an impulse response that
effectively vanishes after about 400µs.
The filter bandwidth is chosen with two considerations.
First, it is significantly smaller than Ω/2πand signifi-
cantly larger thanγ th/2π≈2.79 kHz andγ opt/2π≈363
Hz, as needed by the simplified measurement model [50].
Second, it filters out all the coloured noises (including
the other mechanical modes measurement signals and the
probe laser phase noise).
Considering the filter impulse response, the first ten
400-µs segments of the output currents are discarded.
As such, we make sure that the remaining parts of the
two currents are properly low-pass-filtered. These parts
are then divided to the shorter records. To maximize the
number of records, the record length is minimized while
ensuring that the steady state of filtering and smoothing
is captured or closely approached.
B. Analysing the records
Given thatn th ≫1,κ≫Ω, g(the fast-cavity
limit,g=g 0
√¯ncav ) and Ω≫γ th, γopt, the effective
interaction-frame stochastic master equation of the sys-
tem is [50, 62]
dρF(t) = Γ(n th + 1) dtD
h
ˆb
i
ρF(t) +
Γnth dtD
h
ˆb†
i
ρF(t) +
1
2 ΓCdt
2X
j=1
D
 ˆXj

ρF(t) +
r
1
2 ηΓC
2X
j=1
dWF,j(t)H
 ˆXj

ρF(t)
(41)
whereD[•] andH[•] are, respectively, the standard dis-
sipative and diffusive measurement superoperator; ˆband
ˆb† are, respectively, the annihilation and creation opera-
tor of the resonator; ˆX1 and ˆX2 are (time-independent)
interaction-frame quadrature operators and dW F,1 and
dWF,2 are two independent Wiener increments, each
given by the corresponding measurement record (I 1(t)
orI 2(t)):
dWF,j(t) = Ij(t) dt−
p
2ηΓCTr
h
ρF(t) ˆXj
i
dt .(42)
Using Eq. (41), we can set the matrices employed by
Eqs. (8), (9), (10) and (11) (with ˆx= ( ˆX1, ˆX2)⊤) [39]:
A=− Γ
2 I,D= 2Γn tot I,C=
p
2ηΓCI,Γ=0.(43)
The initial conditions for Eqs. (8) and (9) are now given
by the unconditional state of the resonator. At dynamical
equilibrium, as in the case of our experiment, the uncon-
ditional state is Gaussian with the moments⟨ ˆx⟩uncon =0
andV uncon = 2ntot I— The Markovian master equation
of the system is recovered by removing the last term on
the right hand side of Eq. (41). Solving for the filtered
covariance matrix then givesV F(t) =v F(t)Iwith
˙vF(t) =−Γv F(t) + 2Γntot −2Γ (ηC)v 2
F(t),(44)
yielding
vF(t) =
 1
2ntot −v ss
F
+ 2ηC√1 + 16ηCntot

eΓt√1+16ηCntot − 2ηC√1 + 16ηCntot
−1
+v ss
F ,(45)
where
vss
F = lim
t→∞
vF(t) =
√1 + 16ηCntot −1
4ηC .(46)
Having the covariance matrix, we solve
d⟨ ˆXj⟩F(t) =− Γ
2 ⟨ ˆXj⟩F(t) dt+
√2ηΓCv F(t) dWF,j(t),
(47)

--- 第21页 ---
21
to find the stochastic first moments of the filtered state,
considering Eq. (42).
Solving Eq. (11), with an uninformative final condi-
tion, gives the covariance matrix of the effect operator as
VR(t) =v R(t)Iwith
vR(t) =v ss
R +
 2ηC√1 + 16ηCntot
 
e−Γ (t−T) √1+16ηCntot −1
−1 (48)
where
vss
R = lim
T →∞
vR(t) =
√1 + 16ηCntot + 1
4ηC .(49)
The first moments of the effect operator are then given
by
⟨ ˆXj⟩R(t) =v R(t)Z R,j(t), j= 1,2 (50)
whereZ R,j(t) is found by solving
−dZR,j(t) =−
 Γ
2 + 2Γntot
vR(t)

ZR,j(t) dt+
√2ηΓCI j(t) dt
(51)
which goes backwards in time from the final condition
ZR,j(T) = 0 [39].
Given that the measurement records are sampled in
time, the aforementioned techniques for finding the con-
ditional mean values are accordingly adapted following
the procedures explained in Ref. [1]. The smoothing com-
bination of the filtered and retro-filtered mean values is
also accordingly adapted considering Ref. [75].
C. Modelling the stabilizing feedback
To introduce the stabilizing feedback into our analy-
sis, we consider three points. First, the feedback can
be treated as effectively Markovian [2]: With the feed-
back bandwidthB/2π= 9.7 kHz, we have 1/B ≪1/Γ,
so the timescale of the feedback-induced autocorrelation
is much shorter than that of the dynamical autocorrela-
tion — the additional loop delay is less than 1µs. Sec-
ond, the peak frequency of the mechanical susceptibil-
ity is unaffected by the phase-tuned feedback (Extended
Data FIG. 4b). Third, the effective rotating-frame dy-
namics remain symmetric [50], since (i) Ω/Γ fb >10 4, (ii)
the feedback bandwidth is centered around Ω, and (iii)
B ≪Ω.
With these considerations, the feedback can be incor-
porated into the (retro)filtering equations either formally
or intuitively. In the formal approach, theA,D, andΓ
matrices are updated by adding feedback terms, as in
Ref. [2]. In the intuitive approach, one simply makes the
substitutions Γ→Γ fb andn th →n th ×Γ/Γ fb in all equa-
tions. This intuitive approach performs similarly on our
data because the feedback-induced correlation between
the measurement noise and the process noises is negligi-
ble.
D. Noise injection and analysis
To perform the noise-injection experiment, we add
white noise to the shot-noise-normalised data and then
renormalise it to the new noise floor. The added noise is
weighted such that the detection efficiency reduces from
0.38 to 0.10. The resulting noisier current is demodulated
and the outputs, excluding the initial segments, are di-
vided into 1-ms records. Longer records are required in
this experiment as the reduced detection efficiency pro-
longs the transients.
Each new measurement record is then processed by
Eqs. (47) and (50) to yield⟨ ˆXj⟩η↓
F and⟨ ˆXj⟩η↓
R , while
vη↓
F andv η↓
R are evaluated by Eqs. (45) and (48) with
the reduced detection efficiency. Withρ η↓
F in hand, the
smoothed estimate ofρ LTL
F is given by Eq. (1) with
⟨ˆx⟩F = (⟨ ˆX1⟩η↓
F ,⟨ ˆX2⟩η↓
F )T,⟨ ˆx⟩R = (⟨ ˆX1⟩η↓
R ,⟨ ˆX2⟩η↓
R )T,
VF =v η↓
F I,V R =v η↓
R IandV ss
F =v ss
F I. We note that, for
the purpose of this analysis,V ss
F should not be replaced
byv η↓,ss
F I. When allV ss
F terms are instead replaced by
0, the new outputs of classical smoothing equations are
obtained.
VII. FULL HETERODYNE UNRAVELLING
A full heterodyne unravelling of the resonator’s mas-
ter equation results in the conditional covariance matrix
VT(t) =v T(t)I, wherev T(t) is governed by an equation
similar to Eq. (44) with the the last term in the right
hand side (the measurement term) being updated:
˙vT(t) =−Γv T(t) + 2Γntot −2Γ (C+n th)v 2
T(t).(52)
By putting ˙v T = 0, we find the steady state solution
vss
T = 1, yieldingV ss
T =I.
To clarify the physical meaning of this full unravel-
ling, and to validate its consistency with the assumptions
underlying the resonator’s master equation, we rewrite
Eq. (52) as
˙vT(t) =

−Γv T(t) + Γ

+

−2ΓηCv 2
T(t) + 2ΓηC

+

−2Γ(1−η)Cv 2
T(t) + 2Γ(1−η)C

+

−2Γn th v2
T(t) + 2Γnth

.
(53)

--- 第22页 ---
22
The first bracket describes the resonator in contact with a
zero-temperature thermal bath. Its first term arises from
dynamical drift, while the Γ term represents the min-
imum diffusion required by the fluctuation–dissipation
relation [2]. The second and third brackets correspond
to the observed and unobserved optical baths, respec-
tively. In each case, the first term represents heterodyne
detection via the bath, while the second term is the as-
sociated diffusion, which can be interpreted as the back-
action of the detection. This interpretation is consistent
with the terminology “back-action heating”, used in the
literature to describe the contribution ofCto the to-
tal phonon occupancyn tot of the resonator — we note
that the terminology holds no matter what proportion
(η) of the optical bath is observed. The fourth bracket
describes heterodyne detection via the hot phononic bath
and its diffusive back-action. Such a measurement does
not disturb the dynamical symmetry, as the rate Γn th is
much smaller than Ω. Therefore, the resonator’s master
equation has been unravelled in a manner consistent with
its underlying assumptions, and the resonator can be re-
garded as a harmonic oscillator heated from its ground
state solely by measurement back-action.

--- 第23页 ---
23
SUPPLEMENTARY INFORMATION FOR
POST-PROCESSED ESTIMATION OF QUANTUM STATE TRAJECTORIES
Soroush Khademi, Jesse J. Slim, Kiarn T. Laverick, Jin Chang, Jingkun Guo,
Simon Gr¨ oblacher, Howard M. Wiseman, and Warwick P. Bowen
S1. SAMPLE TRACES OF⟨ ˆX1⟩
The values of⟨ ˆX1⟩, for sample measurement records, are shown in FIG. S1a(main experiment) and FIG. S1c
(noise-injection experiment). They are qualitatively similar to the sample traces of⟨ ˆX2⟩shown in FIG. 2band
FIG. 3b, as ˆX1 and ˆX2 have identical statistics due to dynamical symmetry.
S2. EXTENDED DATA FORδ C
The distributions ofδ C(t) =⟨ ˆXj⟩LTL
F (t)− ⟨ ˆXj⟩C(t), j= 1,2 for three sample times are shown in FIG. S2. They
all have zero means. That is, filtering (C = F) and quantum state smoothing (C = S) are unbiased estimations of
the target mean values. Interestingly, the classical smoothing (C = cS) distributions are also unbiased. The standard
deviations of all distributions decrease over time, as also shown by FIG. 2c, with the quantum state smoothing ones
remaining the smallest.
S3. INFERENCE SELF-CONSISTENCY RELATIONS
In this section, we examine the equalityVar ens

⟨ ˆXj⟩C(t)

=σ 2
uncon −v C(t) for an infinitely large ensemble of
measurement records. The effect of the finite size of the experimental ensemble is discussed in the next section.
For filtering (C = F), Eq. (47) gives
⟨ ˆXj⟩F(t) =e −Γt/2⟨ ˆXj⟩F(0) +
p
2ηΓC
Z t
0
e− Γ
2 (t−s)vF(s)dWF,j(s).(S1)
ConsideringVar ens

⟨ ˆXj⟩F(t)

=E ens

⟨ ˆXj⟩2
F(t)

−E2
ens

⟨ ˆXj⟩F(t)

, whereE ens[•] denotes averaging,E ens

dWF,j(s)

= 0
andE ens

dWF,j(s) dWF,j(s′)

=δ(s−s ′) ds2, we find
Varens

⟨ ˆXj⟩F(t)

=e −Γt Varens

⟨ ˆXj⟩F(0)

+ 2ηΓC
Z t
0
ds e−Γ(t−s)v2
F(s).(S2)
As⟨ ˆXj⟩F(0) is fixed (at zero),Var ens

⟨ ˆXj⟩F(0)

= 0 and
Varens

⟨ ˆXj⟩F(t)

= 2ηΓC
Z t
0
ds e−Γ(t−s)v2
F(s).(S3)
Let us now also consider the quantityℓ(t) =σ 2
uncon −v F(t). Considering Eq. (44), we have
d
dt ℓ(t) =−Γℓ(t) + 2ηΓCv 2
F(t),(S4)
which has the solution
ℓ(t) =e −Γtℓ(0) + 2ηΓC
Z t
0
ds e−Γ(t−s)v2
F(s).(S5)
Asv F(0) =σ 2
uncon,ℓ(0) = 0 and
ℓ(t) = 2ηΓC
Z t
0
ds e−Γ(t−s)v2
F(s).(S6)

--- 第24页 ---
24
FIG. S1.Estimation analysis extended data. a-b,The main experiment data.a,Stochastic traces for the quadrate mean
⟨ ˆX1⟩(t) for a sample measurement record.b,Deterministic conditional variances (v C(t), curves) and the corresponding value
ofσ 2
uncon −Var ens[⟨ ˆXj⟩C(t)] (data points) with error bars.c-d,The noise-injection (η-reduced) experiment data.c,Stochastic
traces for the quadrate mean⟨ ˆX1⟩(t) for a sample measurement record.d,Deterministic conditional variances (v η↓
C (t), curves)
and the corresponding value ofσ 2
uncon −Varens[⟨ ˆXj⟩η↓
C (t)] (data points) with error bars. Inbandd, the vertical axes are limited
to near steady-state values for visual clarity, and each error bar spans two standard deviations of the error (caused by the finite
size of the ensemble of measurement records).
We can therefore conclude from Eqs. (S3) and (S6) that
Varens

⟨ ˆXj⟩F(t)

=ℓ(t) =σ 2
uncon −v F(t).(S7)
To examine the case of quantum state smoothing (C = S), we note that
Varens

⟨ ˆXj⟩S(t)

=
 vS −v tar
vF −v tar
2
Varens

⟨ ˆXj⟩F(t)

+
 vS −v tar
vR +v tar
2
Varens

⟨ ˆXj⟩R(t)

+
2
 vS −v tar
vF −v tar
 vS −v tar
vR +v tar

Covens

⟨ ˆXj⟩F(t),⟨ ˆXj⟩R(t)

(S8)
wherev tar is the variance of the target state. To evaluate this expression, we first investigate the value of
Varens

⟨ ˆXj⟩R(t)

. Considering the definition of the retrofiltered effect operator, we havep( − →O t|ρuncon)∝Tr[ ˆERρuncon].
Given that both the effect operator and the unconditional state are Gaussian, and that Tr[ρσ] = 4π
R
dxWρ(x)Wσ(x),
we find
p(− →O t|ρuncon)∝g(⟨ ˆx⟩R;⟨ ˆx⟩uncon,V R +V unc)≡p(⟨ ˆx⟩R;t) (S9)

--- 第25页 ---
25
FIG. S2.Distributions ofδ C(t) =⟨ ˆXj⟩LTL
F (t)− ⟨ ˆXj⟩C(t), j= 1,2.With the main experiment data, the blue histograms are
for C = F (filtering), the red ones for C = S (quantum smoothing) and the green ones for C = cS (classical smoothing).p(δ C)
is the probability distribution of the realisedδ C values andp max is the maximum bar height of the corresponding histogram.
where the final equivalence comes from the fact that⟨ ˆx⟩R(t) is a deterministic function of − →O t, with the other variables
in the Gaussian being independent of the measurement records. The standard probability theory then yields
Varens

⟨ ˆXj⟩R(t)

=σ 2
uncon +v R(t).(S10)
The next step to evaluate the right hand side of Eq. (S8) is to consider the fact thatVar ens

⟨ ˆXj⟩F(t)− ⟨ ˆXj⟩R(t)

=
vF(t) +v R(t), which alongside Eqs. (S7) and (S10) gives
Covens

⟨ ˆXj⟩F(t),⟨ ˆXj⟩R(t)

=σ 2
uncon −v F(t).(S11)
It is then straightforward to conclude from Eqs. (S7), (S10) and (S11) that
Varens

⟨ ˆXj⟩S(t)

=σ 2
uncon −v S(t).(S12)
Finally, for classical smoothing (C = cS), we have
Varens

⟨ ˆXj⟩cS(t)

=
 vcS
vF
2
Varens

⟨ ˆXj⟩F(t)

+
 vcS
vR
2
Varens

⟨ ˆXj⟩R(t)

+
2
 v2
cS
vF vR

Covens

⟨ ˆXj⟩F(t),⟨ ˆXj⟩R(t)

(S13)
which, considering Eqs. (S7), (S10) and (S11), results in
Varens

⟨ ˆXj⟩cS(t)

=σ 2
uncon −v cS(t).(S14)
S4. ERROR BARS FOR THE SELF-CONSISTENCY TESTS
There is always a statistical error involved in the inference self-consistency tests because, in practice, the number
of available measurement records is finite. As the quantity of interest is the variance of a Gaussian random variable

--- 第26页 ---
26
estimated from a finite number of realizations, the standard deviation of this error equals thestandard error of
variance(SEV) [76]:
σSEV,C(t) =
r
4
2Neff
×

σ2
uncon −Var ens
h
⟨ ˆXj⟩C(t)
i
(S15)
where
Neff =N× 1
1 + 2
N−1X
k=1

1− k
N

e−(Γfb/2)Tk
2
(S16)
is the product of the large size of the ensemble (N= 16653) and a temporal-correlation factor smaller than one (where
T= 750µs) — the replacement Γ→Γ fb has been preformed in the denominator as the stabilising feedback is on.
For the noise-injection experiment, the same formula is used withN= 12489 andT= 1000µs.
The results are shown in FIG. S1b(main experiment) and FIG. S1d(noise-injection experiment), where each error
bar spans 2σ SEV,C(t) and the vertical axes are restricted to values near steady state for visual clarity. As expected,
the data error bars do not include the deterministic values ofv C(t) about one-third of the time.
S5. CONDITIONAL VARIANCES IN THE STEADY STATE
AssumingηC ≫ 1
2, Eqs. (46) and (49) give
vss
F ≈v ss
R ≈
r ntot
ηC (S17)
paving the way to derive approximate expressions for the steady-state smoothing variances (at 0≪t≪ T).
Once we take the “true” state of the resonator to be a displaced ground state, the variance of its smoothed estimate
is
vss
S ≈1 + 1
2
 r ntot
ηC −
r
ηC
ntot
!
.(S18)
This is never smaller than one, the ground state variance, as required for a valid quantum state.
For classical smoothing,
vss
cS ≈ 1
2
r ntot
ηC .(S19)
This becomes smaller than one whenη >0.25 andC/n th >1/(4η−1), indicating that the Gaussian function produced
by the classical smoothing equations does not always correspond to a physical quantum state as it can violate the
Heisenberg uncertainty principle. In our experiment only the first condition holds.
Finally, the difference
vss
S −v ss
cS ≈1− 1
2vss
F
(S20)
is always positive. For this difference to be appreciable, say larger thanv ss
cS/10, so that the benefits of quantum state
smoothing are most pronounced, one needsv ss
F ≲20.
S6. HILBERT-SCHMIDT DISTANCE SQUARED — GENERAL THEORY
In this section, we theoretically derive the ensemble-averaged value of the estimation cost function that equals
∆2
HS[ρtar, ρest] =
X
ρtar
Z
d← →O p(ρtar, ← →O) Tr

(ρtar −ρ est)2
.(S21)

--- 第27页 ---
27
It has been shown [35], for the filtered or smoothed quantum states, that the averaged trace-squared deviation reduces
to the average difference in the purity,i.e.,
∆2
HS[ρtar, ρest] =
Z
d← →O p(← →O) (P[ρ tar]−P[ρ est]) (S22)
where P[ρ] denotes the purity ofρ. Since in LGQ systems, the purity is given by P[ρ] = 1/
p
det[V], where we have
chosenℏsuch that the equality holds, and the covariance matrix is independent of the measurement records, Eq. (S22)
gives
∆2
HS[ρtar, ρest] = 1/
p
det[Vtar]−1/
p
det[Vest].(S23)
As is the case in our system, all covariance matrices are proportional toI, the expression is simplified to
∆2
HS[ρtar, ρest] =v −1
tar −v −1
est .(S24)
Doing the calculation for classical smoothing is slightly more complicated. Usingp(ρ tar, ← →O) =p(ρ tar|← →O)p( ← →O),
expanding the trace term and using the definition of the smoothed state, Eq. (16), one obtains
∆2
HS[ρtar, ρcS] =
Z
d← →O p(← →O)
 
P[ρcS]−2Tr[ρ cSρS] +
X
ρtar
p(ρtar|← →O) P[ρ tar]
!
.(S25)
Regarding the second term of the integrand, it is known [2] that Tr[ρσ] = 4π
R
dxWρ(x)Wσ(x), whereW ρ(x) denotes
the Wigner function ofρ, and the 4πis necessary, so that the proportionality for the purity is unity. For LGQ systems,
the Wigner function is a normalized GaussianW(x) =g(x;µ,V) with meanµand covariance matrixV. Regarding
the argument of the summation,p(ρ tar|← →O)P[ρ tar], because the target state is completely described by the mean⟨ ˆx⟩tar
and covarianceV tar, the latter of which is deterministic, we havep(ρ tar|← →O)≡p(⟨ ˆx⟩tar|← →O). Now, since the purity is
independent of the measurement records ← →Oand the mean⟨ ˆx⟩tar, we have
∆2
HS[ρtar, ρcS] = 1/
p
det[VcS] + 1/
p
det[Vtar]−8π
Z
d← →O p(← →O)
Z
dxWcS(x)WS(x).(S26)
Focusing on the last term on the right hand side, we compute the overlap of the two Gaussian Wigner functions and
find
R
dxWcS(x)WS(x) =g(⟨ ˆx⟩S;⟨ ˆx⟩cS,V S +V cS); the probability of the records can be determined via
p(← →O)∝Tr[E R ˜ρF]
∝
Z
dˆxWF(x)WR(x)
=g(⟨ ˆx⟩F;⟨ ˆx⟩R,V R +V F),
(S27)
where ˜ρF is the unnormalised filter state introduced in Ref. [28] and the final equality results by normalising the
distribution. Importantly, we see that this distribution depends only on the differencer=⟨ ˆx⟩F − ⟨ˆx⟩R. Now, we
simplify the difference⟨ ˆx⟩cS − ⟨ˆx⟩S as follows:
⟨ˆx⟩cS − ⟨ˆx⟩S =V cS(V−1
F ⟨ˆx⟩F +V −1
R ⟨ˆx⟩R)−(V S −V tar)((VF −V tar)−1⟨ˆx⟩F + (VR +V tar)−1⟨ˆx⟩R)
=Z(⟨ ˆx⟩R − ⟨ˆx⟩F)
=Zr
(S28)
whereZ=V cSV−1
R −(V S −V tar)(VR +V tar)−1, and we have usedV −1
cS =V −1
F +V −1
R and (V S −V tar)−1 =
(VF −V tar)−1 + (VR +V tar)−1. Thus,g(⟨ ˆx⟩S;⟨ ˆx⟩cS,V S +V cS) =g(Zr; 0,V S +V cS). The last term on the right
hand side of Eq. (S26) then equals
−8π
Z
d← →O p(← →O)
Z
dxWcS(x)WS(x)≡ −
Z
drg(r; 0,VR +V F)g(Zr; 0,VS +V cS)
=−4
r
det
h
((VF +V R)−1 +Z ⊤(VS +V cS)−1Z) −1
i
p
det[VF +V R]
p
det[VS +V cS]
.
(S29)

--- 第28页 ---
28
Therefore
∆2
HS[ρtar, ρcS] = 1/
p
det[VcS] + 1/
p
det[Vtar]−4
r
det
h
((VF +V R)−1 +Z ⊤(VS +V cS)−1Z) −1
i
p
det[VF +V R]
p
det[VS +V cS]
.(S30)
As is the case in our experimental system, all covariance matrices are proportional toI, the expression is simplified
to
∆2
HS[ρtar, ρcS] =v −1
cS +v −1
tar −4
 
(vS +v cS) +z 2(vF +v R)
−1
(S31)
where
z= vcS
vR
− vS −v tar
vR +v tar
.(S32)
S7. DISTANCE BETWEEN THE MEAN VALUES — THEORY
We here derive the theory curves for the standard deviation of the distanceδ C =⟨ ˆXj⟩tar − ⟨ ˆXj⟩C. It equals
Std(δC) =
sZZ
d⟨ ˆXj⟩tar d← →O p(⟨ ˆXj⟩tar, ← →O)δ 2
C .(S33)
For C = F,δ C is independent of the future measurement record − →y t, since⟨ ˆXj⟩tar depends only on the past
information. This makes averaging over the future record on the right hand of Eq. (S33) trivial, reducing the standard
deviation to Std(δ F) =
qRR
d⟨ ˆXj⟩tar d← −O p(⟨ ˆXj⟩tar, ← −O)δ 2
F . Now, performing the average over the target mean first,
usingp(⟨ ˆXj⟩tar, ← −O) =p(⟨ ˆXj⟩tar|← −O)p( ← −O), andp(⟨ ˆXj⟩tar|← −O) =g(⟨ ˆX⟩tar;⟨ ˆX⟩F, vF −v tar) (see Methods II A, just prior
to Eq. (26)), we get
R
d⟨ ˆXj⟩tar p(⟨ ˆXj⟩tar|← −O) (⟨ ˆXj⟩tar − ⟨ ˆXj⟩F)2 =v F −v tar, which is independent of the measurement
record ← −O t. We therefore have Std(δ F) = √vF −v tar.
For the smoothed estimate of the target (C = S), the average over the future information cannot be performed
trivially as was the case for filtering. Nevertheless, following a similar logic thereafter to the filtered case, one needs
to compute (using Eq. (26))
R
d⟨ ˆXj⟩tar p(⟨ ˆXj⟩tar|← →O) (⟨ ˆXj⟩tar − ⟨ ˆXj⟩S)2 = ◦vS =v S −v tar, which is independent of the
particular record ← →O, making the final average trivial. Thus, one obtains Std(δ S) = √vS −v tar.
For classical smoothing (C = cS), let us first consider the term
R
d⟨ ˆXj⟩tar p(⟨ ˆXj⟩tar|← →O) (⟨ ˆXj⟩tar − ⟨ ˆXj⟩cS)2. Con-
sideringp(⟨ ˆXj⟩tar|← →O) =g(⟨ ˆXj⟩tar;⟨ ˆXj⟩S, ◦vS) (from Eq. (26)), one finds
Z
d⟨ ˆXj⟩tar p(⟨ ˆXj⟩tar|← →O) (⟨ ˆXj⟩cS − ⟨ ˆXj⟩tar)2 = ˜vS + (⟨ ˆXj⟩cS − ⟨ ˆXj⟩S)2 .(S34)
This results in
Std(δcS) =
s
◦vS +
Z
d← →O p(← →O)(⟨ ˆXj⟩cS − ⟨ ˆXj⟩S)2 ,(S35)
where we have used the fact that ◦vS is independent of the measurement record. Using Eq. (S28), we have⟨ ˆXj⟩cS −
⟨ ˆXj⟩S =zr. Consideringp( ← →O)≡g(r; 0, v F +v R) and the fact that Eq. (S28) yields⟨ ˆXj⟩cS − ⟨ ˆXj⟩S =zr, we conclude
Std(δcS) =
s
◦vS +
Z
drg(r; 0, vF +v R)(zr)2 (S36)
=
p◦vS +z 2(vF +v R).(S37)

```

---

