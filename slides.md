% title: Linear optimization in Python
% subtitle: or, search absurdly large spaces using this one weird trick
% author: Miles Gould
% author: Hogarth Worldwide
% thankyou: Thanks everyone!
% contact: <a href="http://pozorvlak.dreamwidth.org/">blog</a>
% contact: <a href="http://github.com/pozorvlak">github</a>
% contact: <a href="http://twitter.com/pozorvlak">twitter</a>
% favicon: http://www.stanford.edu/favicon.ico

---
title: Objectives
build_lists: true

- What is linear programming?
- When is it useful?
- How can I use it?
- How does it work?
- How efficient is it?

---
title: Optimization

"Find the values of a, b, c... such that f(a, b, c, ...) is as big as possible, subject to constraints on a, b, c..."

---
title: Huh?
build_lists: true

- Let's try an example!

---
title: Optimal farming

- I have 100ha of fields and 400 bags of fertilizer
- I can plant rice or barley
- 1ha of barley sells for €300, uses 5 bags
- 1ha of rice sells for €250, uses 3 bags
- how can I maximize my profit?

---
title: Optimal farming

> “Mathematicians are like Frenchmen: whatever you say to them they translate into their own language and forthwith it is something entirely different.”

> ― Johann Wolfgang von Goethe

---
title: Optimal farming
subtitle: Now with ADDED MATHS!

- Maximize `300 * barley + 250 * rice`
- `barley + rice <= 100`
- `5 * barley + 3 * rice <= 400`
- This is **linear**

---
title: Linear programs
build_lists: true

- Given variables $X_0, X_1, \ldots, X_n$
- Minimize (or maximize!) $c_0 X_0 + c_1 X_1 + \ldots + c_n X_n$
- Subject to constraints
$$
a_{00} X_0 + \ldots + a_{0n} X_n <= b_0 \\
\vdots \\
a_{m0} X_0 + \ldots + a_{mn} X_n <= b_m \\
$$

---
title: Let's write some code!

<pre class="prettyprint" data-lang="python">
from pulp import *
</pre>

---
title: Let's write some code!

<pre class="prettyprint" data-lang="python">
from pulp import *

<b>prob = LpProblem("Farmer", LpMaximize)

barley = LpVariable("barley", 0, None)
rice = LpVariable("rice", 0, None)</b>
</pre>

---
title: Let's write some code!

<pre class="prettyprint" data-lang="python">
from pulp import *

prob = LpProblem("Farmer", LpMaximize)

barley = LpVariable("barley", 0, None)
rice = LpVariable("rice", 0, None)

<b>prob += 300 * barley + 250 * rice, "money for selling grain"
prob += barley + rice &lt;= 100, "total size of fields"
prob += 5 * barley + 3 * rice &lt;= 400, "available fertilizer"</b>
</pre>

---
title: Let's write some code!

<pre class="prettyprint" data-lang="python">
from pulp import *

prob = LpProblem("Farmer", LpMaximize)

barley = LpVariable("barley", 0, None)
rice = LpVariable("rice", 0, None)

prob += 300 * barley + 250 * rice, "money for selling grain"
prob += barley + rice &lt;= 100, "total size of fields"
prob += 5 * barley + 3 * rice &lt;= 400, "available fertilizer"

<b>prob.solve()</b>

print("Status:", LpStatus[prob.status])
for v in prob.variables():
    print(v.name, "=", v.varValue)
print("Total income = ", value(prob.objective))
</pre>

---
title: Live demo!

---
title: More examples!
build_lists: true

