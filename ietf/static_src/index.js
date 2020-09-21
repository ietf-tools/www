import './js/public-path'; // MUST be first (yes, before absolute imports)

/** Import Sass entry point for Webpack to bundle styles */
import './css/main.scss';

import $ from 'jquery';
import Popper from 'popper.js';

import 'bootstrap';

window.$ = $;
window.jQuery = $;
window.Popper = Popper;
