/* modelpoisoning.com: Hugging Face model checker.
   Runs entirely in the visitor's browser. It reads public repository metadata from
   Hugging Face's API and sends nothing to this site. No dependencies. */
(function () {
  "use strict";

  var root = document.getElementById("checker");
  var dataEl = document.getElementById("checker-i18n");
  if (!root || !dataEl || !window.fetch) return;

  var S = JSON.parse(dataEl.textContent);
  var LANG = document.documentElement.lang || "en";
  var form = root.querySelector("form");
  var input = form.querySelector("input");
  var button = form.querySelector("button[type=submit]");
  var out = document.getElementById("checker-results");
  var HF = "https://huggingface.co/";
  var API = HF + "api/models/";
  var SEG = /^[A-Za-z0-9][A-Za-z0-9._-]{0,95}$/;
  var REV = /^[A-Za-z0-9._\/-]{1,120}$/;
  var current = null;

  root.classList.add("js");

  /* ---------- helpers ---------- */
  function t(key, vars) {
    var s = S[key] || key;
    if (vars) {
      s = s.replace(/\{(\w+)\}/g, function (m, k) { return k in vars ? vars[k] : m; });
    }
    return s;
  }

  function el(tag, attrs, children) {
    var n = document.createElement(tag);
    if (attrs) {
      for (var k in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, k) || attrs[k] == null) continue;
        if (k === "text") n.textContent = attrs[k];
        else if (k === "cls") n.className = attrs[k];
        else n.setAttribute(k, attrs[k]);
      }
    }
    (children || []).forEach(function (c) {
      if (c == null) return;
      n.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return n;
  }

  /* Turns "text with `code` and [link](url)" into DOM nodes without innerHTML. */
  function rich(s) {
    var frag = document.createDocumentFragment();
    var re = /`([^`]+)`|\[([^\]]+)\]\(([^)]+)\)/g;
    var last = 0, m;
    while ((m = re.exec(s))) {
      if (m.index > last) frag.appendChild(document.createTextNode(s.slice(last, m.index)));
      if (m[1]) frag.appendChild(el("code", { text: m[1] }));
      else frag.appendChild(el("a", { href: m[3], text: m[2] }));
      last = re.lastIndex;
    }
    if (last < s.length) frag.appendChild(document.createTextNode(s.slice(last)));
    return frag;
  }

  function encPath(p) { return p.split("/").map(encodeURIComponent).join("/"); }
  function asList(v) { return v == null ? [] : (Array.isArray(v) ? v : [v]); }
  function uniq(a) { return a.filter(function (x, i) { return x && a.indexOf(x) === i; }); }
  function ext(name) {
    var base = name.split("/").pop().toLowerCase();
    var i = base.lastIndexOf(".");
    return i > 0 ? base.slice(i + 1) : "";
  }
  function fmtNum(n) {
    try { return new Intl.NumberFormat(LANG).format(n); } catch (e) { return String(n); }
  }
  function fmtDate(iso) {
    var d = new Date(iso);
    if (isNaN(d)) return "";
    try { return new Intl.DateTimeFormat(LANG, { dateStyle: "long" }).format(d); }
    catch (e) { return d.toISOString().slice(0, 10); }
  }

  /* ---------- input parsing ---------- */
  function parse(raw) {
    var s = (raw || "").trim();
    var rev = "";
    if (!s) return { error: "err_empty" };
    try {
      if (/^pkg:huggingface\//i.test(s)) {
        s = s.slice("pkg:huggingface/".length).split("?")[0].split("#")[0];
        var at = s.lastIndexOf("@");
        if (at > 0) { rev = decodeURIComponent(s.slice(at + 1)); s = s.slice(0, at); }
        s = s.split("/").map(decodeURIComponent).join("/");
      } else if (/^(https?:\/\/)?(www\.)?(huggingface\.co|hf\.co)(\/|$)/i.test(s)) {
        var u = new URL(/^https?:/i.test(s) ? s : "https://" + s);
        var parts = u.pathname.split("/").filter(Boolean).map(decodeURIComponent);
        if (parts[0] === "datasets" || parts[0] === "spaces") return { error: "err_kind" };
        var verbs = ["tree", "blob", "resolve", "commit", "commits", "discussions", "settings"];
        var n = (parts.length > 1 && verbs.indexOf(parts[1]) === -1) ? 2 : 1;
        var rest = parts.slice(n);
        if (["tree", "blob", "resolve", "commit"].indexOf(rest[0]) !== -1 && rest[1]) rev = rest[1];
        s = parts.slice(0, n).join("/");
      } else {
        var at2 = s.lastIndexOf("@");
        if (at2 > 0) { rev = s.slice(at2 + 1); s = s.slice(0, at2); }
      }
    } catch (e) {
      return { error: "err_format" };
    }
    s = s.replace(/^\/+|\/+$/g, "");
    var segs = s.split("/");
    if (segs.length > 2 || !segs.every(function (x) { return SEG.test(x); })) return { error: "err_format" };
    if (rev && !REV.test(rev)) return { error: "err_format" };
    return { id: segs.join("/"), rev: rev };
  }

  /* ---------- the checks ---------- */
  var PICKLE = ["bin", "pt", "pth", "ckpt", "pkl", "pickle", "joblib", "dill", "sav"];
  var KERAS = ["h5", "hdf5", "keras"];
  var SAFE = { safetensors: "safetensors", gguf: "GGUF", onnx: "ONNX", msgpack: "Flax msgpack", tflite: "TFLite" };
  var TRAINING_STATE = /(^|\/)(training_args|optimizer|scheduler|scaler|rng_state[^/]*)\.(bin|pt|pth)$/i;

  function fileLink(info, path) {
    return HF + encPath(info.id) + "/blob/" + encodeURIComponent(info.sha || "main") + "/" + encPath(path);
  }

  function analyse(info) {
    var checks = [];
    var files = asList(info.siblings).map(function (f) { return f.rfilename; }).filter(Boolean);
    var tags = asList(info.tags);
    var card = info.cardData || {};
    var add = function (status, title, body, items) {
      checks.push({ status: status, title: title, body: body, items: items || [] });
    };
    var fileItems = function (list) {
      return list.slice(0, 12).map(function (p) { return { text: p, href: fileLink(info, p) }; })
        .concat(list.length > 12 ? [{ text: t("and_more", { n: list.length - 12 }) }] : []);
    };

    // 0. Repository status
    if (info.disabled) add("risk", t("disabled_t"), t("disabled_b"));
    if (info.gated) add("note", t("gated_t"), t("gated_b"));

    // 1. Hugging Face scans
    var sec = info.securityRepoStatus;
    if (!sec || !sec.scansDone) {
      add("check", t("scan_none_t"), t("scan_none_b"));
    } else {
      var flagged = asList(sec.filesWithIssues);
      var unsafe = flagged.filter(function (f) { return f.level === "unsafe"; });
      var other = flagged.filter(function (f) { return f.level !== "unsafe"; });
      var toItems = function (list) {
        return list.slice(0, 12).map(function (f) {
          return { text: f.path, href: fileLink(info, f.path), tag: S["level_" + f.level] || f.level };
        });
      };
      if (unsafe.length) add("risk", t("scan_unsafe_t", { n: unsafe.length }), t("scan_unsafe_b"), toItems(unsafe.concat(other)));
      else if (other.length) add("check", t("scan_caution_t", { n: other.length }), t("scan_caution_b"), toItems(other));
      else add("good", t("scan_clean_t"), t("scan_clean_b"));
    }

    // 2. Weight formats
    var stateFiles = files.filter(function (f) { return TRAINING_STATE.test(f); });
    var pickles = files.filter(function (f) {
      if (TRAINING_STATE.test(f) || PICKLE.indexOf(ext(f)) === -1) return false;
      if (ext(f) === "bin") {
        var stem = f.slice(0, -4);
        if (files.indexOf(stem + ".xml") !== -1 || /ggml|openvino/i.test(f)) return false; // raw weights, not pickle
      }
      return true;
    });
    // tf_model.h5 holds transformers' TensorFlow weights, read with load_weights, which does not rebuild layers.
    var keras = files.filter(function (f) { return KERAS.indexOf(ext(f)) !== -1 && !/(^|\/)tf_model\.h5$/i.test(f); });
    var safeKinds = Object.keys(SAFE).filter(function (k) {
      return files.some(function (f) { return ext(f) === k; });
    }).map(function (k) { return SAFE[k]; });
    if (pickles.length && !safeKinds.length) {
      add("risk", t("fmt_pickle_only_t"), t("fmt_pickle_only_b"), fileItems(pickles));
    } else if (pickles.length) {
      add("check", t("fmt_both_t"), t("fmt_both_b", { kinds: safeKinds.join(", ") }), fileItems(pickles));
    } else if (safeKinds.length) {
      add("good", t("fmt_safe_t"), t("fmt_safe_b", { kinds: safeKinds.join(", ") }));
    } else if (!keras.length) {
      add("note", t("fmt_none_t"), t("fmt_none_b"));
    }
    if (keras.length) add("check", t("fmt_keras_t"), t("fmt_keras_b"), fileItems(keras));
    if (stateFiles.length) add("note", t("fmt_state_t"), t("fmt_state_b"), fileItems(stateFiles));

    // 3. Custom code
    var py = files.filter(function (f) { return ext(f) === "py"; });
    var autoMap = info.config && info.config.auto_map;
    if (autoMap || tags.indexOf("custom_code") !== -1) {
      add("check", t("code_remote_t"), t("code_remote_b"), fileItems(py));
    } else if (py.length) {
      add("note", t("code_files_t"), t("code_files_b"), fileItems(py));
    } else {
      add("good", t("code_none_t"), t("code_none_b"));
    }

    // 4. Model card
    var hasReadme = files.some(function (f) { return f.toLowerCase() === "readme.md"; });
    var hasMeta = Object.keys(card).length > 0;
    if (!hasReadme) add("check", t("card_none_t"), t("card_none_b"));
    else if (!hasMeta) add("check", t("card_nometa_t"), t("card_nometa_b"));
    else add("good", t("card_ok_t"), t("card_ok_b"));

    // 5. Licence
    var lic = uniq(asList(card.license).concat(
      tags.filter(function (x) { return x.indexOf("license:") === 0; }).map(function (x) { return x.slice(8); })
    ).map(String));
    var licName = card.license_name || "";
    if (!lic.length) add("check", t("lic_none_t"), t("lic_none_b"));
    else if (lic.every(function (l) { return l === "other" || l === "unknown"; })) {
      add("check", t("lic_other_t", { lic: licName || lic.join(", ") }), t("lic_other_b"));
    } else add("good", t("lic_ok_t", { lic: lic.filter(function (l) { return l !== "other"; }).join(", ") }), t("lic_ok_b"));

    // 6. Training data
    var ds = uniq(asList(card.datasets).map(String).concat(
      tags.filter(function (x) { return x.indexOf("dataset:") === 0; }).map(function (x) { return x.slice(8); })
    ));
    if (ds.length) {
      add("good", t("data_ok_t", { n: ds.length }), t("data_ok_b"), ds.slice(0, 12).map(function (d) {
        return { text: d, href: SEG.test(d.split("/")[0]) ? HF + "datasets/" + encPath(d) : null };
      }));
    } else {
      add("check", t("data_none_t"), t("data_none_b"));
    }

    // 7. Base model
    var rels = {};
    tags.filter(function (x) { return x.indexOf("base_model:") === 0; }).forEach(function (x) {
      var rest = x.slice(11), rel = "";
      var m = /^(finetune|adapter|quantized|merge):(.+)$/.exec(rest);
      if (m) { rel = m[1]; rest = m[2]; }
      if (!rels[rest] || rel) rels[rest] = rel;
    });
    asList(card.base_model).forEach(function (b) { if (typeof b === "string" && !(b in rels)) rels[b] = ""; });
    var bases = Object.keys(rels).filter(function (b) { return b !== info.id; });
    if (bases.length) {
      add("note", t("base_t", { n: bases.length }), t("base_b"), bases.slice(0, 8).map(function (b) {
        return { text: b, check: b, tag: rels[b] ? t("rel_" + rels[b]) : null };
      }));
    }

    var order = { risk: 0, check: 1, note: 2, good: 3 };
    checks.sort(function (a, b) { return order[a.status] - order[b.status]; });
    return checks;
  }

  /* ---------- rendering ---------- */
  var ICON = { risk: "✕", check: "!", note: "i", good: "✓" };

  function copyBlock(label, text) {
    var code = el("code", { text: text });
    var btn = el("button", { type: "button", cls: "copy", text: t("copy") });
    btn.addEventListener("click", function () {
      var done = function () {
        btn.textContent = t("copied");
        setTimeout(function () { btn.textContent = t("copy"); }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () { selectText(code); });
      } else selectText(code);
    });
    return el("div", { cls: "copyblock" }, [
      el("p", { cls: "copy-label", text: label }),
      el("div", { cls: "copy-row" }, [el("pre", null, [code]), btn])
    ]);
  }
  function selectText(node) {
    var r = document.createRange();
    r.selectNodeContents(node);
    var sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(r);
  }

  function purl(info) {
    var parts = info.id.split("/");
    var version = (info.sha || "").toLowerCase();
    return "pkg:huggingface/" + parts.map(encodeURIComponent).join("/") + (version ? "@" + version : "");
  }

  function render(info, checks) {
    out.textContent = "";
    var counts = { risk: 0, check: 0, good: 0, note: 0 };
    checks.forEach(function (c) { counts[c.status]++; });

    var h = el("h2", { tabindex: "-1", id: "results-h" }, [
      t("results_for") + " ",
      el("a", { href: HF + encPath(info.id), text: info.id })
    ]);
    var meta = [];
    if (info.lastModified) meta.push(t("updated", { d: fmtDate(info.lastModified) }));
    if (typeof info.downloads === "number") meta.push(t("downloads", { n: fmtNum(info.downloads) }));
    if (typeof info.likes === "number") meta.push(t("likes", { n: fmtNum(info.likes) }));

    var tally = el("ul", { cls: "tally", "aria-label": t("summary_label") }, ["risk", "check", "good"].map(function (k) {
      return el("li", { cls: "s-" + k }, [
        el("span", { cls: "badge", "aria-hidden": "true", text: ICON[k] }),
        t("count_" + k) + ": ", el("strong", { text: String(counts[k]) })
      ]);
    }));

    var list = el("ol", { cls: "checks" }, checks.map(function (c) {
      var items = c.items.length ? el("ul", { cls: "check-items" }, c.items.map(function (it) {
        var label;
        if (it.check) {
          label = el("button", { type: "button", cls: "linklike", text: it.text });
          label.addEventListener("click", function () { input.value = it.check; run(it.check); });
        } else if (it.href) {
          label = el("a", { href: it.href, text: it.text });
        } else {
          label = el("span", { text: it.text });
        }
        return el("li", null, [label, it.tag ? el("span", { cls: "item-tag", text: it.tag }) : null]);
      })) : null;
      return el("li", { cls: "check s-" + c.status }, [
        el("span", { cls: "badge", "aria-hidden": "true", text: ICON[c.status] }),
        el("div", { cls: "check-body" }, [
          el("h3", null, [el("span", { cls: "status", text: t("status_" + c.status) + ": " }), c.title]),
          el("p", null, [rich(c.body)]),
          items
        ])
      ]);
    }));

    var shortSha = (info.sha || "").slice(0, 12);
    var load = info.library_name === "transformers"
      ? 'from_pretrained("' + info.id + '", revision="' + info.sha + '")'
      : 'snapshot_download("' + info.id + '", revision="' + info.sha + '")';
    var pin = info.sha ? el("section", { cls: "pin", "aria-labelledby": "pin-h" }, [
      el("h3", { id: "pin-h", text: t("pin_t") }),
      el("p", null, [rich(t("pin_b", { sha: shortSha }))]),
      copyBlock(t("pin_code"), load),
      copyBlock(t("pin_purl"), purl(info))
    ]) : null;

    out.appendChild(el("div", { cls: "results-head" }, [
      h,
      meta.length ? el("p", { cls: "results-meta", text: meta.join(" · ") }) : null,
      tally
    ]));
    out.appendChild(list);
    if (pin) out.appendChild(pin);
    out.appendChild(el("p", { cls: "caveat" }, [rich(t("caveat"))]));
    h.focus({ preventScroll: true });
    h.scrollIntoView({ block: "start", behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth" });
  }

  function message(kind, text) {
    out.textContent = "";
    var p = el("p", { cls: "msg msg-" + kind, role: kind === "error" ? "alert" : null }, [rich(text)]);
    out.appendChild(p);
  }

  /* ---------- running ---------- */
  function setBusy(on) {
    button.disabled = on;
    button.textContent = on ? t("checking") : t("check");
    out.setAttribute("aria-busy", on ? "true" : "false");
  }

  function run(raw) {
    var q = parse(raw);
    if (q.error) { message("error", t(q.error)); input.focus(); return; }
    try {
      var url = new URL(location.href);
      url.searchParams.set("model", q.rev ? q.id + "@" + q.rev : q.id);
      history.replaceState(null, "", url.pathname + url.search);
    } catch (e) { /* ignore */ }

    if (current) current.abort();
    var ctrl = window.AbortController ? new AbortController() : null;
    current = ctrl;
    var timer = setTimeout(function () { if (ctrl) ctrl.abort(); }, 20000);
    setBusy(true);
    message("info", t("loading", { id: q.id }));

    var api = API + encPath(q.id) + (q.rev ? "/revision/" + encodeURIComponent(q.rev) : "") + "?securityStatus=true";
    fetch(api, {
      signal: ctrl ? ctrl.signal : undefined,
      credentials: "omit",
      referrerPolicy: "no-referrer",
      headers: { Accept: "application/json" }
    }).then(function (r) {
      if (r.status === 401 || r.status === 403 || r.status === 404) throw { kind: "err_notfound" };
      if (r.status === 429) throw { kind: "err_rate" };
      if (!r.ok) throw { kind: "err_server" };
      return r.json();
    }).then(function (info) {
      if (current !== ctrl) return;
      if (!info || !info.id) throw { kind: "err_server" };
      render(info, analyse(info));
    }).catch(function (e) {
      if (current !== ctrl) return; // a newer check replaced this one
      var kind = e && e.kind ? e.kind : (e && e.name === "AbortError" ? "err_timeout" : "err_network");
      message("error", t(kind, { id: q.id }));
    }).then(function () {
      clearTimeout(timer);
      if (current === ctrl) { setBusy(false); current = null; }
    });
  }

  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    run(input.value);
  });
  Array.prototype.forEach.call(root.querySelectorAll("[data-example]"), function (b) {
    b.addEventListener("click", function () {
      input.value = b.getAttribute("data-example");
      run(input.value);
    });
  });

  var initial = new URLSearchParams(location.search).get("model");
  if (initial) { input.value = initial; run(initial); }
})();
