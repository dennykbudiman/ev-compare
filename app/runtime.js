/* EV Compare web runtime.
 * Runs the Design Component (template + Component class from app/template.dc.html) as a normal web page.
 * The template uses {{holes}}, <sc-for list="{{x}}" as="item"> and <sc-if value="{{x}}">; this file turns it into
 * Preact elements on every render. Needs window.preact (vendored in app/vendor/preact.umd.js).
 */
(function () {
  'use strict';
  var h = preact.h;
  var HOLE = /\{\{\s*([^}]+?)\s*\}\}/g;
  var ONLY_HOLE = /^\{\{\s*([^}]+?)\s*\}\}$/;

  function get(scope, path) {
    if (path === 'true') return true;
    if (path === 'false') return false;
    var parts = path.split('.');
    var x = scope;
    for (var i = 0; i < parts.length; i++) { if (x == null) return undefined; x = x[parts[i]]; }
    return x;
  }
  function sub(str, scope) {
    return str.replace(HOLE, function (_, p) { var x = get(scope, p); return x == null ? '' : String(x); });
  }

  // Template attribute names arrive lower-cased from the HTML parser; map them to the props Preact expects.
  var EVENT = { onclick: 'onClick', onchange: 'onChange', onblur: 'onBlur', onfocus: 'onFocus', onkeydown: 'onKeyDown', onmouseenter: 'onMouseEnter', onmouseleave: 'onMouseLeave', oninput: 'onInput' };
  var BOOL = { disabled: 1, checked: 1, hidden: 1, readonly: 1, required: 1, selected: 1, multiple: 1, autofocus: 1 };

  function props(el, scope) {
    var p = {};
    for (var i = 0; i < el.attributes.length; i++) {
      var a = el.attributes[i], name = a.name, val = a.value;
      if (name.indexOf('hint-') === 0) continue;
      var m = val.match(ONLY_HOLE);
      var v = m ? get(scope, m[1]) : (val.indexOf('{{') >= 0 ? sub(val, scope) : val);
      if (EVENT[name]) {
        if (typeof v !== 'function') continue;
        var tag = el.tagName.toLowerCase();
        // the design was written with React semantics: onChange on a text box fires on every keystroke
        if (name === 'onchange' && (tag === 'input' || tag === 'textarea')) p.onInput = v;
        else p[EVENT[name]] = v;
        continue;
      }
      if (BOOL[name]) { if (v === true || v === 'true' || (v === '' && !m)) p[name] = true; continue; }
      if (v === undefined || v === null || v === false) continue;
      p[name] = v;
    }
    return p;
  }

  function build(node, scope, out) {
    var kids = node.childNodes;
    for (var i = 0; i < kids.length; i++) {
      var c = kids[i];
      if (c.nodeType === 3) {
        var t = c.nodeValue;
        if (!/\S/.test(t) && t.indexOf('\n') >= 0) continue;   // layout whitespace between tags
        out.push(t.indexOf('{{') >= 0 ? sub(t, scope) : t);
        continue;
      }
      if (c.nodeType !== 1) continue;
      var tag = c.tagName.toLowerCase();
      if (tag === 'sc-for') {
        var list = get(scope, (c.getAttribute('list') || '').replace(/[{}\s]/g, '')) || [];
        var as = c.getAttribute('as') || 'item';
        for (var j = 0; j < list.length; j++) {
          var s2 = Object.create(scope); s2[as] = list[j]; s2.index = j;
          build(c, s2, out);
        }
        continue;
      }
      if (tag === 'sc-if') {
        if (get(scope, (c.getAttribute('value') || '').replace(/[{}\s]/g, ''))) build(c, scope, out);
        continue;
      }
      var ch = [];
      build(c, scope, ch);
      out.push(h.apply(null, [tag, props(c, scope)].concat(ch)));
    }
    return out;
  }

  function DCLogic(props) { this.props = props || {}; this.state = {}; }
  DCLogic.prototype.setState = function (patch) {
    var next = typeof patch === 'function' ? patch(this.state) : patch;
    Object.assign(this.state, next || {});
    if (this.__schedule) this.__schedule();
  };

  window.EVCRuntime = {
    start: function () {
      var tpl = document.getElementById('evc-tpl');
      var mount = document.getElementById('app');
      var Component = window.EVC_LOGIC(DCLogic);
      var lang = (navigator.language || 'en').toLowerCase().indexOf('id') === 0 ? 'id' : 'en';
      var comp = new Component({ language: lang });
      var queued = false;
      var render = function () {
        queued = false;
        var vals = comp.renderVals();
        preact.render(h(preact.Fragment, null, build(tpl.content, vals, [])), mount);
      };
      comp.__schedule = function () { if (!queued) { queued = true; Promise.resolve().then(render); } };
      render();
      if (typeof comp.componentDidMount === 'function') comp.componentDidMount();
    }
  };
})();
