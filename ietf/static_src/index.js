/* eslint springload/import/first: 0 */
import './js/public-path'; // MUST be first (yes, before absolute imports)
import './css/main.scss';

import './js/main';

import $ from 'jquery';
import Popper from '@popperjs/core';

import 'bootstrap';

window.$ = $;
window.jQuery = $;
window.Popper = Popper;