- Transport problem
<img src=figures/transport_problem.svg height=200 />
- [Diet problem](https://developers.google.com/optimization/lp/glop)
- Fitting curves to data

--
title: Integer linear programming
class: segue dark nobackground

---
title: Election fever
build_lists: true

- We just had an election
- [Let's pretend we have PR...]
- CON expect 239.38 seats
- er...
- Can we use LPs?

---
title: Election fever
subtitle: LPs to the rescue!

<pre class="prettyprint" data-lang="python">
for party in parties:
    seats = LpVariable("{}_seats".format(party), 0, 650, <b>LpInteger</b>)
</pre>

---
title: Election fever
subtitle: Handling absolute values

<pre class="prettyprint" data-lang="python">
for party in parties:
    seats = LpVariable("{}_seats".format(party), 0, 650, LpInteger)
    <b>bound = LpVariable("{}_bound".format(party), 0, 1)</b>
    diff = seats - expected[party]
    <b>prob += diff <= bound
    prob += -diff <= bound</b>
</pre>

---
title: Election fever

<pre class="prettyprint" data-lang="python">
for party in parties:
    seats = LpVariable("{}_seats".format(party), 0, 650, LpInteger)
    bound = LpVariable("{}_bound".format(party), 0, 1)
    diff = seats - expected[party]
    prob += diff <= bound
    prob += -diff <= bound
    bounds.append(bound)
    seat_vars[party] = seats

<b>prob += lpSum(seat_vars.values()) == 650
prob += lpSum(bounds)</b>
</pre>

---
title: Election fever
subtitle: Live demo!

---
title: Boolean formulae
build_lists: true

- Take a long boolean formula, say
<pre>a and (b or (c and d)) and (e and f)</pre>
- Can we find `a, b, c, d, e, f` to make it true?
- First, convert to conjunctive normal form:
<pre>a and (b or c) and (b or d) and e and f</pre>

---
title: Boolean formulae

<pre>a and (b or c) and (b or d) and e and f</pre>
- One integer variable per input (0 = false, 1 = true)
- One constraint per disjunction:
$$
a >= 1 \\
b + c >= 1 \\
b + d >= 1 \\
e >= 1 \\
f >= 1$$
 - Any objective we like

---
title: Oh dear

We've just sketched out a SAT solver.

---
title: NP-completeness
subtitle: I used to be like
class: img-top-center

<img src=figures/game_over_man.jpg />

---
title: NP-completeness
subtitle: But now I'm like
class: img-top-center

<img src=figures/morpheus.gif />

---
title: A performance investigation

Find $k$ numbers from $1, \ldots, n$ such that

 - none divides any other
 - their sum is as small as possible

---
title: Live demo!

---
title: Here's one I prepared earlier

<pre class="prettyprint" data-lang="shell">
(linprog_pypy3)miles@ended:~/src/linprog_talk/k_from_n 22:53  master 
0 $ time ./recursive.py 100 200
^CTraceback (most recent call last):
  File "./recursive.py", line 16, in <module>
    answer = best(int(sys.argv[1]), range(1, int(sys.argv[2]) + 1))
  File "./recursive.py", line 14, in best
    return best(k, tail)
<i>Many lines of stack trace...</i>
  File "./recursive.py", line 11, in <listcomp>
    with_head = best(k - 1, [o for o in tail if o % head != 0])
KeyboardInterrupt

real    8188m52.074s
user    8023m13.082s
sys     0m15.560s
</pre>

---
title: Takeaways
build_lists: true

- Linear programs are everywhere
- LP solvers are easy to use
- Often much more efficient than hand-rolled code
- NP-completeness != game over

---
title: Python LP libraries
subtitle: High-level

 - [PuLP](http://pythonhosted.org//PuLP/)
 - [Pyomo](https://software.sandia.gov/downloads/pub/pyomo/PyomoOnlineDocs.html)
 - [or-tools](https://developers.google.com/optimization/)
 - [optlang](https://pypi.python.org/pypi/optlang/0.2.6)

---
title: Python LP libraries
subtitle: Lower-level

 - [ecyglpki](https://pypi.python.org/pypi/ecyglpki/0.2.0)
 - [swiglpk](https://pypi.python.org/pypi/swiglpk)
 - [ctypes-glpk](https://code.google.com/p/ctypes-glpk/)
 - [lpsolve55](http://lpsolve.sourceforge.net/5.5/Python.htm#Install_the_lpsolve_driver)
 - [pycplex](http://www.cs.toronto.edu/~darius/software/pycplex/)
 - [cylp](https://pypi.python.org/pypi/cylp/0.7.3-)

---
title: Nonlinear programming libraries

 - [cvxopt](http://cvxopt.org/)
 - [tango](https://pypi.python.org/pypi/TANGO-Project---ALGENCAN/1.0)
 - [optlang](https://pypi.python.org/pypi/optlang/0.2.6)
 - [PyLMI](https://pypi.python.org/pypi/PyLMI-SDP/0.2)
 - [scipy.optimize](http://docs.scipy.org/doc/scipy/reference/optimize.html)

---
title: Further study

- https://www.coursera.org/course/linearprogramming
- http://en.wikipedia.org/wiki/Linear_programming
