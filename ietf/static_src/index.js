/* eslint springload/import/first: 0 */
import './js/public-path'; // MUST be first (yes, before absolute imports)
import './css/main.scss';

import $ from 'jquery';
import Popper from 'popper.js';

import 'bootstrap';

window.$ = $;
window.jQuery = $;
window.Popper = Popper;
