# 物理驱动局部化 - 深度提取内容

**论文ID**: arXiv 2511.08845

**总页数**: 50

---

## 引言/概述

```

--- 第1页 ---
Graphical Abstract
Physics-based localization methodology for Data Assimilation by
Ensemble Kalman Filter
Sarp ER, Marcello MELDI
arXiv:2511.08845v1  [physics.flu-dyn]  11 Nov 2025

--- 第2页 ---
Highlights
Physics-based localization methodology for Data Assimilation by
Ensemble Kalman Filter
Sarp ER, Marcello MELDI
• A physics based online-localization procedure is developed for the lo-
calization of the regions of data assimilation using EnKF.
• The proposed methodology is applied for the synchronization of the
virtual model with a reference simulation in two different cases, namely
2D unsteady flow around square cylinder and 3D turbulent flow around
circular cylinder.
• A significant reduction of the computational costs associated with DA
procedure is observed due to the optimal choice of the DA regions at
each analysis stage, without any loss in the synchronization perfor-
mance as a result of the reduction of DA regions.
• The relationship between the optimized parameters and the flow physics
have been demonstrated.

--- 第3页 ---
Physics-based localization methodology for Data
Assimilation by Ensemble Kalman Filter
Sarp ER, Marcello MELDI
aUniv. Lille, CNRS, ONERA, Arts et Metiers ParisTech, Centrale Lille, UMR 9014-
LMFL- Laboratoire de Mecanique des fluides de Lille -Kampe de Feriet, F-59000 Lille,
France,
Abstract
A physics-based methodology for the determination of the localization func-
tion for the Ensemble Kalman Filter (EnKF) is proposed. The spatial fea-
tures of such function evolve dynamically over time according to the relevant
instantaneous flow features of the ensemble members with the objective, to
reduce the computational cost of the Data Assimilation (DA) procedure when
applied with solvers for Computational Fluid Dynamics (CFD). The valida-
tion of the methodology has been carried out by the analysis of two test cases
exhibiting different features. This permits to investigate different physical
features, tailored for each test case, which affect the localization function.
The flow over a two-dimensional square cylinder at Re = 150 is the first case
investigated. It has been shown that the proposed localization procedure
leads to a more cost-effective DA process by reducing the size of the assim-
ilated regions while keeping the same level of accuracy. The capabilities of
the methodology are further demonstrated by the investigation of the turbu-
lent flow around a three-dimensional circular cylinder for Re = 3900. Again,
the methodology exhibits an excellent trade off in terms of accuracy versus
computational requirements.
Keywords:
DA, EnKF, localization, CFD, synchronization
1. Introduction
Applications of Data Assimilation (DA) [1, 2, 3] to fluid mechanics have
seen a rapid raise in the last decade [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15].
Preprint submitted to Journal of Computational Physics November 13, 2025

--- 第4页 ---
Thanks to the massive advancement in the availability of computational re-
sources and in the development of efficient numerical architectures, one of
the open challenges in the field is represented by the possibility to create dig-
ital twins [16, 17] of complex flow applications using numerical simulations.
In these applications, the numerical replica of the real flow would receive
streaming information of the latter obtained at localized sensors and, thanks
to its capacity to resolve large physical domain, would be able to produce
control techniques to anticipate or delay unwanted physical occurrences. Be-
cause of the relevance of such applications in numerous fields such as urban
and transport engineering, energy harvesting and pharmaceutical applica-
tions, research development for these technologies has seen a rapid increase
in recent times. DA tools are perfectly tailored for this kind of tasks, as
they are able to handle multiple streaming sources of information such as
predictions obtained by the physical and the digital twin. Works available in
the literature on this topic mainly deal with the usage of reduced order mod-
els (ROM) based on data-driven techniques [18] to perform the numerical
tasks of a digital twin [19]. While the computational cost required by ROM
is currently suitable for real-time investigation and coupling with physical
phenomena, their performance over long time window may diverge due to in-
trinsic structural limitations and to quality of the data used for the training.
The usage of high fidelity tools such as scale-resolving numerical simulation
is still prohibitive for the application to digital twins for two main reasons.
The first one is associated with the computational resources required to per-
form Direct Numerical Simulation (DNS) or Large Eddy Simulation (LES)
[20], which is prohibitively large at the present time. New paradigms in com-
putational sciences, such as quantum computing, may however change the
way calculations are performed in the foreseeable future. The second issue
is associated with the computational costs of Data Assimilation to handle
physical systems described by a large number of degrees of freedom (DOF).
While DA has been successfully used to perform flow synchronization [13]
and parametric optimization of the numerical model [21, 13, 14], which are
two cornerstones elements for efficient applications with digital twins, com-
putational costs can be prohibitive if the DA algorithm is applied to the
full physical domain. Some techniques of localization can be used to select
specific regions of application of the DA procedures, potentially reducing the
computational burdens required. Among these techniques, [22] have pub-
lished a localization algorithm referred to as hyperlocalization. This strategy,
which was developed for the Ensemble Kalman Filter (EnKF) [3], a well
2

--- 第5页 ---
known sequential DA algorithm, is able to reduce the computational require-
ment of more than 100 times with equivalent accuracy than classical DA
approaches. The technique consists in applying the DA procedure only in se-
lected region where important information is obtained by sensors. However,
the size of this region is somehow arbitrary and the shape of the region has
been selected to be spherical for practical reasons.
In the present work, the hyperlocalization strategies previously intro-
duced are augmented via infusion of the physical features of the flow. More
precisely, the DA regions are shaped according to physical criteria related
to the flow features observed in the region. The initial volume of such DA
region, which is set to be spherical, is modulated to an ellipsoid whose axes
and size are determined according to the physical criteria imposed. The
new technique, which will be referred to as physics-based online localization
(PBOL), is applied to investigate two unsteady test cases for external flows.
The main difference between the two applications is the Reynolds number of
investigation, which produces a laminar flow in the first case and a turbulent
regime in the second application. Different physical criteria are applied to
determine the size of the DA region for the two test cases, exploiting the
features of the flow.
The present article is structured as follows. In section 2, the details of
the numerical method for the solution of the governing equations are given,
along with the ensemble Kalman filter algorithm used for the data assim-
ilation stage and the various methods used for the localization of DA in
the literature. In section 3 the novel approach for the localization, namely
physics-based online-localization (PBOL), is introduced with a description of
the hyperlocalization methodology. In section 4, the results of the two test
cases are presented. Firstly the 2D flow around the square cylinder, for the
validation and the primary demonstration of the proposed PBOL method-
ology. Secondly the turbulent flow around 3D circular cylinder, where the
application of the PBOL methodology is carried out for a fully turbulent test
case. Finally, in section 5, the conclusions and final remarks are given.
2. Numerical methods and algorithms
This section is devoted to the presentation of the numerical tools used
in this work. This includes the CFD solvers to simulate the flow dynamics
as well as the state of the art DA algorithm, for which the physics-based
localization approach is incorporated.
3

```

