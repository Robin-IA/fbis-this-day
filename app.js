// FBIS This Day. Shows the entry for the visitor's local date and switches
// to the next one at local midnight. ?d=MM-DD pins a day (shareable link).
(function () {
  "use strict";
  var MONTHS = ["January", "February", "March", "April", "May", "June", "July",
    "August", "September", "October", "November", "December"];
  var DAYS_IN = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
  var CATEGORY = {
    "espionage": "Espionage", "defection": "Defection", "covert-action": "Covert action",
    "coup": "Coup", "assassination": "Assassination", "terrorism": "Terrorism",
    "hostage": "Hostage-taking", "war": "War", "crisis": "Crisis", "diplomacy": "Diplomacy",
    "uprising": "Uprising", "disaster": "Disaster", "politics": "Politics"
  };
  var REGIONS = {};
  var $ = function (id) { return document.getElementById(id); };
  var pinned = null;      // MM-DD from the URL, or null to follow the clock
  var shown = null;       // MM-DD currently on screen
  var midnightTimer = null;

  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function todayMd() { var d = new Date(); return pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function label(md) { var p = md.split("-"); return +p[1] + " " + MONTHS[+p[0] - 1]; }
  function shortLabel(md) { var p = md.split("-"); return +p[1] + " " + MONTHS[+p[0] - 1].slice(0, 3); }
  function validMd(md) {
    var m = /^(\d\d)-(\d\d)$/.exec(md || "");
    return !!m && +m[1] >= 1 && +m[1] <= 12 && +m[2] >= 1 && +m[2] <= DAYS_IN[+m[1] - 1];
  }
  function shift(md, by) { // walk a 366-day year, so 02-29 is its own stop
    var p = md.split("-"), m = +p[0] - 1, d = +p[1] + by;
    if (d < 1) { m = (m + 11) % 12; d = DAYS_IN[m]; }
    if (d > DAYS_IN[m]) { m = (m + 1) % 12; d = 1; }
    return pad(m + 1) + "-" + pad(d);
  }
  function longDate(iso) {
    var p = iso.split("-");
    return +p[2] + " " + MONTHS[+p[1] - 1] + " " + p[0];
  }
  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function el(tag, attrs, html) {
    var e = document.createElement(tag);
    for (var k in attrs || {}) e.setAttribute(k, attrs[k]);
    if (html != null) e.innerHTML = html;
    return e;
  }
  function itemUrl(id) { return "https://archive.org/details/" + encodeURIComponent(id); }
  function pageUrl(ev) { return itemUrl(ev.identifier) + "/page/n" + ev.page + "/mode/1up"; }

  function evidenceHtml(ev) {
    return '<div class="evidence">' +
      '<p class="src">Found on page ' + (ev.page + 1) + ' of <a href="' + pageUrl(ev) + '">' + esc(ev.title) + "</a>" +
      (ev.contents_only ? " (in its list of contents)" : "") + ".</p>" +
      "<blockquote>" + esc(ev.snippet) + "</blockquote>" +
      '<p class="ocrnote">Machine-read text from the microfiche scan, uncorrected.</p></div>';
  }

  function renderSheet(md, data) {
    var s = $("sheet"), e = data.pick;
    s.setAttribute("aria-busy", "false");
    if (!e) {
      s.innerHTML = '<div class="dateline"><p class="bigdate">' + esc(label(md)) + "</p></div>" +
        '<p class="empty">No entry has been written for this day yet. The Daily Reports dated ' +
        esc(label(md)) + " are listed below.</p>";
      return;
    }
    var ev = e.evidence;
    s.innerHTML =
      '<div class="dateline"><p class="bigdate">' + esc(label(md)) + '</p><span class="year">' + esc(e.date.slice(0, 4)) + "</span>" +
      (e.spycraft ? '<span class="stamp">Spycraft</span>' : "") +
      (e.category ? '<span class="tag">' + esc(CATEGORY[e.category] || e.category) + "</span>" : "") + "</div>" +
      "<h2>" + esc(e.headline) + "</h2>" +
      "<p>" + esc(e.summary) + "</p>" +
      "<h3>Why it mattered</h3><p>" + esc(e.significance) + "</p>" +
      "<h3>What FBIS heard</h3>" + (e.fbis ? "<p>" + esc(e.fbis) + "</p>" : "") +
      evidenceHtml(ev) +
      '<a class="cta" href="' + pageUrl(ev) + '">Read the ' + esc(longDate(ev.issue_date)) + " Daily Report</a>" +
      '<p class="draft">Draft entry. The event, its date and its context were written with AI assistance (Claude) and checked against the text of this Daily Report, but have not yet been reviewed by a historian. ' +
      '<a href="about.html#method">How entries are made</a>.</p>';
  }

  function renderAlts(data) {
    var ul = $("alts"); ul.innerHTML = "";
    $("altsSection").hidden = !data.alternates.length;
    data.alternates.forEach(function (e) {
      var li = el("li");
      li.innerHTML = '<span class="y">' + esc(e.date.slice(0, 4)) + "</span><strong>" + esc(e.headline) + "</strong>" +
        (e.spycraft ? ' <span class="stamp">Spycraft</span>' : "") +
        "<p>" + esc(e.summary) + "</p>" +
        "<details><summary>Why it mattered, and the report</summary><p>" + esc(e.significance) + "</p>" +
        (e.fbis ? "<p>" + esc(e.fbis) + "</p>" : "") + evidenceHtml(e.evidence) + "</details>";
      ul.appendChild(li);
    });
  }

  function renderIssues(md, data) {
    $("issuesDay").textContent = label(md);
    var byYear = {};
    data.issues.forEach(function (r) { (byYear[r[1].slice(0, 4)] = byYear[r[1].slice(0, 4)] || []).push(r); });
    var years = Object.keys(byYear).sort();
    $("issuesNote").textContent = data.issues.length
      ? data.issues.length + " issues in " + years.length + " years, by year and region."
      : "No Daily Report in the collection is dated " + label(md) + " (FBIS did not publish on some holidays).";
    var box = $("issues"); box.innerHTML = "";
    years.forEach(function (y) {
      var d = el("details");
      d.appendChild(el("summary", null, esc(y) + " · " + byYear[y].length + " issue" + (byYear[y].length > 1 ? "s" : "")));
      var ul = el("ul");
      byYear[y].forEach(function (r) {
        ul.appendChild(el("li", null, '<a href="' + itemUrl(r[0]) + '">' + esc(r[3]) + "</a>" +
          ' <span class="reg">· ' + esc(REGIONS[r[2]] || r[2]) + "</span>"));
      });
      d.appendChild(ul);
      box.appendChild(d);
    });
  }

  function syncControls(md) {
    var p = md.split("-");
    $("month").value = String(+p[0]);
    fillDays(+p[0]);
    $("day").value = String(+p[1]);
    $("prevLabel").textContent = shortLabel(shift(md, -1));
    $("nextLabel").textContent = shortLabel(shift(md, 1));
    $("today").hidden = md === todayMd() && !pinned;
  }

  function show(md, push) {
    if (!validMd(md)) md = todayMd();
    shown = md;
    syncControls(md);
    if (push) {
      var url = md === todayMd() && !pinned ? location.pathname : "?d=" + md;
      history.pushState({ md: md }, "", url);
    }
    document.title = "FBIS This Day: " + label(md);
    $("sheet").setAttribute("aria-busy", "true");
    fetch("data/days/" + md + ".json").then(function (r) {
      if (!r.ok) throw new Error(r.status);
      return r.json();
    }).then(function (data) {
      if (md !== shown) return;
      renderSheet(md, data); renderAlts(data); renderIssues(md, data);
    }).catch(function () {
      $("sheet").innerHTML = '<p class="empty">This day\'s file could not be loaded. Try reloading the page.</p>';
    });
  }

  // At local midnight, move to the new day unless the visitor pinned one.
  function scheduleMidnight() {
    clearTimeout(midnightTimer);
    var now = new Date(), next = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1, 0, 0, 5);
    midnightTimer = setTimeout(function () {
      if (!pinned) show(todayMd(), false);
      scheduleMidnight();
    }, next - now);
  }
  // Timers sleep with the laptop; catch up when the tab comes back.
  document.addEventListener("visibilitychange", function () {
    if (!document.hidden && !pinned && shown !== todayMd()) show(todayMd(), false);
    if (!document.hidden) scheduleMidnight();
  });

  function fillDays(m) {
    var sel = $("day"), cur = sel.value;
    sel.innerHTML = "";
    for (var d = 1; d <= DAYS_IN[m - 1]; d++) sel.appendChild(el("option", { value: String(d) }, String(d)));
    if (cur && +cur <= DAYS_IN[m - 1]) sel.value = cur;
  }
  function go(md) { pinned = md === todayMd() ? null : md; show(md, true); }

  MONTHS.forEach(function (name, i) { $("month").appendChild(el("option", { value: String(i + 1) }, name)); });
  $("month").addEventListener("change", function () { fillDays(+this.value); go(pad(+this.value) + "-" + pad(+$("day").value)); });
  $("day").addEventListener("change", function () { go(pad(+$("month").value) + "-" + pad(+this.value)); });
  $("prev").addEventListener("click", function () { go(shift(shown, -1)); });
  $("next").addEventListener("click", function () { go(shift(shown, 1)); });
  $("today").addEventListener("click", function () { pinned = null; show(todayMd(), true); });
  window.addEventListener("popstate", function () { start(false); });

  function start(push) {
    var q = new URLSearchParams(location.search).get("d");
    pinned = validMd(q) ? q : null;
    show(pinned || todayMd(), push);
  }
  fetch("data/regions.json").then(function (r) { return r.json(); }).catch(function () { return {}; })
    .then(function (r) { REGIONS = r; start(false); scheduleMidnight(); });
})();
