/* modelpoisoning.com: source checker.
   Compares domains against VIGINUM's published lists. Everything runs in the browser;
   the lists come from this site and nothing the visitor pastes is sent anywhere. */
(function () {
  "use strict";

  var root = document.getElementById("source-checker");
  var dataEl = document.getElementById("source-checker-i18n");
  if (!root || !dataEl || !window.fetch) return;

  var S = JSON.parse(dataEl.textContent);
  var form = root.querySelector("form");
  var input = form.querySelector("textarea");
  var button = form.querySelector("button[type=submit]");
  var out = document.getElementById("source-results");
  var MAX = 200;
  var FILE_EXT = /\.(html?|php|aspx?|jsp|js|css|json|xml|png|jpe?g|gif|webp|svg|pdf|docx?|xlsx?|md|txt|py|csv|zip)$/i;
  var data = null;
  var loading = null;

  root.classList.add("js");

  function t(key, vars) {
    var s = S[key] || key;
    return vars ? s.replace(/\{(\w+)\}/g, function (m, k) { return k in vars ? vars[k] : m; }) : s;
  }

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    for (var k in attrs || {}) {
      if (attrs[k] == null) continue;
      if (k === "text") n.textContent = attrs[k];
      else if (k === "cls") n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    }
    (children || []).forEach(function (c) {
      if (c != null) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return n;
  }

  function rich(s) {
    var frag = document.createDocumentFragment();
    var re = /`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)/g, last = 0, m;
    while ((m = re.exec(s))) {
      if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
      frag.appendChild(m[1] ? el("code", { text: m[1] }) : el("a", { href: m[3], text: m[2] }));
      last = re.lastIndex;
    }
    if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
    return frag;
  }

  function defang(host) { return host.replace(/\./g, "[.]"); }

  function fmtDate(iso) {
    if (!iso) return "";
    var d = new Date(iso + "T00:00:00Z");
    if (isNaN(d)) return iso;
    try {
      return new Intl.DateTimeFormat(document.documentElement.lang || "en", { dateStyle: "long", timeZone: "UTC" }).format(d);
    } catch (e) { return iso; }
  }

  function loadData() {
    if (data) return Promise.resolve(data);
    if (!loading) {
      loading = fetch(root.getAttribute("data-src"), { credentials: "omit" })
        .then(function (r) { if (!r.ok) throw new Error(r.status); return r.json(); })
        .then(function (d) {
          var map = Object.create(null);
          d.domains.forEach(function (row) { map[row[0]] = row; });
          data = { lists: d.lists, map: map };
          return data;
        })
        .catch(function (e) { loading = null; throw e; });
    }
    return loading;
  }

  /* ---------- extracting hosts from pasted text ---------- */
  function normHost(h) {
    h = h.trim().toLowerCase().replace(/\.+$/, "").replace(/:\d+$/, "");
    if (h.indexOf("www.") === 0) h = h.slice(4);
    return h;
  }

  function extract(text) {
    var hosts = [];
    var add = function (h) {
      h = normHost(h);
      if (h && /^[a-z0-9.-]+\.[a-z0-9-]{2,}$/.test(h) && !/^[\d.]+$/.test(h) && hosts.indexOf(h) === -1) hosts.push(h);
    };
    // Undo common "defanging": example[.]com, hxxps://
    var s = String(text || "")
      .replace(/\[\.\]|\(\.\)|\{\.\}|\[dot\]|\(dot\)/gi, ".")
      .replace(/\bhxxp(s?):\/\//gi, "http$1://");
    // 1. Full URLs
    s = s.replace(/\bhttps?:\/\/[^\s<>"'`)\]}]+/gi, function (u) {
      try { add(new URL(u).hostname); } catch (e) { /* not a URL */ }
      return " ";
    });
    // 2. Bare domains, with or without a path
    var re = /(?:^|[^a-z0-9@._-])((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z][a-z0-9-]{1,23})(?=$|[^a-z0-9-])/gi;
    var m;
    while ((m = re.exec(s))) {
      if (!FILE_EXT.test(m[1])) add(m[1]);
    }
    return hosts;
  }

  /* ---------- matching ---------- */
  function lookup(host) {
    if (data.map[host]) return { row: data.map[host], via: host };
    var parts = host.split(".");
    for (var i = 1; i < parts.length - 1; i++) {
      var parent = parts.slice(i).join(".");
      if (data.map[parent]) return { row: data.map[parent], via: parent };
    }
    return null;
  }

  /* ---------- rendering ---------- */
  function render(hosts) {
    out.textContent = "";
    var results = hosts.map(function (h) { return { host: h, hit: lookup(h) }; });
    var hits = results.filter(function (r) { return r.hit; });
    results.sort(function (a, b) { return (b.hit ? 1 : 0) - (a.hit ? 1 : 0); });

    var h = el("h2", { tabindex: "-1", id: "source-results-h",
      text: t("summary", { n: hits.length, total: hosts.length }) });

    var list = el("ol", { cls: "checks" }, results.map(function (r) {
      if (!r.hit) {
        return el("li", { cls: "check s-note" }, [
          el("span", { cls: "badge", "aria-hidden": "true", text: "–" }),
          el("div", { cls: "check-body" }, [
            el("h3", null, [el("code", { cls: "host", text: r.host })]),
            el("p", { text: t("not_listed") })
          ])
        ]);
      }
      var row = r.hit.row; // [domain, list, type, dateKind, date]
      var meta = data.lists[row[1]];
      var when = row[4] ? t(row[3] === "seen" ? "first_seen" : "registered", { d: fmtDate(row[4]) }) : "";
      var via = r.hit.via !== r.host ? t("via_parent", { parent: defang(r.hit.via) }) : t("listed_exact");
      return el("li", { cls: "check s-risk" }, [
        el("span", { cls: "badge", "aria-hidden": "true", text: "✕" }),
        el("div", { cls: "check-body" }, [
          el("h3", null, [el("code", { cls: "host", text: defang(r.host) })]),
          el("p", null, [el("strong", { text: t("list_" + row[1]) + ". " }), via + (when ? " " + when + "." : "")]),
          el("p", { cls: "muted-line" }, [rich(t("desc_" + row[1]))])
        ])
      ]);
    }));

    out.appendChild(el("div", { cls: "results-head" }, [h]));
    if (hosts.length >= MAX) out.appendChild(el("p", { cls: "msg", text: t("too_many", { n: MAX }) }));
    out.appendChild(list);
    out.appendChild(el("p", { cls: "caveat" }, [rich(hits.length ? t("caveat_hits") : t("caveat_none"))]));
    out.appendChild(el("p", { cls: "caveat" }, [rich(t("updated", {
      pk: fmtDate(data.lists.pk.updated), rrn: fmtDate(data.lists.rrn.updated)
    }))]));
    h.focus({ preventScroll: true });
    h.scrollIntoView({ block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }

  function message(kind, text) {
    out.textContent = "";
    out.appendChild(el("p", { cls: "msg msg-" + kind, role: kind === "error" ? "alert" : null }, [rich(text)]));
  }

  function run() {
    var hosts = extract(input.value).slice(0, MAX);
    if (!hosts.length) { message("error", t("err_empty")); input.focus(); return; }
    button.disabled = true;
    loadData().then(function () { render(hosts); }, function () { message("error", t("err_data")); })
      .then(function () { button.disabled = false; });
  }

  form.addEventListener("submit", function (ev) { ev.preventDefault(); run(); });
  Array.prototype.forEach.call(root.querySelectorAll("[data-example]"), function (b) {
    b.addEventListener("click", function () { input.value = b.getAttribute("data-example").replace(/\\n/g, "\n"); run(); });
  });
  // Warm the cache so the first check is instant; failures are reported when the user checks.
  loadData().catch(function () {});
})();