---

## 方法/公式

```

--- 第6页 ---
2.1. Fluid state solver
The dynamic behavior of an incompressible, Newtonian fluid flow is de-
scribed by the continuity equation and the Navier-Stokes equations for mass
and momentum conservation,
∇ · u = 0, (1)
∂u
∂t + u∇u = −1
ρ ∇p + ν∇2u + fp, (2)
where u, p and ν are the velocity field, pressure field and the kinematic
viscosity of the fluid and fp is a volume forcing term. In this work, fp is
used to account for the presence of immersed solid bodies via the immersed
boundary method (IBM). A classical penalization approach [23] has been
used for the IBM where the forcing term is defined as
fp(x) =
(
−νD(u − ub), if x ∈ Ωb
0, otherwise
where Ω b stands for the volume of the solid body, ub is the velocity of this
immersed body i.e. ub = 0 if it is stationary, and D is a tensor contain-
ing penalty coefficients, which can be determined for the best compromise
between accuracy and the stability of the numerical solver [23].
Simulations are performed using the open-source, finite-volume platform
OpenFOAM [24] and the implementation of this IBM tool within the solver
used in the present study is detailed in the work by Valero and Meldi [14].
More precisely, the IBM is integrated in the PimpleFOAM solver, a seg-
regated solver where the velocity-pressure coupling is obtained using the
PIMPLE algorithm [24]. The calculations are performed using second order
centered discretization schemes for all the spatial derivatives, while the time
integration is carried out using the backward scheme, which is second order
accurate in time. Because of the relatively low Reynolds number Re of the
test cases analyzed and thanks to the grid refinement selected, no turbulence
modeling or subgrid-scale closure [20] is included in the numerical solvers.
2.2. Data assimilation: ensemble Kalman filter
Data Assimilation (DA) techniques are devoted to obtain an augmented
state estimation taking into account measurements and predictions coming
4

--- 第7页 ---
from different sources of information. For studies in fluid mechanics, classi-
cal applications combine results from a numerical model such as CFD with
available observation. The latter is usually supposed to provide high-fidelity
measurements which are however sparse or limited in the physical domain,
such as samples from sensors in experiments. DA methods can broadly be
categorized in variational and statistical approaches. Variational methods,
such as 3D-Var and 4D-Var originate from optimization theory and rely on
minimizing a cost function that quantifies the discrepancies between model
predictions and observations [1]. On the other hand statistical approaches,
including the Kalman filter (KF), particle filter, and ensemble Kalman filter
(EnKF), which are usually based on Bayesian inference [2]. These methods
not only integrate observation but also account for the uncertainties associ-
ated with both the model and the observation.
The EnKF is an ensemble version of the KF method which is particularly
efficient for applications dealing with high-dimensional, non-linear systems.
The EnKF methodology relies on two steps, namely the forecast and analysis
steps. The forecast step involves the evolution of the system states of the
ensemble members by the model equation while the analysis step produced
the augmented state via the assimilation of the observation and the model
prediction. One relevant feature of this approach is that uncertainties in
the state predicted by the model and in the observation can be rigorously
taken into account. The complete sequential DA process, which can integrate
several forecast-analysis steps, is shown in figure 1.
Let us consider Ne system state vectors ui with i ∈ [1, Ne], where Ne is
the number of ensemble members. These states are physical solutions of the
flow investigated and they are obtained via numerical simulation using the
model. The state vectors advanced in time from the time step k − 1 to k are:
uf
i,k = Mi,k:k−1 uf
i,k−1, (3)
where the superscript f denotes the forecast using the model and M stands
for the model equations i.e. for the present study, M is the numerical CFD
algorithm resolving the governing equations described in the section 2.1.
If observation is available at time k, an analysis phase can be performed
to obtain a DA state estimation. This state is then used to update the
ensemble members’ system states for the following forecast steps. The update
is affected by the discrepancy between the forecast and the observation, which
drives the structure and magnitude of the so called Kalman gain Kk. The
5

--- 第8页 ---
Figure 1: Scheme providing a qualitative representation of sequential DA using the EnKF.
state update performed during the analysis (superscript a) reads as:
ua
i,k = uf
i,k + Kk

yk − H(uf
i,k−1)

. (4)
Here yk is the observation vector at the time step k and H is a mathematical
operator used to project the model state to the observation space. The
Kalman gain governs the update of the system states and it accounts for
the level of confidence/uncertainty for each observation and for the forecast
system state vector. It is computed as
Kk = X f
k (Sk)T
Sk(Sk)T + Rk
−1
, (5)
with
X f
k = ui,k − ⟨uk⟩√Ne − 1 ,
Sk = si,k − ⟨sk⟩√Ne − 1 ,
(6)
where ⟨·⟩ is the ensemble average operation over the ensemble members. In
order to perform a consistent comparison between the ensemble of model
realization and observation, data sampled for the latter is perturbed by a
bounded Gaussian noise based on the covariance matrix of the measurement
6

--- 第9页 ---
error Rk to obtain an Ne set of values. This operation is performed at each
analysis stage k to obtain a well-posed mathematical problem.
One of the main advantages of the EnKF when compared with the KF
is that the error covariance matrix is not evolved explicitly in time but it
is obtained via a Monte-Carlo approach i.e. running a set of Ne ensemble
members with different initial system states (and/or parameters if present)
and sampling the distribution of their system states after the application of
the model equation, see eq. 3. This lower-rank approximation of the er-
ror covariance matrix is then computed from the statistics of the ensemble
distribution by using 6. While this procedure dramatically reduces the com-
putational costs, it is also responsible for drawbacks which will be discussed
in Sec. 2.3.
2.3. Localization
The approximation of the error covariance matrix performed in the EnKF
leads to important advantages when handling non-linear systems as it does
not need an adjoint model nor linearization procedures. On the other hand,
the number of ensemble members Ne that can be reasonable generated via
numerical applications is limited when dealing with numerical problems de-
scribed by a very large number of degrees of freedom, due to heavy com-
putational burden. The representation of the full error covariance matrix
of a very large, complex system using a limited number of snapshots (i.e.
ensemble members) leads to sampling errors [25, 26, 2]. The restricted size
of the ensemble pool leads to non-physical, long-distance correlations, which
can negatively impact the performance of the DA procedure [25, 27].
Several methods have been reported in the literature to reduce and control
these sources of error [2]. One well known technique is the physical localiza-
tion, which is based on the selection of a partition of the physical domain
where DA is applied. In the study of Houtekamer and Mitchell [26], mul-
tiple DA analyses are performed grouping available observation in batches.
The state update is performed sequentially summing up the contributions for
each batch. Similarly in Hunt et al. [27], multiple DA analyses are carried
out for each element of the grid used for the model forecast. In this case
not every available observation is used, but a limited subset is selected ac-
cording to criteria based on the distance of each sensor to the grid element.
This strategy is equivalent to a physical localization as the DA problem is
solved by subsets of observations and/or data points determined by physical
proximity. More recently, Zhang et al. [28] have presented a methodology
7

--- 第10页 ---
based on non-overlapping domain decomposition used for the partition of
the global EnKF problem into smaller regions, which acts as a physical lo-
calization mechanism, eliminating the non-physical correlations arising from
low-rank representation of the error covariance matrix. They employed total
variation regularization to account for the missing covariance information at
the decomposition boundaries, leading to an acceleration in convergence and
improvement of the accuracy of the inferred field.
Another family of strategies used to control sampling errors is known
as covariance localization. The localization is here achieved by the Schur
product of a localization function, with certain features e.g. Gaussian shape,
decaying to zero at a specified distance [25], with the error covariance ma-
trix. This procedure acts as a filter suppressing the non-physical correlations
appearing at long-distance separations[25, 26]. Classical applications set the
value for the localization function to the unity at the observation location.
The function then tends to zero with the increasing distance from the obser-
vation location, based on the expected decrease of the correlation value with
distance [26]. Because of the very large number of degrees of freedom simu-
lated by CFD approaches and the consequent large computational resources
required, localization is a key tool to improve DA stability and efficiency in
terms of accuracy versus costs.
2.4. CONES: Coupling OpenFOAM with numerical environments
A key element governing the DA efficiency when using CFD is related to
the possibility of performing multiple tasks in an online environment. The
EnKF is a sequential DA methodology, meaning that the DA step is carried
out whenever a new observation is available. Thus the DA procedure con-
sists of multiple DA cycles with forecast (model advancement using CFD)
and analysis steps (calculations using a DA software). If the Ne CFD sim-
ulations are stopped at the end of the forecast and restarted at the end of
the analysis phase, this can request prohibitive computational costs in terms
of writing output files and loading the computational grids and variables.
Therefore, the possibility to pause the CFD simulations while the DA code
is running represent a major advantage in terms of computational efficiency.
In the present work, the forecast step in eq. 3 is carried out by the Open-
FOAM algorithm. The analysis step for the computation of the corrected
state matrix ua
i,k is carried out by an independent DA algorithm, coded in
Python language and follows the procedure presented in algorithm 2.1. The
online coupling of the OpenFOAM code and the Python EnKF algorithm is
8

--- 第11页 ---
performed using the CONES library [21, 14] based on the message passing
interface (MPI) [29] and mpi4py [30] libraries.
Figure 2: Scheme representing the work environment of the library CONES used for DA
purposes.
As it can be seen in algorithm 2.1, the DA software starts by the initializa-
tion of the MPI environment and reading the inputs such as the OpenFOAM
grid information, initial parameters (if present) and DA hyperparameters.
After the preparation of the data-structure, the loop over the DA stages
starts for the index k = 0. The DA algorithm waits for the completion of the
forecast step carried out by the OpenFOAM and receives the forecast state
matrices of the ensemble members uf
i,k via CONES when they are ready.
The model samples in the observation space si,k = H(uf
i,k) are received from
each ensemble member along with the parameters Θ i,k if they are present.
With all the information from the ensemble members are now gathered, the
DA algorithm is performed while CFD simulations are paused. Observation
matrix, ensemble means, anomaly matrices, Kalman gain and localization
matrix are computed. Once the augmented state is obtained, the informa-
tion is sent back to the Ne simulations and physical states are updated. The
hold on the CFD simulations is removed and the DA code is paused as the
next forecast begins.
9

--- 第12页 ---
Algorithm 2.1: Algorithm for the Ensemble Kalman Filter (EnKF)
1 MPI initialize
2 Read grid info
3 Prepare objects containing EnKF & simulation parameters
4 Read clipping info from topoSet and construct DA regions data
structure
5 Read observation data and associate them with DA regions
for k = 1 to K do
6 Receive forecast state vectors from OpenFOAM simulations uf
i,k
7 Receive model sampling data si,k = H(uf
i,k)
for j = 1 to Nr do
8 Creation of an observation matrix from the observation data
by introducing observation errors:
yi,k = yk + ei,j, with ei,k ∼ N (0, Rk)
9 Calculation of the ensemble means:
⟨uf
j,k⟩ = 1
Ne
PNe
i=1 uf
i,j,k, ⟨sj,k⟩ = 1
Ne
PNe
i=1 si,j,k,
10 Calculation of the anomaly matrices:
X f
k = ui,k−⟨uk⟩√Ne−1 , Sk = si,k−⟨sk⟩√Ne−1 ,
11 Calculation of the Kalman gain:
Kk = X f
k (Sk)T
Sk(Sk)T + Rk
−1
12 (optional) Apply localization function:
K L
k = L ⊙ Kk
13 Update state matrix:
ua
i,k = uf
i,k + K L
k (yi,k − si,k)
14 Send analysis state vectors to OpenFOAM simulations xa
i,k
10

--- 第13页 ---
3. Hyperlocalization and Physics Based Online-localization
3.1. Hyperlocalization algorithm
Discussion in Sec. 2.3 highlighted how localization is important in terms
of numerical stability and computational efficiently. Recently, Villanueva
et al. [22] proposed a localization technique tailored for CFD applications,
which is referred to as hyperlocalization (HL). This technique is reminiscent
of the works by Hunt et al. [27] and Houtekamer and Mitchell [26] but, unlike
the latter, it is not inherently sequential but it can be performed in parallel.
This last point permits to accelerate the DA analysis procedure, therefore
providing improved efficiency in critical applications using CFD. For the HL
localization procedure, DA regions around sensors are identified as spherical
regions of radius rc as shown in figure 3. The usage of these regions for
DA purposes is justified by the assumption that in fluid flows, especially in
turbulent regimes, the correlation function of physical quantities between two
points decays rapidly with distance [20].
The definition of such zones permits to define NR DA zones, where the
number of degrees of freedom is limited and therefore the size of the matrices
in eq. 5 and eq. 6 is dramatically reduced. In addition, the resolution of the
NR analyses can be performed in parallel, therefore providing an additional
potential speed-up in computational costs. If sensors are relatively far from
another (i.e. the distance between them is larger than rc), then NR is both
the number of DA regions and of sensors. This is the case investigated in
the present analyses, which is chosen for sake of simplicity. However, if the
probes are close, one single DA region can cluster multiple sensors as shown
in fig. 3.
For the case of HL-based EnKF, the state update provided in eq. 4 is
recast in a parallel formulation where NR updates are performed:
ua
i,k = uf
i,k +
NRX
j=1
(Kk)[j]

(yi,k)[j] − (H(uf
i,k))[j]

. (7)
Here [j] indicates that calculations of the matrices used to perform the anal-
ysis step are calculated using the information obtained from the jth DA
region, as shown in the Algorithm 2.1. Therefore, the operations performed
for each [j] also include projections from and to the complete physical state
to the reduced state in each of the j DA regions. The process is repeated NR
times. It must be stressed (see fig. 3) that the DA regions are constructed so
11

--- 第14页 ---
Figure 3: Scheme representing DA regions selected for the hyperlocalization (HL) algo-
rithm.
that the contributions from each DA region j are independent of each other.
Therefore, the procedure can be written as the linear sum of the local DA
updates.
It was previously indicated that the HL localization technique works with
spherical regions described by a prescribed radius rc. Discontinuities of the
flow field at the surface of the region may appear due to the state update.
In order to avoid these discontinuities, covariance localization is used to ar-
tificially damp the state update term to zero in the proximity of the surface
of the DA region. This result is obtained pre-multiplying the Kalman Gain
by a localization matrix:
K L
j,k = Lj ⊙ Kj,k, (8)
where ⊙ stands for element-wise multiplication. Given that the current DA
methodology is developed for applications dealing with continuous physical
variables, a reasonable choice is to use a distance-based localization function
for covariance localization. For this reason, a normal distribution is used
following recommendation in the literature [2]:
L(xc) = exp(−1
2 [(xc − xo) /ξ]2), (9)
where L is the value of the localization function, xc is the location of the
model estimation i.e. the location where the localization function is evalu-
12

--- 第15页 ---
ated, and xo is the location of the probe for observation. The decay rate of
the localization function is determined by a length scale ξ. This parameter
is set so that the state elements of the localized Kalman gain K L
j,k tend to
zero in the proximity of the surface of the DA region, therefore adequately
smoothing the intensity of the state update [21, 13]. The value ofξ is constant
in time and it is set at the beginning of the DA procedure.
The HL procedure has been validated against classical EnKF without
localization for classical test cases such as a lid-driven cavity and a turbu-
lent plane channel flow, obtaining similar results in terms of accuracy [31].
However, due to the reduced number of degrees of freedom considered and
the possibility to easily parallelize the analysis step, computational resources
required are significantly reduced. An interesting point is that this cost re-
duction becomes proportionally more important for systems described by a
larger number of degrees of freedom, therefore showing potential for complex
flow applications of industrial interest.
3.2. Physics-based online localization
The main limitation of the initial proposal for the HL technique relies
on the geometric features of the DA regions. In fact, the shape (usually
spherical) and the size must be prescribed at the beginning of the DA run
and they cannot be changed during the process. While the choice of the
size, driven by the sphere radius rc, can be performed according to apriori
estimation of flow statistics, the geometry cannot adapt to instantaneous
variations of the features of the velocity and pressure fields. This constraint
does not exploit to its fullest the availability of data in a sequential DA
procedure such as the EnKF.
In the present study, a dynamic localization strategy is developed propos-
ing time variation of the geometric features of the DA regions. The method,
which will be referred to as physics-based online-localization (PBOL), identi-
fies the shape and size of the DA regions via observation of predicted flow fea-
tures by the ensemble realizations of the model. These flow features are used
to identify regions which respond to physical criteria selected by the users.
Therefore, this localization technique has the potential to infuse physical
knowledge of the flow to improve the efficiency of the DA method. One ap-
pealing characteristic is that, thanks to the sequential features of the EnKF,
shape modifications of the regions can be performed at each analysis phase.
Therefore, the PBOL technique can provide the means to perform a dynami-
cally changing DA process which adapts to the instantaneous features of the
13

```

