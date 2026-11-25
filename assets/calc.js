// The calculators on /tools/. Everything is worked out here in the browser;
// nothing anyone types is sent anywhere. Starting prices are in the page
// (set from PRICES in _build/build.py).
(function () {
  'use strict';

  var WEEKS_PER_MONTH = 52 / 12;

  function read(form, name) {
    var el = form.elements[name];
    if (!el || String(el.value).trim() === '') return NaN;
    return parseFloat(String(el.value).replace(/[$,\s]/g, ''));
  }
  function optional(form, name) {
    var v = read(form, name);
    return isNaN(v) ? 0 : v;
  }
  function fmt(x, digits) {
    return x.toLocaleString('en-US', { minimumFractionDigits: digits, maximumFractionDigits: digits });
  }
  function money(x) { return '$' + fmt(x, 2); }
  function miles(x) { return fmt(Math.round(x), 0) + ' miles'; }

  function out(form, name, value) {
    var el = form.querySelector('[data-out="' + name + '"]');
    if (el) el.textContent = value;
  }
  function clear(form) {
    var els = form.querySelectorAll('[data-out]');
    for (var i = 0; i < els.length; i++) {
      var k = els[i].getAttribute('data-out');
      if (k !== 'error' && k !== 'big-label') els[i].textContent = '—';
    }
  }
  function fail(form, message) {
    clear(form);
    var e = form.querySelector('[data-out="error"]');
    if (e) { e.textContent = message; e.hidden = !message; }
    return false;
  }
  function ok(form) {
    var e = form.querySelector('[data-out="error"]');
    if (e) { e.textContent = ''; e.hidden = true; }
    return true;
  }
  function positive(values) {
    for (var i = 0; i < values.length; i++) if (!(values[i] > 0)) return false;
    return true;
  }

  var calcs = {
    trip: function (f) {
      var d = read(f, 'miles'), mpg = read(f, 'mpg'), price = read(f, 'price');
      var people = Math.max(1, Math.round(optional(f, 'people')) || 1);
      if (!positive([d, mpg, price])) return fail(f, 'Enter the distance, your MPG and the fuel price.');
      var total = d * (f.elements.round.checked ? 2 : 1);
      var gallons = total / mpg;
      var cost = gallons * price;
      out(f, 'cost', money(cost));
      out(f, 'total-miles', miles(total));
      out(f, 'gallons', fmt(gallons, 1));
      out(f, 'per-mile', money(price / mpg));
      out(f, 'per-person', people > 1 ? money(cost / people) : money(cost));
      return ok(f);
    },

    towing: function (f) {
      var tank = read(f, 'tank'), mpg = read(f, 'mpg'), tow = read(f, 'towmpg');
      var drop = optional(f, 'drop'), reserve = optional(f, 'reserve');
      if (!positive([tank, mpg])) return fail(f, 'Enter your tank size and your MPG when not towing.');
      if (drop < 0 || drop >= 100 || reserve < 0 || reserve >= 100) return fail(f, 'The drop and the reserve must be between 0 and 99%.');
      if (!isNaN(tow) && !(tow > 0)) return fail(f, 'Towing MPG must be more than 0, or leave it blank.');
      var towMpg = tow > 0 ? tow : mpg * (1 - drop / 100);
      var full = tank * towMpg;
      var normal = tank * mpg;
      out(f, 'between', miles(full * (1 - reserve / 100)));
      out(f, 'tow-mpg', fmt(towMpg, 1) + (tow > 0 ? '' : ' (estimated)'));
      out(f, 'tow-range', miles(full));
      out(f, 'range', miles(normal));
      out(f, 'lost', normal > full ? miles(normal - full) : '0 miles');
      out(f, 'reserve-gal', fmt(tank * reserve / 100, 1) + ' gallons');
      return ok(f);
    },

    hotshot: function (f) {
      var weekly = read(f, 'weekly'), mpg = read(f, 'mpg'), price = read(f, 'price');
      var deadhead = optional(f, 'deadhead'), maint = optional(f, 'maint');
      var fixed = optional(f, 'truck') + optional(f, 'trailer') + optional(f, 'insurance') + optional(f, 'other') + optional(f, 'pay');
      if (!positive([weekly, mpg, price])) return fail(f, 'Enter your miles per week, your MPG and the diesel price.');
      if (deadhead < 0 || deadhead >= 100) return fail(f, 'Empty miles must be between 0 and 99%.');
      if (maint < 0 || fixed < 0) return fail(f, 'Costs can\'t be negative.');
      var month = weekly * WEEKS_PER_MONTH;
      var fuel = price / mpg;
      var run = fuel + maint;
      var fixedMile = fixed / month;
      var total = run + fixedMile;
      out(f, 'per-loaded', money(total / (1 - deadhead / 100)));
      out(f, 'big-label', optional(f, 'pay') > 0 ? 'per loaded mile to cover costs and your pay' : 'per loaded mile to break even');
      out(f, 'fuel-mile', money(fuel));
      out(f, 'run-mile', money(run));
      out(f, 'fixed-mile', money(fixedMile));
      out(f, 'total-mile', money(total));
      out(f, 'month-miles', fmt(Math.round(month), 0));
      out(f, 'month-fuel', money(fuel * month));
      out(f, 'month-total', money(total * month));
      return ok(f);
    }
  };

  var forms = document.querySelectorAll('form[data-calc]');
  for (var i = 0; i < forms.length; i++) {
    (function (form) {
      var run = calcs[form.getAttribute('data-calc')];
      if (!run) return;
      form.addEventListener('input', function () { run(form); });
      form.addEventListener('change', function (e) {
        // Picking a fuel moves the price to that fuel's average, unless the
        // price has been typed in by hand.
        if (e.target.name === 'fuel') {
          var price = form.elements.price;
          if (!price.hasAttribute('data-edited')) {
            price.value = e.target.options[e.target.selectedIndex].getAttribute('data-price');
          }
        }
        run(form);
      });
      if (form.elements.price) {
        form.elements.price.addEventListener('input', function () { this.setAttribute('data-edited', ''); });
      }
      form.addEventListener('submit', function (e) { e.preventDefault(); run(form); });
      run(form);
    })(forms[i]);
  }
})();
