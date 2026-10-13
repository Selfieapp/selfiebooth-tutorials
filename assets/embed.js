/* Selfie Booth AI · Tutorials embed
   Usage on any page (e.g. WordPress /tutorials):
     <div id="sbt-tutorials"></div>
     <script src="https://tutorials.selfieboothapp.com/assets/embed.js" defer></script>
   Shows the Tutorials section inline (auto height) and opens guides full screen.
   Deep links: /tutorials#360  or  /tutorials#360.speed  */
(function () {
  var me = document.currentScript;
  var BASE = (me && me.src ? me.src : "").replace(/\/assets\/embed\.js(\?.*)?$/, "") || "https://tutorials.selfieboothapp.com";
  var ORIGIN = new URL(BASE + "/").origin;

  var host = document.getElementById("sbt-tutorials");
  if (!host) { host = document.createElement("div"); host.id = "sbt-tutorials"; me.parentNode.insertBefore(host, me); }

  var section = document.createElement("iframe");
  section.src = BASE + "/";
  section.title = "Selfie Booth AI Tutorials";
  section.setAttribute("scrolling", "no");
  section.style.cssText = "display:block;width:100%;height:1500px;border:0;overflow:hidden;background:transparent";
  host.appendChild(section);

  var overlay = null, viewer = null, lang = null, prevOverflow = "";

  function setHash(h) { try { history.replaceState(null, "", location.pathname + location.search + (h ? "#" + h : "")); } catch (e) {} }

  function open(sec, l) {
    if (l) lang = l;
    var url = BASE + "/viewer.html" + (lang ? "?lang=" + lang : "") + (sec ? "#" + sec : "");
    if (!overlay) {
      overlay = document.createElement("div");
      overlay.style.cssText = "position:fixed;inset:0;z-index:2147483000;background:#fff";
      viewer = document.createElement("iframe");
      viewer.title = "360 Photo Booth Guide";
      viewer.style.cssText = "display:block;width:100%;height:100%;border:0";
      overlay.appendChild(viewer);
    }
    viewer.src = url;
    document.body.appendChild(overlay);
    prevOverflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = "hidden";
    setHash("360" + (sec ? "." + sec : ""));
  }

  function close() {
    if (overlay && overlay.parentNode) overlay.parentNode.removeChild(overlay);
    document.documentElement.style.overflow = prevOverflow;
    setHash("");
  }

  window.addEventListener("message", function (e) {
    if (e.origin !== ORIGIN) return;
    var d = e.data || {};
    if (d.sbt === "h" && d.h > 0) section.style.height = d.h + "px";
    else if (d.sbt === "open") open(d.sec || "", d.lang);
    else if (d.sbt === "close") close();
    else if (d.sbai === "lang") {
      lang = d.lang;
      try { if (e.source !== section.contentWindow) section.contentWindow.postMessage({ sbai: "lang", lang: d.lang }, ORIGIN); } catch (x) {}
    }
  });

  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && overlay && overlay.parentNode) close(); });

  var h = location.hash.slice(1);
  if (h.indexOf("360") === 0) open(h.split(".")[1] || "");
})();