---

## 实验/结果

```

--- 第41页 ---
(a) DA-HL
 (b) DA-PBOL
(c) DA-HL
 (d) DA-PBOL
Figure 17: Time variation of the CL and CD of the reference simulation, assimilated
members and their mean. Both DA-HL and DA-PBOL cases are run with the horizontal-
sparse configuration of the observation probes.
The sensitivity of the parameters characterizing the PBOL to the po-
sitioning of the sensor is now investigated. To this purpose, averages are
performed in the spanwise direction z, so that results are obtained for the
two plane for y = ±0.5D, x ∈ [0.55D, 10D]. The investigation is focused
on how local physical features of the flow affect the determination of such
model constants. Figure 19a shows the spanwise and time averaged angle θ
between the projection of ex′ vector on x − y plane and the streamwise unit
vector i along x-axis.
Circular averaging operation [39] is applied to find the time-averaged θ
values, θ, for a given DA region. Furthermore, by taking advantage of the the
spanwise homogeneity of the case, the θ values of DA regions are averaged
by circular mean for the DA regions sharing the same streamwise location.
The statistics are observed to be symmetric with respect to the y = 0 plane
for the upper and lower observation planes, as shown in figure 19a. In the
zone closer to the cylinder, for x < 3.5D, the parameter θ is affected by
the recirculation bubble forming behind the solid body. Moving downstream
in the streamwise direction, it can be seen that the orientation of ex′ and
therefore θ is mainly determined by the mean streamwise flow direction. It
39

--- 第42页 ---
(a) DA-HL
 (b) DA-PBOL
(c) DA-HL
 (d) DA-PBOL
Figure 18: Time variation of the discrepancy between the CL and CD of the reference
simulation, assimilated members and their mean. Both DA-HL and DA-PBOL cases are
run with the horizontal-sparse configuration of the observation probes.
can also be observed that the standard deviation of the parameter θ (shaded
region) is significantly higher in the regions affected by the separation in the
proximity of the cylinder, exhibiting a maximum value ofσθ = 83◦ for x/D =
0.6. The variation of θ reduces and becomes constant moving downstream in
the wake region. This shows that the instantaneous local convection velocity,
which dominates the local correlation field in the DA regions becomes more
similar to the mean streamwise velocity.
Figure 19b shows the mean and standard deviation of the ξx′/ξc where ξc
is the maximum value for ξx′, ξy′ and ξz′ which leads to L = 0.05 at r = rc.
The average ξx′/ξc value determined by the PBOL methodology is 0 .65 at
the streamwise location of x/D = 0.6, where the effects of the separation just
after the cylinder is still very effective. The mean value of ξx′/ξc increases
when going in the streamwise direction and it approaches to ξx′/ξc = 0 .8
and remains at that value after x/D ≈ 3. This means that the DA volumes
determined by the PBOL are smaller on average at the locations close to
the cylinder, when compared to downstream locations. Even though the
evolution of ξy′/ξc and ξz′/ξc remains qualitatively similar (see figures 19c
and 19d), it can also be observed that the mean values of ξz′/ξc remains
40

--- 第43页 ---
(a) Circular statistics of the orientation of ex′.
 (b) Mean and standard deviation of ξx′ /ξc.
(c) Mean and standard deviation of ξy′ /ξc.
 (d) Mean and standard deviation of ξz′ /ξc.
Figure 19: Statistics of the localization parameters for the PBOL case. (a) Mean value
and the standard deviation of θ, the angle between mean ex′ and the streamwise vector i,
and of of (b) ξx′/ξc, (c) ξy′/ξc, (d) ξz′/ξc along the streamwise direction.
lower than the ξx′/ξc and ξy′/ξc at all the streamwise locations. This shows
that the local velocity correlation lengths in z′ direction remains lower than
the other two directions in the downstream direction.
The standard deviations shown by the shaded regions in figures 19b,
19c and 19d, start with equal values for positive and negative sides of the
mean curve in the range x/D ⪅ 1 for ξx′/ξc, ξy′/ξc and x/D ⪅ 2 for ξz′/ξc.
For these streamwise locations, where the DA regions are located near the
recirculation zone, strongly unsteady motions are driven by the periodic flow
separation. The optimized DA regions are here relatively small on average,
with relatively large, positive and negative variations of the DA volume.
Similarly, a high variance is observed for the orientation of the primary axis
(see figure 19a). Going downstream, the tendency of having DA regions
larger than the average size gets lower after x/D ⪆ 2, while the tendency of
having smaller DA regions than the average size remains similar, manifested
by the unequal standard deviations at the upper/lower sides of the mean
curve.
Finally, a comparison is performed between the computational costs asso-
ciated with DA-HL and DA-PBOL methodologies, in order to highlight the
41

--- 第44页 ---
computational gains of the latter. The computational tasks to be performed
for the calculation of the Kalman gain for both cases are evaluated using the
relation [31],
CK = O(K) = O
"
NrN 3
o +
 NRX
i=1
NDOF,i + Ne + Nr
!
N 2
o + NDOF,i NeNo
#
,
(25)
where Nr is the number of DA regions, NDOF is the number of degrees of
freedom of each of those regions, Ne is the number of ensemble members
and No is the number of observations at each sensor e.g. No = 3 if the three
components of the velocity are observed. Figure 20 shows the ratios ofC P BOL
K
and C HL
K associated with the computational cost of PBOL, as a percentage
of the cost of HL. The cost is not evaluated here as a real computational
cost, but it is estimated by the eq. 25 and presented as a ratio of the both
cases. It can be emphasized here that the difference in the performance is
due to the variation of the NDOF values for the PBOL and HL procedures.
The computational cost of the HL remains constant during the investigation,
as the localization functions applied at each sensor do not change, thus the
volumes of DA regions remain same throughout the time. For the time
interval t/Tref ∈ [0, 60], one can see that the computational cost of the DA-
PBOL corresponds to around 33 .7% of the cost of DA-HL. Therefore, while
the calculation of physical quantities to select DA physical domains increases
complexity and calculations to be performed, the reduction of the global DA
space associated with PBOL localization more than balances that increase,
providing an efficient localization strategy tailored to the physical features
of the flow investigated.
5. Conclusion
This work presents a physics-based online-localization methodology, re-
ferred to as PBOL, for data assimilation by EnKF. The algorithm is de-
veloped for the applications of simulations of turbulent flows with complex
boundaries. Contrary to the more classical, distance-based covariance local-
ization scheme, a methodology where the localization function varies as a
function of the flow conditions in the vicinity of each observation probe is
proposed with the aim of conducting the DA only in the relevant regions i.e.
where the expected correlation with the observation data is significant. The
results from the synchronization test cases has been presented for both 2D
42

--- 第45页 ---
Figure 20: Computational cost of EnKF with the application of the PBOL as a percentage
of the cost of HL.
and 3D simulations of fluid flows, where the former being laminar, unsteady
and the latter being in fully turbulent regime.
The results from the 2D test case, the flow around a square cylinder, shows
a gain in the computational costs. The synchronization of the model achieved
rapidly, while the speed of convergence is observed to be affected highly by
the number of cells being assimilated. In the 3D test case, the PBOL is
applied for the synchronization of the flow around a circular cylinder. First,
the performance of the EnKF for the synchronization of the turbulent flow
simulations with various observation probe configurations are presented with
the HL methodology. Following that, the synchronization case is re-run,
using the PBOL methodology and the results are compared with the HL
case. The variation of the localization function in space and in time for
different DA regions are presented. It is shown that the statistics of the
localization parameters display their connection with the physics of the flow
e.g. the symmetry of the mean flow field with respect to the center-plane.
The synchronization performance remains similar when using PBOL and
HL methodologies, even though the DA regions are much more restricted
and the number of cells being assimilated are much lower with the former
with the choice of the optimal localization extent. Meanwhile, the collapse
of the ensemble member states are less dramatic when PBOL is utilized,
which grants an advantage for the convergence towards the reference state.
In addition to that, the computational cost for the DA stage is shown to
reduce significantly, down to 34% of the DA using HL strategy, thanks to
the dynamic choice of the optimal DA regions based on the physics of the
43

--- 第46页 ---
problem.
Future development will deal with more general formulation of the PBOL
method, in order to prescribe arbitrary shapes of the DA regions containing
potentially multiple sensors. In addition, the possibility to automatize the
choice of the physical constraints by machine learning will be investigated.
This last point will permit to exploit the potential of artificial intelligence to
reduce human supervision in the process and to recognize the best physical
criteria to be selected according to the case of investigation.
6. Acknowledgments
This research activity was performed in the framework of the project ANR
JCJC-2021 IWP-IBM-DA. Numerical computations were performed using
resources by GENCI at the TGCC supercomputer obtained via the grant
2023-A0142A01741 on the supercomputer Joliot Curie’s SKL partition.
References
[1] S. B. Daley, Atmospheric Data Analysis, Cambridge University Press,
1991.
[2] M. Asch, M. Bocquet, M. Nodet, Data Assimilation, Society for Indus-
trial and Applied Mathematics, 2016. doi: 10.1137/1.9781611974546.
[3] G. Evensen, F. C. Vossepoel, P. J. van Leeuwen, Data Assimilation
Fundamentals, Springer Nature, 2022.
[4] T. Suzuki, Reduced-order Kalman-filtered hybrid simulation combining
particle tracking velocimetry and direct numerical simulation, Journal
of Fluid Mechanics 709 (2012) 249 – 288.
[5] M. C. Rochoux, S. Ricci, D. Lucor, B. Cuenot, A. Trouve, Towards
predictive data-driven simulations of wildfire spread - Part I: Reduced-
cost Ensemble Kalman Filter based on a Polynomial Chaos surrogate
model for parameter estimation, Natural Hazards and Earth System
Sciences 14 (2015) 2951–2973.
[6] V. Mons, J. C. Chassaing, T. Gomez, P. Sagaut, Reconstruction of un-
steady viscous flows using data assimilation schemes, Journal of Compu-
tational Physics 316 (2016) 255–280. doi:10.1016/j.jcp.2016.04.022.
44

--- 第47页 ---
[7] M. Meldi, A. Poux, A reduced order model based on Kalman Filtering
for sequential Data Assimilation of turbulent flows, Journal of Compu-
tational Physics 347 (2017) 207–234.
[8] X. Zhang, C. Michelin-Str¨ ofer, H. Xiao, Regularized ensemble Kalman
methods for inverse problems, Journal of Computational Physics 416
(2020) 109517.
[9] P. Chandramouli, E. Memin, D. Heitz, 4D large scale variational data
assimilation of a turbulent flow with a dynamics error model, Journal
of Computational Physics 412 (2020) 109446.
[10] V. Mons, Y. Du, T. Zaki, Ensemble-variational assimilation of sta-
tistical data in large-eddy simulation ensemble-variational assimilation
of statistical data in large eddy simulation, Physical Review Fluids
6 (2021). URL: https://hal.science/hal-03585763. doi: 10.1103/
PhysRevFluids.6.104607.
[11] D. De Marinis, D. Obrist, Data assimilation by stochastic ensemble
kalman filtering to enhance turbulent cardiovascular flow data from
under-resolved observations, Frontiers in Cardiovascular Medicine 8
(2021) 742110.
[12] R. Zhao, S. Liu, J. Lie, N. Jiang, Q. Chen, Generalizability evaluation of
k-epsilon models calibrated by using ensemble kalman filtering for urban
airflow and airborne contaminant dispersion, Building and Environment
212 (2022) 108823.
[13] L. Villanueva, K. Truffin, M. Meldi, Synchronization and optimiza-
tion of large eddy simulation using an online ensemble kalman fil-
ter, International Journal of Heat and Fluid Flow 110 (2024) 109597.
doi:10.1016/j.ijheatfluidflow.2024.109597.
[14] M. M. Valero, M. Meldi, An immersed boundary method using on-
line sequential data assimilation, Journal of Computational Physics 524
(2025). doi:10.1016/j.jcp.2024.113697.
[15] P. Pillai, A. Hetherington, L. Saavedra, S. Le Clainche, A low-cost sin-
gular value decomposition-based data assimilation technique for analysis
of heterogeneous combustion data, Physics of Fluids 37 (2025) 085165.
45

--- 第48页 ---
[16] C. Semeraro, M. Lezoche, H. Panetto, M. Dassisti, Digital twin
paradigm: A systematic literature review, Computers in Industry 130
(2021) 103469.
[17] A. Rasheed, O. San, T. Kvamsdal, Digital Twin: Values, Challenges and
Enablers From a Modeling Perspective, IEEE Access 8 (2020) 21980–
22012.
[18] S. L. Brunton, B. R. Noack, P. Koumoutsakos, Machine learning for
fluid mechanics, Annual Review of Fluid Mechanics 52 (2020) 477–508.
[19] L. Donato, C. Galletti, A. Parente, Self-updating digital twin of
a hydrogen-powered furnace using data assimilation, Applied Ther-
mal Engineering 236 (2024) 121431. doi: https://doi.org/10.1016/j.
applthermaleng.2023.121431.
[20] S. B. Pope, Turbulent flows, Cambridge University Press, 2000.
[21] L. Villanueva, M. Valero, A. ˇSarki´ c Glumac, M. Meldi, Augmented
state estimation of urban settings using on-the-fly sequential data as-
similation, Computers & Fluids 269 (2024) 106118. doi: 10.1016/j.
compfluid.2023.106118.
[22] L. Villanueva, K. Truffin, J. Bor´ ee, M. Meldi, Enhancement of
large eddy simulation for the prediction of an intake flow rig us-
ing sequential data assimilation, Journal of Fluid Mechanics (2025).
URL: acceptedforpublication,preprintathttp://arxiv.org/abs/
2503.14977.
[23] P. Angot, C.-H. Bruneau, P. Fabrie, A penalization method to take into
account obstacles in incompressible viscous flows, Numerische Mathe-
matik 81 (1999) 497–520. doi: 10.1007/s002110050401.
[24] OpenFOAM Foundation, OpenFoam, OpenFOAM Foundation,
https://doc.cfd.direct/openfoam/user-guide-v9/, 2018.
[25] T. M. Hamill, J. S. Whitaker, C. Snyder, Distance-dependent filtering
of background error covariance estimates in an ensemble kalman filter,
Monthly Weather Review 129 (2001) 2776–2790. URL: https://doi.
org/10.1175/1520-0493(2001)129%3C2776:DDFOBE%3E2.0.CO;2.
46

--- 第49页 ---
[26] P. L. Houtekamer, H. L. Mitchell, A sequential ensemble kalman fil-
ter for atmospheric data assimilation, Monthly Weather Review 129
(2001) 123–137. URL: https://doi.org/10.1175/1520-0493(2001)
129%3C0123:ASEKFF%3E2.0.CO;2.
[27] B. R. Hunt, E. J. Kostelich, I. Szunyogh, Efficient data assimilation for
spatiotemporal chaos: A local ensemble transform kalman filter, Physica
D: Nonlinear Phenomena 230 (2007) 112–126. doi: 10.1016/j.physd.
2006.11.008.
[28] X. L. Zhang, L. Zhang, G. He, Parallel ensemble kalman method with
total variation regularization for large-scale field inversion, Journal of
Computational Physics 509 (2024). doi: 10.1016/j.jcp.2024.113059.
[29] Message Passing Interface Forum, MPI: A Message-Passing Interface
Standard Version 4.1, 2023. URL: https://www.mpi-forum.org/docs/
mpi-4.1/mpi41-report.pdf.
[30] L. Dalc´ ın, R. Paz, M. Storti, Mpi for python, Journal of Parallel and Dis-
tributed Computing 65 (2005) 1108–1115. doi: https://doi.org/10.
1016/j.jpdc.2005.03.010.
[31] L. Villanueva, D´ eveloppement d’outils d’assimilation de donn´ ees pour
l’estimation augment´ ee d’´ ecoulements internes, Ph.D. thesis, ISAE-
ENSMA Ecole Nationale Sup´ erieure de M´ ecanique et d’A´ erotechique,
2024. URL: https://theses.hal.science/tel-04833774v1.
[32] A. Sohankar, C. Norberg, L. Davidson, Low-reynolds-number flow
around a square cylinder at incidence: study of blockage, on-
set of vortex shedding and outlet boundary condition, Interna-
tional Journal for Numerical Methods in Fluids 26 (1998) 39–56.
URL: https://doi.org/10.1002/(SICI)1097-0363(19980115)26:1%
3C39::AID-FLD623%3E3.0.CO;2-P.
[33] A. Sohankar, C. Norberg, L. Davidson, Simulation of three-dimensional
flow around a square cylinder at moderate reynolds numbers, Physics
of Fluids 11 (1999) 288–306. doi: 10.1063/1.869879.
[34] A. Saha, G. Biswas, K. Muralidhar, Three-dimensional study of flow
past a square cylinder at low reynolds numbers, International Journal
47

--- 第50页 ---
of Heat and Fluid Flow 24 (2003) 54–66. doi: 10.1016/S0142-727X(02)
00208-4.
[35] M. Breuer, J. Bernsdorf, T. Zeiser, F. Durst, Accurate computations of
the laminar flow past a square cylinder based on two different methods:
lattice-boltzmann and finite-volume, International Journal of Heat and
Fluid Flow 21 (2000) 186–196. doi: 10.1016/S0142-727X(99)00081-8.
[36] X. Ma, G. S. Karamanos, G. E. Karniadakis, Dynamics and low-
dimensionality of a turbulent near wake, Journal of Fluid Mechanics
410 (2000) 29–65. doi: 10.1017/S0022112099007934.
[37] J. Franke, W. Frank, Large eddy simulation of the flow past a circular
cylinder at red=3900, Journal of Wind Engineering and Industrial Aero-
dynamics 90 (2002) 1191–1206. doi: 10.1016/S0167-6105(02)00232-5.
[38] F. A. Portela, G. Papadakis, J. C. Vassilicos, The turbulence cascade in
the near wake of a square prism, Journal of Fluid Mechanics 825 (2017)
315–352. doi:10.1017/jfm.2017.390.
[39] K. V. Mardia, P. E. Jupp, Directional Statistics, Wiley, 1999. doi: 10.
1002/9780470316979.
48

```

---

