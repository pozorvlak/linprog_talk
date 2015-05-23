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
Or in other words...

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

