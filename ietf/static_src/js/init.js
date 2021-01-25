import $ from 'jquery';
import 'jquery-ui/ui/widgets/datepicker';
import Popper from 'popper.js';

import 'bootstrap';

window.$ = $;
window.jQuery = $;
window.Popper = Popper;

document.documentElement.classList.remove('no-js');

document.body.addEventListener('mousedown', () => {
    document.body.classList.add('using-mouse');
});
document.body.addEventListener('keydown', () => {
    document.body.classList.remove('using-mouse');
});
