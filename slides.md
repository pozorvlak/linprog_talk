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

Here is a list that should build:

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
a_00 X_0 + \ldots + \a_0n X_n <= b_0
\vdots
a_m0 X_0 + \ldots + \a_mn X_n <= b_m
$$

---
title: Let's write some code!

<pre class="prettyprint" data-lang="python">
from pulp import *
<pre>

---
title: Let's write some code!

<pre class="prettyprint" data-lang="python">
from pulp import *

<b>prob = LpProblem("Farmer", LpMaximize)

barley = LpVariable("barley", 0, None)
rice = LpVariable("rice", 0, None)</b>
<pre>

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
prob.writeMPS("farmer.mps")
prob.solve()

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

How does it work?

XXX diagram here

---
title: Integer variables
build_lists: true

- We just had an election
- [Let's pretend we have PR...]
- CON expect 239.38 seats
- er...
- Can we use LPs?

---
title: LPs to the rescue!

<pre class="prettyprint" data-lang="python">
for party in parties:
    seats = LpVariable("{}_seats".format(party), 0, 650, <b>LpInteger</b>)
<pre>

---
title: Handling absolute values

<pre class="prettyprint" data-lang="python">
for party in parties:
    seats = LpVariable("{}_seats".format(party), 0, 650, LpInteger)
    <b>bound = LpVariable("{}_bound".format(party), 0, 650)</b>
    diff = seats - expected[party]
    <b>prob += diff <= bound
    prob += -diff <= bound</b>
</pre>

---
title: Slide with a figure
subtitle: Subtitles are cool too
class: img-top-center

<img height=150 src=figures/200px-6n-graf.svg.png />

- Some point to make about about this figure from wikipedia
- This slide has a class that was defined in theme/css/custom.css

<footer class="source"> Always cite your sources! </footer>

---
title: Segue slide
subtitle: I can haz subtitlz?
class: segue dark nobackground

---
title: Maybe some code?

press 'h' to highlight an important section (that is highlighted
with &lt;b&gt;...&lt;/b&gt; tags)

<pre class="prettyprint" data-lang="javascript">
function isSmall() {
  return window.matchMedia("(min-device-width: ???)").matches;
}

<b>function hasTouch() {
  return Modernizr.touch;
}</b>

function detectFormFactor() {
  var device = DESKTOP;
  if (hasTouch()) {
    device = isSmall() ? PHONE : TABLET;
  }
  return device;
}
</pre>

