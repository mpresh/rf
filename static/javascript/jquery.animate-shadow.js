/*!
 * Shadow animation jQuery-plugin
 * http://www.bitstorm.org/jquery/shadow-animation/
 * Copyright 2010 Edwin Martin <edwin@bitstorm.org>
 * Released under the MIT and GPL licenses.
 */

(function($) {

	// First define which property to use
	var boxShadowProperty;
	$.each(['boxShadow', 'MozBoxShadow', 'WebkitBoxShadow'], function(i, property) {
		var val = $('body').css(property);
		if (typeof val == 'string' && val != '') {
			boxShadowProperty = property;
			return false;
		}
	});

	// Extend the animate-function
	if (boxShadowProperty) {
		$.fx.step['shadow'] = function(fx) {
			if (!fx.init) {
				fx.begin = parseShadow($(fx.elem).css(boxShadowProperty));
				fx.end = $.extend({}, fx.begin, parseShadow(fx.options.curAnim['shadow']));

				fx.init = true;
			}

			fx.elem.style[boxShadowProperty] = calculateShadow(fx.begin, fx.end, fx.pos);
		}
	}

	// Calculate an in-between shadow.
	function calculateShadow(begin, end, pos) {
		var parts = [];

		if (begin.inset) {
			parts.push('inset');
		}

		if (typeof end.color != 'undefined') {
			parts.push('#'
				+ get2hex(begin.color[0] + pos * (end.color[0] - begin.color[0]))
				+ get2hex(begin.color[1] + pos * (end.color[1] - begin.color[1]))
				+ get2hex(begin.color[2] + pos * (end.color[2] - begin.color[2])));
		}
		if (typeof end.left != 'undefined') {
			parts.push(parseInt(begin.left + pos * (end.left - begin.left))+'px '
					+parseInt(begin.top + pos * (end.top - begin.top))+'px');
		}
		if (typeof end.blur != 'undefined') {
			parts.push(parseInt(begin.blur + pos * (end.blur - begin.blur))+'px');
		}
		if (typeof end.spread != 'undefined') {
			parts.push(parseInt(begin.spread + pos * (end.spread - begin.spread))+'px');
		}

		return parts.join(' ');
	}

	// Get two-digits hex number
	function get2hex(i) {
		var hex = parseInt(i).toString(16);
		return hex.length == 1 ? '0'+hex : hex;
	}

	// Parse the shadow value and extract the values.
	function parseShadow(shadow) {
		var match, color, parsedShadow = {};

		// Parse an CSS-syntax color. Outputs an array [r, g, b]
		// Match #aabbcc
		if (match = /#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})/.exec(shadow)) {
			color = [parseInt(match[1], 16), parseInt(match[2], 16), parseInt(match[3], 16)];

			// Match #abc
		} else if (match = /#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])/.exec(shadow)) {
			color = [parseInt(match[1], 16) * 17, parseInt(match[2], 16) * 17, parseInt(match[3], 16) * 17];

			// Match rgb(n, n, n)
		} else if (match = /rgb\(\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*,\s*([0-9]{1,3})\s*\)/.exec(shadow)) {
			color = [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];

			// No browser returns rgb(n%, n%, n%), so little reason to support this format.
		}

		// Parse offset, blur and radius
		if (match = /([0-9]+)(?:px)?\s+([0-9]+)(?:px)?(?:\s+([0-9]+)(?:px)?)?(?:\s+([0-9]+)(?:px)?)?/.exec(shadow)) {
			parsedShadow = {left: parseInt(match[1]), top: parseInt(match[2]), blur: match[3] ? parseInt(match[3]) : undefined, spread: match[4] ? parseInt(match[4]) : undefined};
		}

		// Inset or not
		parsedShadow.inset = /inset/.test(shadow);

		parsedShadow.color = color;

		return parsedShadow;
	}
})(jQuery);

