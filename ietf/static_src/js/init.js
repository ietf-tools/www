import $ from 'jquery';
import 'jquery-ui/ui/widgets/datepicker';
import Popper from 'popper.js';

import 'bootstrap';

window.$ = $;
window.jQuery = $;
window.Popper = Popper;

$.datepicker.setDefaults({ dateFormat: 'dd/mm/yy' });
