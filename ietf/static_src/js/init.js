import $ from 'jquery';
import 'jquery-ui/ui/widgets/datepicker';
import * as Popper from '@popperjs/core';

import * as bootstrap from 'bootstrap';

window.$ = $;
window.jQuery = $;
window.Popper = Popper;
window.bootstrap = bootstrap;

document.documentElement.classList.remove('no-js');

document.body.addEventListener('mousedown', () => {
    document.body.classList.add('using-mouse');
});
document.body.addEventListener('keydown', () => {
    document.body.classList.remove('using-mouse');
});
