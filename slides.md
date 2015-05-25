% title: Linear optimization in Python
% subtitle: or, search absurdly large spaces using this one weird trick
% author: Miles Gould
% author: Hogarth Worldwide
% thankyou: Thanks everyone!
% thankyou_details: And especially these people:
% contact: <span>www</span> <a href="http://pozorvlak.dreamwidth.org/">website</a>
% contact: <span>github</span> <a href="http://github.com/pozorvlak">pozorvlak</a>
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
- Diet problem
- Fitting curves to data (XXX)

---
title: Interlude
subtitle: How does it work?
class: segue dark nobackground

---
title: The simplex algorithm

XXX diagram here

---
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
title: Chip layouts

XXX picture goes here

---
title: Boolean formulae
build_lists: true

- Take a long boolean formula, eg <pre>a && (b || (c && d)) && (e && f)</pre>
- Can we find <pre>a, b, c, d, e, f</pre> to make it true?
- one integer variable per input (0 = false, 1 = true)
- XXX look up how this actually works!

---
title: NP-completeness
subtitle: I used to be like
class: img-top-center

<img height=150 src=figures/game_over_man.jpg />

---
title: NP-completeness
subtitle: But now I'm like
class: img-top-center

<img height=150 src=figures/morpheus.gif />

---
title: A performance investigation

Find $k$ numbers from $1, \ldots, n$ such that

 - none divides any other
 - their sum is as small as possible

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
title: Python LP libraries
subtitle: High-level

 - [PuLP](http://pythonhosted.org//PuLP/)
 - [pyglpk](http://tfinley.net/software/pyglpk/)
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
